# src/adaptive_pixelizer/image_label.py の修正版
import sys
import traceback
from PyQt6.QtWidgets import QLabel, QApplication
from PyQt6.QtGui import (
    QPixmap, QImage, QPainter, QColor, QPen, QCursor, QGuiApplication,
    QWheelEvent, QMouseEvent, QKeyEvent, QKeySequence, QPainterPath, QBrush
)
from PyQt6.QtCore import (
    Qt, QPoint, QRectF, QPointF, QRect, pyqtSignal, QLineF
)
from PIL import Image
import math # ドラッグ補間用

# image_utils から pillow_to_qimage をインポート
try:
    from .image_utils import pillow_to_qimage
except ImportError:
    # フォールバック実装 (念のため残す)
    print("Warning: Could not import pillow_to_qimage from image_utils.")
    def pillow_to_qimage(pil_img):
        try:
            if pil_img.mode == 'RGBA':
                data = pil_img.tobytes('raw', 'RGBA')
                qimage = QImage(data, pil_img.width, pil_img.height, QImage.Format.Format_RGBA8888)
                return qimage.copy()
            elif pil_img.mode == 'RGB':
                data = pil_img.tobytes('raw', 'RGB')
                qimage = QImage(data, pil_img.width, pil_img.height, QImage.Format.Format_RGB888)
                return qimage.copy()
            else:
                rgba_img = pil_img.convert('RGBA')
                data = rgba_img.tobytes('raw', 'RGBA')
                qimage = QImage(data, rgba_img.width, rgba_img.height, QImage.Format.Format_RGBA8888)
                return qimage.copy()
        except Exception as e:
            print(f"Error in fallback pillow_to_qimage: {e}")
            return None

GRID_DELETE_MODIFIER = Qt.KeyboardModifier.ControlModifier
PAN_MODIFIER = Qt.KeyboardModifier.AltModifier

# --- グリッド線の色と太さを定義 ---
GRID_PEN = QPen(QColor(100, 100, 100, 128), 1)
GRID_PEN.setCosmetic(True) # スケーリングに関わらず太さ一定

# --- 非選択領域のオーバーレイ色 ---
OVERLAY_COLOR = QColor(0, 0, 0, 80) # 半透明の黒に変更

# --- ホバー/ドラッグ中のグリッド線のハイライト色 ---
GRID_HIGHLIGHT_PEN = QPen(QColor(255, 255, 0, 200), 2)
GRID_HIGHLIGHT_PEN.setCosmetic(True)


class InteractiveImageLabel(QLabel):
    """グリッド/ピクセル編集・ズーム・パン可能なカスタムラベル"""
    # --- シグナル定義 ---
    scaleChanged = pyqtSignal(float)
    viewChanged = pyqtSignal(float, QPointF)
    gridChanged = pyqtSignal()
    requestGridChangeUndoable = pyqtSignal(list, list, list, list, str)
    pixelInteraction = pyqtSignal(QPoint, Qt.KeyboardModifier, str) # press, move, release
    # 領域外クリックのシグナルを追加
    clickedOutsidePixels = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.original_pil_image = None
        self.display_pixmap = None # オリジナル画像表示用 (Phase 1, 2)
        self._scale_factor = 1.0
        self.min_scale = 0.05
        self.max_scale = 50.0
        self._view_center_img_pos = QPointF(0.0, 0.0)
        self.label_center = QPoint(0, 0)
        # グリッド関連
        self._grid_cols = [] # 元画像のX座標リスト
        self._grid_rows = [] # 元画像のY座標リスト
        self.show_grid = True
        self.line_hit_tolerance = 8 # ピクセル単位
        self.dragging_line_type = None # 'col' or 'row'
        self.dragging_line_index = -1
        self.drag_start_pos_label = None
        self.drag_start_grid_cols = []
        self.drag_start_grid_rows = []
        self.grid_editing_enabled = False
        self._hover_line_type = None
        self._hover_line_index = -1
        # パン関連
        self.panning = False
        self.pan_start_pos_label = None
        self.pan_start_view_center = QPointF(0.0, 0.0)
        # ピクセル選択関連
        self.pixel_selection_enabled = False
        self._pixel_map_ref = {} # MainWindowから参照を受け取る
        self._selected_coords_ref = set() # MainWindowから参照を受け取る
        self._is_dragging_pixel_selection = False
        self._last_move_pos_pixel_selection = None

        self.setMinimumSize(300, 300)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("background-color: #333; border: 1px solid gray;")
        self.setMouseTracking(True) # マウスムーブイベントを常に受け取る
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus) # キーイベントを受け取るため

    # --- 参照設定メソッド ---
    def set_pixel_map_ref(self, pixel_map: dict):
        self._pixel_map_ref = pixel_map
        if self.pixel_selection_enabled: self.update()

    def set_selected_coords_ref(self, selected_coords: set):
        self._selected_coords_ref = selected_coords
        if self.pixel_selection_enabled: self.update()

    # --- モード設定メソッド ---
    def setGridEditingEnabled(self, enabled: bool):
        if self.grid_editing_enabled != enabled:
            self.grid_editing_enabled = enabled
            if enabled: self.pixel_selection_enabled = False # 排他制御
            self.update() # モード変更で再描画

    def setPixelSelectionEnabled(self, enabled: bool):
        if self.pixel_selection_enabled != enabled:
            self.pixel_selection_enabled = enabled
            if enabled: self.grid_editing_enabled = False # 排他制御
            self.update() # モード変更で再描画

    # --- ゲッター/セッター/基本操作 ---
    def getScaleFactor(self): return self._scale_factor
    def getViewCenter(self): return self._view_center_img_pos
    def getGridLines(self): return list(self._grid_cols), list(self._grid_rows)

    def setGridLinesDirectly(self, cols, rows):
        # 値をfloatにしてソート
        new_cols = sorted([float(x) for x in cols])
        new_rows = sorted([float(y) for y in rows])
        needs_update = False
        # 変更があったか比較
        if len(new_cols) != len(self._grid_cols) or not all(abs(a - b) < 1e-6 for a, b in zip(new_cols, self._grid_cols)):
            self._grid_cols = new_cols; needs_update = True
        if len(new_rows) != len(self._grid_rows) or not all(abs(a - b) < 1e-6 for a, b in zip(new_rows, self._grid_rows)):
            self._grid_rows = new_rows; needs_update = True
        if needs_update:
            self.update() # 変更があれば再描画

    def setPilImage(self, pil_image):
        """Pillow画像をセットし、表示と状態を初期化"""
        self.original_pil_image = pil_image
        # グリッドと状態をリセット
        self._grid_cols = []; self._grid_rows = []
        self.dragging_line_type = None; self.panning = False
        self._hover_line_type = None; self._hover_line_index = -1
        self._is_dragging_pixel_selection = False

        if self.original_pil_image:
            # Pillow -> QImage -> QPixmap 変換
            qimage = pillow_to_qimage(self.original_pil_image)
            if qimage:
                self.display_pixmap = QPixmap.fromImage(qimage)
                self.show_grid = True
                self.setStyleSheet("background-color: #333; border: 1px solid gray;")
                # 画像中心をビューの中心に設定
                img_w, img_h = self.original_pil_image.size
                self._view_center_img_pos = QPointF(img_w / 2.0, img_h / 2.0)
                # ウィンドウにフィットさせる
                self.fitToWindow() # これが update() を呼ぶ
            else:
                 # 変換失敗時
                 self.display_pixmap = None; self.show_grid = False
                 self.clear(); self.setText("画像表示エラー")
                 self.setStyleSheet("background-color: #500; border: 1px solid red; color: white;")
                 self.update()
        else:
             # 画像がNoneの場合
             self.display_pixmap = None; self.show_grid = False
             self.clear(); self.setText("オリジナル画像")
             self.setStyleSheet("background-color: #333; border: 1px solid gray;")
             self.update()

    def fitToWindow(self):
        """画像をラベル全体に表示するようにスケールと中心を調整"""
        if not self.original_pil_image or self.width() <= 0 or self.height() <= 0:
            # 画像がない場合やラベルサイズが不正な場合はデフォルトに
            new_scale = 1.0
            new_center = QPointF(0,0)
            if self.original_pil_image:
                img_w, img_h = self.original_pil_image.size
                new_center = QPointF(img_w / 2.0, img_h / 2.0)
        else:
             img_w, img_h = self.original_pil_image.size
             label_w, label_h = self.width() - 2, self.height() - 2 # ボーダー分考慮
             if img_w <= 0 or img_h <= 0: # 画像サイズが不正な場合
                 new_scale = 1.0
                 new_center = QPointF(0,0)
             else:
                 scale_w = label_w / img_w; scale_h = label_h / img_h
                 # 幅・高さ両方が収まるようにスケールを決定
                 new_scale = max(self.min_scale, min(min(scale_w, scale_h), self.max_scale))
                 # 中心は画像の中心
                 new_center = QPointF(img_w / 2.0, img_h / 2.0)

        # 変更があった場合のみシグナルを発行して更新
        scale_changed = abs(new_scale - self._scale_factor) > 1e-6
        center_changed = (new_center - self._view_center_img_pos).manhattanLength() > 1e-6

        self._scale_factor = new_scale
        self._view_center_img_pos = new_center

        if scale_changed: self.scaleChanged.emit(self._scale_factor)
        if scale_changed or center_changed: self.viewChanged.emit(self._scale_factor, self._view_center_img_pos)
        self.update()

    def setScaleFactor(self, new_scale, zoom_center_label_pos=None):
        """指定されたスケールに設定し、指定位置中心にズーム"""
        if not self.original_pil_image: return
        # スケールを制限範囲内にクリップ
        new_scale = max(self.min_scale, min(new_scale, self.max_scale))
        # スケールが変わらないなら何もしない
        if abs(new_scale - self._scale_factor) < 1e-6: return

        # ズーム中心が指定されなければラベルの中心を使う
        if zoom_center_label_pos is None:
            zoom_center_label_pos = self.rect().center()

        # ズーム前の中心点の画像座標
        img_pos_before_zoom = self.label_to_image_coords(zoom_center_label_pos)

        old_scale = self._scale_factor
        self._scale_factor = new_scale

        # ズーム後のビュー中心を計算
        # (ズーム中心の画像座標はズーム後も同じラベル位置に来るように調整)
        # ズーム中心から現在のビュー中心までのベクトル (画像座標系)
        center_offset_img = self._view_center_img_pos - img_pos_before_zoom
        # スケール変更後のベクトル
        new_center_offset_img = center_offset_img * (new_scale / old_scale)
        # 新しいビュー中心
        self._view_center_img_pos = img_pos_before_zoom + new_center_offset_img

        # シグナル発行と再描画
        self.scaleChanged.emit(self._scale_factor)
        self.viewChanged.emit(self._scale_factor, self._view_center_img_pos)
        self.update()

    def setViewCenter(self, new_center_img_pos):
         """ビューの中心を指定された画像座標に設定"""
         if not self.original_pil_image: return
         # 中心位置が変わった場合のみ更新
         if (new_center_img_pos - self._view_center_img_pos).manhattanLength() > 1e-6:
             self._view_center_img_pos = new_center_img_pos
             self.viewChanged.emit(self._scale_factor, self._view_center_img_pos)
             self.update()

    # --- 座標変換メソッド ---
    def label_to_image_coords(self, label_pos: QPoint) -> QPointF:
        """ラベル上の座標を元画像の座標に変換"""
        if not self.original_pil_image: return QPointF(0, 0)
        img_w_orig, img_h_orig = self.original_pil_image.size
        if img_w_orig <= 0 or img_h_orig <=0: return QPointF(0,0)

        # ラベルの中心座標
        label_center = self.rect().center()
        # 画像の原点(0,0)がラベル上のどこに来るか計算
        img_x_origin_label = label_center.x() - self._view_center_img_pos.x() * self._scale_factor
        img_y_origin_label = label_center.y() - self._view_center_img_pos.y() * self._scale_factor
        # 指定されたラベル座標の、画像原点からの相対位置（ラベル座標系）
        relative_x_label = label_pos.x() - img_x_origin_label
        relative_y_label = label_pos.y() - img_y_origin_label

        # スケールが0に近い場合はエラーを防ぐ
        if abs(self._scale_factor) < 1e-9: return self._view_center_img_pos

        # ラベル座標系での相対位置をスケールで割って画像座標に変換
        img_x = relative_x_label / self._scale_factor
        img_y = relative_y_label / self._scale_factor
        return QPointF(img_x, img_y)

    def image_to_label_coords(self, img_pos: QPointF) -> QPoint:
        """元画像の座標をラベル上の座標に変換"""
        if not self.original_pil_image: return QPoint(0, 0)

        # ラベルの中心座標
        label_center = self.rect().center()
        # 画像の原点(0,0)がラベル上のどこに来るか計算
        img_x_origin_label = label_center.x() - self._view_center_img_pos.x() * self._scale_factor
        img_y_origin_label = label_center.y() - self._view_center_img_pos.y() * self._scale_factor
        # 画像座標を指定されたスケールで拡大し、画像原点のラベル位置に加算
        label_x = img_x_origin_label + img_pos.x() * self._scale_factor
        label_y = img_y_origin_label + img_pos.y() * self._scale_factor
        # 整数座標に丸めて返す
        return QPoint(int(round(label_x)), int(round(label_y)))

    # --- イベントハンドラ ---
    def resizeEvent(self, event):
        """リサイズ時に再描画"""
        super().resizeEvent(event)
        # リサイズ後にビューの中心を再計算する必要があるかもしれないが、
        # 通常は中心を維持したまま表示領域が変わるだけで良い
        self.update()

    def paintEvent(self, event):
        """描画イベントハンドラ"""
        super().paintEvent(event) # 親クラスの描画（背景など）
        painter = QPainter(self)
        # アンチエイリアスはオフ（ピクセルアート的な表示のため）
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)

        # 画像が表示されるターゲット矩形を計算
        target_rect_on_label = QRectF()
        visible_rect_img_f = QRectF() # 画像座標系での可視範囲
        if self.original_pil_image:
            # 画像の左上(0,0)と右下(w,h)のラベル座標を計算
            target_top_left = self.image_to_label_coords(QPointF(0,0))
            target_bottom_right = self.image_to_label_coords(QPointF(self.original_pil_image.width, self.original_pil_image.height))
            # 座標が反転する場合も考慮して正規化
            target_rect_on_label = QRectF(QPointF(target_top_left), QPointF(target_bottom_right)).normalized()
            # ラベルの表示領域に対応する画像座標範囲
            visible_rect_on_label = self.rect()
            visible_rect_img_f = QRectF(
                self.label_to_image_coords(visible_rect_on_label.topLeft()),
                self.label_to_image_coords(visible_rect_on_label.bottomRight())
            ).normalized()

        # --- 描画処理 ---
        if self.pixel_selection_enabled and self._pixel_map_ref:
            # === フェーズ3: ピクセルマップベース描画 & オーバーレイ ===
            # 1. ピクセル描画 (可視範囲のみ)
            for coords, data in self._pixel_map_ref.items():
                rect_orig_tuple = data['rect'] # (left, top, right, bottom) in image coords
                color_tuple = data['color']    # (R, G, B, A)
                # 元画像の矩形
                rect_orig = QRectF(rect_orig_tuple[0], rect_orig_tuple[1],
                                   rect_orig_tuple[2] - rect_orig_tuple[0], # width
                                   rect_orig_tuple[3] - rect_orig_tuple[1]) # height

                # 可視範囲外のピクセルは描画しない
                if not visible_rect_img_f.intersects(rect_orig): continue

                # ラベル上の描画矩形を計算
                tl_label = self.image_to_label_coords(rect_orig.topLeft())
                br_label = self.image_to_label_coords(rect_orig.bottomRight())
                rect_label_f = QRectF(QPointF(tl_label), QPointF(br_label)).normalized()

                # 色を設定して矩形を描画
                q_color = QColor(color_tuple[0], color_tuple[1], color_tuple[2], color_tuple[3])
                painter.fillRect(rect_label_f, q_color)

            # 2. グリッド線 (ピクセルマップ上にも表示)
            if self.show_grid:
                self._paint_grid_lines(painter, visible_rect_on_label, visible_rect_img_f)

            # 3. 選択オーバーレイ
            if self._selected_coords_ref is not None:
                # 画像全体の領域をパスとして作成
                overlay_path = QPainterPath()
                overlay_path.addRect(target_rect_on_label)
                # 選択されているピクセルの領域をパスとして作成
                selection_path = QPainterPath()
                if self._selected_coords_ref:
                    for c, r in self._selected_coords_ref:
                        if (c, r) in self._pixel_map_ref:
                            rect_orig = self._pixel_map_ref[(c, r)]['rect']
                            tl = self.image_to_label_coords(QPointF(rect_orig[0], rect_orig[1]))
                            br = self.image_to_label_coords(QPointF(rect_orig[2], rect_orig[3]))
                            selection_path.addRect(QRectF(QPointF(tl), QPointF(br)).normalized())
                # 全体パスから選択パスを引いた領域（＝非選択領域）を作成
                final_overlay_path = overlay_path.subtracted(selection_path)
                # 半透明色で非選択領域を塗りつぶす
                painter.fillPath(final_overlay_path, OVERLAY_COLOR)

        elif self.display_pixmap:
            # === フェーズ1, 2: オリジナル画像表示 & グリッド線 ===
            # 1. オリジナル画像描画
            # target_rect_on_label に display_pixmap を描画
            painter.drawPixmap(target_rect_on_label.toRect(), self.display_pixmap)

            # 2. グリッド線描画
            if self.show_grid:
                 self._paint_grid_lines(painter, visible_rect_on_label, visible_rect_img_f)

        else:
             # 画像がない場合はテキスト表示
             painter.setPen(QColor(150, 150, 150))
             painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())

        # --- 4. 操作ヒント描画 ---
        self._paint_operation_hints(painter)

        painter.end()

    def _paint_grid_lines(self, painter, visible_rect_on_label, visible_rect_img_f):
        """グリッド線を描画するヘルパー"""
        if not self.original_pil_image: return

        img_w, img_h = self.original_pil_image.size
        current_pos = self.mapFromGlobal(QCursor.pos()) # 現在のマウスカーソル位置

        # 通常のグリッド線
        painter.setPen(GRID_PEN)
        for i, x_img in enumerate(self._grid_cols):
            # 可視範囲内かチェック（少し余裕を持たせる）
            if visible_rect_img_f.left() - 1 < x_img < visible_rect_img_f.right() + 1:
                p1 = self.image_to_label_coords(QPointF(x_img, 0))
                # ホバー中またはドラッグ中の線はハイライトしない（後で描画）
                if not (self.dragging_line_type == 'col' and self.dragging_line_index == i) and \
                   not (self._hover_line_type == 'col' and self._hover_line_index == i):
                    painter.drawLine(p1.x(), visible_rect_on_label.top(), p1.x(), visible_rect_on_label.bottom())
        for i, y_img in enumerate(self._grid_rows):
            if visible_rect_img_f.top() - 1 < y_img < visible_rect_img_f.bottom() + 1:
                p1 = self.image_to_label_coords(QPointF(0, y_img))
                if not (self.dragging_line_type == 'row' and self.dragging_line_index == i) and \
                   not (self._hover_line_type == 'row' and self._hover_line_index == i):
                    painter.drawLine(visible_rect_on_label.left(), p1.y(), visible_rect_on_label.right(), p1.y())

        # ハイライトするグリッド線 (ホバー中またはドラッグ中)
        painter.setPen(GRID_HIGHLIGHT_PEN)
        if self.dragging_line_type == 'col':
            x_img = self._grid_cols[self.dragging_line_index]
            p1 = self.image_to_label_coords(QPointF(x_img, 0))
            painter.drawLine(p1.x(), visible_rect_on_label.top(), p1.x(), visible_rect_on_label.bottom())
        elif self.dragging_line_type == 'row':
            y_img = self._grid_rows[self.dragging_line_index]
            p1 = self.image_to_label_coords(QPointF(0, y_img))
            painter.drawLine(visible_rect_on_label.left(), p1.y(), visible_rect_on_label.right(), p1.y())
        elif self._hover_line_type == 'col': # ドラッグ中でない場合のみホバー表示
             x_img = self._grid_cols[self._hover_line_index]
             p1 = self.image_to_label_coords(QPointF(x_img, 0))
             painter.drawLine(p1.x(), visible_rect_on_label.top(), p1.x(), visible_rect_on_label.bottom())
        elif self._hover_line_type == 'row':
             y_img = self._grid_rows[self._hover_line_index]
             p1 = self.image_to_label_coords(QPointF(0, y_img))
             painter.drawLine(visible_rect_on_label.left(), p1.y(), visible_rect_on_label.right(), p1.y())


    def _paint_operation_hints(self, painter):
        """操作ヒントを左上に描画するヘルパー"""
        hint_text = ""
        if self.original_pil_image:
            modifiers = QGuiApplication.keyboardModifiers()
            current_pos = self.mapFromGlobal(QCursor.pos()) # 現在のカーソル位置
            is_over_label = self.rect().contains(current_pos)

            if is_over_label:
                 # パン操作が最優先
                 if modifiers & PAN_MODIFIER:
                     hint_text = "Alt+ドラッグ: 画像移動"
                 elif self.grid_editing_enabled:
                     # グリッド編集モードのヒント
                     hit_col_idx, hit_row_idx = self._find_closest_line(current_pos)
                     if modifiers & Qt.KeyboardModifier.ShiftModifier:
                         hint_text = "Shift+左/右クリック: 縦/横線追加"
                     elif modifiers & GRID_DELETE_MODIFIER:
                         if hit_col_idx != -1 or hit_row_idx != -1:
                             hint_text = "Ctrl+クリック: グリッド線削除"
                         else: hint_text = "Ctrl+クリック: グリッド線削除 (線の上で)"
                     elif hit_col_idx != -1 or hit_row_idx != -1:
                         hint_text = "線ドラッグ: 移動 | Delete/Backspace: 削除"
                     else:
                         hint_text = "Shift+Click:線追加, Ctrl+Click:削除, Drag:移動" # デフォルトヒント
                 elif self.pixel_selection_enabled:
                      # ピクセル選択モードのヒント
                      hint_text = "クリック:個別選択/解除, Shift+クリック:同色選択/解除, ドラッグ:範囲選択, 範囲外クリック:全解除"
                 else: # 通常モード (パンのみ可能)
                      hint_text = "Alt+ドラッグ: 画像移動"

        if hint_text:
            # ヒントテキストの描画設定
            painter.setPen(QColor(230, 230, 230, 200)) # 見やすい色
            font = painter.font(); font.setPointSize(10); painter.setFont(font)
            # 背景を少し暗くして読みやすくする
            text_rect = painter.boundingRect(QRectF(10, 5, self.width()-20, 30), Qt.AlignmentFlag.AlignLeft, hint_text)
            bg_rect = text_rect.adjusted(-3, -1, 3, 1)
            painter.fillRect(bg_rect, QColor(0, 0, 0, 100))
            # テキスト描画
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft, hint_text)

    def wheelEvent(self, event: QWheelEvent):
        """マウスホイールでズーム"""
        if not self.original_pil_image: return
        angle = event.angleDelta().y() # Y方向の回転量を取得
        if angle == 0: return # 回転量がなければ何もしない

        # ズーム係数を決定 (回転方向で増減)
        zoom_factor = 1.15 if angle > 0 else 1 / 1.15
        # 現在のカーソル位置を中心にズーム
        self.setScaleFactor(self._scale_factor * zoom_factor, event.position().toPoint())
        event.accept() # イベント処理済み

    def mousePressEvent(self, event: QMouseEvent):
        """マウスクリックイベント"""
        if not self.original_pil_image:
            event.ignore(); return # 画像がなければ無視

        pos_label = event.position().toPoint() # クリック位置（ラベル座標）
        modifiers = QApplication.keyboardModifiers() # 修飾キーの状態
        button = event.button() # クリックされたボタン
        is_alt_pressed = bool(modifiers & PAN_MODIFIER)

        # 1. パン操作開始 (Alt + 左クリック)
        if button == Qt.MouseButton.LeftButton and is_alt_pressed:
            self.panning = True
            self.pan_start_pos_label = pos_label
            self.pan_start_view_center = self._view_center_img_pos
            self.setCursor(Qt.CursorShape.OpenHandCursor) # カーソル変更
            event.accept(); return

        # 2. グリッド編集操作 (グリッド編集モード時)
        if self.grid_editing_enabled:
            is_ctrl = bool(modifiers & GRID_DELETE_MODIFIER)
            is_shift = bool(modifiers & Qt.KeyboardModifier.ShiftModifier)

            # グリッド線削除 (Ctrl + 左クリック)
            if button == Qt.MouseButton.LeftButton and is_ctrl and not is_shift:
                 hit_col_idx, hit_row_idx = self._find_closest_line(pos_label)
                 if hit_col_idx != -1 or hit_row_idx != -1:
                     old_cols, old_rows = self.getGridLines()
                     new_cols, new_rows = self._delete_closest_line(pos_label, hit_col_idx, hit_row_idx, old_cols, old_rows)
                     if new_cols is not None: # 実際に削除された場合
                         # Undo可能なコマンドとしてリクエスト
                         self.requestGridChangeUndoable.emit(old_cols, old_rows, new_cols, new_rows, "グリッド線削除")
                 event.accept(); return

            # 縦線追加 (Shift + 左クリック)
            elif button == Qt.MouseButton.LeftButton and is_shift and not is_ctrl:
                 img_pos = self.label_to_image_coords(pos_label)
                 img_w, img_h = self.original_pil_image.size
                 min_dist_label = 5 # ラベル上で最低5px離す
                 # 画像範囲内か、既存線と近すぎないかチェック
                 if 0 < img_pos.x() < img_w:
                     old_cols, old_rows = self.getGridLines()
                     can_add = all(abs(pos_label.x() - self.image_to_label_coords(QPointF(x, 0)).x()) >= min_dist_label for x in old_cols)
                     if can_add:
                         new_cols = sorted(list(old_cols) + [img_pos.x()])
                         self.requestGridChangeUndoable.emit(old_cols, old_rows, new_cols, old_rows, "縦グリッド線追加")
                 event.accept(); return

            # 横線追加 (Shift + 右クリック)
            elif button == Qt.MouseButton.RightButton and is_shift:
                 img_pos = self.label_to_image_coords(pos_label)
                 img_w, img_h = self.original_pil_image.size
                 min_dist_label = 5
                 if 0 < img_pos.y() < img_h:
                     old_cols, old_rows = self.getGridLines()
                     can_add = all(abs(pos_label.y() - self.image_to_label_coords(QPointF(0, y)).y()) >= min_dist_label for y in old_rows)
                     if can_add:
                         new_rows = sorted(list(old_rows) + [img_pos.y()])
                         self.requestGridChangeUndoable.emit(old_cols, old_rows, old_cols, new_rows, "横グリッド線追加")
                 event.accept(); return

            # グリッド線ドラッグ開始 (修飾キーなし + 左クリック + 線の上)
            elif button == Qt.MouseButton.LeftButton and not is_ctrl and not is_shift:
                 hit_col_idx, hit_row_idx = self._find_closest_line(pos_label)
                 drag_target, idx = self._determine_drag_target(pos_label, hit_col_idx, hit_row_idx)
                 if drag_target: # 線の上でクリックされた場合
                     self.dragging_line_type = drag_target
                     self.dragging_line_index = idx
                     self.drag_start_pos_label = pos_label
                     # Undo用にドラッグ開始時のグリッド状態を保存
                     self.drag_start_grid_cols, self.drag_start_grid_rows = self.getGridLines()
                     # カーソル変更
                     cursor = Qt.CursorShape.SizeHorCursor if drag_target == 'col' else Qt.CursorShape.SizeVerCursor
                     self.setCursor(cursor)
                     event.accept(); return
                 else: # 線の上でない場合は無視
                     event.ignore()
            else: # その他のグリッド編集中のクリックは無視
                event.ignore()

        # 3. ピクセル選択操作 (ピクセル選択モード時 + 左クリック)
        elif self.pixel_selection_enabled and button == Qt.MouseButton.LeftButton:
            # クリック位置がピクセル上かどうかチェック
            img_pos_f = self.label_to_image_coords(pos_label)
            pixel_coords = self._get_pixel_coords_at_img_pos(img_pos_f)

            if pixel_coords is not None:
                 # ピクセル上でクリックされた場合
                 self._is_dragging_pixel_selection = True
                 self._last_move_pos_pixel_selection = pos_label
                 # MainWindowにインタラクションを通知
                 self.pixelInteraction.emit(pos_label, modifiers, 'press')
                 event.accept(); return
            else:
                 # ピクセル外でクリックされた場合 (全選択解除)
                 # 選択がある場合のみシグナル発行
                 if self._selected_coords_ref:
                     self.clickedOutsidePixels.emit()
                 event.accept(); return # 領域外クリックも処理済みとする

        # 上記のいずれにも該当しない場合はイベントを無視
        event.ignore()

    def mouseMoveEvent(self, event: QMouseEvent):
        """マウス移動イベント"""
        if not self.original_pil_image: return
        pos_label = event.position().toPoint()
        modifiers = QApplication.keyboardModifiers()

        # 1. パン操作中 (左ボタン押下中)
        if self.panning and (event.buttons() & Qt.MouseButton.LeftButton):
            # カーソル形状がまだ変わっていなければ変更
            if self.cursor().shape() != Qt.CursorShape.ClosedHandCursor:
                self.setCursor(Qt.CursorShape.ClosedHandCursor)
            # 移動量を計算 (ラベル座標系)
            delta_label = pos_label - self.pan_start_pos_label
            # スケールが0に近い場合は処理しない
            if abs(self._scale_factor) < 1e-9: return
            # 移動量を画像座標系に変換
            delta_img_x = delta_label.x() / self._scale_factor
            delta_img_y = delta_label.y() / self._scale_factor
            # 新しいビュー中心を計算して設定
            new_center = self.pan_start_view_center - QPointF(delta_img_x, delta_img_y)
            self.setViewCenter(new_center)
            event.accept(); return

        # 2. グリッド線ドラッグ中 (左ボタン押下中)
        if self.grid_editing_enabled and self.dragging_line_type and (event.buttons() & Qt.MouseButton.LeftButton):
            # グリッド線を移動させる
            moved = self._move_dragging_grid_line(pos_label)
            if moved:
                self.update() # 再描画
                self.gridChanged.emit() # グリッド変更シグナル発行 (プレビュー更新用)
            event.accept(); return

        # 3. ピクセル選択ドラッグ中 (左ボタン押下中)
        if self.pixel_selection_enabled and self._is_dragging_pixel_selection and (event.buttons() & Qt.MouseButton.LeftButton):
            prev_pos = self._last_move_pos_pixel_selection
            # 前回の位置と異なる場合のみ処理 (Noneチェックも)
            if pos_label != prev_pos and prev_pos is not None:
                # 線形補間して間のピクセルも選択/解除できるようにする
                line = QLineF(QPointF(prev_pos), QPointF(pos_label))
                length = line.length()
                # 5ピクセルごとに補間点を生成（最低1ステップ）
                steps = max(1, int(length / 5))

                for i in range(steps + 1): # 終点も含む
                    t = i / steps if steps > 0 else 0.0
                    # QPointFで補間点を計算
                    interpolated_pos_f = QPointF(prev_pos) + (QPointF(pos_label) - QPointF(prev_pos)) * t
                    # QPointに丸めてシグナルを発行
                    interpolated_pos_int = QPoint(round(interpolated_pos_f.x()), round(interpolated_pos_f.y()))
                    self.pixelInteraction.emit(interpolated_pos_int, modifiers, 'move')

                # 最後の位置を更新
                self._last_move_pos_pixel_selection = pos_label
            event.accept()
            return

        # 4. ホバー処理とカーソル形状変更 (ボタン押下なし)
        if not (event.buttons() & Qt.MouseButton.LeftButton): # ボタンが押されていない場合のみ
            cursor_shape = Qt.CursorShape.ArrowCursor # デフォルトカーソル
            new_hover_line_type = None
            new_hover_line_index = -1

            if self.original_pil_image:
                 # パン可能か (Altキー)
                 if bool(modifiers & PAN_MODIFIER):
                     cursor_shape = Qt.CursorShape.OpenHandCursor
                 # グリッド編集モードか
                 elif self.grid_editing_enabled:
                     cursor_shape, new_hover_line_type, new_hover_line_index = self._get_grid_edit_cursor_and_hover(pos_label, modifiers)
                 # ピクセル選択モードか
                 elif self.pixel_selection_enabled:
                     # カーソルは通常矢印のままか、十字カーソルなどが考えられる
                     # ここでは特に変更しない
                      pass

            # ホバー状態が変化した場合のみ更新
            if new_hover_line_type != self._hover_line_type or new_hover_line_index != self._hover_line_index:
                 self._hover_line_type = new_hover_line_type
                 self._hover_line_index = new_hover_line_index
                 self.update() # ホバーハイライトのために再描画

            # カーソル形状が変化した場合のみ設定
            if self.cursor().shape() != cursor_shape:
                self.setCursor(cursor_shape)

        event.ignore() # 上記以外は無視

    def mouseReleaseEvent(self, event: QMouseEvent):
        """マウスボタン解放イベント"""
        pos_label = event.position().toPoint()
        modifiers = QApplication.keyboardModifiers()

        # 1. パン終了
        if event.button() == Qt.MouseButton.LeftButton and self.panning:
            self.panning = False
            self.unsetCursor() # カーソルを元に戻す
            event.accept(); return

        # 2. グリッド線ドラッグ終了
        if self.grid_editing_enabled and event.button() == Qt.MouseButton.LeftButton and self.dragging_line_type:
            # ドラッグ前後でグリッド状態が変わったかチェック
            current_cols, current_rows = self.getGridLines()
            if self._grid_state_changed(self.drag_start_grid_cols, self.drag_start_grid_rows, current_cols, current_rows):
                 # 変更があればUndo可能なコマンドとしてリクエスト
                 self.requestGridChangeUndoable.emit(self.drag_start_grid_cols, self.drag_start_grid_rows, current_cols, current_rows, "グリッド線移動")
            # ドラッグ状態をリセット
            self.dragging_line_type = None; self.dragging_line_index = -1; self.drag_start_pos_label = None
            self.drag_start_grid_cols = []; self.drag_start_grid_rows = []
            self.unsetCursor() # カーソルを元に戻す
            # ホバー状態も更新しておく
            self._update_hover_state(pos_label)
            self.update() # 最終的な状態で再描画
            event.accept(); return

        # 3. ピクセル選択ドラッグ終了
        if self.pixel_selection_enabled and event.button() == Qt.MouseButton.LeftButton and self._is_dragging_pixel_selection:
            self._is_dragging_pixel_selection = False
            # 最後の位置で release イベントを通知
            self.pixelInteraction.emit(pos_label, modifiers, 'release')
            self._last_move_pos_pixel_selection = None # 最後の位置情報をクリア
            event.accept()
            return

        # 上記以外は無視
        event.ignore()

    def leaveEvent(self, event):
        """マウスカーソルがラベル外に出たイベント"""
        # ホバー状態をリセットして再描画
        if self._hover_line_type is not None:
            self._hover_line_type = None
            self._hover_line_index = -1
            self.update()
        super().leaveEvent(event)


    def keyPressEvent(self, event: QKeyEvent):
        """キー押下イベント"""
        if not self.original_pil_image: event.ignore(); return
        key = event.key()

        # 1. グリッド線削除 (Delete/Backspaceキー)
        if self.grid_editing_enabled and key in (Qt.Key.Key_Delete, Qt.Key.Key_Backspace):
             current_pos = self.mapFromGlobal(QCursor.pos()) # 現在のカーソル位置
             if self.rect().contains(current_pos): # カーソルがラベル上にあるか
                 hit_col_idx, hit_row_idx = self._find_closest_line(current_pos)
                 if hit_col_idx != -1 or hit_row_idx != -1: # 線の上か
                     old_cols, old_rows = self.getGridLines()
                     new_cols, new_rows = self._delete_closest_line(current_pos, hit_col_idx, hit_row_idx, old_cols, old_rows)
                     if new_cols is not None: # 削除成功
                         self.requestGridChangeUndoable.emit(old_cols, old_rows, new_cols, new_rows, "グリッド線削除 (キー)")
             event.accept(); return

        # 2. ズーム / フィット (+, -, 0 キー)
        if key == Qt.Key.Key_Plus or key == Qt.Key.Key_Equal:
            self.setScaleFactor(self._scale_factor * 1.2); event.accept(); return
        elif key == Qt.Key.Key_Minus:
            self.setScaleFactor(self._scale_factor / 1.2); event.accept(); return
        elif key == Qt.Key.Key_0:
            self.fitToWindow(); event.accept(); return

        # 上記以外は無視
        event.ignore()

    # --- ヘルパーメソッド ---
    def _find_closest_line(self, pos_label):
        """指定したラベル座標に最も近いグリッド線を見つける"""
        if not self.show_grid or not self.original_pil_image or (not self._grid_cols and not self._grid_rows):
             return -1, -1 # グリッド非表示、画像なし、線なしの場合

        min_dist_col, hit_col_idx = float('inf'), -1
        min_dist_row, hit_row_idx = float('inf'), -1

        # 画像が表示されているラベル上の矩形を計算
        img_w, img_h = self.original_pil_image.size
        img_tl = self.image_to_label_coords(QPointF(0,0))
        img_br = self.image_to_label_coords(QPointF(img_w, img_h))
        img_rect_label = QRect(img_tl, img_br).normalized()
        vy_min, vy_max = img_rect_label.top(), img_rect_label.bottom()
        vx_min, vx_max = img_rect_label.left(), img_rect_label.right()

        # 許容範囲 (ラベル上のピクセル数)
        tol = self.line_hit_tolerance

        # 縦線をチェック
        for i, x_img in enumerate(self._grid_cols):
            lx = self.image_to_label_coords(QPointF(x_img, 0)).x() # 縦線のX座標 (ラベル上)
            dx = abs(pos_label.x() - lx) # クリック位置とのX距離
            # X距離が許容範囲内 かつ Y座標が画像表示範囲内(許容範囲込み) かつ 最も近い線か
            if dx <= tol and (vy_min - tol <= pos_label.y() <= vy_max + tol) and dx < min_dist_col:
                 min_dist_col = dx; hit_col_idx = i

        # 横線をチェック
        for i, y_img in enumerate(self._grid_rows):
            ly = self.image_to_label_coords(QPointF(0, y_img)).y() # 横線のY座標 (ラベル上)
            dy = abs(pos_label.y() - ly) # クリック位置とのY距離
            # Y距離が許容範囲内 かつ X座標が画像表示範囲内(許容範囲込み) かつ 最も近い線か
            if dy <= tol and (vx_min - tol <= pos_label.x() <= vx_max + tol) and dy < min_dist_row:
                 min_dist_row = dy; hit_row_idx = i

        return hit_col_idx, hit_row_idx

    def _determine_drag_target(self, pos_label, hit_col_idx, hit_row_idx):
        """ヒットした線の中から、ドラッグ対象となる線を決定する"""
        if hit_col_idx == -1 and hit_row_idx == -1: return None, -1 # ヒットなし
        if hit_col_idx != -1 and hit_row_idx == -1: return 'col', hit_col_idx # 縦線のみ
        if hit_col_idx == -1 and hit_row_idx != -1: return 'row', hit_row_idx # 横線のみ

        # 両方の線にヒットした場合、より近い方を返す
        lx = self.image_to_label_coords(QPointF(self._grid_cols[hit_col_idx], 0)).x()
        ly = self.image_to_label_coords(QPointF(0, self._grid_rows[hit_row_idx])).y()
        dist_x = abs(pos_label.x() - lx)
        dist_y = abs(pos_label.y() - ly)
        return ('col', hit_col_idx) if dist_x <= dist_y else ('row', hit_row_idx)

    def _move_dragging_grid_line(self, current_pos_label) -> bool:
        """ドラッグ中のグリッド線を指定位置に移動させる"""
        if not self.dragging_line_type or self.dragging_line_index < 0 or not self.original_pil_image:
             return False

        # 現在のラベル座標を画像座標に変換
        new_img_pos = self.label_to_image_coords(current_pos_label)
        img_w, img_h = self.original_pil_image.size
        # グリッド線間の最小間隔 (画像座標系) - 0にはならないように
        min_sep = max(0.1, 1.0 / self._scale_factor) # 1ピクセル相当か0.1の大きい方

        temp_cols, temp_rows = list(self._grid_cols), list(self._grid_rows)
        moved = False
        idx = self.dragging_line_index

        try:
            if self.dragging_line_type == 'col' and 0 <= idx < len(temp_cols):
                # 新しいX座標を画像範囲内にクリップ
                new_x = max(0, min(new_img_pos.x(), img_w))
                # 隣接する線との最小間隔を考慮
                prev_x = temp_cols[idx-1] + min_sep if idx > 0 else 0
                next_x = temp_cols[idx+1] - min_sep if idx < len(temp_cols) - 1 else img_w
                new_x = max(prev_x, min(new_x, next_x)) # 上下限制限
                # 位置が変わったかチェック (微小な変化は無視)
                if abs(temp_cols[idx] - new_x) > 1e-6:
                    temp_cols[idx] = new_x
                    temp_cols.sort() # 順番を維持
                    self._grid_cols = temp_cols # 更新
                    moved = True
            elif self.dragging_line_type == 'row' and 0 <= idx < len(temp_rows):
                # 新しいY座標を画像範囲内にクリップ
                new_y = max(0, min(new_img_pos.y(), img_h))
                # 隣接する線との最小間隔を考慮
                prev_y = temp_rows[idx-1] + min_sep if idx > 0 else 0
                next_y = temp_rows[idx+1] - min_sep if idx < len(temp_rows) - 1 else img_h
                new_y = max(prev_y, min(new_y, next_y))
                # 位置が変わったかチェック
                if abs(temp_rows[idx] - new_y) > 1e-6:
                    temp_rows[idx] = new_y
                    temp_rows.sort()
                    self._grid_rows = temp_rows
                    moved = True
        except IndexError:
             print(f"Error moving grid line: Index {idx} out of bounds.")
             moved = False

        return moved

    def _grid_state_changed(self, old_cols, old_rows, new_cols, new_rows, tol=1e-6):
        """グリッドの状態が変化したかどうかを比較"""
        if len(old_cols) != len(new_cols) or len(old_rows) != len(new_rows): return True
        # ソートして比較
        if not all(abs(a - b) < tol for a, b in zip(sorted(old_cols), sorted(new_cols))): return True
        if not all(abs(a - b) < tol for a, b in zip(sorted(old_rows), sorted(new_rows))): return True
        return False # 変化なし

    def _get_grid_edit_cursor_and_hover(self, pos_label, modifiers):
        """グリッド編集モード時のカーソル形状とホバー状態を取得"""
        cursor_shape = Qt.CursorShape.ArrowCursor
        hover_type = None
        hover_index = -1

        # Shiftキー: 追加モード -> 十字カーソル
        if modifiers & Qt.KeyboardModifier.ShiftModifier:
            cursor_shape = Qt.CursorShape.CrossCursor
        else:
            # 線の上にカーソルがあるかチェック
            hit_col_idx, hit_row_idx = self._find_closest_line(pos_label)
            if hit_col_idx != -1 or hit_row_idx != -1:
                # Ctrlキー: 削除モード -> 指カーソル
                if modifiers & GRID_DELETE_MODIFIER:
                    cursor_shape = Qt.CursorShape.PointingHandCursor
                # 修飾キーなし: 移動モード
                else:
                    drag_target, idx = self._determine_drag_target(pos_label, hit_col_idx, hit_row_idx)
                    if drag_target == 'col':
                        cursor_shape = Qt.CursorShape.SizeHorCursor
                        hover_type = 'col'; hover_index = idx
                    elif drag_target == 'row':
                        cursor_shape = Qt.CursorShape.SizeVerCursor
                        hover_type = 'row'; hover_index = idx
            # 線の上でない場合はデフォルトの矢印カーソル
            else:
                cursor_shape = Qt.CursorShape.ArrowCursor

        return cursor_shape, hover_type, hover_index

    def _update_hover_state(self, current_pos_label):
        """現在のカーソル位置に基づいてホバー状態を更新"""
        if self.grid_editing_enabled and not self.dragging_line_type:
             _, new_hover_type, new_hover_index = self._get_grid_edit_cursor_and_hover(current_pos_label, QApplication.keyboardModifiers())
             if new_hover_type != self._hover_line_type or new_hover_index != self._hover_line_index:
                 self._hover_line_type = new_hover_type
                 self._hover_line_index = new_hover_index
                 self.update()
        elif self._hover_line_type is not None: # グリッド編集でない、またはドラッグ中ならホバー解除
             self._hover_line_type = None
             self._hover_line_index = -1
             self.update()


    def _delete_closest_line(self, pos_label, hit_col_idx, hit_row_idx, current_cols, current_rows):
        """指定位置に最も近いグリッド線を削除した新しいリストを返す"""
        if hit_col_idx == -1 and hit_row_idx == -1: return None, None # 削除対象なし

        new_cols, new_rows = list(current_cols), list(current_rows)
        deleted = False
        # 削除対象を決定 (ドラッグと同じロジック)
        drag_target, idx = self._determine_drag_target(pos_label, hit_col_idx, hit_row_idx)

        try:
            if drag_target == 'col' and 0 <= idx < len(new_cols):
                del new_cols[idx]
                deleted = True
            elif drag_target == 'row' and 0 <= idx < len(new_rows):
                del new_rows[idx]
                deleted = True
        except IndexError:
            print(f"Error deleting grid line: Index {idx} out of bounds.")
            deleted = False

        # 削除された場合のみ新しいリストを返す
        return (new_cols, new_rows) if deleted else (None, None)

    def getGridPositions(self):
        """グリッド線リストから、処理に使用する境界座標リストを生成"""
        if not self.original_pil_image: return [], []
        img_w, img_h = self.original_pil_image.size

        # グリッド線の座標リストを取得し、画像の境界(0, W)と(0, H)を追加
        # 画像範囲外の線は除外
        col_b_float = sorted([0.0] + [float(x) for x in self._grid_cols if 0.0 < x < img_w] + [float(img_w)])
        row_b_float = sorted([0.0] + [float(y) for y in self._grid_rows if 0.0 < y < img_h] + [float(img_h)])

        # 座標を整数に丸め、重複を除去
        col_b_int = sorted(list(set(int(round(x)) for x in col_b_float)))
        row_b_int = sorted(list(set(int(round(y)) for y in row_b_float)))

        # 最終的な境界リストを生成するヘルパー
        def finalize_bounds(bounds_int, max_v):
            # 空リストの場合、[0, max_v] を返す
            if not bounds_int: return [0, max_v]
            # 0が含まれていなければ追加
            if bounds_int[0] != 0: bounds_int.insert(0, 0)
            # max_vが含まれていなければ追加
            if bounds_int[-1] != max_v: bounds_int.append(max_v)
            # 再度ソートして重複除去（念のため）
            return sorted(list(set(bounds_int)))

        final_cols = finalize_bounds(col_b_int, img_w)
        final_rows = finalize_bounds(row_b_int, img_h)

        # 隣接する同じ値を除去するヘルパー (例: [0, 5, 5, 10] -> [0, 5, 10])
        def remove_adjacent_duplicates(sorted_list):
            if len(sorted_list) < 2: return sorted_list
            result = [sorted_list[0]]
            for i in range(1, len(sorted_list)):
                if sorted_list[i] > result[-1]: # 直前の値より大きい場合のみ追加
                    result.append(sorted_list[i])
            return result

        # 重複を除去して返す
        return remove_adjacent_duplicates(final_cols), remove_adjacent_duplicates(final_rows)

    def _get_pixel_coords_at_img_pos(self, img_pos_f: QPointF) -> tuple | None:
        """指定された画像座標に対応する処理後画像の座標 (c, r) を返す (pixel_map_refを使用)"""
        if not self._pixel_map_ref: return None
        img_x, img_y = img_pos_f.x(), img_pos_f.y()
        # どのピクセルの矩形に含まれるか検索
        for coords, data in self._pixel_map_ref.items():
            rect = data['rect'] # (left, top, right, bottom) in image coords
            # right, bottom は含まない境界 (<) で判定
            if rect[0] <= img_x < rect[2] and rect[1] <= img_y < rect[3]:
                return coords # 処理後座標 (c, r) を返す
        return None # どのピクセルにも含まれない場合
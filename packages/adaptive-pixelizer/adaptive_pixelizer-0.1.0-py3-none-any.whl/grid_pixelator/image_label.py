# src/grid_pixelator/image_label.py
import sys
import traceback # 必要なら
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import (
    QPixmap, QImage, QPainter, QColor, QPen, QCursor, QGuiApplication,
    QWheelEvent, QMouseEvent, QKeyEvent, QUndoCommand # QUndoCommandは不要かも
)
from PyQt6.QtCore import (
    Qt, QPoint, QRectF, QPointF, QRect, pyqtSignal
)
from PIL import Image # Pillow自体は必要

# 他の自作モジュールからのインポート
from .image_utils import pillow_to_qimage
from .commands import GridChangeCommand # requestGridChangeUndoableシグナルで型ヒントなどに使うため

# --- 定数 ---
GRID_DELETE_MODIFIER = Qt.KeyboardModifier.ControlModifier
PAN_MODIFIER = Qt.KeyboardModifier.AltModifier

class InteractiveImageLabel(QLabel):
    """グリッド操作・ズーム・パン可能なカスタムラベル"""
    # シグナル定義
    scaleChanged = pyqtSignal(float)
    viewChanged = pyqtSignal(float, QPointF)
    gridChanged = pyqtSignal()
    # Undoコマンド発行要求シグナル (引数は old_cols, old_rows, new_cols, new_rows, description)
    requestGridChangeUndoable = pyqtSignal(list, list, list, list, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        # メンバー変数の初期化 (省略せず全て記述)
        self.original_pil_image = None
        self.display_pixmap = None
        self._scale_factor = 1.0
        self.min_scale = 0.05
        self.max_scale = 50.0
        self._view_center_img_pos = QPointF(0.0, 0.0)
        self.label_center = QPoint(0, 0)
        self._grid_cols = []
        self._grid_rows = []
        self.show_grid = False
        self.line_hit_tolerance = 8
        self.dragging_line_type = None
        self.dragging_line_index = -1
        self.drag_start_pos_label = None
        self.drag_start_grid_cols = []
        self.drag_start_grid_rows = []
        self.panning = False
        self.pan_start_pos_label = None
        self.pan_start_view_center = QPointF(0.0, 0.0)

        # UI設定
        self.setMinimumSize(300, 300)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("background-color: #333; border: 1px solid gray;")
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

    # --- ゲッターメソッド ---
    def getScaleFactor(self): return self._scale_factor
    def getViewCenter(self): return self._view_center_img_pos
    def getGridLines(self): return list(self._grid_cols), list(self._grid_rows)

    # --- セッター/操作メソッド ---
    def setGridLinesDirectly(self, cols, rows):
        """グリッド線を直接設定（Undo/Redo用）"""
        self._grid_cols = sorted([float(x) for x in cols])
        self._grid_rows = sorted([float(y) for y in rows])
        self.update() # 再描画

    def setPilImage(self, pil_image):
        """表示するPillow画像をセット"""
        self.original_pil_image = pil_image
        # 状態リセット
        self._grid_cols = []; self._grid_rows = []
        self.dragging_line_type = None; self.panning = False

        if self.original_pil_image:
            # Pillow画像をQImageに変換 (image_utilsの関数を使用)
            qimage = pillow_to_qimage(self.original_pil_image)
            if qimage:
                self.display_pixmap = QPixmap.fromImage(qimage)
                self.show_grid = True
                self.setStyleSheet("background-color: #333; border: 1px solid gray;")
                self.fitToWindow() # 画像セット後にフィット
            else:
                # 変換失敗
                self.display_pixmap = None; self.show_grid = False
                self.clear(); self.setText("画像表示エラー")
                self.setStyleSheet("border: 1px solid red; color: red;")
                self._scale_factor = 1.0; self._view_center_img_pos = QPointF(0.0, 0.0)
                self.scaleChanged.emit(self._scale_factor)
                self.viewChanged.emit(self._scale_factor, self._view_center_img_pos)
        else:
            # 画像がNoneの場合
            self.display_pixmap = None; self.show_grid = False
            self.clear(); self.setText("オリジナル画像")
            self.setStyleSheet("border: 1px solid gray; color: gray;")
            self._scale_factor = 1.0; self._view_center_img_pos = QPointF(0.0, 0.0)
            self.scaleChanged.emit(self._scale_factor)
            self.viewChanged.emit(self._scale_factor, self._view_center_img_pos)
        self.update() # 状態変更後に再描画

    def fitToWindow(self):
        """画像をラベル全体にフィットさせる"""
        if not self.original_pil_image or self.width() <= 0 or self.height() <= 0:
            new_scale = 1.0
            new_center = QPointF(0.0, 0.0)
            if self.original_pil_image:
                new_center = QPointF(self.original_pil_image.width / 2.0, self.original_pil_image.height / 2.0)
        else:
            img_w, img_h = self.original_pil_image.size
            label_w, label_h = self.width(), self.height()
            scale_w = label_w / img_w if img_w > 0 else 1.0
            scale_h = label_h / img_h if img_h > 0 else 1.0
            new_scale = min(scale_w, scale_h)
            new_scale = max(self.min_scale, min(new_scale, self.max_scale))
            new_center = QPointF(img_w / 2.0, img_h / 2.0)

        scale_changed = abs(new_scale - self._scale_factor) > 1e-6
        center_changed = (new_center - self._view_center_img_pos).manhattanLength() > 1e-6
        self._scale_factor = new_scale
        self._view_center_img_pos = new_center
        if scale_changed: self.scaleChanged.emit(self._scale_factor)
        if scale_changed or center_changed: self.viewChanged.emit(self._scale_factor, self._view_center_img_pos)
        self.update()

    def setScaleFactor(self, new_scale, zoom_center_label_pos=None):
        """スケールを設定し、指定位置中心にズーム"""
        if not self.original_pil_image: return
        new_scale = max(self.min_scale, min(new_scale, self.max_scale))
        if abs(new_scale - self._scale_factor) < 1e-6: return

        if zoom_center_label_pos is None:
            zoom_center_label_pos = self.label_center
        img_pos_before_zoom = self.label_to_image_coords(zoom_center_label_pos)
        self._scale_factor = new_scale
        delta_x = (zoom_center_label_pos.x() - self.label_center.x()) / self._scale_factor
        delta_y = (zoom_center_label_pos.y() - self.label_center.y()) / self._scale_factor
        # スケール変更後に正しい中心を再計算
        self._view_center_img_pos = img_pos_before_zoom - QPointF(delta_x, delta_y)

        self.scaleChanged.emit(self._scale_factor)
        self.viewChanged.emit(self._scale_factor, self._view_center_img_pos)
        self.update()

    def setViewCenter(self, new_center_img_pos):
        """ビューの中心を直接設定"""
        if not self.original_pil_image: return
        if (new_center_img_pos - self._view_center_img_pos).manhattanLength() > 1e-6:
            self._view_center_img_pos = new_center_img_pos
            self.viewChanged.emit(self._scale_factor, self._view_center_img_pos)
            self.update()

    # --- 座標変換メソッド ---
    def label_to_image_coords(self, label_pos: QPoint) -> QPointF:
        """ラベル座標 (ピクセル) を画像座標 (小数含む) に変換"""
        if not self.display_pixmap: return QPointF(0, 0)
        relative_pos = QPointF(label_pos - self.label_center)
        if abs(self._scale_factor) < 1e-9: return self._view_center_img_pos
        img_relative_x = relative_pos.x() / self._scale_factor
        img_relative_y = relative_pos.y() / self._scale_factor
        return self._view_center_img_pos + QPointF(img_relative_x, img_relative_y)

    def image_to_label_coords(self, img_pos: QPointF) -> QPoint:
        """画像座標 (小数含む) をラベル座標 (ピクセル) に変換"""
        if not self.display_pixmap: return QPoint(0, 0)
        img_relative = img_pos - self._view_center_img_pos
        relative_x = img_relative.x() * self._scale_factor
        relative_y = img_relative.y() * self._scale_factor
        label_pos_f = QPointF(self.label_center) + QPointF(relative_x, relative_y)
        return label_pos_f.toPoint()

    # --- イベントハンドラ ---
    def resizeEvent(self, event):
        """ラベルのリサイズ時に中心座標を更新"""
        super().resizeEvent(event)
        self.label_center = QPoint(self.width() // 2, self.height() // 2)
        self.update()

    def paintEvent(self, event):
        """描画イベントハンドラ"""
        super().paintEvent(event)
        painter = QPainter(self)
        if not self.display_pixmap:
            painter.setPen(QColor(150, 150, 150))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())
            painter.end()
            return

        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)

        # 画像描画 (QRect使用)
        source_rect_int = QRect(0, 0, self.display_pixmap.width(), self.display_pixmap.height())
        img_w_disp = self.display_pixmap.width() # 表示用Pixmapのサイズ
        img_h_disp = self.display_pixmap.height()
        target_w = img_w_disp * self._scale_factor
        target_h = img_h_disp * self._scale_factor
        target_x = self.label_center.x() - self._view_center_img_pos.x() * self._scale_factor
        target_y = self.label_center.y() - self._view_center_img_pos.y() * self._scale_factor
        target_rect_int = QRect(int(round(target_x)), int(round(target_y)),
                                int(round(target_w)), int(round(target_h)))
        painter.drawPixmap(target_rect_int, self.display_pixmap, source_rect_int)

        # グリッド線描画
        if self.show_grid and self.original_pil_image:
            pen = QPen(QColor(255, 0, 0, 180)); pen.setWidth(1); painter.setPen(pen)
            clip_rect = self.rect()
            img_w_orig = self.original_pil_image.width
            img_h_orig = self.original_pil_image.height
            for x_img in self._grid_cols:
                p1_label = self.image_to_label_coords(QPointF(x_img, 0))
                if clip_rect.left() <= p1_label.x() <= clip_rect.right(): # 縦線が左右に表示範囲内か
                   painter.drawLine(p1_label.x(), clip_rect.top(), p1_label.x(), clip_rect.bottom())
            for y_img in self._grid_rows:
                p1_label = self.image_to_label_coords(QPointF(0, y_img))
                if clip_rect.top() <= p1_label.y() <= clip_rect.bottom(): # 横線が上下に表示範囲内か
                   painter.drawLine(clip_rect.left(), p1_label.y(), clip_rect.right(), p1_label.y())

        # 操作ヒント描画
        if self.original_pil_image:
            modifiers = QGuiApplication.keyboardModifiers(); hint_text = ""
            current_pos = self.mapFromGlobal(QCursor.pos())
            if self.rect().contains(current_pos): # カーソルがラベル内にある場合のみ
                if modifiers & Qt.KeyboardModifier.ShiftModifier:
                    hint_text = "Shift+左クリック: 縦線追加 | Shift+右クリック: 横線追加"
                elif modifiers & GRID_DELETE_MODIFIER:
                    hint_text = "Ctrl+クリックでグリッド線削除"
                elif modifiers & PAN_MODIFIER:
                    hint_text = "Alt+ドラッグで画像移動"
                else:
                    hit_col_idx, hit_row_idx = self._find_closest_line(current_pos)
                    if hit_col_idx != -1 or hit_row_idx != -1:
                        hint_text = "線をクリックしてドラッグで移動 | Delete/Backspaceで削除"
            if hint_text:
                painter.setPen(QColor(200, 200, 0, 220)); painter.drawText(10, 20, hint_text)

        painter.end()

    def wheelEvent(self, event: QWheelEvent):
        """マウスホイールでズーム"""
        if not self.original_pil_image: return
        angle = event.angleDelta().y();
        if angle == 0: return
        zoom_factor = 1.15 if angle > 0 else 1 / 1.15
        self.setScaleFactor(self._scale_factor * zoom_factor, event.position().toPoint())
        event.accept()

    def mousePressEvent(self, event: QMouseEvent):
        """マウスクリック時のイベントハンドラ"""
        if not self.original_pil_image: return
        pos_label = event.position().toPoint(); modifiers = event.modifiers()

        # パン開始
        if event.button() == Qt.MouseButton.LeftButton and (modifiers & PAN_MODIFIER):
            self.panning = True; self.pan_start_pos_label = pos_label
            self.pan_start_view_center = self._view_center_img_pos
            self.setCursor(Qt.CursorShape.OpenHandCursor); event.accept(); return

        # グリッド線削除 (Ctrl+Click)
        if event.button() == Qt.MouseButton.LeftButton and (modifiers & GRID_DELETE_MODIFIER):
            hit_col_idx, hit_row_idx = self._find_closest_line(pos_label)
            if hit_col_idx != -1 or hit_row_idx != -1:
                old_cols, old_rows = self.getGridLines(); new_cols, new_rows = list(old_cols), list(old_rows)
                deleted = False; indices_to_delete_col = []; indices_to_delete_row = []
                if hit_col_idx != -1: indices_to_delete_col.append(hit_col_idx)
                if hit_row_idx != -1: indices_to_delete_row.append(hit_row_idx)
                for idx in sorted(indices_to_delete_col, reverse=True):
                    if idx < len(new_cols): del new_cols[idx]; deleted = True
                for idx in sorted(indices_to_delete_row, reverse=True):
                    if idx < len(new_rows): del new_rows[idx]; deleted = True
                if deleted: self.requestGridChangeUndoable.emit(old_cols, old_rows, new_cols, new_rows, "グリッド線削除")
                event.accept(); return

        # グリッド線追加 (Shift+Click)
        if modifiers & Qt.KeyboardModifier.ShiftModifier:
            img_pos = self.label_to_image_coords(pos_label); img_w, img_h = self.original_pil_image.size
            if not (0 < img_pos.x() < img_w and 0 < img_pos.y() < img_h): event.ignore(); return
            old_cols, old_rows = self.getGridLines(); new_cols, new_rows = list(old_cols), list(old_rows)
            added = False; description = ""; min_dist_threshold_label = 5

            if event.button() == Qt.MouseButton.LeftButton: # 縦線
                can_add = True
                for x in old_cols:
                    if abs(pos_label.x() - self.image_to_label_coords(QPointF(x, 0)).x()) < min_dist_threshold_label:
                        can_add = False; break
                if can_add: new_cols.append(img_pos.x()); added = True; description = "縦グリッド線追加"
            elif event.button() == Qt.MouseButton.RightButton: # 横線
                can_add = True
                for y in old_rows:
                    if abs(pos_label.y() - self.image_to_label_coords(QPointF(0, y)).y()) < min_dist_threshold_label:
                        can_add = False; break
                if can_add: new_rows.append(img_pos.y()); added = True; description = "横グリッド線追加"

            if added: self.requestGridChangeUndoable.emit(old_cols, old_rows, new_cols, new_rows, description)
            event.accept(); return

        # グリッド線ドラッグ開始
        if event.button() == Qt.MouseButton.LeftButton and not modifiers:
            hit_col_idx, hit_row_idx = self._find_closest_line(pos_label); drag_target = None; idx = -1
            if hit_col_idx != -1 and hit_row_idx != -1:
                 dist_x = abs(pos_label.x() - self.image_to_label_coords(QPointF(self._grid_cols[hit_col_idx], 0)).x())
                 dist_y = abs(pos_label.y() - self.image_to_label_coords(QPointF(0, self._grid_rows[hit_row_idx])).y())
                 if dist_x <= dist_y: drag_target = 'col'; idx = hit_col_idx
                 else: drag_target = 'row'; idx = hit_row_idx
            elif hit_col_idx != -1: drag_target = 'col'; idx = hit_col_idx
            elif hit_row_idx != -1: drag_target = 'row'; idx = hit_row_idx
            if drag_target:
                 self.dragging_line_type = drag_target; self.dragging_line_index = idx
                 self.drag_start_pos_label = pos_label; self.drag_start_grid_cols, self.drag_start_grid_rows = self.getGridLines()
                 cursor = Qt.CursorShape.SizeHorCursor if drag_target == 'col' else Qt.CursorShape.SizeVerCursor
                 self.setCursor(cursor); event.accept(); return

        event.ignore()

    def mouseMoveEvent(self, event: QMouseEvent):
        """マウス移動時のイベントハンドラ"""
        if not self.original_pil_image: return
        pos_label = event.position().toPoint(); modifiers = event.modifiers()

        # パン操作中
        if self.panning and (event.buttons() & Qt.MouseButton.LeftButton):
            if self.cursor().shape() != Qt.CursorShape.ClosedHandCursor: self.setCursor(Qt.CursorShape.ClosedHandCursor)
            delta_label = pos_label - self.pan_start_pos_label
            if abs(self._scale_factor) < 1e-9: return
            delta_img_x = delta_label.x() / self._scale_factor; delta_img_y = delta_label.y() / self._scale_factor
            new_center = self._view_center_img_pos - QPointF(delta_img_x, delta_img_y)
            self.setViewCenter(new_center); self.pan_start_pos_label = pos_label; event.accept(); return

        # グリッド線ドラッグ中
        if self.dragging_line_type and (event.buttons() & Qt.MouseButton.LeftButton) and not (modifiers & (PAN_MODIFIER | Qt.KeyboardModifier.ShiftModifier | GRID_DELETE_MODIFIER)):
            new_img_pos = self.label_to_image_coords(pos_label); img_w, img_h = self.original_pil_image.size; min_dist = 0.1
            temp_cols, temp_rows = list(self._grid_cols), list(self._grid_rows)
            moved = False
            if self.dragging_line_type == 'col' and 0 <= self.dragging_line_index < len(temp_cols):
                new_x_img = max(0, min(new_img_pos.x(), img_w))
                if self.dragging_line_index > 0: new_x_img = max(temp_cols[self.dragging_line_index-1] + min_dist, new_x_img)
                if self.dragging_line_index < len(temp_cols) - 1: new_x_img = min(temp_cols[self.dragging_line_index+1] - min_dist, new_x_img)
                if abs(temp_cols[self.dragging_line_index] - new_x_img) > 1e-6:
                    temp_cols[self.dragging_line_index] = new_x_img; moved = True
            elif self.dragging_line_type == 'row' and 0 <= self.dragging_line_index < len(temp_rows):
                new_y_img = max(0, min(new_img_pos.y(), img_h))
                if self.dragging_line_index > 0: new_y_img = max(temp_rows[self.dragging_line_index-1] + min_dist, new_y_img)
                if self.dragging_line_index < len(temp_rows) - 1: new_y_img = min(temp_rows[self.dragging_line_index+1] - min_dist, new_y_img)
                if abs(temp_rows[self.dragging_line_index] - new_y_img) > 1e-6:
                    temp_rows[self.dragging_line_index] = new_y_img; moved = True
            if moved: self.setGridLinesDirectly(temp_cols, temp_rows) # 直接更新 & 再描画
            event.accept(); return

        # カーソル形状変更
        if not self.panning and not self.dragging_line_type:
             if self.show_grid and self.original_pil_image:
                require_modifier = GRID_DELETE_MODIFIER if (modifiers & GRID_DELETE_MODIFIER) else None
                hit_col_idx, hit_row_idx = self._find_closest_line(pos_label, require_modifier=require_modifier)
                cursor_shape = Qt.CursorShape.ArrowCursor
                if modifiers & PAN_MODIFIER: cursor_shape = Qt.CursorShape.OpenHandCursor
                elif modifiers & Qt.KeyboardModifier.ShiftModifier: cursor_shape = Qt.CursorShape.CrossCursor
                elif modifiers & GRID_DELETE_MODIFIER and (hit_col_idx != -1 or hit_row_idx != -1): cursor_shape = Qt.CursorShape.PointingHandCursor
                elif not modifiers and (hit_col_idx != -1 or hit_row_idx != -1):
                     dist_x = abs(pos_label.x() - self.image_to_label_coords(QPointF(self._grid_cols[hit_col_idx], 0)).x()) if hit_col_idx != -1 else float('inf')
                     dist_y = abs(pos_label.y() - self.image_to_label_coords(QPointF(0, self._grid_rows[hit_row_idx])).y()) if hit_row_idx != -1 else float('inf')
                     if dist_x <= dist_y and hit_col_idx != -1: cursor_shape = Qt.CursorShape.SizeHorCursor
                     elif dist_y < dist_x and hit_row_idx != -1: cursor_shape = Qt.CursorShape.SizeVerCursor
                if self.cursor().shape() != cursor_shape: self.setCursor(cursor_shape)
             else: self.unsetCursor()
        event.ignore()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """マウスボタン解放時のイベントハンドラ"""
        if event.button() == Qt.MouseButton.LeftButton and self.panning:
            self.panning = False; self.unsetCursor(); event.accept(); return
        if event.button() == Qt.MouseButton.LeftButton and self.dragging_line_type:
            current_cols, current_rows = self.getGridLines()
            def are_lists_equal(list1, list2, tol=1e-6):
                 if len(list1) != len(list2): return False
                 return all(abs(a - b) < tol for a, b in zip(sorted(list1), sorted(list2))) # ソートして比較
            if not are_lists_equal(self.drag_start_grid_cols, current_cols) or \
               not are_lists_equal(self.drag_start_grid_rows, current_rows):
                 # 変更後のリストはソートしてから渡す
                 self.requestGridChangeUndoable.emit(
                     self.drag_start_grid_cols, self.drag_start_grid_rows,
                     sorted(current_cols), sorted(current_rows), # ソート済みを渡す
                     "グリッド線移動"
                 )
            self.dragging_line_type = None; self.dragging_line_index = -1
            self.drag_start_grid_cols = []; self.drag_start_grid_rows = []
            self.unsetCursor(); event.accept(); return
        event.ignore()

    def keyPressEvent(self, event: QKeyEvent):
        """キー押下時のイベントハンドラ"""
        if not self.original_pil_image: event.ignore(); return
        key = event.key()

        # グリッド線削除 (Delete/Backspace)
        if key in (Qt.Key.Key_Delete, Qt.Key.Key_Backspace):
             current_pos = self.mapFromGlobal(QCursor.pos())
             hit_col_idx, hit_row_idx = self._find_closest_line(current_pos)
             if hit_col_idx != -1 or hit_row_idx != -1:
                 old_cols, old_rows = self.getGridLines(); new_cols, new_rows = list(old_cols), list(old_rows)
                 deleted = False; indices_to_delete_col = []; indices_to_delete_row = []
                 if hit_col_idx != -1 and hit_row_idx != -1:
                     dist_x = abs(current_pos.x() - self.image_to_label_coords(QPointF(old_cols[hit_col_idx], 0)).x())
                     dist_y = abs(current_pos.y() - self.image_to_label_coords(QPointF(0, old_rows[hit_row_idx])).y())
                     if dist_x <= dist_y: indices_to_delete_col.append(hit_col_idx)
                     else: indices_to_delete_row.append(hit_row_idx)
                 elif hit_col_idx != -1: indices_to_delete_col.append(hit_col_idx)
                 elif hit_row_idx != -1: indices_to_delete_row.append(hit_row_idx)
                 for idx in sorted(indices_to_delete_col, reverse=True):
                      if idx < len(new_cols): del new_cols[idx]; deleted = True
                 for idx in sorted(indices_to_delete_row, reverse=True):
                      if idx < len(new_rows): del new_rows[idx]; deleted = True
                 if deleted: self.requestGridChangeUndoable.emit(old_cols, old_rows, new_cols, new_rows, "グリッド線削除 (キー)")
                 event.accept(); return

        # ズーム (+/-)
        elif key == Qt.Key.Key_Plus or key == Qt.Key.Key_Equal:
            self.setScaleFactor(self._scale_factor * 1.2); event.accept(); return
        elif key == Qt.Key.Key_Minus:
            self.setScaleFactor(self._scale_factor / 1.2); event.accept(); return
        # フィット (0)
        elif key == Qt.Key.Key_0:
            self.fitToWindow(); event.accept(); return

        event.ignore()

    # --- ヘルパーメソッド ---
    def _find_closest_line(self, pos_label, require_modifier=None):
        """指定されたラベル座標に最も近いグリッド線を見つける"""
        if not self.show_grid or not self.original_pil_image: return -1, -1
        if require_modifier and not (QGuiApplication.keyboardModifiers() & require_modifier): return -1, -1
        min_dist_col, hit_col_idx = float('inf'), -1; min_dist_row, hit_row_idx = float('inf'), -1
        img_w, img_h = self.original_pil_image.size

        for i, x_img in enumerate(self._grid_cols): # 垂直線
            p1 = self.image_to_label_coords(QPointF(x_img, 0))
            p2 = self.image_to_label_coords(QPointF(x_img, img_h)) # 線のY範囲を考慮
            line_rect_x = p1.x()
            line_rect_y_min = min(p1.y(), p2.y()); line_rect_y_max = max(p1.y(), p2.y())
            dist_x = abs(pos_label.x() - line_rect_x)
            if dist_x <= self.line_hit_tolerance and (line_rect_y_min - self.line_hit_tolerance <= pos_label.y() <= line_rect_y_max + self.line_hit_tolerance):
                 if dist_x < min_dist_col: min_dist_col = dist_x; hit_col_idx = i
        for i, y_img in enumerate(self._grid_rows): # 水平線
            p1 = self.image_to_label_coords(QPointF(0, y_img))
            p2 = self.image_to_label_coords(QPointF(img_w, y_img)) # 線のX範囲を考慮
            line_rect_y = p1.y()
            line_rect_x_min = min(p1.x(), p2.x()); line_rect_x_max = max(p1.x(), p2.x())
            dist_y = abs(pos_label.y() - line_rect_y)
            if dist_y <= self.line_hit_tolerance and (line_rect_x_min - self.line_hit_tolerance <= pos_label.x() <= line_rect_x_max + self.line_hit_tolerance):
                 if dist_y < min_dist_row: min_dist_row = dist_y; hit_row_idx = i
        return hit_col_idx, hit_row_idx

    # --- グリッド操作メソッド ---
    def updateGridFromSpinbox(self, cols_count, rows_count):
        """スピンボックスの値に基づいてグリッド線を均等に再配置"""
        if not self.original_pil_image: return
        old_cols, old_rows = self.getGridLines(); img_width, img_height = self.original_pil_image.size
        new_cols = [(c + 1) * img_width / cols_count for c in range(cols_count - 1)] if cols_count > 1 else []
        new_rows = [(r + 1) * img_height / rows_count for r in range(rows_count - 1)] if rows_count > 1 else []
        def is_close(list1, list2, tol=1e-6): # floatリスト比較
            if len(list1) != len(list2): return False
            return all(abs(a - b) < tol for a, b in zip(sorted(list1), sorted(list2)))
        if not is_close(old_cols, new_cols) or not is_close(old_rows, new_rows):
             self.requestGridChangeUndoable.emit(old_cols, old_rows, new_cols, new_rows, "グリッド数変更")

    def getGridPositions(self):
        """処理のためにグリッド境界のピクセル座標リストを取得"""
        if not self.original_pil_image: return [], []
        img_width, img_height = self.original_pil_image.size
        col_bounds = sorted([0.0] + [float(x) for x in self._grid_cols] + [float(img_width)])
        row_bounds = sorted([0.0] + [float(y) for y in self._grid_rows] + [float(img_height)])
        col_bounds_int = sorted(list(set(int(round(x)) for x in col_bounds)))
        row_bounds_int = sorted(list(set(int(round(y)) for y in row_bounds)))

        # 幅/高さ0のセルを防ぐための調整
        final_cols = []; final_rows = []
        if col_bounds_int:
            final_cols.append(col_bounds_int[0])
            for i in range(1, len(col_bounds_int)):
                current_val = max(col_bounds_int[i], final_cols[-1] + 1)
                final_cols.append(min(current_val, img_width)) # 幅を超えない
        if final_cols and len(final_cols) > 1 and final_cols[-1] <= final_cols[-2]: # 最後の調整
             final_cols.pop() # 無効な最後の境界を削除

        if row_bounds_int:
            final_rows.append(row_bounds_int[0])
            for i in range(1, len(row_bounds_int)):
                current_val = max(row_bounds_int[i], final_rows[-1] + 1)
                final_rows.append(min(current_val, img_height)) # 高さを超えない
        if final_rows and len(final_rows) > 1 and final_rows[-1] <= final_rows[-2]: # 最後の調整
             final_rows.pop()

        return final_cols, final_rows
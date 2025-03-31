# src/adaptive_pixelizer/commands.py
from PyQt6.QtGui import QUndoCommand, QColor

class GridChangeCommand(QUndoCommand):
    """グリッド線の変更（追加、削除、移動）を記録するコマンド"""
    def __init__(self, label, old_cols, old_rows, new_cols, new_rows, description, parent=None):
        super().__init__(description, parent)
        self.label = label # InteractiveImageLabel への参照
        # 変更前後のグリッド線リストをコピーして保持
        self.old_cols = list(old_cols); self.old_rows = list(old_rows)
        self.new_cols = list(new_cols); self.new_rows = list(new_rows)

    def undo(self):
        """アンドゥ操作: グリッド線を変更前の状態に戻す"""
        self.label.setGridLinesDirectly(self.old_cols, self.old_rows)
        # グリッド変更シグナルを発行してプレビューなどを更新させる
        self.label.gridChanged.emit()

    def redo(self):
        """リドゥ操作: グリッド線を変更後の状態に適用する"""
        self.label.setGridLinesDirectly(self.new_cols, self.new_rows)
        # グリッド変更シグナルを発行
        self.label.gridChanged.emit()

class ColorChangeCommand(QUndoCommand):
    """処理結果画像のピクセル色変更を記録するコマンド (複数ピクセル、複数元色、選択状態復元対応)"""
    def __init__(self, window, pixel_coords_list, old_colors_list, new_color, old_selection_set, description, parent=None):
        super().__init__(description, parent)
        self.window = window
        self.pixel_coords_list = list(pixel_coords_list)
        self.old_colors_list = list(old_colors_list)
        self.new_color = new_color
        # 変更前の選択状態をコピーして保持
        self.old_selection_set = old_selection_set.copy() # ここはコピーでOK
        if len(self.pixel_coords_list) != len(self.old_colors_list):
            raise ValueError("Coordinate list and old color list must have the same length.")

    def undo(self):
        """アンドゥ操作: ピクセル色を元に戻し、色変更前の選択状態(Sn)も復元する"""
        # 処理対象の画像が存在し、かつ色編集フェーズであるか確認
        if self.window.processed_image and self.window.current_phase == self.window.PHASE_EDIT_COLOR:
            img_w = self.window.processed_image.width
            img_h = self.window.processed_image.height
            changed = False
            try:
                # --- ループで各ピクセルを対応する元の色に戻す ---
                for i, coords in enumerate(self.pixel_coords_list):
                    c, r = coords
                    old_color = self.old_colors_list[i] # 対応する元の色を取得
                    # 座標が画像の範囲内か確認
                    if 0 <= c < img_w and 0 <= r < img_h:
                        # processed_image (Pillow Image) のピクセルを更新
                        self.window.processed_image.putpixel(coords, old_color)
                        # pixel_map (表示とインタラクション用データ) も更新
                        if coords in self.window.pixel_map:
                            self.window.pixel_map[coords]['color'] = old_color
                        changed = True

                if changed:
                    # --- 選択状態を色変更前の状態(Sn)に復元 ---
                    self.window.selected_coords_set.clear()
                    self.window.selected_coords_set.update(self.old_selection_set)

                    # --- UI更新 ---
                    self.window.display_processed_image() # 右側プレビュー更新、これがUI全体更新もトリガー
                    self.window.setStatusMessage("色変更を元に戻しました", 1500)

            except Exception as e:
                print(f"Error undoing color change: {e}")
                # エラーが発生してもUIは更新しておく
                self.window.update_ui_for_phase() # UI全体の整合性を取る

    def redo(self):
        """リドゥ操作: ピクセル色を新しい色(Cn)に変更し、次のコマンドの選択状態(Sn+1)を復元する"""
        # 処理対象の画像が存在し、かつ色編集フェーズであるか確認
        if self.window.processed_image and self.window.current_phase == self.window.PHASE_EDIT_COLOR:
            img_w = self.window.processed_image.width
            img_h = self.window.processed_image.height
            changed = False
            try:
                # --- ループで各ピクセルを新しい色(Cn)にする ---
                for coords in self.pixel_coords_list:
                    c, r = coords
                    # 座標が画像の範囲内か確認
                    if 0 <= c < img_w and 0 <= r < img_h:
                       # processed_image のピクセルを更新
                       self.window.processed_image.putpixel(coords, self.new_color)
                       # pixel_map も更新
                       if coords in self.window.pixel_map:
                           self.window.pixel_map[coords]['color'] = self.new_color
                       changed = True

                if changed:
                    # --- 次のコマンド(n+1)の選択状態(Sn+1)を取得 ---
                    stack = self.window.undo_stack
                    # redo実行前のindexは現在のコマンド(n)を指すため、次のコマンド(n+1)のindexは +1 する
                    next_command_index = stack.index() + 1
                    next_selection_set = None

                    # 次のコマンドが存在するかチェック (インデックスは stack.count() 未満)
                    if next_command_index < stack.count():
                        next_command = stack.command(next_command_index)
                        # 次のコマンドが期待する型と属性を持っているか確認
                        if isinstance(next_command, ColorChangeCommand) and hasattr(next_command, 'old_selection_set'):
                            next_selection_set = next_command.old_selection_set # Sn+1 を取得

                    # --- 選択状態を適用 ---
                    self.window.selected_coords_set.clear() # 現在の選択をクリア
                    if next_selection_set is not None:
                        # Sn+1 が取得できたら適用
                        self.window.selected_coords_set.update(next_selection_set)
                    # else: Sn+1 がない (履歴の最後) 場合はクリアされたまま

                    # --- UI更新 ---
                    # display_processed_image -> update_ui_for_phase -> update_color_selection_ui -> original_image_label.update()
                    self.window.display_processed_image()
                    self.window.setStatusMessage("色変更をやり直しました", 1500)

            except Exception as e:
                print(f"Error redoing color change: {e}")
                # エラーが発生してもUIは更新しておく
                self.window.update_ui_for_phase() # UI全体の整合性を取る
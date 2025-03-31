# src/grid_pixelator/commands.py
from PyQt6.QtGui import QUndoCommand

class GridChangeCommand(QUndoCommand):
    """グリッド線の変更（追加、削除、移動）を記録するコマンド"""
    def __init__(self, label, old_cols, old_rows, new_cols, new_rows, description, parent=None):
        super().__init__(description, parent)
        self.label = label # InteractiveImageLabel のインスタンス
        self.old_cols = list(old_cols)
        self.old_rows = list(old_rows)
        self.new_cols = list(new_cols)
        self.new_rows = list(new_rows)

    def undo(self):
        """アンドゥ操作"""
        self.label.setGridLinesDirectly(self.old_cols, self.old_rows)
        self.label.gridChanged.emit() # グリッド変更を通知 (プレビュー更新のため)

    def redo(self):
        """リドゥ操作"""
        self.label.setGridLinesDirectly(self.new_cols, self.new_rows)
        self.label.gridChanged.emit() # グリッド変更を通知 (プレビュー更新のため)
# src/adaptive_pixelizer/main_window.py
import sys
import os
import traceback
from PIL import Image, ImageColor

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFileDialog, QSpinBox, QMessageBox, QSizePolicy, QSlider, QComboBox,
    QCheckBox, QMainWindow, QMenuBar, QStatusBar, QToolBar, QStyle,
    QColorDialog, QGroupBox
)
from PyQt6.QtGui import (
    QPixmap, QImage, QAction, QIcon, QKeySequence, QUndoStack, QPainter, QColor,
    QMouseEvent
)
# Qt.KeyboardModifier と QPointF をインポート
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint, QRectF, QPointF

# InteractiveImageLabel は大幅に変更される前提
from .image_label import InteractiveImageLabel
from .commands import GridChangeCommand, ColorChangeCommand
from .image_utils import (
    calculate_average_color, calculate_median_color, calculate_mode_color,
    pillow_to_qimage_for_display, NEAREST_NEIGHBOR, NUMPY_AVAILABLE, IMAGEQT_AVAILABLE
)
# --- 修正ここまで ---

# --- 処理結果表示用ラベル (プレビュー専用に) ---
class InteractiveProcessedImageLabel(QLabel):
    """処理結果画像のプレビューを表示するラベル (操作不可)"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(200, 200)
        self.setStyleSheet("border: 1px solid gray; color: gray; background-color: #333;")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # クリックイベントを受け付けないようにする
        self.setEnabled(False) # 見た目は変わるがクリックは無効になる

    # mousePressEvent をオーバーライドして何もしないようにする
    def mousePressEvent(self, event: QMouseEvent):
        event.ignore() # イベントを無視

    def setPixmap(self, pixmap):
        # 有効状態を一時的に True にして Pixmap を設定し、再度 False に戻す
        # (QLabelが無効状態だとPixmapが更新されないことがあるため)
        was_enabled = self.isEnabled()
        self.setEnabled(True)
        super().setPixmap(pixmap)
        self.setEnabled(was_enabled)

    def clear(self):
        was_enabled = self.isEnabled()
        self.setEnabled(True)
        super().clear()
        self.setEnabled(was_enabled)

    def setText(self, text):
        was_enabled = self.isEnabled()
        self.setEnabled(True)
        super().setText(text)
        self.setEnabled(was_enabled)

# --- メインウィンドウクラス ---
class PixelatorWindow(QMainWindow):
    """メインウィンドウクラス"""
    # フェーズ定数
    PHASE_INITIAL_GRID = 1
    PHASE_EDIT_GRID = 2
    PHASE_EDIT_COLOR = 3

    def __init__(self):
        super().__init__()
        self.original_image = None
        self.processed_image = None
        self._is_slider_adjusting = False
        self.undo_stack = QUndoStack(self)
        self.last_processed_config = {}
        self.pixel_map = {} # Map processed (c, r) to {'rect': original_rect_tuple, 'color': rgba_tuple}
        self.selected_coords_set = set() # 選択中の処理後ピクセル座標 (c, r) のセット
        self.preview_update_timer = QTimer(self)
        self.preview_update_timer.setSingleShot(True)
        self.preview_update_timer.setInterval(300)
        self.current_phase = self.PHASE_INITIAL_GRID
        self.grid_state_before_color_edit = None
        self._last_interacted_coords = set() # handle_pixel_interaction用
        self._drag_selection_mode = None     # handle_pixel_interaction用

        if not NUMPY_AVAILABLE: print("Warning: NumPy not found. Median calculation will be slower.")
        if not IMAGEQT_AVAILABLE: print("Warning: Pillow-PIL (ImageQt) not found. Pillow to QImage conversion might be less efficient.")

        self.initUI()
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.connectSignals()
        self.set_phase(self.PHASE_INITIAL_GRID) # 初期UI状態設定

    def initUI(self):
        """UI要素の初期化と配置"""
        self.setWindowTitle('adaptive-pixelizer')
        self.setGeometry(100, 100, 1200, 900)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # --- ファイル選択エリア ---
        file_layout = QHBoxLayout()
        open_icon = QIcon.fromTheme("document-open", self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon))
        self.load_button_widget = QPushButton(open_icon, " 画像ファイルを開く")
        self.load_button_widget.setToolTip("画像ファイルを選択します (Ctrl+O)")
        self.file_label = QLabel('画像が選択されていません')
        self.file_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        file_layout.addWidget(self.load_button_widget)
        file_layout.addWidget(self.file_label)
        main_layout.addLayout(file_layout)

        # --- 画像表示エリア ---
        image_layout = QHBoxLayout()
        # --- InteractiveImageLabel: 編集用 ---
        self.original_image_label = InteractiveImageLabel()
        # MainWindowの管理するデータへの参照を渡す
        self.original_image_label.set_pixel_map_ref(self.pixel_map)
        self.original_image_label.set_selected_coords_ref(self.selected_coords_set)
        self.original_image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        image_layout.addWidget(self.original_image_label, 3)
        # --- InteractiveProcessedImageLabel: プレビュー用 ---
        self.processed_image_label = InteractiveProcessedImageLabel() # 修正後のプレビュー専用ラベル
        image_layout.addWidget(self.processed_image_label, 2)
        main_layout.addLayout(image_layout)

        # --- コントロールパネル コンテナ ---
        control_panel_container = QWidget()
        control_panel_main_layout = QVBoxLayout(control_panel_container)
        control_panel_main_layout.setContentsMargins(0,0,0,0)

        # --- ズームコントロール (常に表示) ---
        zoom_group_box = QGroupBox("表示操作")
        zoom_layout = QHBoxLayout(zoom_group_box); zoom_layout.setContentsMargins(5, 5, 5, 5)
        zoom_layout.addWidget(QLabel("ズーム:"))
        self.zoom_out_button = QPushButton("-"); self.zoom_out_button.setFixedWidth(30); self.zoom_out_button.setToolTip("ズームアウト (-)")
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setRange(int(self.original_image_label.min_scale * 100), int(self.original_image_label.max_scale * 100))
        self.zoom_slider.setValue(100); self.zoom_slider.setTickInterval(100); self.zoom_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.zoom_slider.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.zoom_in_button = QPushButton("+"); self.zoom_in_button.setFixedWidth(30); self.zoom_in_button.setToolTip("ズームイン (+)")
        self.zoom_percent_label = QLabel("100%"); self.zoom_percent_label.setFixedWidth(50)
        self.fit_button = QPushButton("全体表示"); self.fit_button.setToolTip("全体表示 (0)")
        zoom_layout.addWidget(self.zoom_out_button); zoom_layout.addWidget(self.zoom_slider); zoom_layout.addWidget(self.zoom_in_button)
        zoom_layout.addWidget(self.zoom_percent_label); zoom_layout.addWidget(self.fit_button); zoom_layout.addStretch(1)
        control_panel_main_layout.addWidget(zoom_group_box)

        # --- フェーズ1: 初期グリッド設定 ---
        self.phase1_group_box = QGroupBox("ステップ1: 初期グリッド設定")
        phase1_layout = QHBoxLayout(self.phase1_group_box)
        phase1_layout.addWidget(QLabel('初期グリッド数:'))
        self.cols_spinbox = QSpinBox(); self.cols_spinbox.setRange(1, 256); self.cols_spinbox.setValue(8); self.cols_spinbox.setPrefix("横 ")
        self.rows_spinbox = QSpinBox(); self.rows_spinbox.setRange(1, 256); self.rows_spinbox.setValue(8); self.rows_spinbox.setPrefix("縦 ")
        phase1_layout.addWidget(self.cols_spinbox); phase1_layout.addWidget(self.rows_spinbox)
        phase1_layout.addWidget(QLabel(" | 計算方法:"))
        self.color_mode_combo = QComboBox(); self.color_mode_combo.addItems(["平均 (Average)", "中央値 (Median)", "最頻色 (Mode)"])
        phase1_layout.addWidget(self.color_mode_combo)
        self.auto_preview_checkbox = QCheckBox("プレビュー自動更新"); self.auto_preview_checkbox.setChecked(True)
        self.auto_preview_checkbox.setToolTip("設定変更時にプレビューを自動で更新します")
        phase1_layout.addWidget(self.auto_preview_checkbox)
        self.process_button = QPushButton('プレビュー更新'); self.process_button.setToolTip("現在の設定でプレビューを更新 (Enter)")
        phase1_layout.addWidget(self.process_button)
        phase1_layout.addStretch(1)
        self.go_to_phase2_button = QPushButton("グリッド編集へ進む →")
        phase1_layout.addWidget(self.go_to_phase2_button)
        control_panel_main_layout.addWidget(self.phase1_group_box)

        # --- フェーズ2: グリッド編集 ---
        self.phase2_group_box = QGroupBox("ステップ2: グリッド線 編集")
        phase2_layout = QHBoxLayout(self.phase2_group_box)
        self.back_to_phase1_button = QPushButton("← 初期グリッドに戻る")
        self.back_to_phase1_button.setToolTip("グリッド編集を破棄してステップ1に戻ります")
        phase2_layout.addWidget(self.back_to_phase1_button)
        phase2_layout.addWidget(QLabel("編集: Shift+Click:追加, Ctrl+Click/Del:削除, Drag:移動"))
        phase2_layout.addWidget(QLabel(" | 計算方法:"))
        self.color_mode_combo_phase2 = QComboBox(); self.color_mode_combo_phase2.addItems(["平均 (Average)", "中央値 (Median)", "最頻色 (Mode)"])
        phase2_layout.addWidget(self.color_mode_combo_phase2)
        self.auto_preview_checkbox_phase2 = QCheckBox("プレビュー自動更新"); self.auto_preview_checkbox_phase2.setChecked(True)
        phase2_layout.addWidget(self.auto_preview_checkbox_phase2)
        self.process_button_phase2 = QPushButton('プレビュー更新'); self.process_button_phase2.setToolTip("現在のグリッドでプレビューを更新 (Enter)")
        phase2_layout.addWidget(self.process_button_phase2)
        phase2_layout.addStretch(1)
        self.go_to_phase3_button = QPushButton("色編集へ進む →")
        phase2_layout.addWidget(self.go_to_phase3_button)
        control_panel_main_layout.addWidget(self.phase2_group_box)

        # --- フェーズ3: 色編集 (ラベル、ツールチップ更新) ---
        self.phase3_group_box = QGroupBox("ステップ3: 色 編集 (左画像上で操作: クリック:個別選択/解除, Shift+クリック:同色選択/解除, ドラッグ:範囲選択, 範囲外クリック:全解除)") # ツールチップ更新
        phase3_layout = QVBoxLayout(self.phase3_group_box)
        phase3_top_layout = QHBoxLayout()
        self.back_to_phase2_button = QPushButton("← グリッド編集に戻る")
        self.back_to_phase2_button.setToolTip("色編集を破棄してステップ2に戻ります")
        phase3_top_layout.addWidget(self.back_to_phase2_button)
        self.color_info_label = QLabel("左の画像上でピクセルを選択してください") # 初期メッセージ更新
        self.color_info_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        phase3_top_layout.addWidget(self.color_info_label)
        phase3_top_layout.addStretch(1)
        phase3_layout.addLayout(phase3_top_layout)
        phase3_bottom_layout = QHBoxLayout()
        self.edit_color_button = QPushButton("選択ピクセルを編集...") # ボタンテキスト変更
        self.edit_color_button.setToolTip("選択中のピクセルの色を一括編集します (複数色可)") # ツールチップ更新
        self.edit_color_button.setEnabled(False) # 初期状態は無効
        phase3_bottom_layout.addWidget(self.edit_color_button)
        phase3_bottom_layout.addStretch(1)
        phase3_layout.addLayout(phase3_bottom_layout)
        control_panel_main_layout.addWidget(self.phase3_group_box)

        main_layout.addWidget(control_panel_container)

        # 初期状態ではフェーズ2, 3を隠す
        self.phase2_group_box.setVisible(False)
        self.phase3_group_box.setVisible(False)

    def createActions(self):
        """メニューバーやツールバーのアクションを作成"""
        def get_icon(theme_name, fallback_sp):
            icon = QIcon.fromTheme(theme_name)
            if not icon.isNull(): return icon
            std_icon = self.style().standardIcon(fallback_sp)
            if not std_icon.isNull(): return std_icon
            return QIcon() # Empty icon

        # ファイル・ズーム・プロセスアクション
        self.open_action = QAction(get_icon("document-open", QStyle.StandardPixmap.SP_DirOpenIcon), "開く...", self)
        self.open_action.setShortcut(QKeySequence.StandardKey.Open); self.open_action.setStatusTip("画像ファイルを開きます")
        self.save_action = QAction(get_icon("document-save-as", QStyle.StandardPixmap.SP_DialogSaveButton), "名前を付けて保存...", self)
        self.save_action.setShortcut(QKeySequence.StandardKey.SaveAs); self.save_action.setStatusTip("処理結果の画像を保存します"); self.save_action.setEnabled(False)
        self.exit_action = QAction("終了", self); self.exit_action.setShortcut(QKeySequence.StandardKey.Quit); self.exit_action.setStatusTip("アプリケーションを終了します")
        self.zoom_in_action = QAction(get_icon("zoom-in", QStyle.StandardPixmap.SP_ArrowUp), "ズームイン", self)
        self.zoom_in_action.setShortcut(QKeySequence.StandardKey.ZoomIn); self.zoom_in_action.setEnabled(False)
        self.zoom_out_action = QAction(get_icon("zoom-out", QStyle.StandardPixmap.SP_ArrowDown), "ズームアウト", self)
        self.zoom_out_action.setShortcut(QKeySequence.StandardKey.ZoomOut); self.zoom_out_action.setEnabled(False)
        self.fit_action = QAction(get_icon("zoom-fit-best", QStyle.StandardPixmap.SP_FileDialogListView), "全体表示", self)
        self.fit_action.setShortcut(QKeySequence("Ctrl+0")); self.fit_action.setEnabled(False)
        self.process_action = QAction(get_icon("media-playback-start", QStyle.StandardPixmap.SP_MediaPlay), "プレビュー更新", self)
        self.process_action.setShortcut(QKeySequence(Qt.Key.Key_Return)); self.process_action.setEnabled(False)

        # Undo/Redo
        self.undo_action = self.undo_stack.createUndoAction(self, "元に戻す")
        self.undo_action.setIcon(get_icon("edit-undo", QStyle.StandardPixmap.SP_ArrowBack)); self.undo_action.setShortcut(QKeySequence.StandardKey.Undo); self.undo_action.setEnabled(False)
        self.redo_action = self.undo_stack.createRedoAction(self, "やり直し")
        self.redo_action.setIcon(get_icon("edit-redo", QStyle.StandardPixmap.SP_ArrowForward)); self.redo_action.setShortcut(QKeySequence.StandardKey.Redo); self.redo_action.setEnabled(False)

        # 色編集アクション (ツールチップ更新)
        self.edit_color_action = QAction(get_icon("color-picker", QStyle.StandardPixmap.SP_CustomBase), "選択ピクセルを一括編集...", self)
        self.edit_color_action.setStatusTip("選択中のピクセルの色をまとめて編集します (複数色可)")
        self.edit_color_action.setEnabled(False)

        # フェーズ遷移アクション
        self.go_phase1_action = QAction("ステップ1: 初期グリッド設定に戻る", self); self.go_phase1_action.setStatusTip("変更を破棄してステップ1に戻ります")
        self.go_phase2_action = QAction("ステップ2: グリッド編集に進む", self); self.go_phase2_action.setStatusTip("ステップ2に進んでグリッド線を編集します")
        self.go_phase3_action = QAction("ステップ3: 色編集に進む", self); self.go_phase3_action.setStatusTip("現在のグリッドを確定してステップ3に進みます")

    def createMenus(self):
        """メニューバーを作成"""
        menu_bar = self.menuBar()
        # ファイルメニュー
        file_menu = menu_bar.addMenu("ファイル")
        file_menu.addAction(self.open_action); file_menu.addAction(self.save_action)
        file_menu.addSeparator(); file_menu.addAction(self.exit_action)
        # 編集メニュー
        edit_menu = menu_bar.addMenu("編集")
        edit_menu.addAction(self.undo_action); edit_menu.addAction(self.redo_action)
        edit_menu.addSeparator(); edit_menu.addAction(self.edit_color_action)
        # 表示メニュー
        view_menu = menu_bar.addMenu("表示")
        view_menu.addAction(self.zoom_in_action); view_menu.addAction(self.zoom_out_action)
        view_menu.addAction(self.fit_action); view_menu.addSeparator()
        # 処理メニュー
        process_menu = menu_bar.addMenu("処理")
        process_menu.addAction(self.process_action)
        # ステップメニュー
        phase_menu = menu_bar.addMenu("ステップ")
        phase_menu.addAction(self.go_phase1_action)
        phase_menu.addAction(self.go_phase2_action)
        phase_menu.addAction(self.go_phase3_action)

    def createToolBars(self):
        """ツールバーを作成"""
        toolbar = QToolBar("メインツールバー"); self.addToolBar(toolbar)
        toolbar.addAction(self.open_action); toolbar.addAction(self.save_action); toolbar.addSeparator()
        toolbar.addAction(self.undo_action); toolbar.addAction(self.redo_action); toolbar.addSeparator()
        toolbar.addAction(self.edit_color_action); toolbar.addSeparator()
        toolbar.addAction(self.zoom_out_action); toolbar.addAction(self.zoom_in_action); toolbar.addAction(self.fit_action); toolbar.addSeparator()
        toolbar.addAction(self.process_action)

    def createStatusBar(self):
        """ステータスバーを作成"""
        self.status_label = QLabel("準備完了")
        self.phase_label = QLabel(f"ステップ: {self.current_phase}")
        self.statusBar().addWidget(self.status_label, 1)
        self.statusBar().addPermanentWidget(self.phase_label)

    def connectSignals(self):
        """シグナルとスロットを接続"""
        # ファイル
        self.load_button_widget.clicked.connect(self.load_image)
        self.open_action.triggered.connect(self.load_image)
        self.save_action.triggered.connect(self.save_image)
        self.exit_action.triggered.connect(self.close)

        # オリジナル画像ラベル (左側: 編集用)
        self.original_image_label.scaleChanged.connect(self.update_zoom_controls_from_label)
        self.original_image_label.viewChanged.connect(self.handle_view_change)
        # グリッド編集関連
        self.original_image_label.gridChanged.connect(self.schedule_preview_update)
        self.original_image_label.requestGridChangeUndoable.connect(self.add_grid_change_command)
        # --- ピクセル選択インタラクションのシグナルを接続 ---
        self.original_image_label.pixelInteraction.connect(self.handle_pixel_interaction)
        # --- 領域外クリックのシグナルを接続 ---
        self.original_image_label.clickedOutsidePixels.connect(self.clear_color_selection_if_phase3)

        # 処理結果画像ラベル (右側: プレビュー用) - シグナル接続は不要

        # ズーム
        self.zoom_out_button.clicked.connect(self.zoom_out); self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_slider.valueChanged.connect(self.zoom_slider_changed)
        self.zoom_slider.sliderPressed.connect(lambda: setattr(self, '_is_slider_adjusting', True))
        self.zoom_slider.sliderReleased.connect(lambda: setattr(self, '_is_slider_adjusting', False))
        self.fit_button.clicked.connect(self.fit_image_to_window)
        self.zoom_in_action.triggered.connect(self.zoom_in); self.zoom_out_action.triggered.connect(self.zoom_out); self.fit_action.triggered.connect(self.fit_image_to_window)

        # フェーズ1 コントロール
        self.cols_spinbox.valueChanged.connect(self.update_grid_from_spinbox)
        self.rows_spinbox.valueChanged.connect(self.update_grid_from_spinbox)
        self.color_mode_combo.currentIndexChanged.connect(self.sync_and_preview)
        self.auto_preview_checkbox.toggled.connect(self.toggle_auto_preview)
        self.process_button.clicked.connect(self.trigger_process_image_preview)
        self.go_to_phase2_button.clicked.connect(self.confirm_and_go_to_phase2)

        # フェーズ2 コントロール
        self.back_to_phase1_button.clicked.connect(self.confirm_and_go_to_phase1)
        self.color_mode_combo_phase2.currentIndexChanged.connect(self.sync_and_preview)
        self.auto_preview_checkbox_phase2.toggled.connect(self.toggle_auto_preview)
        self.process_button_phase2.clicked.connect(self.trigger_process_image_preview)
        self.go_to_phase3_button.clicked.connect(self.confirm_and_go_to_phase3)

        # フェーズ3 コントロール
        self.back_to_phase2_button.clicked.connect(self.confirm_and_go_to_phase2_from_3)
        self.edit_color_button.clicked.connect(self.edit_selected_color_group) # 複数色編集に対応
        self.edit_color_action.triggered.connect(self.edit_selected_color_group) # 複数色編集に対応

        # 共通処理アクション
        self.process_action.triggered.connect(self.trigger_process_image_preview)

        # タイマー
        self.preview_update_timer.timeout.connect(self.trigger_process_image_preview)

        # Undo/Redo
        self.undo_stack.canUndoChanged.connect(self.undo_action.setEnabled)
        self.undo_stack.canRedoChanged.connect(self.redo_action.setEnabled)
        self.undo_stack.cleanChanged.connect(self.updateWindowTitle)

        # フェーズ遷移アクション (メニュー)
        self.go_phase1_action.triggered.connect(self.confirm_and_go_to_phase1)
        self.go_phase2_action.triggered.connect(self.confirm_and_go_to_phase2)
        self.go_phase3_action.triggered.connect(self.confirm_and_go_to_phase3)

    def set_phase(self, new_phase):
        """指定されたフェーズにUI状態を設定"""
        old_phase = self.current_phase
        self.current_phase = new_phase
        print(f"Setting phase to: {self.current_phase}")
        self.phase_label.setText(f"ステップ: {self.current_phase}")

        # フェーズが変わるときは色選択を解除
        if old_phase != new_phase and old_phase == self.PHASE_EDIT_COLOR:
            self.clear_color_selection() # UI更新を含む

        # --- 左側ラベルの編集モードを制御 ---
        self.original_image_label.setGridEditingEnabled(new_phase == self.PHASE_EDIT_GRID)
        self.original_image_label.setPixelSelectionEnabled(new_phase == self.PHASE_EDIT_COLOR)

        self.update_ui_for_phase() # ボタン等の有効/無効を更新
        self.updateWindowTitle()

    def update_ui_for_phase(self):
        """現在のフェーズに基づいてUI要素の有効/無効/表示状態を更新"""
        has_image = self.original_image is not None
        has_processed = self.processed_image is not None
        has_selection = bool(self.selected_coords_set) and has_processed

        # グループボックスの表示制御
        self.phase1_group_box.setVisible(self.current_phase == self.PHASE_INITIAL_GRID and has_image)
        self.phase2_group_box.setVisible(self.current_phase == self.PHASE_EDIT_GRID and has_image)
        self.phase3_group_box.setVisible(self.current_phase == self.PHASE_EDIT_COLOR and has_image)

        # 各ウィジェット/アクションの有効無効
        # 画像依存
        self.save_action.setEnabled(has_processed)
        self.zoom_in_action.setEnabled(has_image); self.zoom_out_action.setEnabled(has_image); self.fit_action.setEnabled(has_image)
        self.zoom_in_button.setEnabled(has_image); self.zoom_out_button.setEnabled(has_image); self.zoom_slider.setEnabled(has_image); self.fit_button.setEnabled(has_image)
        # プレビューラベルは処理結果があれば有効
        self.processed_image_label.setEnabled(has_processed)

        # フェーズ1 コントロール
        is_phase1 = self.current_phase == self.PHASE_INITIAL_GRID and has_image
        self.cols_spinbox.setEnabled(is_phase1); self.rows_spinbox.setEnabled(is_phase1); self.color_mode_combo.setEnabled(is_phase1)
        self.auto_preview_checkbox.setEnabled(is_phase1); self.process_button.setEnabled(is_phase1); self.go_to_phase2_button.setEnabled(is_phase1)
        self.go_phase2_action.setEnabled(is_phase1)

        # フェーズ2 コントロール
        is_phase2 = self.current_phase == self.PHASE_EDIT_GRID and has_image
        self.back_to_phase1_button.setEnabled(is_phase2); self.color_mode_combo_phase2.setEnabled(is_phase2)
        self.auto_preview_checkbox_phase2.setEnabled(is_phase2); self.process_button_phase2.setEnabled(is_phase2)
        self.go_to_phase3_button.setEnabled(is_phase2); self.go_phase3_action.setEnabled(is_phase2)
        # グリッド編集有効化は set_phase で行う

        # フェーズ3 コントロール
        is_phase3 = self.current_phase == self.PHASE_EDIT_COLOR and has_image
        self.back_to_phase2_button.setEnabled(is_phase3)
        # 色編集ボタンは選択があれば常に有効
        can_edit_color = is_phase3 and has_selection
        self.edit_color_button.setEnabled(can_edit_color)
        self.edit_color_action.setEnabled(can_edit_color)
        self.go_phase1_action.setEnabled(is_phase2 or is_phase3) # ステップ1に戻る
        # self.go_phase2_action.setEnabled(False) # フェーズ3からは直接2へは行けない - これは誤り、戻るボタンがある
        self.go_phase2_action.setEnabled(is_phase3 and self.grid_state_before_color_edit is not None) # 戻れるのはフェーズ3からのみ
        self.go_phase3_action.setEnabled(False) # フェーズ3にいるので無効
        # ピクセル選択有効化は set_phase で行う

        # 共通アクション
        self.process_action.setEnabled((is_phase1 or is_phase2)) # プレビュー更新はフェーズ1, 2のみ

        # 計算方法/自動更新の有効化 (フェーズ1, 2 のみ)
        self.auto_preview_checkbox.setEnabled(is_phase1 or is_phase2)
        self.auto_preview_checkbox_phase2.setEnabled(is_phase1 or is_phase2)
        self.color_mode_combo.setEnabled(is_phase1)
        self.color_mode_combo_phase2.setEnabled(is_phase2)
        self.process_button.setEnabled(is_phase1)
        self.process_button_phase2.setEnabled(is_phase2)

        # --- 色選択状態に応じてラベル更新 ---
        # この関数が直接呼ばれるのではなく、選択状態が変わる可能性のある場所
        # (clear_color_selection, handle_pixel_interaction, ColorChangeCommandのundo/redo)
        # から update_color_selection_ui が呼ばれることを確認
        self.update_color_selection_ui()

    def updateWindowTitle(self):
        """ウィンドウタイトルに変更状態(*)とフェーズを表示"""
        title = f"adaptive-pixelizer [ステップ{self.current_phase}]"
        if self.original_image:
            title += f" - {os.path.basename(self.file_label.text())}"
        if not self.undo_stack.isClean():
            title += " *"
        self.setWindowTitle(title)

    def statusBar(self) -> QStatusBar:
        return super().statusBar()

    def setStatusMessage(self, message, timeout=0):
        """ステータスバーのメッセージを更新"""
        # timeout引数は現在使っていないが、将来のために残す
        self.status_label.setText(message)

    # --- フェーズ遷移メソッド ---
    def confirm_and_go_to_phase1(self):
        """フェーズ1への遷移を確認し実行"""
        confirm_needed = False; message = ""
        # フェーズ2または3にいて、かつ変更がある場合
        if (self.current_phase == self.PHASE_EDIT_GRID or self.current_phase == self.PHASE_EDIT_COLOR) and not self.undo_stack.isClean():
            confirm_needed = True
            phase_name = "グリッド編集" if self.current_phase == self.PHASE_EDIT_GRID else "色編集"
            message = f"{phase_name}の変更内容は破棄されます。ステップ1に戻りますか？"
        # フェーズ3にいて、まだ変更がない場合でも確認（色編集状態がリセットされるため）
        elif self.current_phase == self.PHASE_EDIT_COLOR and self.undo_stack.isClean():
             # ただし、グリッド編集から来て何も変更していない場合は確認不要かもしれない。
             # 一旦、フェーズ3から1へ戻る場合は常に確認する方針とする。
             confirm_needed = True
             message = "色編集の状態は破棄されます。ステップ1に戻りますか？"

        if confirm_needed:
             reply = QMessageBox.question(self, '確認', message,
                                          QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
             if reply == QMessageBox.StandardButton.No: return

        self.go_to_phase1()

    def go_to_phase1(self):
        """フェーズ1に遷移する実際の処理"""
        self.setStatusMessage("ステップ1: 初期グリッド設定")
        self.undo_stack.clear()
        # set_phase が呼ばれる前にフェーズに応じたクリア処理を行う
        if self.current_phase == self.PHASE_EDIT_COLOR:
             self.clear_color_selection()
        self.set_phase(self.PHASE_INITIAL_GRID) # UI更新を含む
        # スピンボックスの値でグリッド再生成 & プレビュー更新
        self.update_grid_from_spinbox(force_update=True) # これがprocess_imageを呼ぶ

    def confirm_and_go_to_phase2(self):
        """フェーズ2への遷移を実行 (ステップ1からは確認不要)"""
        if not self.original_image: return
        self.go_to_phase2() # ステップ1から2へは確認不要

    def go_to_phase2(self):
        """フェーズ2に遷移する実際の処理"""
        self.setStatusMessage("ステップ2: グリッド線 編集")
        self.undo_stack.clear()
        # set_phase が呼ばれる前にフェーズに応じたクリア処理を行う
        if self.current_phase == self.PHASE_EDIT_COLOR:
            self.clear_color_selection()
        self.set_phase(self.PHASE_EDIT_GRID) # UI更新を含む
        # 現在のグリッドは維持される

    def confirm_and_go_to_phase3(self):
        """フェーズ3への遷移を実行 (グリッドを確定)"""
        if not self.original_image: return
        self.setStatusMessage("色編集の準備中...")
        QApplication.processEvents()
        # 現在のグリッド状態を保存
        self.grid_state_before_color_edit = self.original_image_label.getGridLines()
        # 最終的な画像処理を実行 (プレビューではない)
        self.process_image(is_preview=False) # これがpixel_mapを確定しUI更新
        if self.processed_image:
            self.go_to_phase3()
        else:
            self.setStatusMessage("色編集に進めません: 画像処理に失敗しました", 3000)

    def go_to_phase3(self):
        """フェーズ3に遷移する実際の処理"""
        self.setStatusMessage("ステップ3: 色 編集")
        self.undo_stack.clear()
        # self.clear_color_selection() # set_phase内で呼ばれる (これは不要、フェーズ遷移元でクリア済みか、影響なし)
        self.set_phase(self.PHASE_EDIT_COLOR) # UI更新を含む

    def confirm_and_go_to_phase2_from_3(self):
         """フェーズ3からフェーズ2への遷移を確認し実行"""
         # フェーズ3にいて、かつ変更がある場合のみ確認
         if self.current_phase == self.PHASE_EDIT_COLOR and not self.undo_stack.isClean():
             reply = QMessageBox.question(self, '確認', "色編集の変更内容は破棄されます。ステップ2に戻りますか？",
                                          QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
             if reply == QMessageBox.StandardButton.No: return
         # 変更がない場合でも、色編集状態は破棄されるため確認する方が親切か？ -> 上記の分岐で十分
         self.go_to_phase2_from_3()

    def go_to_phase2_from_3(self):
        """フェーズ3からフェーズ2に戻る実際の処理"""
        self.setStatusMessage("ステップ2: グリッド線 編集に戻っています...")
        QApplication.processEvents()
        self.undo_stack.clear()
        # set_phase が呼ばれる前にフェーズに応じたクリア処理を行う
        if self.current_phase == self.PHASE_EDIT_COLOR:
            self.clear_color_selection()
        # フェーズ3に入る前のグリッド状態に戻す
        if self.grid_state_before_color_edit:
            cols, rows = self.grid_state_before_color_edit
            self.original_image_label.setGridLinesDirectly(cols, rows)
        # 画像を再処理して色編集前の状態に戻す
        self.process_image(is_preview=False) # これがUI更新も行う
        self.set_phase(self.PHASE_EDIT_GRID) # UI更新を含む

    # --- スロットメソッド (UI操作系) ---
    def zoom_in(self): self.original_image_label.setScaleFactor(self.original_image_label.getScaleFactor() * 1.2)
    def zoom_out(self): self.original_image_label.setScaleFactor(self.original_image_label.getScaleFactor() / 1.2)
    def zoom_slider_changed(self, value):
        new_scale = value / 100.0; self.zoom_percent_label.setText(f"{value}%")
        # ズームの中心をラベルの中心にする
        self.original_image_label.setScaleFactor(new_scale, self.original_image_label.rect().center())
    def update_zoom_controls_from_label(self, scale):
        slider_value = int(round(scale * 100))
        # スライダー操作中は更新しない (無限ループ防止)
        if not self._is_slider_adjusting:
            self.zoom_slider.blockSignals(True); self.zoom_slider.setValue(slider_value); self.zoom_slider.blockSignals(False)
        self.zoom_percent_label.setText(f"{slider_value}%")
    def fit_image_to_window(self): self.original_image_label.fitToWindow()
    def handle_view_change(self, scale, center_pos): self.update_zoom_controls_from_label(scale)

    def update_grid_from_spinbox(self, force_update=False):
        """スピンボックスの値に基づいてグリッド線を均等に再配置 (フェーズ1用)"""
        if self.current_phase != self.PHASE_INITIAL_GRID or not self.original_image:
            return
        cols_count = self.cols_spinbox.value(); rows_count = self.rows_spinbox.value()
        old_cols, old_rows = self.original_image_label.getGridLines()
        img_width, img_height = self.original_image.size
        new_cols = [(c + 1) * img_width / cols_count for c in range(cols_count - 1)] if cols_count > 1 else []
        new_rows = [(r + 1) * img_height / rows_count for r in range(rows_count - 1)] if rows_count > 1 else []
        def is_close(list1, list2, tol=1e-6): # リスト比較ヘルパー
            if len(list1) != len(list2): return False
            return all(abs(a - b) < tol for a, b in zip(sorted(list1), sorted(list2)))
        if force_update or not is_close(old_cols, new_cols) or not is_close(old_rows, new_rows):
             self.original_image_label.setGridLinesDirectly(new_cols, new_rows)
             self.schedule_preview_update() # 自動更新が有効ならプレビューをトリガー

    def add_grid_change_command(self, old_cols, old_rows, new_cols, new_rows, description):
        """グリッド変更コマンドを追加 (フェーズ2用)"""
        if self.current_phase == self.PHASE_EDIT_GRID:
            command = GridChangeCommand(self.original_image_label, old_cols, old_rows, new_cols, new_rows, description)
            self.undo_stack.push(command)
            # schedule_preview_update は gridChanged シグナル経由で呼ばれるはず

    def schedule_preview_update(self):
        """プレビュー更新を予約 (フェーズ1, 2 用)"""
        auto_update_enabled = False
        if self.current_phase == self.PHASE_INITIAL_GRID:
            auto_update_enabled = self.auto_preview_checkbox.isChecked()
        elif self.current_phase == self.PHASE_EDIT_GRID:
             auto_update_enabled = self.auto_preview_checkbox_phase2.isChecked()

        if auto_update_enabled:
            self.setStatusMessage("プレビュー更新予約...", 1000)
            self.preview_update_timer.start()

    def trigger_process_image_preview(self):
        """プレビュー/処理を実行 (フェーズ1, 2 用)"""
        if self.current_phase == self.PHASE_INITIAL_GRID or self.current_phase == self.PHASE_EDIT_GRID:
            self.process_image(is_preview=True)

    def sync_and_preview(self):
        """計算方法コンボボックスの値を同期し、プレビューを更新"""
        sender = self.sender()
        if sender == self.color_mode_combo and self.current_phase == self.PHASE_INITIAL_GRID:
            self.color_mode_combo_phase2.blockSignals(True); self.color_mode_combo_phase2.setCurrentIndex(self.color_mode_combo.currentIndex()); self.color_mode_combo_phase2.blockSignals(False)
        elif sender == self.color_mode_combo_phase2 and self.current_phase == self.PHASE_EDIT_GRID:
            self.color_mode_combo.blockSignals(True); self.color_mode_combo.setCurrentIndex(self.color_mode_combo_phase2.currentIndex()); self.color_mode_combo.blockSignals(False)
        self.schedule_preview_update()

    def toggle_auto_preview(self, checked):
        """自動更新チェックボックスの状態を同期"""
        sender = self.sender()
        if sender == self.auto_preview_checkbox and self.current_phase == self.PHASE_INITIAL_GRID:
            self.auto_preview_checkbox_phase2.blockSignals(True); self.auto_preview_checkbox_phase2.setChecked(checked); self.auto_preview_checkbox_phase2.blockSignals(False)
        elif sender == self.auto_preview_checkbox_phase2 and self.current_phase == self.PHASE_EDIT_GRID:
            self.auto_preview_checkbox.blockSignals(True); self.auto_preview_checkbox.setChecked(checked); self.auto_preview_checkbox.blockSignals(False)
        if checked: # 有効になった場合はプレビューを試みる
            self.schedule_preview_update()


    # --- 色関連メソッド (フェーズ3用) ---

    def get_processed_coords_at_label_pos(self, label_widget, label_pos: QPoint) -> tuple | None:
        """指定されたラベル座標に対応する処理後画像の座標 (c, r) を返す"""
        if label_widget is not self.original_image_label or not self.pixel_map:
            return None
        # ラベル座標 -> オリジナル画像座標
        img_pos_f = label_widget.label_to_image_coords(label_pos)
        img_x, img_y = img_pos_f.x(), img_pos_f.y()
        # オリジナル画像座標が含まれるピクセル矩形をpixel_mapから検索
        for coords, data in self.pixel_map.items():
            rect = data['rect'] # (left, top, right, bottom)
            # right, bottom は含まない境界 ( < ) で判定
            if rect[0] <= img_x < rect[2] and rect[1] <= img_y < rect[3]:
                return coords # 処理後座標 (c, r) を返す
        return None # 見つからなかった場合

    def clear_color_selection(self):
        """色選択状態をリセットし、UIを更新"""
        if self.selected_coords_set: # 変更があった場合のみ更新
            self.selected_coords_set.clear()
            self.update_color_selection_ui() # ラベル、ボタン状態更新
            self.original_image_label.update() # 左側ラベルの再描画
            self.setStatusMessage("ピクセル選択を解除しました", 1500)

    # 領域外クリック時に呼び出すスロット
    def clear_color_selection_if_phase3(self):
        """フェーズ3の場合のみ色選択を解除する"""
        if self.current_phase == self.PHASE_EDIT_COLOR and self.selected_coords_set:
            self.clear_color_selection()

    def update_color_selection_ui(self):
        """選択状態に基づいて情報ラベルと編集ボタンの状態を更新し、左ラベルを再描画"""
        num_selected = len(self.selected_coords_set)
        # フェーズ3で、かつ処理結果が存在する場合のみ編集可能
        can_edit = num_selected > 0 and self.current_phase == self.PHASE_EDIT_COLOR and self.processed_image is not None

        info_text = "左の画像上でピクセルを選択してください" # デフォルト
        if self.current_phase == self.PHASE_EDIT_COLOR and num_selected > 0:
            selected_colors = set()
            if self.pixel_map:
                for c, r in self.selected_coords_set:
                    if (c, r) in self.pixel_map:
                         selected_colors.add(self.pixel_map[(c, r)]['color'])
            num_unique_colors = len(selected_colors)
            if num_unique_colors == 1:
                color = selected_colors.pop()
                hex_color = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
                alpha_info = f", Alpha={color[3]}" if len(color) > 3 else ""
                info_text = f"{num_selected} 個選択中 (単一色: {hex_color}{alpha_info})"
            else:
                info_text = f"{num_selected} 個選択中 ({num_unique_colors} 色)"
        elif self.current_phase == self.PHASE_EDIT_COLOR and self.processed_image is None:
            info_text = "画像処理結果がありません" # 処理失敗時など

        self.color_info_label.setText(info_text)
        self.edit_color_button.setEnabled(can_edit)
        self.edit_color_action.setEnabled(can_edit)
        # 左側ラベルの表示更新（選択状態が変わったことをpaintEventで反映させるため）
        self.original_image_label.update()


    def handle_pixel_interaction(self, label_pos: QPoint, modifiers: Qt.KeyboardModifier, event_type: str):
        """左側画像ラベルからのインタラクション(クリック/ドラッグ)を処理"""
        if self.current_phase != self.PHASE_EDIT_COLOR:
            return

        # 領域外クリックは image_label からの clickedOutsidePixels シグナルで処理するため、ここでは何もしない
        # if coords is None and event_type == 'press':
        #     self.clear_color_selection() # 以前のロジック（重複するので削除）
        #     return

        coords = self.get_processed_coords_at_label_pos(self.original_image_label, label_pos)
        # ドラッグ終了時(`release`)以外は、ピクセル上の操作でなければ無視
        if coords is None and event_type != 'release':
             # ドラッグ中に領域外に出ても、最後のピクセル上の座標で処理を続ける
             if event_type == 'move' and self._drag_selection_mode:
                 pass # ドラッグ中は領域外に出ても継続
             else:
                 return # 領域外でのプレス開始などは無視

        is_shift_pressed = bool(modifiers & Qt.KeyboardModifier.ShiftModifier)
        current_pixel_color = self.pixel_map.get(coords, {}).get('color') if coords else None

        if event_type == 'press':
            self._last_interacted_coords = set() # ドラッグ中の重複処理防止用リセット
            self._drag_selection_mode = None     # ドラッグモードリセット

            if coords is None: return # クリック開始位置がピクセル外なら何もしない

            if is_shift_pressed:
                # --- Shift + Press: 同色一括選択/解除 ---
                if current_pixel_color:
                    same_color_coords = {c for c, data in self.pixel_map.items() if data['color'] == current_pixel_color}
                    if not same_color_coords: return # 該当色なし
                    # 既に選択されている同色ピクセルが存在するかどうか
                    is_currently_selected = bool(self.selected_coords_set.intersection(same_color_coords))
                    # 選択操作前の選択状態をUndo用に保存する（ColorChangeCommand用ではないが、将来的な選択操作Undo用）
                    # current_selection_for_undo = self.selected_coords_set.copy()
                    if is_currently_selected:
                        self.selected_coords_set.difference_update(same_color_coords)
                        self.setStatusMessage(f"色 {current_pixel_color[0:3]} を一括解除", 1500)
                    else:
                        self.selected_coords_set.update(same_color_coords)
                        self.setStatusMessage(f"色 {current_pixel_color[0:3]} を一括選択", 1500)
                    # TODO: 選択操作自体のUndo/Redoが必要な場合は、ここでコマンドを発行する
                    self.update_color_selection_ui() # UI更新
            else:
                # --- Normal Press: 個別選択/解除 or ドラッグ準備 ---
                # 選択操作前の選択状態をUndo用に保存する（同上）
                # current_selection_for_undo = self.selected_coords_set.copy()
                if coords in self.selected_coords_set:
                    # 選択済み -> 解除モードでドラッグ開始
                    self.selected_coords_set.remove(coords)
                    self._drag_selection_mode = 'remove'
                    self.setStatusMessage(f"ピクセル ({coords[0]},{coords[1]}) 解除", 1500)
                else:
                    # 未選択 -> 選択モードでドラッグ開始
                    self.selected_coords_set.add(coords)
                    self._drag_selection_mode = 'add'
                    self.setStatusMessage(f"ピクセル ({coords[0]},{coords[1]}) 選択", 1500)
                # TODO: 選択操作自体のUndo/Redoが必要な場合は、ここでコマンドを発行する
                self._last_interacted_coords.add(coords) # 最初に操作した座標を記録
                self.update_color_selection_ui() # UI更新 (ラベル、ボタン、左画像描画)

        elif event_type == 'move':
            # ドラッグ選択モード中 かつ 最後に操作した座標と違う場合のみ処理
            # かつ、カーソルが有効なピクセル上にある場合
            if self._drag_selection_mode and coords and coords not in self._last_interacted_coords:
                 selection_changed = False
                 if self._drag_selection_mode == 'add':
                     if coords not in self.selected_coords_set:
                         self.selected_coords_set.add(coords); selection_changed = True
                 elif self._drag_selection_mode == 'remove':
                     if coords in self.selected_coords_set:
                         self.selected_coords_set.remove(coords); selection_changed = True
                 if selection_changed:
                     self._last_interacted_coords.add(coords)
                     # ドラッグ中は左ラベル描画のみ更新 (高速化のため)
                     self.original_image_label.update()

        elif event_type == 'release':
             # ドラッグ終了時に最終的なUI状態を更新
             # (選択操作自体のUndo/Redoを実装する場合は、ここで最終状態をコマンドとして確定する)
             self._last_interacted_coords = set()
             self._drag_selection_mode = None
             self.update_color_selection_ui() # ラベルとボタン状態を更新
             # print(f"Selection ended. Count: {len(self.selected_coords_set)}") # Debug

    def edit_selected_color_group(self):
        """選択中のピクセル群の色を編集 (複数色対応)"""
        if not self.selected_coords_set or self.current_phase != self.PHASE_EDIT_COLOR:
            return

        # --- Undo/Redo 用に現在の選択状態をコピー ---
        # この old_selection_set が Undo/Redo 時に復元される選択状態となる
        old_selection_set = self.selected_coords_set.copy()

        # ... (色リスト作成、カラーダイアログ表示などの処理は変更なし) ...
        coords_list = sorted(list(self.selected_coords_set))
        old_colors_list = []
        initial_dialog_color = QColor(255, 255, 255)
        unique_colors = set()
        for c, r in coords_list:
            color_tuple = self.pixel_map.get((c, r), {}).get('color')
            if color_tuple:
                 old_colors_list.append(color_tuple)
                 unique_colors.add(color_tuple)
            else:
                 old_colors_list.append((0,0,0,0))
        if len(coords_list) != len(old_colors_list):
            QMessageBox.warning(self, "エラー", "選択ピクセルの元の色の取得に問題が発生しました。")
            return
        if len(unique_colors) == 1:
            single_color = unique_colors.pop()
            initial_dialog_color = QColor(single_color[0], single_color[1], single_color[2], single_color[3])

        new_qcolor = QColorDialog.getColor(initial_dialog_color, self,
                                           f"選択中の {len(coords_list)} 個のピクセルの新しい色を選択",
                                           options=QColorDialog.ColorDialogOption.ShowAlphaChannel)

        if new_qcolor.isValid():
            new_color_rgba = (new_qcolor.red(), new_qcolor.green(), new_qcolor.blue(), new_qcolor.alpha())

            # --- ColorChangeCommand に選択状態も渡す ---
            command = ColorChangeCommand(
                window=self,
                pixel_coords_list=coords_list,
                old_colors_list=old_colors_list, # 元の色リスト
                new_color=new_color_rgba,        # 新しい色は共通
                old_selection_set=old_selection_set, # 変更前の選択状態
                description=f"{len(coords_list)}個のピクセルの色変更"
            )
            self.undo_stack.push(command) # コマンド実行 (redoが呼ばれる)

            # --- ★修正箇所: コマンド実行直後の選択解除処理を削除 ---
            # self.clear_color_selection() # この行を削除またはコメントアウト


    # --- コア機能メソッド ---
    def load_image(self):
        """画像ファイルをロードし、フェーズ1に設定"""
        file_path, _ = QFileDialog.getOpenFileName(self, "画像ファイルを選択", "", "画像ファイル (*.png *.jpg *.jpeg *.bmp *.gif *.tiff)")
        if file_path:
            try:
                self.setStatusMessage(f"読み込み中: {os.path.basename(file_path)}..."); QApplication.processEvents()
                pil_img = Image.open(file_path)
                # RGBAに変換しておく
                self.original_image = pil_img.convert('RGBA')
                # --- 左ラベルに画像設定 ---
                self.original_image_label.setPilImage(self.original_image)
                # --- 状態リセット ---
                self.undo_stack.clear()
                self.pixel_map = {}
                self.original_image_label.set_pixel_map_ref(self.pixel_map) # 参照も更新
                # 色選択状態もクリア (set_phaseで呼ばれるので不要かもだが念のため)
                self.clear_color_selection()
                self.grid_state_before_color_edit = None
                # --- フェーズ設定 ---
                self.set_phase(self.PHASE_INITIAL_GRID) # UI更新を含む

                # --- 初期グリッド設定と処理 ---
                cols = self.cols_spinbox.value(); rows = self.rows_spinbox.value()
                img_w, img_h = self.original_image.size
                initial_cols = [(c + 1) * img_w / cols for c in range(cols - 1)] if cols > 1 else []
                initial_rows = [(r + 1) * img_h / rows for r in range(rows - 1)] if rows > 1 else []
                self.original_image_label.setGridLinesDirectly(initial_cols, initial_rows)
                self.process_image(is_preview=False) # 初期表示、UI更新含む

                self.file_label.setText(os.path.basename(file_path))
                self.setStatusMessage(f"画像 '{os.path.basename(file_path)}' を読み込みました", 3000)
                if self.original_image: self.original_image_label.fitToWindow()

            except Exception as e:
                error_msg = f"画像ファイルの読み込みに失敗しました:\n{e}\n\n{traceback.format_exc()}"
                QMessageBox.warning(self, "エラー", error_msg)
                # --- エラー時の状態リセット ---
                self.original_image = None
                self.original_image_label.setPilImage(None)
                self.processed_image = None
                self.processed_image_label.clear()
                self.pixel_map = {}; self.original_image_label.set_pixel_map_ref(self.pixel_map)
                self.clear_color_selection() # エラー時も選択クリア
                self.undo_stack.clear(); self.setStatusMessage("画像の読み込みに失敗しました")
                self.set_phase(self.PHASE_INITIAL_GRID) # UI更新含む
            # finally は不要

    def process_image(self, is_preview=True):
        """画像を処理して低解像度化 & ピクセルマップ作成 & UI更新"""
        if not self.original_image or not self.original_image_label:
            if not is_preview: QMessageBox.warning(self, "エラー", "画像が読み込まれていません。")
            self.setStatusMessage("処理失敗: 画像なし", 2000)
            self.processed_image = None # 処理結果をNoneに
            self.pixel_map = {} # pixel_mapもクリア
            self.original_image_label.set_pixel_map_ref(self.pixel_map)
            self.display_processed_image() # 右側ラベルクリア & UI更新
            return

        col_boundaries, row_boundaries = self.original_image_label.getGridPositions()
        color_mode_index = 0; current_combo_text = ""
        if self.current_phase == self.PHASE_INITIAL_GRID:
            color_mode_index = self.color_mode_combo.currentIndex(); current_combo_text = self.color_mode_combo.currentText()
        else: # PHASE_EDIT_GRID or PHASE_EDIT_COLOR
            # 色編集フェーズでは計算方法はPhase2のものを使う
            color_mode_index = self.color_mode_combo_phase2.currentIndex(); current_combo_text = self.color_mode_combo_phase2.currentText()
        color_mode = ["average", "median", "mode"][color_mode_index]
        current_config = {'cols': tuple(col_boundaries), 'rows': tuple(row_boundaries), 'mode': color_mode}

        # --- プレビュー時のスキップ判定 ---
        # 色編集フェーズでは常に再処理（Undo/Redoで画像が変わる可能性があるため）
        can_skip_preview = (is_preview and
                            current_config == self.last_processed_config and
                            self.processed_image is not None and
                            self.current_phase != self.PHASE_EDIT_COLOR and # 色編集中はスキップしない
                            self.undo_stack.isClean()) # 変更がない場合のみ
        if can_skip_preview:
             # print("Skipping preview generation, config hasn't changed.") # Debug
             return

        # --- 選択解除ロジック (改善) ---
        # グリッドや計算方法が変わる場合（フェーズ1, 2）は選択を解除
        # フェーズ3での処理（色変更コマンドのUndo/Redo時）は選択解除しない
        if self.current_phase == self.PHASE_INITIAL_GRID or self.current_phase == self.PHASE_EDIT_GRID:
             self.clear_color_selection() # これがUI更新も行う

        # --- pixel_map 再構築 ---
        new_pixel_map = {} # 新しいマップを作成
        self.last_processed_config = current_config # 処理設定を記録

        # --- グリッド境界チェック ---
        if len(col_boundaries) < 2 or len(row_boundaries) < 2:
            msg = "有効なグリッドが設定されていません (最低1x1のセルが必要です)。"; self.processed_image = None
            if not is_preview: QMessageBox.warning(self, "エラー", msg)
            else: self.setStatusMessage(f"プレビュー失敗: {msg}", 2000)
            self.pixel_map = new_pixel_map # 空のマップをセット
            self.original_image_label.set_pixel_map_ref(self.pixel_map) # 参照更新
            self.display_processed_image(); return # 右側更新して終了

        output_cols = len(col_boundaries) - 1; output_rows = len(row_boundaries) - 1
        if output_cols <= 0 or output_rows <= 0:
            msg = "グリッドから有効なセルが生成されませんでした。"; self.processed_image = None
            if not is_preview: QMessageBox.warning(self, "エラー", msg)
            else: self.setStatusMessage(f"プレビュー失敗: {msg}", 2000)
            self.pixel_map = new_pixel_map # 空のマップをセット
            self.original_image_label.set_pixel_map_ref(self.pixel_map) # 参照更新
            self.display_processed_image(); return

        # --- 画像処理ループ ---
        progress_msg = f"処理中 ({current_combo_text}, {output_cols}x{output_rows})..."; self.setStatusMessage(progress_msg); QApplication.processEvents()
        try:
            output_mode = 'RGBA'
            new_processed_image = Image.new(output_mode, (output_cols, output_rows))
            # 元画像は毎回RGBAに変換しておくのが安全
            source_image_for_proc = self.original_image.convert('RGBA')
            calculation_func = {"average": calculate_average_color, "median": calculate_median_color, "mode": calculate_mode_color}.get(color_mode, calculate_average_color)
            total_cells = output_rows * output_cols; processed_cells = 0

            for r in range(output_rows):
                for c in range(output_cols):
                    left, top = col_boundaries[c], row_boundaries[r]; right, bottom = col_boundaries[c+1], row_boundaries[r+1]
                    # crop_boxは整数である必要がある
                    crop_box = (int(round(left)), int(round(top)), int(round(right)), int(round(bottom)))
                    final_color = (0, 0, 0, 0) # デフォルト (完全透明)

                    # crop領域が有効かチェック
                    if crop_box[2] > crop_box[0] and crop_box[3] > crop_box[1]:
                        try:
                            region = source_image_for_proc.crop(crop_box)
                            if region.width > 0 and region.height > 0:
                                calculated_color = calculation_func(region, output_mode)
                                # 計算結果がNoneや不正な値でないか確認
                                if isinstance(calculated_color, tuple) and len(calculated_color) == 4:
                                     final_color = calculated_color
                                else:
                                     print(f"Warning: Invalid color calculated for cell ({c},{r}). Using default.")
                                     final_color = (128, 128, 128, 255) # デフォルト色 (グレー)
                            else:
                                # crop結果が空の場合もデフォルト色
                                final_color = (128, 128, 128, 255)
                        except Exception as cell_error:
                             print(f"Error processing cell ({c},{r}): {cell_error}")
                             final_color = (255, 0, 255, 255) # エラー色 (マゼンタ)

                    # putpixelの座標が画像の範囲内か確認
                    if 0 <= c < output_cols and 0 <= r < output_rows:
                        try:
                            new_processed_image.putpixel((c, r), final_color)
                            # 新しいpixel_mapに結果を格納
                            # 矩形情報は元の浮動小数点数の方が精度が良い場合があるため、そちらを保存
                            original_rect_tuple = (left, top, right, bottom)
                            new_pixel_map[(c, r)] = {'rect': original_rect_tuple, 'color': final_color}
                        except IndexError:
                             print(f"Error: putpixel index ({c},{r}) out of bounds for image size ({output_cols}x{output_rows}).")
                             pass # エラー発生時はスキップ

                    processed_cells += 1
                    # プログレス表示の頻度調整
                    if total_cells > 0 and processed_cells % (max(1, total_cells // 20)) == 0:
                         progress_percent = int(100 * processed_cells / total_cells); self.setStatusMessage(f"{progress_msg} {progress_percent}%"); QApplication.processEvents()

            # --- 処理完了後 ---
            self.processed_image = new_processed_image
            self.pixel_map = new_pixel_map # 新しいマップを正式に採用
            # --- 左側ラベルに新しいpixel_map参照を渡し、再描画を促す ---
            self.original_image_label.set_pixel_map_ref(self.pixel_map)
            self.original_image_label.update() # 左側を明示的に更新
            # --- 右側プレビュー更新 & UI更新 ---
            self.display_processed_image() # これが右側表示と全体のUI状態更新を行う
            status_end_msg = "プレビュー更新完了" if is_preview else "処理完了"; self.setStatusMessage(status_end_msg, 2000)

        except Exception as e:
            error_msg = f"画像の処理中にエラーが発生しました:\n{e}\n\n{traceback.format_exc()}"; QMessageBox.critical(self, "処理エラー", error_msg)
            self.processed_image = None; self.pixel_map = {}; # エラー時はマップもクリア
            self.original_image_label.set_pixel_map_ref(self.pixel_map) # 参照更新
            self.display_processed_image(); self.setStatusMessage("処理エラー") # UI更新含む

    def display_processed_image(self):
        """処理結果画像を右側ラベルに表示し、UI状態を更新"""
        if not self.processed_image:
            self.processed_image_label.clear()
            self.processed_image_label.setText("結果なし")
            # 結果がない場合は選択もクリア (UI更新含む)
            self.clear_color_selection()
            # UI状態更新も行う
            self.update_ui_for_phase()
            return
        try:
            # --- 右側は単純に処理結果を表示 ---
            # PillowからQImageへ変換
            qimage_disp = pillow_to_qimage_for_display(self.processed_image)
            if qimage_disp:
                pixmap_disp = QPixmap.fromImage(qimage_disp)
                # QLabelに合わせてNearest Neighborでリサイズ
                label_w = self.processed_image_label.width()
                label_h = self.processed_image_label.height()
                # FastTransformationがNearest Neighbor相当
                scaled_pixmap = pixmap_disp.scaled(label_w, label_h,
                                                   Qt.AspectRatioMode.KeepAspectRatio,
                                                   Qt.TransformationMode.FastTransformation)
                self.processed_image_label.setPixmap(scaled_pixmap)
            else:
                self.processed_image_label.clear(); self.processed_image_label.setText("表示エラー(QImage)")
                # エラー時はクリア
                self.clear_color_selection()
        except Exception as display_err:
            print(f"Error displaying processed image: {display_err}\n{traceback.format_exc()}")
            self.processed_image_label.clear(); self.processed_image_label.setText("表示エラー")
            # エラー時はクリア
            self.clear_color_selection()

        # --- 表示更新後、選択状態に応じたUI更新 ---
        # update_color_selection_ui は選択状態が変わった時やフェーズ変更時に呼ばれる
        # ここでは表示だけを行い、UI全体の更新は update_ui_for_phase に任せる
        self.update_ui_for_phase() # UI全体の状態を更新
        # update_color_selection_ui() # これも update_ui_for_phase 内で呼ばれるはず

    def save_image(self):
        """処理結果を保存"""
        if not self.processed_image: QMessageBox.warning(self, "エラー", "保存する処理結果がありません。"); return
        # --- 保存処理 (変更なし) ---
        original_filename = self.file_label.text()
        default_save_path = "pixelated_image.png"
        if original_filename != '画像が選択されていません' and '.' in original_filename:
            base, _ = os.path.splitext(original_filename); default_save_path = f"{base}_pixelated.png"
        file_path, selected_filter = QFileDialog.getSaveFileName(self, "処理結果を保存", default_save_path, "PNG (*.png);;JPEG (*.jpg *.jpeg);;BMP (*.bmp);;GIF (*.gif);;TIFF (*.tif *.tiff)")
        if file_path:
            self.setStatusMessage(f"保存中: {os.path.basename(file_path)}..."); QApplication.processEvents()
            try:
                save_kwargs = {}; img_to_save = self.processed_image
                file_ext = os.path.splitext(file_path)[1].lower()
                if file_ext in ('.jpg', '.jpeg'):
                     # JPEG保存時にアルファチャンネルを扱う
                     if img_to_save.mode == 'RGBA':
                         # 白背景で合成
                         background = Image.new("RGB", img_to_save.size, (255, 255, 255))
                         background.paste(img_to_save, mask=img_to_save.split()[3]) # アルファチャンネルをマスクとして使用
                         img_to_save = background
                     elif img_to_save.mode != 'RGB': # RGB以外なら変換
                          img_to_save = img_to_save.convert("RGB")
                     save_kwargs['quality'] = 95; save_kwargs['subsampling'] = 0 # 高画質設定
                elif file_ext == '.png': save_kwargs['optimize'] = True # PNG最適化
                elif file_ext in ('.tif', '.tiff'): save_kwargs['compression'] = 'tiff_lzw' # TIFFはLZW圧縮
                # その他のフォーマットはデフォルト設定

                img_to_save.save(file_path, **save_kwargs)
                self.setStatusMessage(f"画像を保存しました: {file_path}", 3000)
                QMessageBox.information(self, "成功", f"画像を保存しました:\n{file_path}")
            except Exception as e:
                error_msg = f"画像の保存に失敗しました:\n{e}\n\n{traceback.format_exc()}"
                self.setStatusMessage("画像の保存に失敗しました", 3000)
                QMessageBox.critical(self, "保存エラー", error_msg)

    def closeEvent(self, event):
        """ウィンドウクローズイベント"""
        if not self.undo_stack.isClean():
             reply = QMessageBox.question(self, '確認', "未保存の変更があります。終了しますか？", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
             if reply == QMessageBox.StandardButton.Yes: event.accept()
             else: event.ignore()
        else: event.accept()


# --- アプリケーションエントリーポイント ---
def main():
    # 高DPI設定
    if hasattr(Qt.ApplicationAttribute, 'AA_EnableHighDpiScaling'): QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    if hasattr(Qt.ApplicationAttribute, 'AA_UseHighDpiPixmaps'): QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    window = PixelatorWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
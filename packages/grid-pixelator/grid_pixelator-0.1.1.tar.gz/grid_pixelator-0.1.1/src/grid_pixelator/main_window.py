# src/grid_pixelator/main_window.py
import sys
import os
import traceback
from PIL import Image

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFileDialog, QSpinBox, QMessageBox, QSizePolicy, QSlider, QComboBox,
    QCheckBox, QMainWindow, QMenuBar, QStatusBar, QToolBar, QStyle
)
from PyQt6.QtGui import (
    QPixmap, QImage, QAction, QIcon, QKeySequence, QUndoStack
)
from PyQt6.QtCore import Qt, QTimer

# 他の自作モジュールからのインポート
from .image_label import InteractiveImageLabel
from .commands import GridChangeCommand
from .image_utils import (
    calculate_average_color, calculate_median_color, calculate_mode_color,
    pillow_to_qimage_for_display, NEAREST_NEIGHBOR, NUMPY_AVAILABLE, IMAGEQT_AVAILABLE
)

class PixelatorWindow(QMainWindow):
    """メインウィンドウクラス"""
    def __init__(self):
        super().__init__()
        self.original_image = None
        self.processed_image = None
        self._is_slider_adjusting = False
        self.undo_stack = QUndoStack(self)
        self.last_processed_config = {}
        self.preview_update_timer = QTimer(self)
        self.preview_update_timer.setSingleShot(True)
        self.preview_update_timer.setInterval(300) # プレビュー更新遅延 (ms)

        # NumPy/ImageQtの警告を一度だけ表示
        if not NUMPY_AVAILABLE: print("Warning: NumPy not found. Median calculation will be slower.")
        if not IMAGEQT_AVAILABLE: print("Warning: Pillow-PIL (ImageQt) not found. Pillow to QImage conversion might be less efficient.")

        self.initUI()
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.connectSignals()
        self.updateActions() # 初期状態設定

    def initUI(self):
        """UI要素の初期化と配置"""
        self.setWindowTitle('AdaptivePixelizer') # アプリ名変更
        self.setGeometry(100, 100, 1100, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # ファイル選択エリア
        file_layout = QHBoxLayout()
        # アイコン取得 (テーマ優先、なければ標準アイコン)
        open_icon = QIcon.fromTheme("document-open", self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon))
        self.load_button_widget = QPushButton(open_icon, " 画像ファイルを開く")
        self.load_button_widget.setToolTip("画像ファイルを選択します (Ctrl+O)")
        self.file_label = QLabel('画像が選択されていません')
        self.file_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        file_layout.addWidget(self.load_button_widget)
        file_layout.addWidget(self.file_label)
        main_layout.addLayout(file_layout)

        # 画像表示エリア
        image_layout = QHBoxLayout()
        self.original_image_label = InteractiveImageLabel() # InteractiveImageLabelを使用
        self.original_image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        image_layout.addWidget(self.original_image_label, 3)

        self.processed_image_label = QLabel('処理結果')
        self.processed_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.processed_image_label.setMinimumSize(200, 200)
        self.processed_image_label.setStyleSheet("border: 1px solid gray; color: gray; background-color: #333;")
        self.processed_image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        image_layout.addWidget(self.processed_image_label, 2)
        main_layout.addLayout(image_layout)

        # コントロールパネル
        control_panel_layout = QHBoxLayout()

        # ズームコントロール
        zoom_group_box = QWidget(); zoom_layout = QHBoxLayout(zoom_group_box); zoom_layout.setContentsMargins(5, 5, 5, 5)
        zoom_layout.addWidget(QLabel("ズーム:"))
        self.zoom_out_button = QPushButton("-"); self.zoom_out_button.setFixedWidth(30); self.zoom_out_button.setToolTip("ズームアウト (-)")
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        # スライダー範囲はラベルのmin/maxに合わせる
        self.zoom_slider.setRange(int(self.original_image_label.min_scale * 100), int(self.original_image_label.max_scale * 100))
        self.zoom_slider.setValue(100); self.zoom_slider.setTickInterval(100); self.zoom_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.zoom_slider.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred) # 横拡張
        self.zoom_in_button = QPushButton("+"); self.zoom_in_button.setFixedWidth(30); self.zoom_in_button.setToolTip("ズームイン (+)")
        self.zoom_percent_label = QLabel("100%"); self.zoom_percent_label.setFixedWidth(50)
        self.fit_button = QPushButton("全体表示"); self.fit_button.setToolTip("全体表示 (0)")
        zoom_layout.addWidget(self.zoom_out_button); zoom_layout.addWidget(self.zoom_slider); zoom_layout.addWidget(self.zoom_in_button)
        zoom_layout.addWidget(self.zoom_percent_label); zoom_layout.addWidget(self.fit_button); zoom_layout.addStretch(1)
        control_panel_layout.addWidget(zoom_group_box)

        # グリッド設定 & 処理コントロール
        settings_group_box = QWidget(); settings_layout = QHBoxLayout(settings_group_box); settings_layout.setContentsMargins(5, 5, 5, 5)
        settings_layout.addWidget(QLabel('初期グリッド:'))
        self.cols_spinbox = QSpinBox(); self.cols_spinbox.setRange(1, 256); self.cols_spinbox.setValue(8); self.cols_spinbox.setPrefix("横 ")
        self.rows_spinbox = QSpinBox(); self.rows_spinbox.setRange(1, 256); self.rows_spinbox.setValue(8); self.rows_spinbox.setPrefix("縦 ")
        settings_layout.addWidget(self.cols_spinbox); settings_layout.addWidget(self.rows_spinbox)
        settings_layout.addWidget(QLabel(" | 計算方法:"))
        self.color_mode_combo = QComboBox(); self.color_mode_combo.addItems(["平均 (Average)", "中央値 (Median)", "最頻色 (Mode)"])
        settings_layout.addWidget(self.color_mode_combo)
        self.auto_preview_checkbox = QCheckBox("プレビュー自動更新"); self.auto_preview_checkbox.setChecked(True)
        self.auto_preview_checkbox.setToolTip("グリッドや設定変更時にプレビューを自動で更新します")
        settings_layout.addWidget(self.auto_preview_checkbox)
        self.process_button = QPushButton('プレビュー更新 / 実行'); self.process_button.setToolTip("現在の設定で処理を実行し、右側に表示 (Enter)")
        settings_layout.addWidget(self.process_button); settings_layout.addStretch(1)
        control_panel_layout.addWidget(settings_group_box)
        main_layout.addLayout(control_panel_layout)

    def createActions(self):
        """メニューバーやツールバーのアクションを作成"""
        # アイコン取得ヘルパー (テーマ -> 標準 -> なし)
        def get_icon(theme_name, fallback_sp):
            icon = QIcon.fromTheme(theme_name)
            if not icon.isNull(): return icon
            std_icon = self.style().standardIcon(fallback_sp, None, "") # オプション指定しない
            if not std_icon.isNull(): return std_icon
            return QIcon() # 空のアイコン

        # ファイル操作
        self.open_action = QAction(get_icon("document-open", QStyle.StandardPixmap.SP_DirOpenIcon), "開く...", self)
        self.open_action.setShortcut(QKeySequence.StandardKey.Open); self.open_action.setStatusTip("画像ファイルを開きます")
        self.save_action = QAction(get_icon("document-save-as", QStyle.StandardPixmap.SP_DialogSaveButton), "名前を付けて保存...", self)
        self.save_action.setShortcut(QKeySequence.StandardKey.SaveAs); self.save_action.setStatusTip("処理結果の画像を保存します"); self.save_action.setEnabled(False)
        self.exit_action = QAction("終了", self); self.exit_action.setShortcut(QKeySequence.StandardKey.Quit); self.exit_action.setStatusTip("アプリケーションを終了します")

        # 編集操作
        self.undo_action = self.undo_stack.createUndoAction(self, "元に戻す")
        self.undo_action.setIcon(get_icon("edit-undo", QStyle.StandardPixmap.SP_ArrowBack)); self.undo_action.setShortcut(QKeySequence.StandardKey.Undo); self.undo_action.setEnabled(False)
        self.redo_action = self.undo_stack.createRedoAction(self, "やり直し")
        self.redo_action.setIcon(get_icon("edit-redo", QStyle.StandardPixmap.SP_ArrowForward)); self.redo_action.setShortcut(QKeySequence.StandardKey.Redo); self.redo_action.setEnabled(False)

        # 表示操作
        self.zoom_in_action = QAction(get_icon("zoom-in", QStyle.StandardPixmap.SP_ArrowUp), "ズームイン", self)
        self.zoom_in_action.setShortcut(QKeySequence.StandardKey.ZoomIn); self.zoom_in_action.setEnabled(False)
        self.zoom_out_action = QAction(get_icon("zoom-out", QStyle.StandardPixmap.SP_ArrowDown), "ズームアウト", self)
        self.zoom_out_action.setShortcut(QKeySequence.StandardKey.ZoomOut); self.zoom_out_action.setEnabled(False)
        self.fit_action = QAction(get_icon("zoom-fit-best", QStyle.StandardPixmap.SP_FileDialogListView), "全体表示", self)
        self.fit_action.setShortcut(QKeySequence("Ctrl+0")); self.fit_action.setEnabled(False)

        # 処理操作
        self.process_action = QAction(get_icon("media-playback-start", QStyle.StandardPixmap.SP_MediaPlay), "処理実行/プレビュー更新", self)
        self.process_action.setShortcut(QKeySequence(Qt.Key.Key_Return)); self.process_action.setEnabled(False)

    def createMenus(self):
        """メニューバーを作成"""
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("ファイル"); file_menu.addAction(self.open_action); file_menu.addAction(self.save_action); file_menu.addSeparator(); file_menu.addAction(self.exit_action)
        edit_menu = menu_bar.addMenu("編集"); edit_menu.addAction(self.undo_action); edit_menu.addAction(self.redo_action)
        view_menu = menu_bar.addMenu("表示"); view_menu.addAction(self.zoom_in_action); view_menu.addAction(self.zoom_out_action); view_menu.addAction(self.fit_action); view_menu.addSeparator()
        # 自動プレビューメニュー
        process_menu = menu_bar.addMenu("処理"); process_menu.addAction(self.process_action)
        auto_preview_action = process_menu.addAction("プレビュー自動更新"); auto_preview_action.setCheckable(True)
        auto_preview_action.setChecked(self.auto_preview_checkbox.isChecked()); auto_preview_action.toggled.connect(self.auto_preview_checkbox.setChecked)
        self.auto_preview_checkbox.toggled.connect(auto_preview_action.setChecked)

    def createToolBars(self):
        """ツールバーを作成"""
        toolbar = QToolBar("メインツールバー"); self.addToolBar(toolbar)
        toolbar.addAction(self.open_action); toolbar.addAction(self.save_action); toolbar.addSeparator()
        toolbar.addAction(self.undo_action); toolbar.addAction(self.redo_action); toolbar.addSeparator()
        toolbar.addAction(self.zoom_out_action); toolbar.addAction(self.zoom_in_action); toolbar.addAction(self.fit_action); toolbar.addSeparator()
        toolbar.addAction(self.process_action)

    def createStatusBar(self):
        """ステータスバーを作成"""
        self.statusBar().showMessage("準備完了")

    def connectSignals(self):
        """シグナルとスロットを接続"""
        # ファイル
        self.load_button_widget.clicked.connect(self.load_image)
        self.open_action.triggered.connect(self.load_image)
        self.save_action.triggered.connect(self.save_image)
        self.exit_action.triggered.connect(self.close)
        # 画像ラベル
        self.original_image_label.scaleChanged.connect(self.update_zoom_controls_from_label)
        self.original_image_label.viewChanged.connect(self.handle_view_change)
        self.original_image_label.gridChanged.connect(self.schedule_preview_update)
        self.original_image_label.requestGridChangeUndoable.connect(self.add_grid_change_command)
        # ズーム
        self.zoom_out_button.clicked.connect(self.zoom_out); self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_slider.valueChanged.connect(self.zoom_slider_changed)
        self.zoom_slider.sliderPressed.connect(lambda: setattr(self, '_is_slider_adjusting', True))
        self.zoom_slider.sliderReleased.connect(lambda: setattr(self, '_is_slider_adjusting', False))
        self.fit_button.clicked.connect(self.fit_image_to_window)
        self.zoom_in_action.triggered.connect(self.zoom_in); self.zoom_out_action.triggered.connect(self.zoom_out); self.fit_action.triggered.connect(self.fit_image_to_window)
        # グリッド・処理
        self.cols_spinbox.valueChanged.connect(self.update_grid_from_spinbox)
        self.rows_spinbox.valueChanged.connect(self.update_grid_from_spinbox)
        self.color_mode_combo.currentIndexChanged.connect(self.schedule_preview_update)
        self.process_button.clicked.connect(self.trigger_process_image_preview)
        self.process_action.triggered.connect(self.trigger_process_image_preview)
        self.preview_update_timer.timeout.connect(self.trigger_process_image_preview) # タイマー接続
        # Undo/Redo
        self.undo_stack.canUndoChanged.connect(self.undo_action.setEnabled)
        self.undo_stack.canRedoChanged.connect(self.redo_action.setEnabled)
        self.undo_stack.cleanChanged.connect(self.updateWindowTitle) # ウィンドウタイトル更新

    def updateActions(self):
        """アクションやウィジェットの有効/無効を更新"""
        has_image = self.original_image is not None
        has_processed = self.processed_image is not None
        self.save_action.setEnabled(has_processed)
        self.zoom_in_action.setEnabled(has_image); self.zoom_out_action.setEnabled(has_image); self.fit_action.setEnabled(has_image)
        self.zoom_in_button.setEnabled(has_image); self.zoom_out_button.setEnabled(has_image); self.zoom_slider.setEnabled(has_image); self.fit_button.setEnabled(has_image)
        self.process_action.setEnabled(has_image); self.process_button.setEnabled(has_image)
        self.cols_spinbox.setEnabled(has_image); self.rows_spinbox.setEnabled(has_image); self.color_mode_combo.setEnabled(has_image); self.auto_preview_checkbox.setEnabled(has_image)
        # Undo/Redo はスタックに接続済み

    def updateWindowTitle(self):
        """ウィンドウタイトルに変更状態(*)を表示"""
        title = "AdaptivePixelizer"
        if self.original_image:
            title += f" - {os.path.basename(self.file_label.text())}" # ファイル名表示
        if not self.undo_stack.isClean():
            title += " *" # 変更ありマーク
        self.setWindowTitle(title)

    # --- スロットメソッド (UI操作系) ---
    def zoom_in(self): self.original_image_label.setScaleFactor(self.original_image_label.getScaleFactor() * 1.2)
    def zoom_out(self): self.original_image_label.setScaleFactor(self.original_image_label.getScaleFactor() / 1.2)
    def zoom_slider_changed(self, value):
        new_scale = value / 100.0; self.zoom_percent_label.setText(f"{value}%")
        # ドラッグ中はスケール更新しないオプション（コメントアウト中）
        # if not self._is_slider_adjusting:
        self.original_image_label.setScaleFactor(new_scale, self.original_image_label.label_center)
    def update_zoom_controls_from_label(self, scale):
        slider_value = int(round(scale * 100))
        self.zoom_slider.blockSignals(True); self.zoom_slider.setValue(slider_value); self.zoom_slider.blockSignals(False)
        self.zoom_percent_label.setText(f"{slider_value}%")
    def fit_image_to_window(self): self.original_image_label.fitToWindow()
    def handle_view_change(self, scale, center_pos): self.update_zoom_controls_from_label(scale) # スケール表示更新のみ
    def update_grid_from_spinbox(self):
        cols = self.cols_spinbox.value(); rows = self.rows_spinbox.value()
        self.original_image_label.updateGridFromSpinbox(cols, rows) # ラベルに更新を依頼
    def add_grid_change_command(self, old_cols, old_rows, new_cols, new_rows, description):
        command = GridChangeCommand(self.original_image_label, old_cols, old_rows, new_cols, new_rows, description)
        self.undo_stack.push(command)
        # self.schedule_preview_update() # コマンドのundo/redoでgridChangedがemitされるので不要かも？確認。-> undo/redo時にも更新したいので必要
        self.schedule_preview_update()
    def schedule_preview_update(self):
        if self.auto_preview_checkbox.isChecked():
            self.statusBar().showMessage("プレビュー更新予約...", 1000)
            self.preview_update_timer.start()
        else:
            self.statusBar().showMessage("自動プレビュー更新オフ", 1000)
    def trigger_process_image_preview(self):
        self.process_image(is_preview=True)

    # --- コア機能メソッド ---
    def load_image(self):
        """画像ファイルをロード"""
        file_path, _ = QFileDialog.getOpenFileName(self, "画像ファイルを選択", "", "画像ファイル (*.png *.jpg *.jpeg *.bmp *.gif *.tiff)")
        if file_path:
            try:
                self.statusBar().showMessage(f"読み込み中: {os.path.basename(file_path)}..."); QApplication.processEvents()
                pil_img = Image.open(file_path)
                self.original_image = pil_img
                self.original_image_label.setPilImage(self.original_image)
                self.undo_stack.clear() # 新規画像で履歴クリア
                cols = self.cols_spinbox.value(); rows = self.rows_spinbox.value(); img_w, img_h = pil_img.size
                initial_cols = [(c + 1) * img_w / cols for c in range(cols - 1)] if cols > 1 else []
                initial_rows = [(r + 1) * img_h / rows for r in range(rows - 1)] if rows > 1 else []
                self.original_image_label.setGridLinesDirectly(initial_cols, initial_rows) # 初期グリッド設定
                self.process_image(is_preview=False) # 初期プレビュー生成
                self.file_label.setText(os.path.basename(file_path))
                self.statusBar().showMessage(f"画像 '{os.path.basename(file_path)}' を読み込みました", 3000)
            except Exception as e:
                error_msg = f"画像ファイルの読み込みに失敗しました:\n{e}\n\n{traceback.format_exc()}"
                QMessageBox.warning(self, "エラー", error_msg); self.original_image = None
                self.original_image_label.setPilImage(None); self.file_label.setText('画像が選択されていません')
                self.processed_image = None; self.processed_image_label.clear(); self.processed_image_label.setText("処理結果")
                self.processed_image_label.setStyleSheet("border: 1px solid gray; color: gray; background-color: #333;")
                self.undo_stack.clear(); self.statusBar().showMessage("画像の読み込みに失敗しました")
            finally:
                self.updateActions()
                self.updateWindowTitle() # ウィンドウタイトル更新
                if self.original_image: self.original_image_label.fitToWindow() # 読み込めたらフィット

    def process_image(self, is_preview=True):
        """画像を処理して低解像度化"""
        if not self.original_image or not self.original_image_label:
            if not is_preview: QMessageBox.warning(self, "エラー", "画像が読み込まれていません。")
            self.statusBar().showMessage("処理失敗: 画像なし", 2000); return

        col_boundaries, row_boundaries = self.original_image_label.getGridPositions()
        color_mode_index = self.color_mode_combo.currentIndex(); color_mode = ["average", "median", "mode"][color_mode_index]
        current_config = {'cols': tuple(col_boundaries), 'rows': tuple(row_boundaries), 'mode': color_mode}
        if is_preview and current_config == self.last_processed_config and self.processed_image is not None:
            self.statusBar().showMessage("プレビュー: 設定変更なし", 1000); return
        self.last_processed_config = current_config

        if len(col_boundaries) < 2 or len(row_boundaries) < 2:
            msg = "有効なグリッドが設定されていません (最低1x1のセルが必要です)。"
            if not is_preview: QMessageBox.warning(self, "エラー", msg)
            else: self.statusBar().showMessage(f"プレビュー失敗: {msg}", 2000)
            self.processed_image = None; self.display_processed_image(); self.updateActions(); return
        output_cols = len(col_boundaries) - 1; output_rows = len(row_boundaries) - 1
        if output_cols <= 0 or output_rows <= 0:
            msg = "グリッドから有効なセルが生成されませんでした。"
            if not is_preview: QMessageBox.warning(self, "エラー", msg)
            else: self.statusBar().showMessage(f"プレビュー失敗: {msg}", 2000)
            self.processed_image = None; self.display_processed_image(); self.updateActions(); return

        progress_msg = f"処理中 ({self.color_mode_combo.currentText()}, {output_cols}x{output_rows})..."; self.statusBar().showMessage(progress_msg); QApplication.processEvents()
        try:
            output_mode = 'RGBA' if self.original_image.mode in ('RGBA', 'LA', 'P') else 'RGB'
            self.processed_image = Image.new(output_mode, (output_cols, output_rows))
            source_image_for_proc = self.original_image
            # 計算関数を取得 (image_utilsからインポートしたものを使用)
            calculation_func = {
                "average": calculate_average_color,
                "median": calculate_median_color,
                "mode": calculate_mode_color
            }.get(color_mode, calculate_average_color) # デフォルトは平均

            total_cells = output_rows * output_cols; processed_cells = 0
            for r in range(output_rows):
                for c in range(output_cols):
                    left, top = col_boundaries[c], row_boundaries[r]; right, bottom = col_boundaries[c+1], row_boundaries[r+1]
                    if right <= left or bottom <= top:
                        fallback_color = (0, 0, 0, 0) if output_mode == 'RGBA' else (0, 0, 0)
                        if 0 <= c < output_cols and 0 <= r < output_rows: 
                            try: self.processed_image.putpixel((c, r), fallback_color); 
                            except IndexError: pass
                        continue
                    crop_box = (int(left), int(top), int(right), int(bottom))
                    try:
                        region = source_image_for_proc.crop(crop_box)
                        if region.width == 0 or region.height == 0:
                            fallback_color = (0, 0, 0, 0) if output_mode == 'RGBA' else (0, 0, 0)
                            if 0 <= c < output_cols and 0 <= r < output_rows: try: self.processed_image.putpixel((c, r), fallback_color); except IndexError: pass
                            continue
                        avg_color = calculation_func(region, output_mode)
                        fallback_color = (128, 128, 128, 255) if output_mode == 'RGBA' else (128, 128, 128)
                        final_color = avg_color if avg_color else fallback_color
                        if 0 <= c < output_cols and 0 <= r < output_rows: try: self.processed_image.putpixel((c, r), final_color); except IndexError: pass
                    except Exception as cell_error:
                         print(f"Error processing cell ({c},{r}) box {crop_box}: {cell_error}")
                         fallback_color = (255, 0, 255, 255) if output_mode == 'RGBA' else (255, 0, 255)
                         if 0 <= c < output_cols and 0 <= r < output_rows: try: self.processed_image.putpixel((c, r), fallback_color); except IndexError: pass
                    processed_cells += 1
                    if processed_cells % (max(1, output_cols // 4)) == 0: # 進捗更新頻度調整
                         progress_percent = int(100 * processed_cells / total_cells); self.statusBar().showMessage(f"{progress_msg} {progress_percent}%"); QApplication.processEvents()

            self.display_processed_image()
            status_end_msg = "プレビュー更新完了" if is_preview else "処理完了"; self.statusBar().showMessage(status_end_msg, 2000)
        except Exception as e:
            error_msg = f"画像の処理中にエラーが発生しました:\n{e}\n\n{traceback.format_exc()}"; QMessageBox.critical(self, "処理エラー", error_msg)
            self.processed_image = None; self.display_processed_image(); self.statusBar().showMessage("処理エラー")
        finally: self.updateActions()

    def get_color_calculation_func(self, mode):
        """計算モードに対応する関数を返す (image_utils内の関数を返す)"""
        # 注意: このメソッドは process_image 内で直接辞書を使っているため、現在は未使用
        if mode == "median": return calculate_median_color
        elif mode == "mode": return calculate_mode_color
        else: return calculate_average_color

    def display_processed_image(self):
        """処理結果画像を表示"""
        if not self.processed_image:
            self.processed_image_label.clear(); self.processed_image_label.setText("結果なし")
            self.processed_image_label.setStyleSheet("border: 1px solid gray; color: gray; background-color: #333;"); return
        try:
            processed_w, processed_h = self.processed_image.size; label_w = self.processed_image_label.width(); label_h = self.processed_image_label.height()
            if processed_w <= 0 or processed_h <= 0 or label_w <= 0 or label_h <= 0:
                self.processed_image_label.clear(); self.processed_image_label.setText("表示不可 (サイズ0)"); return
            scale = min(label_w / processed_w, label_h / processed_h)
            display_w = int(processed_w * scale); display_h = int(processed_h * scale)
            if display_w > 0 and display_h > 0:
                # NEAREST_NEIGHBOR は image_utils からインポート
                scaled_pil = self.processed_image.resize((display_w, display_h), resample=NEAREST_NEIGHBOR)
            else: scaled_pil = self.processed_image
            # pillow_to_qimage_for_display は image_utils からインポート
            qimage_disp = pillow_to_qimage_for_display(scaled_pil)
            if qimage_disp:
                pixmap_disp = QPixmap.fromImage(qimage_disp); self.processed_image_label.setPixmap(pixmap_disp)
                self.processed_image_label.setStyleSheet("border: 1px solid gray; background-color: #333;")
            else:
                self.processed_image_label.clear(); self.processed_image_label.setText("結果表示エラー (QImage変換失敗)")
                self.processed_image_label.setStyleSheet("border: 1px solid red; color: red; background-color: #333;")
        except Exception as display_err:
            print(f"Error displaying processed image: {display_err}\n{traceback.format_exc()}")
            self.processed_image_label.clear(); self.processed_image_label.setText("結果表示エラー")
            self.processed_image_label.setStyleSheet("border: 1px solid red; color: red; background-color: #333;")

    def save_image(self):
        """処理結果を保存"""
        if not self.processed_image: QMessageBox.warning(self, "エラー", "保存する処理結果がありません。"); return
        original_filename = self.file_label.text()
        default_save_path = "pixelated_image.png"
        if original_filename != '画像が選択されていません' and '.' in original_filename:
            base, _ = os.path.splitext(original_filename); default_save_path = f"{base}_pixelated.png"
        file_path, selected_filter = QFileDialog.getSaveFileName(self, "処理結果を保存", default_save_path, "PNG (*.png);;JPEG (*.jpg *.jpeg);;BMP (*.bmp);;GIF (*.gif);;TIFF (*.tif *.tiff)")
        if file_path:
            self.statusBar().showMessage(f"保存中: {os.path.basename(file_path)}..."); QApplication.processEvents()
            try:
                save_kwargs = {}; img_to_save = self.processed_image; file_ext = os.path.splitext(file_path)[1].lower()
                if file_ext in ('.jpg', '.jpeg'):
                     if img_to_save.mode in ('RGBA', 'LA', 'P'):
                         if 'A' in img_to_save.mode or (img_to_save.mode == 'P' and 'transparency' in img_to_save.info):
                             background = Image.new("RGB", img_to_save.size, (255, 255, 255)); img_rgba = img_to_save.convert('RGBA')
                             background.paste(img_rgba, mask=img_rgba.split()[3]); img_to_save = background
                         else: img_to_save = img_to_save.convert("RGB")
                     elif img_to_save.mode != 'RGB': img_to_save = img_to_save.convert("RGB")
                     save_kwargs['quality'] = 95; save_kwargs['subsampling'] = 0
                elif file_ext == '.png': save_kwargs['optimize'] = True
                elif file_ext in ('.tif', '.tiff'): save_kwargs['compression'] = 'tiff_lzw'
                img_to_save.save(file_path, **save_kwargs)
                self.statusBar().showMessage(f"画像を保存しました: {file_path}", 3000); QMessageBox.information(self, "成功", f"画像を保存しました:\n{file_path}")
                self.undo_stack.setClean() # 保存したらクリーン状態にする
                self.updateWindowTitle()
            except Exception as e:
                error_msg = f"画像の保存に失敗しました:\n{e}\n\n{traceback.format_exc()}"; self.statusBar().showMessage("画像の保存に失敗しました", 3000); QMessageBox.critical(self, "保存エラー", error_msg)

    def closeEvent(self, event):
        """ウィンドウクローズイベント"""
        if not self.undo_stack.isClean():
             reply = QMessageBox.question(self, '確認', "未保存の変更があります。終了しますか？", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
             if reply == QMessageBox.StandardButton.Yes: event.accept()
             else: event.ignore()
        else: event.accept()

# --- アプリケーションエントリーポイント ---
def main():
    """アプリケーションのメイン関数"""
    # 高DPI対応
    if hasattr(Qt, 'AA_EnableHighDpiScaling'): QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'): QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    # アプリアイコン設定 (任意)
    # app_icon = QIcon("path/to/icon.png") # パッケージリソースから読む場合は importlib.resources を使う
    # app.setWindowIcon(app_icon)

    window = PixelatorWindow()
    window.show()
    sys.exit(app.exec())

# このファイルが直接実行された場合にmain()を呼び出す
if __name__ == '__main__':
    main()
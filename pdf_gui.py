from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTabWidget, QFileDialog, QMessageBox
)
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
import os
import sys
from pdf_to_image import convert_pdf_to_images
from PIL import Image, ImageOps
from color_convert import convert_colors, process_directory


class DragDropLineEdit(QLineEdit):
    """支持拖拽的输入框 (浮浮酱特制的拖拽输入框喵～)"""

    def __init__(self, parent=None, accept_files=True, accept_folders=True):
        super().__init__(parent)
        self.accept_files = accept_files  # 是否接受文件
        self.accept_folders = accept_folders  # 是否接受文件夹
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """处理拖拽进入事件 (检查拖进来的东西是否合法喵)"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        """处理放置事件 (处理拖拽放下的文件喵～)"""
        urls = event.mimeData().urls()
        if urls:
            # 只取第一个文件/文件夹
            file_path = urls[0].toLocalFile()

            # 检查是文件还是文件夹
            is_file = os.path.isfile(file_path)
            is_folder = os.path.isdir(file_path)

            # 根据设置决定是否接受
            if (is_file and self.accept_files) or (is_folder and self.accept_folders):
                self.setText(file_path)
                event.acceptProposedAction()
            else:
                event.ignore()


class PDFConverterGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF工具集")
        self.setGeometry(100, 100, 700, 500)

        # 居中显示窗口 (让窗口出现在屏幕中央喵～)
        self.center_window()

        # 创建主部件和布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # 创建标签页
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # 添加各个功能标签页
        self.setup_pdf_tab()
        self.setup_invert_tab()
        self.setup_color_tab()
        self.setup_merge_tab()

    def center_window(self):
        """将窗口居中显示 (计算屏幕中心位置喵)"""
        screen = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        center_point = screen.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

    def setup_pdf_tab(self):
        """设置PDF转图片标签页 (第一个功能页面喵～)"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # PDF文件选择 (支持拖拽PDF文件进来喵～)
        pdf_layout = QHBoxLayout()
        pdf_layout.addWidget(QLabel("PDF文件:"))
        self.pdf_path_edit = DragDropLineEdit(accept_files=True, accept_folders=False)
        pdf_layout.addWidget(self.pdf_path_edit, stretch=1)
        pdf_btn = QPushButton("浏览")
        pdf_btn.clicked.connect(self.select_pdf)
        pdf_layout.addWidget(pdf_btn)
        layout.addLayout(pdf_layout)

        # 输出目录选择 (支持拖拽文件夹进来喵～)
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("输出目录:"))
        self.pdf_output_edit = DragDropLineEdit(accept_files=False, accept_folders=True)
        output_layout.addWidget(self.pdf_output_edit, stretch=1)
        output_btn = QPushButton("浏览")
        output_btn.clicked.connect(self.select_output_dir)
        output_layout.addWidget(output_btn)
        layout.addLayout(output_layout)

        # DPI设置 (设置图片质量喵)
        dpi_layout = QHBoxLayout()
        dpi_layout.addWidget(QLabel("图片DPI:"))
        self.dpi_edit = QLineEdit("200")
        self.dpi_edit.setMaximumWidth(100)
        dpi_layout.addWidget(self.dpi_edit)
        dpi_layout.addStretch()
        layout.addLayout(dpi_layout)

        # 转换按钮
        convert_btn = QPushButton("开始转换")
        convert_btn.clicked.connect(self.start_convert)
        layout.addWidget(convert_btn)

        # 状态显示
        self.pdf_status_label = QLabel("")
        self.pdf_status_label.setWordWrap(True)
        layout.addWidget(self.pdf_status_label)

        layout.addStretch()
        self.tabs.addTab(tab, "PDF转图片")

    def setup_invert_tab(self):
        """设置图片反转标签页 (反转图片颜色的功能喵～)"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # 输入目录选择
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("图片目录:"))
        self.invert_input_edit = DragDropLineEdit(accept_files=False, accept_folders=True)
        input_layout.addWidget(self.invert_input_edit, stretch=1)
        input_btn = QPushButton("浏览")
        input_btn.clicked.connect(self.select_invert_input_dir)
        input_layout.addWidget(input_btn)
        layout.addLayout(input_layout)

        # 输出目录选择
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("输出目录:"))
        self.invert_output_edit = DragDropLineEdit(accept_files=False, accept_folders=True)
        output_layout.addWidget(self.invert_output_edit, stretch=1)
        output_btn = QPushButton("浏览")
        output_btn.clicked.connect(self.select_invert_output_dir)
        output_layout.addWidget(output_btn)
        layout.addLayout(output_layout)

        # 反转按钮
        invert_btn = QPushButton("开始反转")
        invert_btn.clicked.connect(self.start_invert)
        layout.addWidget(invert_btn)

        # 状态显示
        self.invert_status_label = QLabel("")
        self.invert_status_label.setWordWrap(True)
        layout.addWidget(self.invert_status_label)

        layout.addStretch()
        self.tabs.addTab(tab, "图片反转")

    def setup_color_tab(self):
        """设置颜色转换标签页 (特定颜色转换功能喵～)"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # 输入目录选择
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("图片目录:"))
        self.color_input_edit = DragDropLineEdit(accept_files=False, accept_folders=True)
        input_layout.addWidget(self.color_input_edit, stretch=1)
        input_btn = QPushButton("浏览")
        input_btn.clicked.connect(self.select_color_input_dir)
        input_layout.addWidget(input_btn)
        layout.addLayout(input_layout)

        # 输出目录选择
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("输出目录:"))
        self.color_output_edit = DragDropLineEdit(accept_files=False, accept_folders=True)
        output_layout.addWidget(self.color_output_edit, stretch=1)
        output_btn = QPushButton("浏览")
        output_btn.clicked.connect(self.select_color_output_dir)
        output_layout.addWidget(output_btn)
        layout.addLayout(output_layout)

        # 颜色信息显示
        info_label1 = QLabel("白色 (255,255,255) → (255,223,63)")
        info_label2 = QLabel("黑色 (0,0,0) → (31,77,120)")
        layout.addWidget(info_label1)
        layout.addWidget(info_label2)

        # 转换按钮
        convert_btn = QPushButton("开始转换")
        convert_btn.clicked.connect(self.start_color_convert)
        layout.addWidget(convert_btn)

        # 状态显示
        self.color_status_label = QLabel("")
        self.color_status_label.setWordWrap(True)
        layout.addWidget(self.color_status_label)

        layout.addStretch()
        self.tabs.addTab(tab, "颜色转换")

    def setup_merge_tab(self):
        """设置图片合并PDF标签页 (把图片合并成PDF喵～)"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # 输入目录选择
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("图片目录:"))
        self.merge_input_edit = DragDropLineEdit(accept_files=False, accept_folders=True)
        input_layout.addWidget(self.merge_input_edit, stretch=1)
        input_btn = QPushButton("浏览")
        input_btn.clicked.connect(self.select_merge_input_dir)
        input_layout.addWidget(input_btn)
        layout.addLayout(input_layout)

        # 输出PDF文件选择
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("输出PDF:"))
        self.merge_output_edit = DragDropLineEdit(accept_files=True, accept_folders=False)
        output_layout.addWidget(self.merge_output_edit, stretch=1)
        output_btn = QPushButton("浏览")
        output_btn.clicked.connect(self.select_merge_output_file)
        output_layout.addWidget(output_btn)
        layout.addLayout(output_layout)

        # 合并按钮
        merge_btn = QPushButton("开始合并")
        merge_btn.clicked.connect(self.start_merge)
        layout.addWidget(merge_btn)

        # 状态显示
        self.merge_status_label = QLabel("")
        self.merge_status_label.setWordWrap(True)
        layout.addWidget(self.merge_status_label)

        layout.addStretch()
        self.tabs.addTab(tab, "图片合并PDF")

    def select_pdf(self):
        """选择PDF文件 (浏览选择PDF文件喵～)"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "选择PDF文件",
            "",
            "PDF文件 (*.pdf);;所有文件 (*.*)"
        )
        if filename:
            self.pdf_path_edit.setText(filename)
            # 自动设置输出目录为PDF所在目录
            self.pdf_output_edit.setText(os.path.dirname(filename))

    def select_output_dir(self):
        """选择输出目录"""
        dirname = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if dirname:
            self.pdf_output_edit.setText(dirname)

    def select_invert_input_dir(self):
        """选择反转输入目录"""
        dirname = QFileDialog.getExistingDirectory(self, "选择图片目录")
        if dirname:
            self.invert_input_edit.setText(dirname)
            # 自动设置输出目录
            self.invert_output_edit.setText(os.path.join(dirname, "inverted"))

    def select_invert_output_dir(self):
        """选择反转输出目录"""
        dirname = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if dirname:
            self.invert_output_edit.setText(dirname)

    def select_color_input_dir(self):
        """选择颜色转换输入目录"""
        dirname = QFileDialog.getExistingDirectory(self, "选择图片目录")
        if dirname:
            self.color_input_edit.setText(dirname)
            # 自动设置输出目录
            self.color_output_edit.setText(os.path.join(dirname, "color_converted"))

    def select_color_output_dir(self):
        """选择颜色转换输出目录"""
        dirname = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if dirname:
            self.color_output_edit.setText(dirname)

    def select_merge_input_dir(self):
        """选择合并输入目录"""
        dirname = QFileDialog.getExistingDirectory(self, "选择图片目录")
        if dirname:
            self.merge_input_edit.setText(dirname)
            # 自动设置输出PDF文件路径
            self.merge_output_edit.setText(os.path.join(dirname, "merged.pdf"))

    def select_merge_output_file(self):
        """选择合并输出文件"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "保存PDF文件",
            "",
            "PDF文件 (*.pdf);;所有文件 (*.*)"
        )
        if filename:
            self.merge_output_edit.setText(filename)

    def start_convert(self):
        """开始PDF转换 (执行PDF转图片功能喵～)"""
        pdf_path = self.pdf_path_edit.text()
        output_dir = self.pdf_output_edit.text()
        dpi = self.dpi_edit.text()

        if not pdf_path:
            QMessageBox.critical(self, "错误", "请选择PDF文件！")
            return

        try:
            dpi = int(dpi) if dpi.strip() else 200
            self.pdf_status_label.setText("正在转换中...")
            QApplication.processEvents()  # 刷新界面

            convert_pdf_to_images(pdf_path, output_dir, dpi)

            self.pdf_status_label.setText("转换完成！")
            QMessageBox.information(self, "成功", "PDF转换完成！")

        except Exception as e:
            self.pdf_status_label.setText(f"转换失败: {str(e)}")
            QMessageBox.critical(self, "错误", f"转换过程中出现错误：{str(e)}")

    def start_invert(self):
        """开始图片反转 (反转图片颜色喵～)"""
        input_dir = self.invert_input_edit.text()
        output_dir = self.invert_output_edit.text()

        if not input_dir:
            QMessageBox.critical(self, "错误", "请选择图片目录！")
            return

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        try:
            self.invert_status_label.setText("正在处理图片...")
            QApplication.processEvents()

            # 支持的图片格式
            image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
            processed_count = 0

            for filename in os.listdir(input_dir):
                if filename.lower().endswith(image_extensions):
                    input_path = os.path.join(input_dir, filename)
                    output_path = os.path.join(output_dir, f"inverted_{filename}")

                    # 打开图片并反转颜色
                    with Image.open(input_path) as img:
                        inverted_img = ImageOps.invert(img.convert('RGB'))
                        inverted_img.save(output_path)
                        processed_count += 1

                    self.invert_status_label.setText(f"已处理 {processed_count} 张图片...")
                    QApplication.processEvents()

            self.invert_status_label.setText(f"处理完成！共处理 {processed_count} 张图片")
            QMessageBox.information(self, "成功", f"图片反转完成！共处理 {processed_count} 张图片")

        except Exception as e:
            self.invert_status_label.setText(f"处理失败: {str(e)}")
            QMessageBox.critical(self, "错误", f"处理过程中出现错误：{str(e)}")

    def start_color_convert(self):
        """开始颜色转换 (执行特定颜色转换喵～)"""
        input_path = self.color_input_edit.text()
        output_path = self.color_output_edit.text()

        if not input_path:
            QMessageBox.critical(self, "错误", "请选择输入目录！")
            return

        try:
            self.color_status_label.setText("正在转换颜色...")
            QApplication.processEvents()

            # 处理整个目录
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            processed_count = process_directory(input_path, output_path)
            self.color_status_label.setText(f"转换完成！共处理 {processed_count} 个文件")
            QMessageBox.information(self, "成功", f"目录中的图片颜色转换完成！共处理 {processed_count} 个文件")

        except Exception as e:
            self.color_status_label.setText(f"转换失败: {str(e)}")
            QMessageBox.critical(self, "错误", f"转换过程中出现错误：{str(e)}")

    def start_merge(self):
        """开始图片合并 (把多张图片合并成一个PDF喵～)"""
        input_dir = self.merge_input_edit.text()
        output_file = self.merge_output_edit.text()

        if not input_dir:
            QMessageBox.critical(self, "错误", "请选择图片目录！")
            return

        if not output_file:
            QMessageBox.critical(self, "错误", "请选择输出PDF文件！")
            return

        try:
            self.merge_status_label.setText("正在合并图片...")
            QApplication.processEvents()

            # 支持的图片格式
            image_extensions = ('.png', '.jpg', '.jpeg', '.bmp')
            images = []
            first_image = None

            # 获取所有图片文件并按自然排序
            def natural_sort_key(s):
                import re
                # 将字符串中的数字转换为整数，用于自然排序
                return [int(text) if text.isdigit() else text.lower()
                        for text in re.split('([0-9]+)', s)]

            # 获取所有图片文件并按自然排序
            image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(image_extensions)]
            image_files.sort(key=natural_sort_key)

            for filename in image_files:
                input_path = os.path.join(input_dir, filename)
                img = Image.open(input_path)

                # 如果是PNG格式且有透明通道,转换为RGB
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                elif img.mode != 'RGB':
                    img = img.convert('RGB')

                if first_image is None:
                    first_image = img
                else:
                    images.append(img)

            if first_image:
                first_image.save(output_file, save_all=True, append_images=images)
                self.merge_status_label.setText(f"合并完成！共处理 {len(images) + 1} 张图片")
                QMessageBox.information(self, "成功", f"图片合并完成！共处理 {len(images) + 1} 张图片")
            else:
                raise Exception("未找到任何图片文件")

        except Exception as e:
            self.merge_status_label.setText(f"合并失败: {str(e)}")
            QMessageBox.critical(self, "错误", f"合并过程中出现错误：{str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PDFConverterGUI()
    window.show()
    sys.exit(app.exec())

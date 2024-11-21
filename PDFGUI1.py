import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QMessageBox, QScrollArea
)
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QFont
import PyPDF2


class DragDropArea(QWidget):
    """
    Custom widget to create a drag-and-drop area for PDF files.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.label = QLabel('Drag and drop PDF files here')
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont('Segoe UI', 12))
        self.label.setStyleSheet('''
            QLabel {
                border: 2px dashed #0078D7;
                border-radius: 10px;
                padding: 50px;
                color: #0078D7;
                background-color: #F3F3F3;
            }
        ''')
        layout.addWidget(self.label)
        self.setLayout(layout)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            # Check if at least one of the files is a PDF
            for url in event.mimeData().urls():
                if url.toLocalFile().lower().endswith('.pdf'):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dragMoveEvent(self, event: QDragEnterEvent):
        event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        pdf_files = [url.toLocalFile() for url in urls if url.toLocalFile().lower().endswith('.pdf')]
        if not pdf_files:
            QMessageBox.warning(self, "Invalid File", "Please drop only PDF files.")
            return
        for file_path in pdf_files:
            self.parent().add_file(file_path)
        event.acceptProposedAction()


class MainWindow(QWidget):
    """
    Main window of the application.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PDF Text Extractor')
        self.setMinimumSize(800, 600)
        self.files_data = []
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Drag and Drop Area
        self.drag_drop_area = DragDropArea(self)
        main_layout.addWidget(self.drag_drop_area)

        # Scroll Area to Display Extracted Texts
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.text_display_widget = QWidget()
        self.text_layout = QVBoxLayout()
        self.text_display_widget.setLayout(self.text_layout)
        self.scroll_area.setWidget(self.text_display_widget)
        main_layout.addWidget(self.scroll_area)

        # Clear Button
        button_layout = QHBoxLayout()
        clear_button = QPushButton('Clear All')
        clear_button.clicked.connect(self.clear_all)
        button_layout.addStretch()
        button_layout.addWidget(clear_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def add_file(self, file_path):
        """
        Extract text from the PDF file and display it.
        """
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text += page.extract_text() + "\n"

            # Create a container for each PDF's text
            container = QWidget()
            container_layout = QVBoxLayout()
            container.setLayout(container_layout)

            # Label with file name
            file_label = QLabel(f'File: {file_path.split("/")[-1]}')
            file_label.setFont(QFont('Segoe UI', 10, QFont.Weight.Bold))
            container_layout.addWidget(file_label)

            # Text Edit to display extracted text
            text_edit = QTextEdit()
            text_edit.setReadOnly(True)
            text_edit.setPlainText(text)
            text_edit.setFont(QFont('Consolas', 10))
            container_layout.addWidget(text_edit)

            self.text_layout.addWidget(container)
            self.files_data.append((file_path, text))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read PDF file.\n{e}")

    def clear_all(self):
        """
        Clear all displayed texts and reset the application.
        """
        for i in reversed(range(self.text_layout.count())):
            widget = self.text_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        self.files_data.clear()


def main():
    app = QApplication(sys.argv)
    # Set Microsoft Windows-like style
    app.setStyle('Fusion')  # 'Fusion' is a clean, modern style. You can choose others like 'Windows'

    # Optional: Customize the palette to match Windows aesthetics
    from PyQt6.QtGui import QPalette, QColor

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    palette.setColor(QPalette.ColorRole.Link, QColor(0, 120, 215))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
    app.setPalette(palette)

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

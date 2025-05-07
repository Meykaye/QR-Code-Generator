import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QFrame, QMessageBox, QFileDialog)
from PyQt5.QtGui import QPixmap, QIcon, QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QSize
import qrcode
from urllib.parse import urlparse

class DarkMaterialButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Roboto", 10, QFont.Medium))
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: #BB86FC;
                color: #121212;
                border-radius: 4px;
                padding: 8px 16px;
                min-width: 64px;
                border: none;
            }
            QPushButton:hover {
                background-color: #CF9FFF;
            }
            QPushButton:pressed {
                background-color: #9A67EA;
            }
            QPushButton:disabled {
                background-color: #424242;
                color: #757575;
            }
        """)

class DarkMaterialLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Roboto", 10))
        self.setStyleSheet("""
            QLineEdit {
                border: 1px solid #424242;
                border-radius: 4px;
                padding: 8px;
                background-color: #424242;
                color: #E0E0E0;
                selection-background-color: #BB86FC;
                selection-color: #121212;
            }
            QLineEdit:focus {
                border: 2px solid #BB86FC;
                padding: 7px;
            }
        """)

class DarkQRCodeGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Code Generator")
        self.setWindowIcon(QIcon(":qrcode-icon"))
        self.setMinimumSize(400, 500)
        
        # Set dark material design palette
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#121212"))
        palette.setColor(QPalette.WindowText, QColor("#E0E0E0"))
        palette.setColor(QPalette.Base, QColor("#1E1E1E"))
        palette.setColor(QPalette.AlternateBase, QColor("#121212"))
        palette.setColor(QPalette.ToolTipBase, QColor("#1E1E1E"))
        palette.setColor(QPalette.ToolTipText, QColor("#E0E0E0"))
        palette.setColor(QPalette.Text, QColor("#E0E0E0"))
        palette.setColor(QPalette.Button, QColor("#BB86FC"))
        palette.setColor(QPalette.ButtonText, QColor("#121212"))
        palette.setColor(QPalette.BrightText, Qt.white)
        palette.setColor(QPalette.Highlight, QColor("#BB86FC"))
        palette.setColor(QPalette.HighlightedText, QColor("#121212"))
        palette.setColor(QPalette.Disabled, QPalette.Button, QColor("#424242"))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor("#757575"))
        self.setPalette(palette)
        
        self.init_ui()
        
    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("QR Code Generator")
        header.setFont(QFont("Roboto", 18, QFont.Bold))
        header.setStyleSheet("color: #BB86FC;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Input section
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            background-color: #1E1E1E;
            border-radius: 8px;
            padding: 16px;
            border: 1px solid #424242;
        """)
        input_layout = QVBoxLayout(input_frame)
        input_layout.setSpacing(16)
        
        input_label = QLabel("Enter URL:")
        input_label.setFont(QFont("Roboto", 10, QFont.Medium))
        input_label.setStyleSheet("color: #E0E0E0;")
        input_layout.addWidget(input_label)
        
        self.url_input = DarkMaterialLineEdit()
        self.url_input.setPlaceholderText("https://example.com")
        input_layout.addWidget(self.url_input)
        
        generate_btn = DarkMaterialButton("Generate QR Code")
        generate_btn.clicked.connect(self.generate_qr_code)
        input_layout.addWidget(generate_btn)
        
        layout.addWidget(input_frame)
        
        # QR Code display section
        self.qr_frame = QFrame()
        self.qr_frame.setStyleSheet("""
            background-color: #1E1E1E;
            border-radius: 8px;
            padding: 16px;
            border: 1px solid #424242;
        """)
        self.qr_frame.setVisible(False)
        qr_layout = QVBoxLayout(self.qr_frame)
        qr_layout.setSpacing(16)
        
        qr_label = QLabel("Your QR Code:")
        qr_label.setFont(QFont("Roboto", 10, QFont.Medium))
        qr_label.setStyleSheet("color: #E0E0E0;")
        qr_layout.addWidget(qr_label)
        
        self.qr_image_label = QLabel()
        self.qr_image_label.setAlignment(Qt.AlignCenter)
        qr_layout.addWidget(self.qr_image_label)
        
        save_btn = DarkMaterialButton("Save QR Code")
        save_btn.clicked.connect(self.save_qr_code)
        qr_layout.addWidget(save_btn)
        
        layout.addWidget(self.qr_frame)
        
        # Add stretch to push everything up
        layout.addStretch()
        
        main_widget.setLayout(layout)
        
    def is_link_valid(self, website_link: str) -> bool:
        parsed = urlparse(website_link)
        return all([parsed.scheme in ("http", "https"), parsed.netloc])
    
    def generate_qr_code(self):
        website_link = self.url_input.text().strip()
        
        try:
            if not website_link:
                raise ValueError("Please enter a URL")
            if not self.is_link_valid(website_link):
                raise ValueError("Invalid URL. Please enter a valid http or https URL")
            
            # Generate QR code
            qr = qrcode.QRCode(version=5, box_size=5, border=5)
            qr.add_data(website_link)
            qr.make()
            
            img = qr.make_image(fill_color='white', back_color='black')
            
            # Convert to pixmap and display
            img.save('temp_qr.png')
            pixmap = QPixmap('temp_qr.png')
            self.qr_image_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.qr_frame.setVisible(True)
            
        except Exception as e:
            self.show_error_message(str(e))
    
    def save_qr_code(self):
        if not self.qr_image_label.pixmap():
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Save QR Code", 
            "", 
            "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;All Files (*)"
        )
        
        if file_path:
            self.qr_image_label.pixmap().save(file_path)
            self.show_success_message("QR code saved successfully!")
    
    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1E1E1E;
            }
            QLabel {
                color: #E0E0E0;
            }
            QPushButton {
                background-color: #BB86FC;
                color: #121212;
                border-radius: 4px;
                padding: 5px 10px;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #CF9FFF;
            }
        """)
        msg.exec_()
    
    def show_success_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("Success")
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1E1E1E;
            }
            QLabel {
                color: #E0E0E0;
            }
            QPushButton {
                background-color: #BB86FC;
                color: #121212;
                border-radius: 4px;
                padding: 5px 10px;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #CF9FFF;
            }
        """)
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style and font
    app.setStyle("Fusion")
    app.setFont(QFont("Roboto", 10))
    
    window = DarkQRCodeGeneratorApp()
    window.show()
    sys.exit(app.exec_())
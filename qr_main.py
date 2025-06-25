import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QFrame, QMessageBox, QFileDialog)
from PyQt5.QtGui import QPixmap, QIcon, QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QSize
import qrcode
from urllib.parse import urlparse
import os

class ModernButton(QPushButton):
    def __init__(self, text, parent=None, style="primary"):
        super().__init__(text, parent)
        self.style_type = style
        self.setFont(QFont("Arial", 11, QFont.Bold))
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(45)
        
        if style == "primary":
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                               stop:0 #4f46e5, stop:1 #7c3aed);
                    color: white;
                    border-radius: 8px;
                    padding: 0px 20px;
                    font-weight: bold;
                    border: none;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                               stop:0 #5b21b6, stop:1 #8b5cf6);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                               stop:0 #3730a3, stop:1 #6d28d9);
                }
                QPushButton:disabled {
                    background: #374151;
                    color: #9ca3af;
                }
            """)
        else:  # secondary style
            self.setStyleSheet("""
                QPushButton {
                    background: #374151;
                    color: #e5e7eb;
                    border: 1px solid #4b5563;
                    border-radius: 8px;
                    padding: 0px 20px;
                    font-weight: normal;
                }
                QPushButton:hover {
                    background: #4b5563;
                    border: 1px solid #6b7280;
                    color: white;
                }
                QPushButton:pressed {
                    background: #1f2937;
                    border: 1px solid #374151;
                }
            """)

class DarkLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Arial", 12))
        self.setFixedHeight(50)
        self.setStyleSheet("""
            QLineEdit {
                background: #1f2937;
                border: 2px solid #374151;
                border-radius: 8px;
                padding: 12px 16px;
                color: #f9fafb;
                font-size: 14px;
                selection-background-color: #4f46e5;
                selection-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #4f46e5;
                background: #111827;
            }
            QLineEdit::placeholder {
                color: #9ca3af;
            }
        """)

class DarkFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background: #111827;
                border: 1px solid #374151;
                border-radius: 12px;
                padding: 30px;
            }
        """)

class QRDisplayFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background: #111827;
                border: 1px solid #374151;
                border-radius: 12px;
                padding: 30px;
            }
        """)

class DarkQRCodeGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Code Generator - Dark Theme")
        
        # Increased window height and fixed size
        self.setFixedSize(1000, 700)
        
        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background: #0f172a;
                color: #f8fafc;
            }
        """)
        
        self.qr_pixmap = None
        self.init_ui()
        
    def init_ui(self):
        # Main widget with horizontal layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Main horizontal layout for two sections
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # LEFT SECTION - Input Section
        left_section = self.create_input_section()
        main_layout.addWidget(left_section)
        
        # RIGHT SECTION - QR Display Section  
        right_section = self.create_qr_section()
        main_layout.addWidget(right_section)
        
        # Set equal widths for both sections
        main_layout.setStretchFactor(left_section, 1)
        main_layout.setStretchFactor(right_section, 1)
        
        main_widget.setLayout(main_layout)
    
    def create_input_section(self):
        """Create the left input section"""
        # Create main container widget without frame styling
        input_container = QWidget()
        input_container.setStyleSheet("""
            QWidget {
                background: #111827;
                border: 1px solid #374151;
                border-radius: 12px;
            }
        """)
        
        input_layout = QVBoxLayout(input_container)
        input_layout.setContentsMargins(30, 30, 30, 30)
        input_layout.setSpacing(20)
        
        # Section title
        title = QLabel("Generate QR Code")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("""
            QLabel {
                color: #f8fafc;
                background: transparent;
                border: none;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        input_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Enter a valid URL to generate QR code")
        subtitle.setFont(QFont("Arial", 14))
        subtitle.setStyleSheet("""
            QLabel {
                color: #94a3b8;
                background: transparent;
                border: none;
            }
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        input_layout.addWidget(subtitle)
        
        # Add flexible spacing
        input_layout.addStretch(1)
        
        # Input label
        input_label = QLabel("Enter URL:")
        input_label.setFont(QFont("Arial", 14, QFont.Bold))
        input_label.setStyleSheet("""
            QLabel {
                color: #f8fafc;
                background: transparent;
                border: none;
            }
        """)
        input_layout.addWidget(input_label)
        
        # Input field
        self.url_input = DarkLineEdit()
        self.url_input.setPlaceholderText("https://example.com")
        self.url_input.returnPressed.connect(self.generate_qr_code)
        input_layout.addWidget(self.url_input)
        
        # Add spacing before buttons
        input_layout.addSpacing(15)
        
        # Generate button
        generate_btn = ModernButton("Generate QR Code", style="primary")
        generate_btn.clicked.connect(self.generate_qr_code)
        input_layout.addWidget(generate_btn)
        
        # Add spacing between buttons
        input_layout.addSpacing(10)
        
        # Clear button
        clear_btn = ModernButton("Clear", style="secondary")
        clear_btn.clicked.connect(self.clear_input)
        input_layout.addWidget(clear_btn)
        
        # Add flexible spacing at bottom
        input_layout.addStretch(1)
        
        return input_container
    
    def create_qr_section(self):
        """Create the right QR display section"""
        self.qr_frame = QRDisplayFrame()
        qr_layout = QVBoxLayout(self.qr_frame)
        qr_layout.setSpacing(20)
        
        # QR Section title
        qr_title = QLabel("QR Code Preview")
        qr_title.setFont(QFont("Arial", 20, QFont.Bold))
        qr_title.setStyleSheet("""
            QLabel {
                color: #f8fafc;
                margin-bottom: 10px;
            }
        """)
        qr_title.setAlignment(Qt.AlignCenter)
        qr_layout.addWidget(qr_title)
        
        # QR Code display area
        self.qr_image_label = QLabel()
        self.qr_image_label.setAlignment(Qt.AlignCenter)
        self.qr_image_label.setStyleSheet("""
            QLabel {
                background: #1f2937;
                border: 2px dashed #4b5563;
                border-radius: 12px;
                padding: 30px;
                min-height: 350px;
                color: #9ca3af;
                font-size: 16px;
            }
        """)
        self.qr_image_label.setText("QR Code will appear here\n\nEnter a valid URL and click\n'Generate QR Code'")
        self.qr_image_label.setMinimumSize(350, 350)
        qr_layout.addWidget(self.qr_image_label)
        
        # URL display
        self.url_display = QLabel()
        self.url_display.setFont(QFont("Arial", 11))
        self.url_display.setStyleSheet("""
            QLabel {
                color: #94a3b8;
                background: #1f2937;
                border-radius: 6px;
                padding: 10px 12px;
                border: 1px solid #374151;
            }
        """)
        self.url_display.setWordWrap(True)
        self.url_display.setAlignment(Qt.AlignCenter)
        self.url_display.hide()  # Initially hidden
        qr_layout.addWidget(self.url_display)
        
        # Save button
        self.save_btn = ModernButton("Save QR Code", style="primary")
        self.save_btn.clicked.connect(self.save_qr_code)
        self.save_btn.hide()  # Initially hidden
        qr_layout.addWidget(self.save_btn)
        
        return self.qr_frame
    
    def clear_input(self):
        self.url_input.clear()
        self.qr_image_label.clear()
        self.qr_image_label.setText("QR Code will appear here\n\nEnter a valid URL and click\n'Generate QR Code'")
        self.qr_image_label.setStyleSheet("""
            QLabel {
                background: #1f2937;
                border: 2px dashed #4b5563;
                border-radius: 12px;
                padding: 30px;
                min-height: 350px;
                color: #9ca3af;
                font-size: 16px;
            }
        """)
        self.url_display.hide()
        self.save_btn.hide()
        self.qr_pixmap = None
        
    def is_valid_url(self, url: str) -> bool:
        """Strictly validate if the input is a proper URL"""
        if not url.strip():
            return False
        
        try:
            parsed = urlparse(url.strip())
            
            # Must have both scheme and netloc (domain)
            if not parsed.scheme or not parsed.netloc:
                return False
            
            # Must be http or https
            if parsed.scheme.lower() not in ('http', 'https'):
                return False
            
            # Basic domain validation - must contain at least one dot
            if '.' not in parsed.netloc:
                return False
            
            # Domain should not start or end with dot or hyphen
            domain_parts = parsed.netloc.split('.')
            for part in domain_parts:
                if not part or part.startswith('-') or part.endswith('-'):
                    return False
            
            return True
            
        except Exception:
            return False
    
    def generate_qr_code(self):
        input_text = self.url_input.text().strip()
        
        try:
            if not input_text:
                raise ValueError("Please enter a URL")
            
            if not self.is_valid_url(input_text):
                raise ValueError("Please enter a valid URL (must start with http:// or https://)")
            
            # Generate QR code with high quality settings
            qr = qrcode.QRCode(
                version=1,  # Let it auto-determine size
                error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
                box_size=10,  # Good box size for quality
                border=4,
            )
            qr.add_data(input_text)
            qr.make(fit=True)
            
            # Create QR code image with high contrast
            img = qr.make_image(fill_color='black', back_color='white')
            
            # Save temporarily and load as pixmap
            temp_path = 'temp_qr.png'
            img.save(temp_path)
            
            # Load and scale the QR code to fit the display area
            pixmap = QPixmap(temp_path)
            scaled_pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # Update the QR display
            self.qr_image_label.setPixmap(scaled_pixmap)
            self.qr_image_label.setStyleSheet("""
                QLabel {
                    background: white;
                    border: 2px solid #4b5563;
                    border-radius: 12px;
                    padding: 20px;
                    min-height: 350px;
                }
            """)
            
            self.qr_pixmap = pixmap  # Store original for saving
            
            # Display the input text
            display_text = input_text
            if len(display_text) > 60:
                display_text = display_text[:60] + "..."
            self.url_display.setText(f"URL: {display_text}")
            self.url_display.show()
            
            # Show save button
            self.save_btn.show()
            
            # Clean up temp file
            try:
                os.remove(temp_path)
            except:
                pass
                
        except Exception as e:
            self.show_error_message(str(e))
    
    def save_qr_code(self):
        if not self.qr_pixmap:
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Save QR Code", 
            f"qrcode_{self.url_input.text()[:20].replace('/', '_').replace(':', '_')}.png",
            "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;All Files (*)"
        )
        
        if file_path:
            # Save the original high-quality version
            self.qr_pixmap.save(file_path)
            self.show_success_message("QR code saved successfully!")
    
    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.setStyleSheet("""
            QMessageBox {
                background: #111827;
                color: #f8fafc;
                border-radius: 8px;
            }
            QMessageBox QLabel {
                color: #f8fafc;
                font-size: 14px;
                padding: 10px;
            }
            QMessageBox QPushButton {
                background: #dc2626;
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
                min-width: 80px;
                font-weight: bold;
                border: none;
            }
            QMessageBox QPushButton:hover {
                background: #ef4444;
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
                background: #111827;
                color: #f8fafc;
                border-radius: 8px;
            }
            QMessageBox QLabel {
                color: #f8fafc;
                font-size: 14px;
                padding: 10px;
            }
            QMessageBox QPushButton {
                background: #059669;
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
                min-width: 80px;
                font-weight: bold;
                border: none;
            }
            QMessageBox QPushButton:hover {
                background: #10b981;
            }
        """)
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set dark application style
    app.setStyle("Fusion")
    app.setFont(QFont("Arial", 10))
    
    # Set dark palette for the entire application
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#0f172a"))
    palette.setColor(QPalette.WindowText, QColor("#f8fafc"))
    palette.setColor(QPalette.Base, QColor("#1f2937"))
    palette.setColor(QPalette.AlternateBase, QColor("#111827"))
    palette.setColor(QPalette.ToolTipBase, QColor("#1f2937"))
    palette.setColor(QPalette.ToolTipText, QColor("#f8fafc"))
    palette.setColor(QPalette.Text, QColor("#f8fafc"))
    palette.setColor(QPalette.Button, QColor("#374151"))
    palette.setColor(QPalette.ButtonText, QColor("#f8fafc"))
    palette.setColor(QPalette.BrightText, QColor("#ffffff"))
    palette.setColor(QPalette.Highlight, QColor("#4f46e5"))
    palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    app.setPalette(palette)
    
    # Create and show the window
    window = DarkQRCodeGeneratorApp()
    window.show()
    
    sys.exit(app.exec_())
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView  # Use QWebEngineView for better HTML rendering
from markdown2 import markdown

class ChatboxWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Chat display area
        self.chat_display = QWebEngineView(self)
        self.chat_display.setHtml("<html><body style='font-size:14pt;'></body></html>")  # Initialize with empty content
        layout.addWidget(self.chat_display)

        # Input area
        input_layout = QHBoxLayout()
        self.input_field = QTextEdit(self)  # Use QTextEdit for multi-line input
        self.input_field.setStyleSheet("font-size: 12pt;")
        self.input_field.setMaximumHeight(int(self.height() * 0.2))  # Convert to int for setMaximumHeight
        self.input_field.textChanged.connect(self.adjust_input_height)  # Adjust height dynamically
        input_layout.addWidget(self.input_field)

        self.send_button = QPushButton("Send", self)
        self.send_button.setStyleSheet("font-size: 12pt;")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        layout.addLayout(input_layout)

    def adjust_input_height(self):
        # Adjust the height of the input field dynamically based on content
        document_height = self.input_field.document().size().height()
        max_height = int(self.height() * 0.2)  # Convert to int for consistency
        self.input_field.setFixedHeight(int(min(document_height + 10, max_height)))  # Ensure height is an integer

    def send_message(self):
        user_message = self.input_field.toPlainText().strip()  # Use toPlainText for QTextEdit
        if user_message:
            self.display_message(user_message, "right")
            self.input_field.clear()
            self.adjust_input_height()  # Reset height after clearing
            self.receive_response(user_message)

    def display_message(self, message, alignment):
        # Render markdown to HTML
        html_message = markdown(message)
        if alignment == "right":
            formatted_message = (
                f'<div style="text-align:right; margin-bottom:10px;">'
                f'<div style="display:inline-block; background-color:#d1e7ff; color:black; '
                f'padding:10px; border-radius:10px; border:2px solid black; '
                f'max-width:75%; box-sizing:border-box; word-wrap:break-word;">{html_message}</div>'
                f'</div>'
            )
        else:
            formatted_message = (
                f'<div style="text-align:left; margin-bottom:10px;">'
                f'<div style="display:inline-block; background-color:#e6ffe6; color:green; '
                f'padding:10px; border-radius:10px; border:2px solid black; '
                f'max-width:75%; box-sizing:border-box; word-wrap:break-word;">{html_message}</div>'
                f'</div>'
            )
        
        # Append the new message to the existing content
        self.chat_display.page().runJavaScript(
            f"document.body.innerHTML += `{formatted_message}`;"
        )

    def receive_response(self, user_message):
        # Simulate a bot response (replace with actual logic)
        bot_response = f"{user_message}"
        self.display_message(bot_response, "left")
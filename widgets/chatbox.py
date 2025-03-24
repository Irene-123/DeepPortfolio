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
        input_layout = QVBoxLayout()  # Use QVBoxLayout to stack live preview and input field vertically

        # Live markdown preview
        self.live_preview = QWebEngineView(self)
        self.live_preview.setStyleSheet("border: 1px solid #ccc; background-color: #f9f9f9;")  # Add clarity
        self.live_preview.setHtml("<html><body style='font-size:12pt;'></body></html>")  # Initialize empty preview
        self.live_preview.setFixedHeight(50)  # Start with a small height
        input_layout.addWidget(self.live_preview)

        # Input field for markdown text
        self.input_field = QTextEdit(self)
        self.input_field.setStyleSheet("font-size: 12pt;")
        self.input_field.setMinimumHeight(50)
        self.input_field.setMaximumHeight(int(self.height() * 0.2))  # Ensure input field height does not exceed 20%
        self.input_field.setFixedHeight(50)
        self.input_field.textChanged.connect(self.update_live_preview)
        self.input_field.installEventFilter(self)
        input_layout.addWidget(self.input_field)

        # Send button
        self.send_button = QPushButton("Send", self)
        self.send_button.setStyleSheet("font-size: 12pt;")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        layout.addLayout(input_layout)

    def adjust_input_height(self):
        # Adjust the height of the input field and live preview dynamically based on content
        document_height = self.input_field.document().size().height()
        max_height = int(self.height() * 0.2)  # Ensure height does not exceed 20% of the chat screen
        min_height = 50  # Ensure the height does not go below this value
        new_height = int(min(max(document_height + 10, min_height), max_height))
        self.input_field.setFixedHeight(new_height)  # Ensure height is an integer
        self.live_preview.setFixedHeight(new_height)  # Match live preview height with input field height

    def update_live_preview(self):
        # Render the markdown text in the live preview
        markdown_text = self.input_field.toPlainText()
        markdown_text = markdown_text.replace("\t", "    ")  # Replace tabs with four spaces
        markdown_text = markdown_text.replace("\n", "  \n")  # Ensure single newlines are treated as Markdown line breaks
        html_content = markdown(markdown_text).replace("\n", "<br>").replace("`", "\\`")  # Convert newlines to <br> in HTML
        self.live_preview.setHtml(f"<html><body style='font-size:12pt;'>{html_content}</body></html>")
        self.adjust_input_height()

    def send_message(self):
        user_message = self.input_field.toPlainText().strip()  # Use toPlainText for QTextEdit
        if user_message:
            user_message = user_message.replace("\n", "  \n")  # Convert newlines to Markdown line breaks
            self.display_message(user_message, "right")
            self.input_field.clear()
            self.update_live_preview()  # Clear the live preview after sending
            self.receive_response(user_message)

    def display_message(self, message, alignment):
        # Render markdown to HTML
        html_message = markdown(message).replace("\n", "<br>").replace("`", "\\`")  # Convert newlines to <br>
        if alignment == "right":
            formatted_message = (
                f'<div style="text-align:right; margin-bottom:2px; line-height:1.0;">'  # Reduce margin and line-height
                f'<div style="display:inline-block; background-color:#d1e7ff; color:black; '
                f'padding:4px; border-radius:15px 15px 0 15px; border:2px solid black; '
                f'max-width:75%; box-sizing:border-box; word-wrap:break-word; line-height:1.0;">{html_message}</div>'
                f'</div>'
            )
        else:
            formatted_message = (
                f'<div style="text-align:left; margin-bottom:2px; line-height:1.0;">'  # Reduce margin and line-height
                f'<div style="display:inline-block; background-color:#e6ffe6; color:green; '
                f'padding:4px; border-radius:15px 15px 15px 0; border:2px solid black; '
                f'max-width:75%; box-sizing:border-box; word-wrap:break-word; line-height:1.0;">{html_message}</div>'
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

    def eventFilter(self, source, event):
        if source == self.input_field and event.type() == event.KeyPress:
            if event.key() == Qt.Key_Return:
                if event.modifiers() == Qt.ShiftModifier:  # Check if Shift is pressed
                    cursor = self.input_field.textCursor()
                    cursor.insertText("\n")  # Add a newline
                    return True
                elif not event.isAutoRepeat():
                    self.send_message()
                    return True
            elif event.key() == Qt.Key_Tab:  # Handle Tab key
                cursor = self.input_field.textCursor()
                cursor.insertText("    ")  # Insert four spaces for a tab
                event.accept()  # Explicitly accept the event to prevent further propagation
                return True
        return super().eventFilter(source, event)
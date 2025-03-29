from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt

class PriceBarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(50)
        self.setMinimumHeight(300)
        self.high_52_week = 0
        self.low_52_week = 0
        self.current_price = 0
        self.buy_average = 0
        self.trade_prices = []

    def set_prices(self, high_52_week, low_52_week, current_price, buy_average, trade_prices):
        self.high_52_week = high_52_week
        self.low_52_week = low_52_week
        self.current_price = current_price
        self.buy_average = buy_average
        self.trade_prices = trade_prices
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw background
        painter.fillRect(self.rect(), QColor(240, 240, 240))

        # Calculate scale
        bar_height = self.height()
        price_range = (self.high_52_week * 1.1) - (self.low_52_week * 0.9)
        if price_range == 0:
            return

        def price_to_y(price):
            return int(bar_height - ((price - (self.low_52_week * 0.9)) / price_range * bar_height))

        # Draw the rectangular bar with gradient
        bar_x = self.width() // 2
        bar_width = 60
        gradient = QColor(100, 149, 237)  # Slightly darker blue
        for y in range(bar_height):
            alpha = int(255 * (1 - y / bar_height))  # Darker as price increases
            gradient.setAlpha(alpha)
            painter.setPen(QPen(gradient))
            painter.drawLine(bar_x - bar_width // 2, y, bar_x + bar_width // 2, y)

        # Mark 52-week high and low with black lines and display values
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(bar_x - bar_width // 2, price_to_y(self.high_52_week), bar_x + bar_width // 2, price_to_y(self.high_52_week))
        painter.drawLine(bar_x - bar_width // 2, price_to_y(self.low_52_week), bar_x + bar_width // 2, price_to_y(self.low_52_week))
        painter.drawText(bar_x - bar_width - 40, price_to_y(self.high_52_week) + 5, f"{self.high_52_week}")
        painter.drawText(bar_x - bar_width - 40, price_to_y(self.low_52_week) + 5, f"{self.low_52_week}")

        # Mark current price with green line and display value
        painter.setPen(QPen(Qt.green, 2))
        painter.drawLine(bar_x - bar_width // 2, price_to_y(self.current_price), bar_x + bar_width // 2, price_to_y(self.current_price))
        painter.drawText(bar_x - bar_width - 40, price_to_y(self.current_price) + 5, f"{self.current_price}")

        # Mark buy average with blue line and display value
        painter.setPen(QPen(Qt.blue, 2))
        painter.drawLine(bar_x - bar_width // 2, price_to_y(self.buy_average), bar_x + bar_width // 2, price_to_y(self.buy_average))
        painter.drawText(bar_x - bar_width - 40, price_to_y(self.buy_average) + 5, f"{self.buy_average}")

        # Mark trade prices with small black dots
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(Qt.black)
        for trade_price in self.trade_prices:
            y = price_to_y(trade_price.price)
            painter.drawEllipse(bar_x - 3, y - 3, 6, 6)  # Small black dots for trade prices

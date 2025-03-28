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
        price_range = self.high_52_week - self.low_52_week
        if price_range == 0:
            return

        def price_to_y(price):
            return int(bar_height - ((price - self.low_52_week) / price_range * bar_height))  # Cast to int

        # Draw whiskers (lines for 52-week high and low)
        bar_x = self.width() // 2
        whisker_width = 20
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(bar_x - whisker_width // 2, price_to_y(self.high_52_week), bar_x + whisker_width // 2, price_to_y(self.high_52_week))
        painter.drawLine(bar_x, price_to_y(self.high_52_week), bar_x, price_to_y(self.low_52_week))
        painter.drawLine(bar_x - whisker_width // 2, price_to_y(self.low_52_week), bar_x + whisker_width // 2, price_to_y(self.low_52_week))

        # Draw box (range between buy average and current price)
        box_top = min(price_to_y(self.buy_average), price_to_y(self.current_price))
        box_bottom = max(price_to_y(self.buy_average), price_to_y(self.current_price))
        box_width = 40
        painter.setBrush(QColor(200, 200, 255))
        painter.drawRect(bar_x - box_width // 2, box_top, box_width, box_bottom - box_top)

        # Draw median line (current price)
        painter.setPen(QPen(Qt.blue, 3))  # Blue thick line for current price
        painter.drawLine(bar_x - box_width // 2, price_to_y(self.current_price), bar_x + box_width // 2, price_to_y(self.current_price))

        # Mark 52-week high and low
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(Qt.black)
        painter.drawEllipse(bar_x - 5, price_to_y(self.high_52_week) - 5, 10, 10)  # Black circle for 52-week high
        painter.drawEllipse(bar_x - 5, price_to_y(self.low_52_week) - 5, 10, 10)  # Black circle for 52-week low

        # Mark buy average
        painter.setPen(QPen(Qt.green, 2))
        painter.setBrush(Qt.green)
        painter.drawEllipse(bar_x - 5, price_to_y(self.buy_average) - 5, 10, 10)  # Green circle for buy average

        # Mark trade prices
        painter.setPen(QPen(Qt.red, 2))
        painter.setBrush(Qt.red)
        for trade_price in self.trade_prices:
            y = price_to_y(trade_price)
            painter.drawEllipse(bar_x - 5, y - 5, 10, 10)  # Red circle for trade prices

        # Add text for 52-week high, low, and current price
        painter.setPen(Qt.black)
        painter.drawText(self.width() - 40, price_to_y(self.high_52_week) - 5, f"{self.high_52_week}")
        painter.drawText(self.width() - 40, price_to_y(self.low_52_week) + 15, f"{self.low_52_week}")
        painter.setPen(Qt.blue)
        painter.drawText(self.width() - 40, price_to_y(self.current_price) - 5, f"{self.current_price}")

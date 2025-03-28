from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QBrush, QFont
from datetime import datetime

class TradeBookTable(QTableWidget):
    """
    A custom table widget to display the user's tradebook.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setColumnCount(7)  # Adjust based on Trade attributes
        self.setHorizontalHeaderLabels(["Date", "Symbol", "Quantity", "Price", "Type", "Investment", "Remarks"])
        self.setSortingEnabled(True)  # Enable sorting by columns

        # Set alternating row colors
        self.setAlternatingRowColors(True)
        self.setStyleSheet("alternate-background-color: #f9f9f9; background-color: #ffffff;")

        # Customize grid style
        self.setShowGrid(True)
        self.setGridStyle(Qt.SolidLine)

        # Customize header appearance
        header = self.horizontalHeader()
        header.setStyleSheet("QHeaderView::section { background-color: #4CAF50; color: white; font-weight: bold; }")
        header.setFont(QFont("Arial", 10, QFont.Bold))
        header.setDefaultAlignment(Qt.AlignCenter)

        # Set row height and column width
        self.verticalHeader().setDefaultSectionSize(30)
        self.horizontalHeader().setStretchLastSection(True)

        # Hide the vertical header (index)
        self.verticalHeader().setVisible(False)

    def populateTable(self, trades):
        """
        Populate the table with a list of Trade objects.

        :param trades: List of models.Trade objects
        """
        self.setRowCount(len(trades))
        for row, trade in enumerate(trades):
            # Assuming models.Trade has attributes: date, symbol, quantity, price, and typ
            date_item = QTableWidgetItem(trade.date.strftime("%Y-%m-%d"))
            date_item.setData(Qt.UserRole, trade.date)  # Store raw date for sorting
            symbol_item = QTableWidgetItem(trade.symbol)
            quantity_item = QTableWidgetItem(str(trade.quantity))
            price_item = QTableWidgetItem(f"{trade.price:.2f}")
            typ_item = QTableWidgetItem(trade.typ)
            if trade.typ == "buy":
                typ_item.setBackground(QBrush(QColor(144, 238, 144)))  # Light green
            elif trade.typ == "sell":
                typ_item.setBackground(QBrush(QColor(255, 182, 193)))  # Light red
            elif trade.typ == "bonus":
                typ_item.setBackground(QBrush(QColor(255, 255, 102)))  # Yellow
            investment_item = QTableWidgetItem(f"{trade.price * trade.quantity:.2f}")

            # Align numeric columns to the right
            quantity_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            investment_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            # Add items to the table
            self.setItem(row, 0, date_item)
            self.setItem(row, 1, symbol_item)
            self.setItem(row, 2, quantity_item)
            self.setItem(row, 3, price_item)
            self.setItem(row, 4, typ_item)
            self.setItem(row, 5, investment_item)
            self.setItem(row, 6, QTableWidgetItem(trade.remarks))

        # Sort by date (column 0) in ascending order
        self.sortItems(0, Qt.DescendingOrder)

from typing import List
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QLabel, QSplitter, QFormLayout, QTextEdit, QFrame, QGroupBox, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QBrush, QFont

from src.models.holding import Holding

class HoldingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout with QSplitter for adjustable widths
        main_layout = QVBoxLayout(self)
        splitter = QSplitter(Qt.Horizontal)

        # Left: Table for holdings
        self.holdings_table = QTableWidget()
        self.holdings_table.setColumnCount(6)  # Updated to 6 columns
        self.holdings_table.setHorizontalHeaderLabels([
            "Symbol", "Quantity", "Buy Average", "Current Position", "Investment", "Profit/Loss"
        ])
        self.holdings_table.cellClicked.connect(self.display_details)
        splitter.addWidget(self.holdings_table)

        # Customize table appearance
        self.holdings_table.setAlternatingRowColors(True)
        self.holdings_table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f9f9f9;
                border: 1px solid #dcdcdc;
            }
            QTableWidget::item {
                border-bottom: 1px solid #dcdcdc;
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #cce5ff;
                color: #000000;
            }
        """)
        self.holdings_table.setShowGrid(False)

        # Customize header appearance
        header = self.holdings_table.horizontalHeader()
        header.setStyleSheet("""
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                border: 1px solid #dcdcdc;
                padding: 5px;
            }
        """)
        header.setFont(QFont("Arial", 10, QFont.Bold))
        header.setDefaultAlignment(Qt.AlignCenter)

        # Set row height and column width
        self.holdings_table.verticalHeader().setDefaultSectionSize(35)
        self.holdings_table.horizontalHeader().setStretchLastSection(True)

        # Set column widths
        self.holdings_table.setColumnWidth(0, 120)  # Symbol
        self.holdings_table.setColumnWidth(1, 100)  # Quantity
        self.holdings_table.setColumnWidth(2, 150)  # Buy Average
        self.holdings_table.setColumnWidth(3, 180)  # Current Position
        self.holdings_table.setColumnWidth(4, 140)  # Investment
        self.holdings_table.setColumnWidth(5, 120)  # Profit/Loss

        # Hide the vertical header (index)
        self.holdings_table.verticalHeader().setVisible(False)

        # Right: Detailed description pane with a grid layout inside a group box
        self.details_group = QGroupBox("Holding Details")
        self.details_group.setStyleSheet("""
            QGroupBox {
                font: bold 12px;
                border: 2px solid #4CAF50;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
                color: #4CAF50;
            }
        """)

        # Create a vertical layout for the details group
        self.details_layout = QVBoxLayout()
        self.details_group.setLayout(self.details_layout)  # Explicitly set the layout

        # Top section: Symbol
        self.top_section = QVBoxLayout()

        # Symbol label (top, center-aligned)
        self.symbol_label = QLabel()
        self.symbol_label.setStyleSheet("""
            QLabel {
                font-size: 60px; /* Increased font size */
                font-weight: bold;
                color: #333;
            }
        """)
        self.top_section.addWidget(self.symbol_label, alignment=Qt.AlignCenter)  # Changed alignment to center

        # Details section (below the symbol)
        self.details_below_symbol = QGridLayout()
        self.details_below_symbol.setHorizontalSpacing(20)
        self.details_below_symbol.setVerticalSpacing(10)

        # Add placeholders for details (except description)
        self.details_widgets = {
            "Industry Type": QLabel(),
            "Sector Type": QLabel(),
            "Market Cap": QLabel(),
            "Risk-Free Return": QLabel(),
            "Index Returns": QLabel(),
            "Total Investment": QLabel()
        }
        for row, (label, widget) in enumerate(self.details_widgets.items()):
            label_widget = QLabel(f"{label}:")
            label_widget.setStyleSheet("font-weight: bold; color: #333;")
            self.details_below_symbol.addWidget(label_widget, row, 0, alignment=Qt.AlignRight)
            self.details_below_symbol.addWidget(widget, row, 1, alignment=Qt.AlignLeft)

        self.top_section.addLayout(self.details_below_symbol)

        # Profit section (right side)
        self.profit_section = QVBoxLayout()

        # Realized and Unrealized Profit (side by side)
        self.profit_row_layout = QHBoxLayout()

        # Realized Profit
        self.realized_profit_layout = QVBoxLayout()
        self.realized_profit_value = QLabel()
        self.realized_profit_label = QLabel("Realized Profit")
        self.realized_profit_value.setStyleSheet("""
            QLabel {
                font-size: 40px; /* Increased font size */
                font-weight: bold;
            }
        """)
        self.realized_profit_label.setStyleSheet("""
            QLabel {
                font-size: 12px; /* Label font size */
                color: #666;
            }
        """)
        self.realized_profit_layout.addWidget(self.realized_profit_value, alignment=Qt.AlignCenter)
        self.realized_profit_layout.addWidget(self.realized_profit_label, alignment=Qt.AlignCenter)

        # Unrealized Profit
        self.unrealized_profit_layout = QVBoxLayout()
        self.unrealized_profit_value = QLabel()
        self.unrealized_profit_label = QLabel("Unrealized Profit")
        self.unrealized_profit_value.setStyleSheet("""
            QLabel {
                font-size: 40px; /* Increased font size */
                font-weight: bold;
            }
        """)
        self.unrealized_profit_label.setStyleSheet("""
            QLabel {
                font-size: 12px; /* Label font size */
                color: #666;
            }
        """)
        self.unrealized_profit_layout.addWidget(self.unrealized_profit_value, alignment=Qt.AlignCenter)
        self.unrealized_profit_layout.addWidget(self.unrealized_profit_label, alignment=Qt.AlignCenter)

        # Add Realized and Unrealized Profit to the row layout
        self.profit_row_layout.addLayout(self.realized_profit_layout)
        self.profit_row_layout.addLayout(self.unrealized_profit_layout)

        # Invested Amount (below Realized and Unrealized Profit)
        self.invested_amount_layout = QVBoxLayout()
        self.invested_amount_value = QLabel()
        self.invested_amount_label = QLabel("Invested Amount")
        self.invested_amount_value.setStyleSheet("""
            QLabel {
                font-size: 40px; /* Increased font size */
                font-weight: bold;
            }
        """)
        self.invested_amount_label.setStyleSheet("""
            QLabel {
                font-size: 12px; /* Label font size */
                color: #666;
            }
        """)
        self.invested_amount_layout.addWidget(self.invested_amount_value, alignment=Qt.AlignCenter)
        self.invested_amount_layout.addWidget(self.invested_amount_label, alignment=Qt.AlignCenter)

        # Add the profit row and invested amount to the profit section
        self.profit_section.addLayout(self.profit_row_layout)
        self.profit_section.addLayout(self.invested_amount_layout)

        # Combine the symbol and profit sections
        self.symbol_and_profit_layout = QHBoxLayout()
        self.symbol_and_profit_layout.addLayout(self.top_section, stretch=1)
        self.symbol_and_profit_layout.addLayout(self.profit_section, stretch=1)
        self.details_layout.addLayout(self.symbol_and_profit_layout)

        splitter.addWidget(self.details_group)

        # Set initial splitter sizes (40% for table, 60% for description)
        splitter.setSizes([450, 550])  # Adjust sizes explicitly (e.g., 40% and 60% of 1000px)

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

    def set_holdings(self, holdings: List[Holding]):
        """
        Populate the table with holdings data.
        :param holdings: List of tuples [(symbol, quantity, buy_average, current_position, investment, profit_loss), ...]
        """
        self.holdings_table.setRowCount(len(holdings))
        for row, holding in enumerate(holdings):
            quantity_item = QTableWidgetItem(str(abs(holding.quantity)))
            buy_average_item = QTableWidgetItem(str(holding.buy_average))
            current_position_item = QTableWidgetItem(str("BUY" if holding.quantity > 0 else "SELL"))
            investment_item = QTableWidgetItem(str(holding.investment))
            profit_loss_item = QTableWidgetItem(str(holding.unrealized_profit))

            # Align numeric columns to the right
            quantity_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            buy_average_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            current_position_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            investment_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            profit_loss_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            # Apply conditional formatting for profit/loss
            if holding.unrealized_profit == "N/A":
                profit_loss_item.setForeground(QBrush(QColor(255, 255, 0)))  # Yellow for data not available
            elif float(holding.unrealized_profit) > 0:
                profit_loss_item.setForeground(QBrush(QColor(0, 128, 0)))  # Green for profit
            else:
                profit_loss_item.setForeground(QBrush(QColor(255, 0, 0)))  # Red for loss

            # Add items to the table
            self.holdings_table.setItem(row, 0, QTableWidgetItem(holding.symbol))
            self.holdings_table.setItem(row, 1, quantity_item)
            self.holdings_table.setItem(row, 2, buy_average_item)
            self.holdings_table.setItem(row, 3, current_position_item)
            self.holdings_table.setItem(row, 4, investment_item)
            self.holdings_table.setItem(row, 5, profit_loss_item)

        # Automatically select the first row and display its details
        if len(holdings) > 0:
            self.holdings_table.selectRow(0)
            self.display_details(0, 0)

    def display_details(self, row, column):
        """
        Display details of the selected holding in the right pane.
        :param row: Row index of the selected holding.
        :param column: Column index of the selected holding.
        """
        symbol = self.holdings_table.item(row, 0).text()
        quantity = self.holdings_table.item(row, 1).text()
        buy_average = self.holdings_table.item(row, 2).text()
        current_position = self.holdings_table.item(row, 3).text()
        investment = self.holdings_table.item(row, 4).text()
        profit_loss = self.holdings_table.item(row, 5).text()

        # Fetch additional details (mocked for now, replace with actual data source)
        details = {
            "Symbol": symbol,
            "Industry Type": "Technology",
            "Sector Type": "Software",
            "Market Cap": "Large Cap",
            "Realized Profit": "$500",
            "Unrealized Profit": "$200",
            "Risk-Free Return": "3%",
            "Index Returns": "8%",
            "Total Investment": investment,
            "Description": f"{symbol} is a leading company in the technology sector, specializing in software solutions."
        }

        # Update the symbol label
        self.symbol_label.setText(details["Symbol"])

        # Update the profit values with conditional coloring
        realized_profit = float(details["Realized Profit"].replace("$", ""))
        unrealized_profit = float(details["Unrealized Profit"].replace("$", ""))
        invested_amount = float(details["Total Investment"].replace("$", ""))

        self.realized_profit_value.setText(details["Realized Profit"])
        self.realized_profit_value.setStyleSheet(f"""
            QLabel {{
                font-size: 40px;
                font-weight: bold;
                color: {"green" if realized_profit > 0 else "red"};
            }}
        """)

        self.unrealized_profit_value.setText(details["Unrealized Profit"])
        self.unrealized_profit_value.setStyleSheet(f"""
            QLabel {{
                font-size: 40px;
                font-weight: bold;
                color: {"green" if unrealized_profit > 0 else "red"};
            }}
        """)

        self.invested_amount_value.setText(f"${invested_amount:,.2f}")
        self.invested_amount_value.setStyleSheet("""
            QLabel {
                font-size: 40px;
                font-weight: bold;
                color: #333;
            }
        """)

        # Update other details
        for key, value in details.items():
            if key in self.details_widgets:
                self.details_widgets[key].setText(value)

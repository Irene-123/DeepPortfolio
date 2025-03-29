from typing import List
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QLabel, QSplitter, QFormLayout, QTextEdit, QFrame, QGroupBox, QGridLayout, QHeaderView, QStyledItemDelegate
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QBrush, QFont, QPainter

from src.models.holding import Holding

class ProfitLossDelegate(QStyledItemDelegate):
    """
    Custom delegate to handle coloring of profit/loss cells.
    """
    def paint(self, painter, option, index):
        value = index.data()  # Get the cell value
        if value is not None and isinstance(value, str):
            try:
                numeric_value = float(value)
                if numeric_value > 0:
                    option.palette.setColor(option.palette.Text, QColor(0, 128, 0))  # Dark green
                elif numeric_value < 0:
                    option.palette.setColor(option.palette.Text, QColor(255, 0, 0))  # Red
            except ValueError:
                pass  # Ignore non-numeric values
        super().paint(painter, option, index)

class HoldingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout with QSplitter for adjustable widths
        main_layout = QVBoxLayout(self)
        splitter = QSplitter(Qt.Horizontal)

        # Left: Two tables for holdings (current and past)
        left_pane = QVBoxLayout()

        # Label for Current Holdings Table
        current_holdings_label = QLabel("Current Holdings")
        current_holdings_label.setStyleSheet("""
            QLabel {
                font-size: 22px; /* Increased font size */
                font-weight: bold;
                color: #4CAF50;
                margin-bottom: 5px;
            }
        """)
        left_pane.addWidget(current_holdings_label)

        # Current Holdings Table
        self.current_holdings_table = QTableWidget()
        self.current_holdings_table.setColumnCount(5)  # Updated to 5 columns
        self.current_holdings_table.setHorizontalHeaderLabels([
            "Symbol", "Quantity", "Price Average", "Invested Value", "Unrealized Profit"
        ])
        self.current_holdings_table.cellClicked.connect(lambda row, col: self.display_details(row, col, "current"))
        self.current_holdings_table.setSortingEnabled(True)
        self._customize_table(self.current_holdings_table)
        left_pane.addWidget(self.current_holdings_table)

        # Label for Past Holdings Table
        past_holdings_label = QLabel("Past Holdings")
        past_holdings_label.setStyleSheet("""
            QLabel {
                font-size: 22px; /* Increased font size */
                font-weight: bold;
                color: #4CAF50;
                margin-top: 10px;
                margin-bottom: 5px;
            }
        """)
        left_pane.addWidget(past_holdings_label)

        # Past Holdings Table
        self.past_holdings_table = QTableWidget()
        self.past_holdings_table.setColumnCount(5)  # Updated to 5 columns
        self.past_holdings_table.setHorizontalHeaderLabels([
            "Symbol", "Dividend Earned", "Profitable Trades", "Loss Trades", "Realized Profit"
        ])
        self.past_holdings_table.cellClicked.connect(lambda row, col: self.display_details(row, col, "past"))
        self.past_holdings_table.setSortingEnabled(True)
        self._customize_table(self.past_holdings_table)
        left_pane.addWidget(self.past_holdings_table)

        # Add left pane to splitter
        left_widget = QWidget()
        left_widget.setLayout(left_pane)
        splitter.addWidget(left_widget)

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

        # Set initial splitter sizes (50% for left, 50% for right)
        splitter.setSizes([500, 500])
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

    def _customize_table(self, table):
        """
        Apply common customizations to the tables.
        """
        table.setAlternatingRowColors(True)
        table.setStyleSheet("""
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
                background-color: #cce5ff; /* Highlight entire row */
                color: #000000;
            }
        """)
        table.setSelectionBehavior(table.SelectRows)  # Highlight entire row on selection
        table.setShowGrid(True)
        table.setGridStyle(Qt.SolidLine)
        header = table.horizontalHeader()
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
        header.setSectionResizeMode(QHeaderView.Stretch)  # Make all columns expand equally
        table.verticalHeader().setDefaultSectionSize(35)
        table.verticalHeader().setVisible(False)

        # Apply delegate to the correct columns
        if table == self.current_holdings_table:
            table.setItemDelegateForColumn(4, ProfitLossDelegate())  # Unrealized Profit column
        elif table == self.past_holdings_table:
            table.setItemDelegateForColumn(4, ProfitLossDelegate())  # Realized Profit column

    def set_holdings(self, current_holdings: List[Holding], past_holdings: List[Holding]):
        """
        Populate the tables with current and past holdings data.
        :param current_holdings: List of current holdings.
        :param past_holdings: List of past holdings.
        """
        self._populate_table(self.current_holdings_table, current_holdings, "current")
        self._populate_table(self.past_holdings_table, past_holdings, "past")

        # Automatically select the first row in the current holdings table
        if len(current_holdings) > 0:
            self.current_holdings_table.selectRow(0)
            self.display_details(0, 0, "current")

    def _populate_table(self, table, holdings: List[Holding], table_type: str):
        """
        Populate a given table with holdings data.
        """
        table.setRowCount(len(holdings))
        for row, holding in enumerate(holdings):
            if table_type == "current":
                # Populate Current Holdings Table
                table.setItem(row, 0, QTableWidgetItem(holding.symbol))
                table.setItem(row, 1, QTableWidgetItem(str(abs(holding.quantity))))
                table.setItem(row, 2, QTableWidgetItem(str(round(holding.buy_average, 2))))
                table.setItem(row, 3, QTableWidgetItem(str(round(holding.investment, 2))))

                # Unrealized Profit with numeric data for sorting and text color
                unrealized_profit_item = QTableWidgetItem()
                unrealized_profit_item.setData(Qt.DisplayRole, round(holding.unrealized_profit, 2))
                color = QColor(0, 128, 0) if holding.unrealized_profit >= 0 else QColor(255, 0, 0)
                unrealized_profit_item.setForeground(QBrush(color))
                table.setItem(row, 4, unrealized_profit_item)

            elif table_type == "past":
                # Populate Past Holdings Table
                table.setItem(row, 0, QTableWidgetItem(holding.symbol))
                table.setItem(row, 1, QTableWidgetItem(str(round(holding.dividend_income, 2))))
                table.setItem(row, 2, QTableWidgetItem(str(sum(1 for profit in holding.realized_profit_history if profit > 0))))  # Fixed
                table.setItem(row, 3, QTableWidgetItem(str(sum(1 for profit in holding.realized_profit_history if profit <= 0))))  # Fixed

                # Realized Profit with numeric data for sorting and text color
                realized_profit_item = QTableWidgetItem()
                realized_profit_item.setData(Qt.DisplayRole, round(holding.realized_profit, 2))
                color = QColor(0, 128, 0) if holding.realized_profit >= 0 else QColor(255, 0, 0)
                realized_profit_item.setForeground(QBrush(color))
                table.setItem(row, 4, realized_profit_item)

    def display_details(self, row, column, table_type):
        """
        Display details of the selected holding in the right pane.
        :param row: Row index of the selected holding.
        :param column: Column index of the selected holding.
        :param table_type: Type of table ("current" or "past").
        """
        table = self.current_holdings_table if table_type == "current" else self.past_holdings_table
        symbol = table.item(row, 0).text()
        quantity = table.item(row, 1).text()
        buy_average = table.item(row, 2).text()
        current_position = table.item(row, 3).text()
        investment = table.item(row, 4).text()

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

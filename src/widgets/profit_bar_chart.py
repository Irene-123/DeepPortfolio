from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis, QLineSeries
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt

class ProfitBarChart(QWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.chart = QChart()
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.chart_view)
        self.setLayout(layout)

        self.update_chart()

    def update_chart(self):
        """
        Update the chart with the current data.
        """
        self.chart.removeAllSeries()  # Clear existing series

        # Remove existing axes
        for axis in self.chart.axes():
            self.chart.removeAxis(axis)

        # Create the bar series
        series = QBarSeries()
        positive_bar_set = QBarSet("Positive Profit")
        negative_bar_set = QBarSet("Negative Profit")
        categories = []

        for dt, value in self.data:
            categories.append(dt.strftime("%Y-%m-%d"))
            if value > 0:
                positive_bar_set.append(value)
                negative_bar_set.append(0)  # Add 0 for alignment
            else:
                positive_bar_set.append(0)  # Add 0 for alignment
                negative_bar_set.append(value)

        # Set colors for the bar sets
        positive_bar_set.setColor(QColor(144, 238, 144))  # Light green
        negative_bar_set.setColor(QColor(255, 182, 193))  # Light red

        # Add bar sets to the series
        series.append(positive_bar_set)
        series.append(negative_bar_set)
        self.chart.addSeries(series)

        # Update axes
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        self.chart.setAxisX(axisX, series)

        axisY = QValueAxis()
        axisY.setTitleText("Profit")
        self.chart.setAxisY(axisY, series)

        # Draw a thick black line at 0 for reference using QLineSeries
        zero_line = QLineSeries()
        zero_line.append(0, 0)  # Start point
        zero_line.append(len(categories) - 1, 0)  # End point

        # Configure the pen for the line
        pen = QPen(QColor(0, 0, 0))  # Black color
        pen.setWidth(2)  # Thick line
        zero_line.setPen(pen)

        self.chart.addSeries(zero_line)
        zero_line.attachAxis(axisX)
        zero_line.attachAxis(axisY)

        # Update chart properties
        self.chart.setTitle("Profit Bar Chart")
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

    def update_data(self, data):
        """
        Update the chart's data and refresh the view.
        :param data: List of tuples (datetime, value) representing the new data.
        """
        self.data = data
        self.update_chart()  # Refresh the chart with new data

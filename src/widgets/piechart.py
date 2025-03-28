from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QCursor, QPainter

class PieChartWidget(QWidget):
    def __init__(self, labels, sizes, parent=None):
        super().__init__(parent)
        self.labels = labels
        self.sizes = sizes
        self.explode = [0] * len(labels)  # Initialize explode values for all slices

        # Create layout and canvas
        layout = QVBoxLayout(self)  
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Add hover label
        self.hover_label = QLabel("", self)
        self.hover_label.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc; padding: 5px; font-size: 18px;")
        self.hover_label.setVisible(False)

        # Draw the pie chart
        self.ax = self.figure.add_subplot(111)
        self.wedges, _ = self.ax.pie(
            self.sizes, labels=self.labels, autopct=None, startangle=90, explode=self.explode,
            wedgeprops=dict(width=0.4), textprops={'fontsize': 12}
        )
        self.ax.axis('equal')  # Ensure the pie chart is circular
        total = sum(self.sizes)
        self.ax.text(0, 0, f"{total}", ha='center', va='center', fontsize=16, weight='bold')

        # Connect hover event
        self.canvas.mpl_connect("motion_notify_event", self.on_hover)

    def on_hover(self, event):
        if event.inaxes == self.ax:
            for i, wedge in enumerate(self.wedges):
                if wedge.contains_point([event.x, event.y]):
                    percentage = (self.sizes[i] / sum(self.sizes)) * 100
                    self.hover_label.setText(f"{self.labels[i]}: {percentage:.2f}%")
                    self.hover_label.adjustSize()
                    cursor_pos = self.mapFromGlobal(QCursor.pos())
                    self.hover_label.move(cursor_pos.x() + 10, cursor_pos.y() + 10)
                    self.hover_label.setVisible(True)

                    self.explode = [0] * len(self.wedges)
                    self.explode[i] = 0.1

                    # Update center text with the actual count
                    self.update_center_text(self.sizes[i])
                    self.redraw_chart()
                    return

        self.hover_label.setVisible(False)
        self.explode = [0] * len(self.wedges)

        # Update center text with the total count
        self.update_center_text(sum(self.sizes))
        self.redraw_chart()

    def update_center_text(self, value):
        """Update the center text of the pie chart."""
        self.ax.text(0, 0, f"{value}", ha='center', va='center', fontsize=16, weight='bold')

    def redraw_chart(self):
        self.ax.clear()
        self.wedges, _ = self.ax.pie(
            self.sizes, labels=self.labels, autopct=None, startangle=90, explode=self.explode,
            wedgeprops=dict(width=0.4), textprops={'fontsize': 12}
        )
        self.ax.axis('equal')
        # Redraw the center text
        current_value = sum(self.sizes) if all(e == 0 for e in self.explode) else self.sizes[self.explode.index(0.1)]
        self.ax.text(0, 0, f"{current_value}", ha='center', va='center', fontsize=16, weight='bold')
        self.canvas.draw_idle()

    def paintEvent(self, event):
        painter = QPainter(self)
        # ...existing code for painting the pie chart...
"""
Author: Raul Granados
Company: Swipall
Description: Window that displays a bar chart of students per carrier.
"""
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class ChartWindow(QMainWindow):
    """
    Window that displays a bar chart of students per carrier.
    Includes labels above each bar.
    """

    def __init__(self, data_dict: dict[str, int], parent=None):
        super().__init__(parent)
        self.setWindowTitle("Students per Carrier")

        central = QWidget()
        layout = QVBoxLayout()
        central.setLayout(layout)
        self.setCentralWidget(central)

        # Matplotlib Figure
        fig = Figure(figsize=(6, 4))
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

        ax = fig.add_subplot(111)

        # Data
        labels = list(data_dict.keys())
        values = list(data_dict.values())

        # Plot
        bars = ax.bar(labels, values)

        ax.set_title("Students per Carrier")
        ax.set_ylabel("Number of Students")
        ax.set_xlabel("Carrier")

        # Add value labels above each bar
        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f"{height}",  # text to display
                xy=(bar.get_x() + bar.get_width() / 2, height),  # bar center
                xytext=(0, 5),  # 5px above bar
                textcoords="offset points",
                ha='center', va='bottom',
                fontsize=10,
                fontweight='bold'
            )

        # Fit layout
        fig.tight_layout()
        canvas.draw()

from PyQt6.QtWidgets import QDialog, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class PieChartWindow(QDialog):
    """
    Generic pie chart window for showing proportions.
    """

    def __init__(self, data: dict, parent=None, title="Pie Chart"):
        super().__init__(parent)
        self.setWindowTitle(title)

        layout = QVBoxLayout(self)

        fig = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(fig)
        layout.addWidget(self.canvas)

        ax = fig.add_subplot(111)

        labels = list(data.keys())
        values = list(data.values())

        wedges, texts, autotexts = ax.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=140
        )

        ax.axis("equal")
        ax.set_title(title)

        self.canvas.draw()

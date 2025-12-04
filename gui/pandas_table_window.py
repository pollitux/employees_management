from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel


class PandasTableWindow(QDialog):
    """Displays a Pandas DataFrame inside a QTableWidget."""

    def __init__(self, df, title="Analatica", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(800, 600)

        layout = QVBoxLayout(self)

        label = QLabel(title)
        layout.addWidget(label)

        table = QTableWidget()
        layout.addWidget(table)

        table.setColumnCount(len(df.columns))
        table.setHorizontalHeaderLabels(df.columns)

        for _, row in df.iterrows():
            row_idx = table.rowCount()
            table.insertRow(row_idx)

            for col_idx, value in enumerate(row):
                table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

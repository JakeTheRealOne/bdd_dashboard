from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

def create_center_bold_title(title):
        """
        Create a QLabel with a bold font and center alignment.

        Args:
            title (str): The title text to be displayed.

        Returns:
             QLabel: A QLabel object with the specified title, bold font, and center alignment.
        """

        title_label = QLabel(title)
        bold_font = title_label.font()
        bold_font.setBold(True)
        bold_font.setPointSize(20)
        title_label.setFont(bold_font)
        title_label.setAlignment(Qt.AlignCenter)
        return title_label
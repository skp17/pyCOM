
# Standard libraries
from enum import Enum

# Third-party modules
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication


class Theme(Enum):
    Dark = 0
    Light = 1

Stylesheet = {
    Theme.Light: "",
    Theme.Dark: ":/dark/stylesheet.qss"
}

def apply_theme(theme: Theme):
    """
    Toggle the stylesheet to use the desired path in the Qt resource
    system (prefixed by `:/`) or generically (a path to a file on
    system).

    :path: A full path to a resource or file on system
    """

    # Get the QApplication instance, or crash if not set
    app = QApplication.instance()
    if app is None:
        raise RuntimeError("No Qt Application found.")

    path = Stylesheet.get(theme, "")
    file = QFile(path)
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())

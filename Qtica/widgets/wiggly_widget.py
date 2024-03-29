from PySide6.QtCore import QBasicTimer, Property
from PySide6.QtGui import QColor, QFontMetrics, QPainter, QPalette
from PySide6.QtWidgets import QWidget

from ..enums.events import EventTypeVar
from ..enums.signals import SignalTypeVar
from ..core.base import WidgetBase


class _WigglyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._step = 0
        self._text = ""

        self.setBackgroundRole(QPalette.ColorRole.Midlight)
        # self.setAutoFillBackground(False)

        new_font = self.font()
        new_font.setPointSize(new_font.pointSize() + 20)

        self.setFont(new_font)
        self._timer = QBasicTimer()

    def isRunning(self):
        return self._timer.isActive()

    def setRunning(self, r: bool):
        if r == self.isRunning():
            return
        if r:
            self._timer.start(60, self)
        else:
            self._timer.stop()

    def paintEvent(self, event):
        if not self._text:
            return

        sineTable = [0, 38, 71, 92, 100, 92, 71, 38, 0, -38, -71, -92, -100,
                     -92, -71, -38]

        metrics = QFontMetrics(self.font())
        x = (self.width() - metrics.horizontalAdvance(self.text)) / 2
        y = (self.height() + metrics.ascent() - metrics.descent()) / 2
        color = QColor()

        with QPainter(self) as painter:
            for i in range(len(self.text)):
                index = (self._step + i) % 16
                color.setHsv((15 - index) * 16, 255, 191)
                painter.setPen(color)
                dy = (sineTable[index] * metrics.height()) / 400
                c = self._text[i]
                painter.drawText(x, y - dy, str(c))
                x += metrics.horizontalAdvance(c)

    def timerEvent(self, event):
        if event.timerId() == self._timer.timerId():
            self._step += 1
            self.update()
        else:
            QWidget.timerEvent(event)

    def text(self):
        return self._text

    def setText(self, text):
        self._text = text
        self.update()

    running = Property(bool, isRunning, setRunning)
    text = Property(str, text, setText)


class WigglyWidget(WidgetBase, _WigglyWidget):
    def __init__(self, 
                 uid: str = None, 
                 signals: SignalTypeVar = None, 
                 events: EventTypeVar = None,
                 text: str = None,
                 running: bool = True,
                 **kwargs):
        _WigglyWidget.__init__(self)
        super().__init__(uid, signals, events, **kwargs)

        if text is not None:
            self.setText(text)

        if running is not None:
            self.setRunning(running)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QPainter
from PySide6.QtWidgets import QFrame, QGraphicsProxyWidget, QGraphicsScene, QGraphicsView, QWidget


class _GraphicsView(QGraphicsView):
    def __init__(self, child: QWidget):
        QGraphicsView.__init__(self)

        self._graphics_scene = QGraphicsScene(self)

        self.setScene(self._graphics_scene)

        self.setBackgroundBrush(Qt.GlobalColor.transparent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setFrameShadow(QFrame.Shadow.Raised)

        self.setBackgroundRole(QPalette.ColorRole.NoRole)
        self.setStyleSheet("background: transparent")
        self.setContentsMargins(0, 0, 0, 0)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setInteractive(True)
        self.setUpdatesEnabled(True)

        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.SmartViewportUpdate)

        self.setRenderHints(
            QPainter.RenderHint.Antialiasing
            | QPainter.RenderHint.TextAntialiasing
            | QPainter.RenderHint.SmoothPixmapTransform
        )

        self._proxy = self.scene().addWidget(child)
        self._proxy.setTransformOriginPoint(self._proxy.boundingRect().center())
        self._proxy.setContentsMargins(0, 0, 0, 0)

        self.centerOn(self.sceneRect().center())

    @property
    def graphics_scene(self):
        return self._graphics_scene

    @property
    def proxy(self) -> QGraphicsProxyWidget:
        return self._proxy

    def update_size(self):
        self.fitInView(self._proxy.graphicsItem(),
                       Qt.AspectRatioMode.KeepAspectRatio)

    def resizeEvent(self, event):
        self.fitInView(self._proxy.graphicsItem(),
                       Qt.AspectRatioMode.KeepAspectRatio)
        super().resizeEvent(event)



from ..core.base import WidgetBase
from ..enums.events import EventTypeVar
from ..enums.signals import SignalTypeVar


class GraphicsView(WidgetBase, _GraphicsView):
    def __init__(self, 
                 child: QWidget,
                 uid: str = None, 
                 signals: SignalTypeVar = None, 
                 events: EventTypeVar = None, 
                 qss: str | dict = None, 
                 attrs: list[Qt.WidgetAttribute] | dict[Qt.WidgetAttribute, bool] = None, 
                 flags: list[Qt.WindowType] | dict[Qt.WindowType, bool] = None,
                 **kwargs):
        _GraphicsView.__init__(self, child)
        super().__init__(uid, signals, events, qss, attrs, flags, **kwargs)
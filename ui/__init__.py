import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from MainWindow import MainWindow, MainWindowInitializer

class FullscreenManager:

    def __init__(self, monitorNumber = 1, keyval = Gdk.KEY_F11):
        self.monitorNumber = monitorNumber
        self.keyval = keyval
        self.fullscreenEnabled = False
        self.windows = []
        self.positionBeforeFullscreen = {}

    def handleWindow(self, window):
        window.connect("key-release-event", self._onKeyRelease)
        self._applyStateToWindow(window)
        self.windows.append(window)

    def toggleAll(self):
        self.fullscreenEnabled = not self.fullscreenEnabled
        for window in self.windows:
            self._applyStateToWindow(window)

    def _onKeyRelease(self, widget, event, data = None):
        if event.keyval == self.keyval:
            self.toggleAll()

    def _applyStateToWindow(self, window):
        if self.fullscreenEnabled:
            self.positionBeforeFullscreen[window] = window.get_position()
            window.fullscreen_on_monitor(window.get_screen(), 1)
        else:
            window.unfullscreen()
            if window in self.positionBeforeFullscreen:
                window.move(*self.positionBeforeFullscreen[window])

if __name__ == "__main__":
    fullscreenManager =  FullscreenManager()

    win = MainWindow()
    initer = MainWindowInitializer(win)
    initer.initFromFile("test.yaml")

    win.connect("destroy", Gtk.main_quit)
    win.show_all()

    fullscreenManager.handleWindow(win)

    Gtk.main()
import tkinter


class WindowChannelConfig():

    def __init__(self, system):
        self._root = tkinter.Toplevel()
        self._root.grab_set()
        self._system = system
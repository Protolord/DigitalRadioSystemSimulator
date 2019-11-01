import tkinter


class WindowRadioConfig():

    def __init__(self, system):
        self._root = tkinter.Toplevel()
        self._root.grab_set()
        self._system = system

    def apply(self):
        return None

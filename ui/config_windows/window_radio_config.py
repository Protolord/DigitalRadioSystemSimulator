import tkinter
import core.config.radio_config as config


class WindowRadioConfig():

    def __init__(self):
        self.root = tkinter.Toplevel()
        self.root.grab_set()

    def apply(self):
        # TO DO: Retrieved settings in window to create RadioConfig
        cfg = config.RadioConfig()
        return cfg
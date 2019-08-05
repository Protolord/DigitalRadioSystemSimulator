import tkinter
import core.config.system_config as config


class WindowSystemConfig():

    def __init__(self):
        self.root = tkinter.Toplevel()
        self.root.grab_set()

    def apply(self):
        # TO DO: Retrieved settings in window to create SystemConfig
        cfg = config.SystemConfig()
        return cfg
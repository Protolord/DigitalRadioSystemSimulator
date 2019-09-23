import tkinter
import core.config.system_config as config
import core.utils.utils as utils


FADE_TIMEOUT = 40
FADE_COLOR_DELTA = 10
INITIAL_FADE_DELAY = 600
WINDOW_COLOR = 240

class WindowSystemConfig():

    def __init__(self, current_config):
        self.root = tkinter.Toplevel()
        self.root.title("System Configuration")
        self.root['background'] = '#%02x%02x%02x' % (WINDOW_COLOR, WINDOW_COLOR, WINDOW_COLOR)
        self.root.grab_set()
        self.cfg = current_config
        self.msg_color = 0
        self.is_fading = False
        # widgets
        self.label_sampling_rate = tkinter.Label(self.root, text="Sampling Rate")
        self.label_sim_duration = tkinter.Label(self.root, text="Simulation Duration")
        self.label_msg = tkinter.Label(self.root, text="")
        self.entry_sampling_rate = tkinter.Entry(self.root, width=25, bd=3)
        self.entry_sim_duration = tkinter.Entry(self.root, width=25, bd=3)
        self.button_apply = tkinter.Button(self.root, text="Apply", width=35, bd=4, command=self.apply)
        self.entry_sampling_rate.insert(0, str(self.cfg.sampling_rate))
        self.entry_sim_duration.insert(0, str(self.cfg.sim_duration))
        self.entry_sampling_rate.focus()
        self.root.bind('<Return>', self.apply)
        self.root.bind('<Escape>', self.close)
        # grids
        self.label_sampling_rate.grid(row=0, column=0, sticky=tkinter.E, padx=(10, 0))
        self.entry_sampling_rate.grid(row=0, column=1, padx=(0, 10))
        self.label_sim_duration.grid(row=1, column=0, sticky=tkinter.E, padx=(10, 0))
        self.entry_sim_duration.grid(row=1, column=1, padx=(0, 10))
        self.button_apply.grid(row=2, columnspan=2, pady=(4, 8))
        self.label_msg.grid(row=3, columnspan=2, sticky=tkinter.W, pady=(2, 0))
        self.label_msg.grid_remove()

    def reset_msg(self, text):
        self.msg_color = 0
        self.label_msg.grid()
        self.label_msg['foreground'] = '#%02x%02x%02x' % (self.msg_color, self.msg_color, self.msg_color)
        self.label_msg['text'] = text
        if not self.is_fading:
            self.label_msg.after(INITIAL_FADE_DELAY, self.fade_msg)
        self.is_fading = True

    def fade_msg(self):
        if self.msg_color > WINDOW_COLOR:
            self.label_msg.grid_remove()
            self.is_fading = False
        else:
            self.msg_color = self.msg_color + FADE_COLOR_DELTA
            self.label_msg['foreground'] = '#%02x%02x%02x' % (self.msg_color, self.msg_color, self.msg_color)
            self.label_msg.after(FADE_TIMEOUT, self.fade_msg)

    def apply(self, event=None):
        if not utils.check_input_validity(self.entry_sampling_rate.get(), (1, 1e10), 'int'):
            self.reset_msg("Invalid Sampling Rate")
            return
        if not utils.check_input_validity(self.entry_sim_duration.get(), (1, 100), 'float'):
            self.reset_msg("Invalid Simulation Duration")
            return
        self.cfg.sampling_rate = int(self.entry_sampling_rate.get())
        self.cfg.sim_duration = float(self.entry_sim_duration.get())
        self.close()

    def close(self, event=None):
        self.root.destroy()
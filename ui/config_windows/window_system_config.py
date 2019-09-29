import tkinter
import core.utils.utils as utils


FADE_TIMEOUT = 40
FADE_COLOR_DELTA = 10
INITIAL_FADE_DELAY = 600
WINDOW_COLOR = 240

class WindowSystemConfig():

    def __init__(self, system):
        self._root = tkinter.Toplevel()
        self._root.title('System Configuration')
        self._root['background'] = '#%02x%02x%02x' % (WINDOW_COLOR, WINDOW_COLOR, WINDOW_COLOR)
        self._root.grab_set()
        self._system = system
        self._msg_color = 0
        self._is_fading = False
        # widgets
        label_sampling_rate = tkinter.Label(self._root, text='Sampling Rate')
        label_sim_duration = tkinter.Label(self._root, text='Simulation Duration')
        button_apply = tkinter.Button(self._root, text='Apply', width=35, bd=4, command=self.apply)
        system_config = self._system.config['system']
        self._label_msg = tkinter.Label(self._root, text='')
        self._entry_sampling_rate = tkinter.Entry(self._root, width=25, bd=3)
        self._entry_sim_duration = tkinter.Entry(self._root, width=25, bd=3)
        self._entry_sampling_rate.insert(0, system_config['sampling rate'])
        self._entry_sim_duration.insert(0, system_config['sim duration'])
        self._entry_sampling_rate.focus()
        self._root.bind('<Return>', self.apply)
        self._root.bind('<Escape>', self.close)
        # grids
        label_sampling_rate.grid(row=0, column=0, sticky=tkinter.E, padx=(10, 0))
        label_sim_duration.grid(row=1, column=0, sticky=tkinter.E, padx=(10, 0))
        self._entry_sampling_rate.grid(row=0, column=1, padx=(0, 10))
        self._entry_sim_duration.grid(row=1, column=1, padx=(0, 10))
        button_apply.grid(row=2, columnspan=2, pady=(4, 8))
        self._label_msg.grid(row=3, columnspan=2, sticky=tkinter.W, pady=(2, 0))
        self._label_msg.grid_remove()

    def reset_msg(self, text):
        self._msg_color = 0
        self._label_msg.grid()
        self._label_msg['fg'] = f'#{self._msg_color:02x}{self._msg_color:02x}{self._msg_color:02x}'
        self._label_msg['text'] = text
        if not self._is_fading:
            self._label_msg.after(INITIAL_FADE_DELAY, self.fade_msg)
        self._is_fading = True

    def fade_msg(self):
        if self._msg_color > WINDOW_COLOR:
            self._label_msg.grid_remove()
            self._is_fading = False
        else:
            self._msg_color = self._msg_color + FADE_COLOR_DELTA
            self._label_msg['fg'] = f'#{self._msg_color:02x}{self._msg_color:02x}{self._msg_color:02x}'
            self._label_msg.after(FADE_TIMEOUT, self.fade_msg)

    def apply(self, event=None):
        if not utils.check_input_validity(self._entry_sampling_rate.get(), (1, 1e10), 'int'):
            self.reset_msg('Invalid Sampling Rate')
            return
        if not utils.check_input_validity(self._entry_sim_duration.get(), (1, 100), 'float'):
            self.reset_msg('Invalid Simulation Duration')
            return
        self._system.update_config(
            system=
            {
                'sampling rate': self._entry_sampling_rate.get(),
                'sim duration' : self._entry_sim_duration.get()
            }
        )
        self.close()

    def close(self, event=None):
        self._root.destroy()
import tkinter
import tkinter.ttk
import core.utils.utils as utils


FADE_TIMEOUT = 40
FADE_COLOR_DELTA = 10
INITIAL_FADE_DELAY = 600
WINDOW_COLOR = 240

class WindowSystemConfig():

    def __init__(self, system):
        self._root = tkinter.Toplevel()
        self._root.title('System Configuration')
        self._root['background'] = '#'+ 3*f'{WINDOW_COLOR:02x}'
        self._root.grab_set()
        self._system = system
        self._msg_color = 0
        self._is_fading = False
        system_config = self._system.config['system']
        # widgets
        label_samplingrate = tkinter.ttk.Label(self._root, text='Sampling Rate')
        label_simduration = tkinter.ttk.Label(self._root, text='Simulation Duration')
        button_apply = tkinter.ttk.Button(self._root, text='Apply', width=35, command=self.apply)
        self._label_msg = tkinter.ttk.Label(self._root, text='')
        self._entry_samplingrate = tkinter.ttk.Entry(self._root, width=25)
        self._entry_simduration = tkinter.ttk.Entry(self._root, width=25)
        self._entry_samplingrate.insert(0, system_config['sampling rate'])
        self._entry_simduration.insert(0, system_config['sim duration'])
        self._entry_samplingrate.focus()
        # key bindings
        self._root.bind('<Return>', self.apply)
        self._root.bind('<Escape>', lambda event=None: self._root.destroy())
        # geometry
        label_samplingrate.grid(row=0, column=0, sticky='E', padx=(10, 0))
        label_simduration.grid(row=1, column=0, sticky='E', padx=(10, 0))
        button_apply.grid(row=2, columnspan=2, pady=(4, 8))
        self._entry_samplingrate.grid(row=0, column=1, padx=(0, 10))
        self._entry_simduration.grid(row=1, column=1, padx=(0, 10))
        self._label_msg.grid(row=3, columnspan=2, sticky='W', pady=(2, 0))
        self._label_msg.grid_remove()

    def reset_msg(self, text):
        self._msg_color = 0
        self._label_msg.grid()
        self._label_msg['foreground'] = '#'+ 3*f'{self._msg_color:02x}'
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
            self._label_msg['foreground'] = '#'+ 3*f'{self._msg_color:02x}'
            self._label_msg.after(FADE_TIMEOUT, self.fade_msg)

    def apply(self, event=None):
        if not utils.check_input_validity(self._entry_samplingrate.get(), (1, 1e10), 'int'):
            self.reset_msg('Invalid Sampling Rate')
            return
        if not utils.check_input_validity(self._entry_simduration.get(), (0.5, 100), 'float'):
            self.reset_msg('Invalid Simulation Duration')
            return
        self._system.config_update(
            system=
            {
                'sampling rate': self._entry_samplingrate.get(),
                'sim duration' : self._entry_simduration.get()
            }
        )
        self._system.config_writefile()
        self._root.destroy()
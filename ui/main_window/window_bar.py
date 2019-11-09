import tkinter
import tkinter.ttk


LENGTH = 400
FULL_BAR = 100
HALF_BAR = 50


class WindowBar():

    def __init__(self, parent, system):
        self._root = tkinter.Toplevel()
        self._root.title('Simulation Run Progress')
        self._root.transient(parent)
        self._root.resizable(0, 0)
        self._root.protocol('WM_DELETE_WINDOW', self.close)
        self._root.grab_set()
        self._system = system
        self._tx_add = 0
        self._rx_add = 0
        self._bar = tkinter.ttk.Progressbar(
            self._root, length=300, mode='determinate', maximum=FULL_BAR
        )
        self._label_status = tkinter.ttk.Label(self._root, font=('', 8))
        button_cancel = tkinter.ttk.Button(
            self._root, text='Stop', command=self.stop_simulation
        )
        button_cancel.focus()
        self._bar.grid(row=0, padx=(10, 10))
        self._label_status.grid(row=1, pady=(0, 5))
        button_cancel.grid(row=2, pady=(5, 5))
        self._root.geometry('+500+200')

    def set_count(self, tx_count, rx_count):
        self._tx_add = HALF_BAR/tx_count
        self._rx_add = HALF_BAR/rx_count

    def stop_simulation(self):
        self._system.run_stop()
        self.close()

    def close(self):
        self._root.destroy()

    def update(self, status, value):
        self._label_status['text'] = status
        self._bar['value'] = value
        # self._bars[component]['bar']['value'] = data['bar']*LENGTH_MULTIPLIER
        # self._bars[component]['status']['text'] = data['status']

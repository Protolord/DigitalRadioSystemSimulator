import tkinter
import tkinter.ttk
import ui.main_window.window_main as main
import ui.utils.utils_bind as utils


WRAP_LENGTH = 70
LAYER_HEIGHT = 5
LAYER_WIDTH = 9
STREAM_HEIGHT = 2
STREAM_WIDTH = 12
CHANNEL_WIDTH = 15


class WindowWorkspace():

    def __init__(self, system, window_main):
        self._system = system
        self._main = window_main
        self._root = tkinter.ttk.Frame(window_main.window)
        self._root.configure(width=main.WIDTH, height=main.HEIGHT//2)
        self._root.configure(relief=tkinter.SUNKEN)
        diagram = window_main.window_diagram
        self._callbacks = {
            'Input Data': diagram.render_inputbox,
            'Output Data': diagram.render_outputbox,
            'Bitstream': diagram.render_bitstream,
            'In-phase & Quadrature Mapper': diagram.render_iqmapping,
            'In-phase & Quadrature Demapper': diagram.render_iqmapping,
            'Symbol Stream': diagram.render_symbolstream,
            'Waveform Generator': diagram.render_wavetransform,
            'Waveform Detector': diagram.render_wavetransform,
            'Signal': diagram.render_signal,
            'Channel': diagram.render_channel
        }

    @property
    def root(self):
        return self._root

    def label_init(self, txt):
        return tkinter.Label(self._root, text=txt, relief=utils.RELIEF)

    def render(self):
        tx_count = 0
        rx_count = 0
        for name, radio in self._system.radios.items():
            if name.startswith('tx'):
                self.render_tx_radio(radio, row=tx_count)
                tx_count += 1
            elif name.startswith('rx'):
                self.render_rx_radio(radio, row=rx_count)
                rx_count += 1
        if tx_count or rx_count:
            self.render_channel(span=max(tx_count, rx_count))

    def render_channel(self, span):
        label_channel = tkinter.Label(
            self._root, text='Channel', relief=utils.RELIEF
        )
        utils.bind_mouseover(label_channel)
        utils.bind_mouseclick(
            label_channel, self._callbacks[label_channel['text']]
        )
        self._root.grid_columnconfigure(7, weight=1)
        label_channel.configure(width=CHANNEL_WIDTH)
        label_channel.grid(row=0, column=7, rowspan=span, sticky='NSEW')

    def render_tx_radio(self, radio, row):
        label_name = tkinter.ttk.Label(self._root, text=radio)
        label_inputbox = self.label_init('Input Data')
        label_bitstream = self.label_init('Bitstream')
        label_iqmapper = self.label_init('In-phase & Quadrature Mapper')
        label_symbolstream = self.label_init('Symbol Stream')
        label_wavegenerator = self.label_init('Waveform Generator')
        label_signal = self.label_init('Signal')
        layers = [label_inputbox, label_iqmapper, label_wavegenerator]
        streams = [label_bitstream, label_symbolstream, label_signal]
        # bindings
        for label in (layers + streams):
            utils.bind_mouseover(label)
            utils.bind_mouseclick(label, self._callbacks[label['text']], radio)
        # size and geometry
        label_name.grid(row=row, column=0, padx=(5, 0))
        for i, label in enumerate(layers):
            self._root.grid_rowconfigure(row, weight=1)
            self._root.grid_columnconfigure(2*i + 1, weight=1)
            label.configure(width=LAYER_WIDTH, height=LAYER_HEIGHT)
            label.configure(wraplength=WRAP_LENGTH)
            label.grid(row=row, column=2*i + 1, sticky='NSEW')
        for i, label in enumerate(streams):
            self._root.grid_rowconfigure(row, weight=1)
            self._root.grid_columnconfigure(2*i + 2, weight=1)
            label.configure(width=STREAM_WIDTH, height=STREAM_HEIGHT)
            label.grid(row=row, column=2*i + 2, sticky='EW')

    def render_rx_radio(self, radio, row):
        label_signal = self.label_init('Signal')
        label_wavedetector = self.label_init('Waveform Detector')
        label_symbolstream = self.label_init('Symbol Stream')
        label_iqdemapper = self.label_init('In-phase & Quadrature Demapper')
        label_bitstream = self.label_init('Bitstream')
        label_outputbox = self.label_init('Output Data')
        label_name = tkinter.ttk.Label(self._root, text=radio)
        streams = [label_signal, label_symbolstream, label_bitstream]
        layers = [label_wavedetector, label_iqdemapper, label_outputbox]
        # key bindings
        for label in (layers + streams):
            utils.bind_mouseover(label)
            utils.bind_mouseclick(label, self._callbacks[label['text']], radio)
        # size and geometry
        for i, label in enumerate(streams):
            self._root.grid_rowconfigure(row, weight=1)
            self._root.grid_columnconfigure(2*i + 8, weight=1)
            label.configure(width=STREAM_WIDTH, height=STREAM_HEIGHT)
            label.grid(row=row, column=2*i + 8, sticky='EW')
        for i, label in enumerate(layers):
            self._root.grid_rowconfigure(row, weight=1)
            self._root.grid_columnconfigure(2*i + 9, weight=1)
            label.configure(width=LAYER_WIDTH, height=LAYER_HEIGHT)
            label.configure(wraplength=WRAP_LENGTH)
            label.grid(row=row, column=2*i + 9, sticky='NSEW')
        label_name.grid(row=row, column=14, padx=(0, 5))

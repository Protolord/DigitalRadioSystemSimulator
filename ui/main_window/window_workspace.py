import tkinter
import tkinter.ttk
import ui.main_window.window_main as main
import ui.utils_bind as utils


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

    def create_label(self, txt):
        return tkinter.Label(self._root, text=txt, relief=utils.RELIEF)

    def render(self):
        tx_count = 0
        rx_count = 0
        for name, radio in self._system.radios.items():
            if 'tx' == name[:2]:
                self.render_tx_radio(radio, row=tx_count)
                tx_count += 1
            elif 'rx' == name[:2]:
                self.render_rx_radio(radio, row=rx_count)
                rx_count += 1
        self.render_channel(span=max(tx_count, rx_count))

    def render_channel(self, span):
        label_channel = tkinter.Label(
            self._root, text='Channel', relief=utils.RELIEF
        )
        utils.bind_mouseover(label_channel)
        utils.bind_mouseclick(
            label_channel, self._callbacks[label_channel['text']]
        )
        label_channel.configure(width=CHANNEL_WIDTH)
        label_channel.grid(row=0, column=7, rowspan=span, sticky='NS')

    def render_tx_radio(self, radio, row):
        label_name = tkinter.ttk.Label(self._root, text=radio)
        label_inputbox = self.create_label('Input Data')
        label_bitstream = self.create_label('Bitstream')
        label_iqmapper = self.create_label('In-phase & Quadrature Mapper')
        label_symbolstream = self.create_label('Symbol Stream')
        label_wavegenerator = self.create_label('Waveform Generator')
        label_signal = self.create_label('Signal')
        layers = [label_inputbox, label_iqmapper, label_wavegenerator]
        streams = [label_bitstream, label_symbolstream, label_signal]
        # bindings
        for label in (layers + streams):
            utils.bind_mouseover(label)
        for label in (layers + streams):
            utils.bind_mouseclick(label, self._callbacks[label['text']], radio)
        # size and geometry
        label_name.grid(row=row, column=0, padx=(5, 0))
        for i, label in enumerate(layers):
            label.configure(width=LAYER_WIDTH, height=LAYER_HEIGHT)
            label.configure(wraplength=WRAP_LENGTH)
            label.grid(row=row, column=2*i + 1)
        for i, label in enumerate(streams):
            label.configure(width=STREAM_WIDTH, height=STREAM_HEIGHT)
            label.grid(row=row, column=2*i + 2)

    def render_rx_radio(self, radio, row):
        label_signal = self.create_label('Signal')
        label_wavedetector = self.create_label('Waveform Detector')
        label_symbolstream = self.create_label('Symbol Stream')
        label_iqdemapper = self.create_label('In-phase & Quadrature Demapper')
        label_bitstream = self.create_label('Bitstream')
        label_outputbox = self.create_label('Output Data')
        label_name = tkinter.ttk.Label(self._root, text=radio)
        streams = [label_signal, label_symbolstream, label_bitstream]
        layers = [label_wavedetector, label_iqdemapper, label_outputbox]
        # key bindings
        for label in (layers + streams):
            utils.bind_mouseover(label)
        for label in (layers + streams):
            utils.bind_mouseclick(label, self._callbacks[label['text']], radio)
        # size and geometry
        for i, label in enumerate(streams):
            label.configure(width=STREAM_WIDTH, height=STREAM_HEIGHT)
            label.grid(row=row, column=2*i + 8)
        for i, label in enumerate(layers):
            label.configure(width=LAYER_WIDTH, height=LAYER_HEIGHT)
            label.configure(wraplength=WRAP_LENGTH)
            label.grid(row=row, column=2*i + 9)
        label_name.grid(row=row, column=14, padx=(0, 5))

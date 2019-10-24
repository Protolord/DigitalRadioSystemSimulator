import tkinter
import tkinter.ttk
import ui.main_window.window_main as main
import ui.utils_bind as utils


WRAP_LENGTH = 70
LAYER_HEIGHT = 5
LAYER_WIDTH = 9
DATASTREAM_HEIGHT = 2
DATASTREAM_WIDTH = 12
CHANNEL_WIDTH = 15

class WindowWorkspace():

    def __init__(self, system, window_main):
        self._system = system
        self._frame = tkinter.ttk.Frame(window_main, relief=tkinter.SUNKEN)
        self._frame.configure(width=main.WIDTH, height=main.HEIGHT//2)

    @property
    def frame(self):
        return self._frame

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
        label_channel = tkinter.Label(self._frame, text='Channel', relief=utils.RELIEF)
        utils.bind_mouseover(label_channel)
        utils.bind_mouseclick(label_channel, self.open_channel)
        label_channel.configure(width=CHANNEL_WIDTH)
        label_channel.grid(row=0, column=7, rowspan=span, sticky='NS')

    def render_tx_radio(self, radio, row):
        label_name = tkinter.ttk.Label(self._frame, text=radio.name)
        label_inputbox = tkinter.Label(self._frame, text='Input Data', relief=utils.RELIEF)
        label_bitstream = tkinter.Label(self._frame, text='Bitstream', relief=utils.RELIEF)
        label_iqmapper = tkinter.Label(self._frame, text='In-phase & Quadrature Mapper', relief=utils.RELIEF)
        label_symbolstream = tkinter.Label(self._frame, text='Symbol Stream', relief=utils.RELIEF)
        label_wavegenerator = tkinter.Label(self._frame, text='Waveform Generator', relief=utils.RELIEF)
        label_signal = tkinter.Label(self._frame, text='Signal', relief=utils.RELIEF)
        # key bindings
        utils.bind_mouseover(label_inputbox)
        utils.bind_mouseover(label_bitstream)
        utils.bind_mouseover(label_iqmapper)
        utils.bind_mouseover(label_symbolstream)
        utils.bind_mouseover(label_wavegenerator)
        utils.bind_mouseover(label_signal)
        utils.bind_mouseclick(label_inputbox, self.open_inputbox, radio.name)
        utils.bind_mouseclick(label_bitstream, self.open_bitstream, radio.name)
        utils.bind_mouseclick(label_iqmapper, self.open_iqmapping, radio.name)
        utils.bind_mouseclick(label_symbolstream, self.open_symbolstream, radio.name)
        utils.bind_mouseclick(label_wavegenerator, self.open_wavetransfom, radio.name)
        utils.bind_mouseclick(label_signal, self.open_signal, radio.name)
        # size
        label_inputbox.configure(width=LAYER_WIDTH, height=LAYER_HEIGHT)
        label_bitstream.configure(width=DATASTREAM_WIDTH, height=DATASTREAM_HEIGHT)
        label_iqmapper.configure(width=LAYER_WIDTH, height=LAYER_HEIGHT, wraplength=WRAP_LENGTH)
        label_symbolstream.configure(width=DATASTREAM_WIDTH, height=DATASTREAM_HEIGHT)
        label_wavegenerator.configure(width=LAYER_WIDTH, height=LAYER_HEIGHT, wraplength=WRAP_LENGTH)
        label_signal.configure(width=LAYER_WIDTH, height=DATASTREAM_HEIGHT)
        # geometry
        label_name.grid(row=row, column=0, padx=(5, 0))
        label_inputbox.grid(row=row, column=1)
        label_bitstream.grid(row=row, column=2)
        label_iqmapper.grid(row=row, column=3)
        label_symbolstream.grid(row=row, column=4)
        label_wavegenerator.grid(row=row, column=5)
        label_signal.grid(row=row, column=6)

    def render_rx_radio(self, radio, row):
        label_signal = tkinter.Label(self._frame, text='Signal', relief=utils.RELIEF)
        label_wavedetector = tkinter.Label(self._frame, text='Waveform Detector', relief=utils.RELIEF)
        label_symbolstream = tkinter.Label(self._frame, text='Symbol Stream', relief=utils.RELIEF)
        label_iqdemapper = tkinter.Label(self._frame, text='In-phase & Quadrature Demapper', relief=utils.RELIEF)
        label_bitstream = tkinter.Label(self._frame, text='Bitstream', relief=utils.RELIEF)
        label_outputbox = tkinter.Label(self._frame, text='Output Data', relief=utils.RELIEF)
        label_name = tkinter.Label(self._frame, text=radio.name)
        # key bindings
        utils.bind_mouseover(label_signal)
        utils.bind_mouseover(label_wavedetector)
        utils.bind_mouseover(label_symbolstream)
        utils.bind_mouseover(label_iqdemapper)
        utils.bind_mouseover(label_bitstream)
        utils.bind_mouseover(label_outputbox)
        utils.bind_mouseclick(label_signal, self.open_signal, radio.name)
        utils.bind_mouseclick(label_wavedetector, self.open_wavetransfom, radio.name)
        utils.bind_mouseclick(label_symbolstream, self.open_symbolstream, radio.name)
        utils.bind_mouseclick(label_iqdemapper, self.open_iqmapping, radio.name)
        utils.bind_mouseclick(label_bitstream, self.open_bitstream, radio.name)
        utils.bind_mouseclick(label_outputbox, self.open_outputbox, radio.name)
        # size
        label_signal.configure(width=DATASTREAM_WIDTH, height=DATASTREAM_HEIGHT)
        label_wavedetector.configure(width=LAYER_WIDTH, height=LAYER_HEIGHT, wraplength=WRAP_LENGTH)
        label_symbolstream.configure(width=DATASTREAM_WIDTH, height=DATASTREAM_HEIGHT)
        label_iqdemapper.configure(width=LAYER_WIDTH, height=LAYER_HEIGHT, wraplength=WRAP_LENGTH)
        label_bitstream.configure(width=DATASTREAM_WIDTH, height=DATASTREAM_HEIGHT)
        label_outputbox.configure(width=LAYER_WIDTH, height=LAYER_HEIGHT)
        # geometry
        label_signal.grid(row=row, column=8)
        label_wavedetector.grid(row=row, column=9)
        label_symbolstream.grid(row=row, column=10)
        label_iqdemapper.grid(row=row, column=11)
        label_bitstream.grid(row=row, column=12)
        label_outputbox.grid(row=row, column=13)
        label_name.grid(row=row, column=14, padx=(0, 5))

    def open_channel(self, event):
        print('Clicked Channel')

    def open_iqmapping(self, event, radio_name):
        print(f'Clicked IQ mapping for {radio_name}')

    def open_wavetransfom(self, event, radio_name):
        print(f'Clicked wave transformation for {radio_name}')

    def open_inputbox(self, event, radio_name):
        print(f'Clicked Button{event.num} inputbox for {radio_name}')

    def open_outputbox(self, event, radio_name):
        print(f'Clicked Button{event.num} output for {radio_name}')

    def open_signal(self, event, radio_name):
        print(f'Clicked Button{event.num} signal for {radio_name}')

    def open_symbolstream(self, event, radio_name):
        print(f'Clicked Button{event.num} symbol stream for {radio_name}')

    def open_bitstream(self, event, radio_name):
        print(f'Clicked Button{event.num} bitstream for {radio_name}')
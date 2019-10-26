import tkinter
import tkinter.ttk
import ui.main_window.window_main as main
import ui.utils_bind as utils


class WindowDiagram():

    def __init__(self, system, window_main):
        self._system = system
        self._window = tkinter.ttk.PanedWindow(window_main.window, orient=tkinter.HORIZONTAL)
        self._frame_left = tkinter.ttk.Frame(self._window, relief=tkinter.SUNKEN)
        self._frame_right = tkinter.ttk.Frame(self._window, relief=tkinter.SUNKEN)
        self._frame_left.configure(width=main.WIDTH//2, height=main.HEIGHT//2)
        self._frame_right.configure(width=main.WIDTH//2, height=main.HEIGHT//2)
        self._window.add(self._frame_left, weight=1)
        self._window.add(self._frame_right, weight=1)

    @property
    def window(self):
        return self._window

    def render_channel(self, event):
        print('Clicked Channel')

    def render_inputbox(self, event, radio_name):
        print(f'Clicked Button{event.num} inputbox for {radio_name}')

    def render_outputbox(self, event, radio_name):
        print(f'Clicked Button{event.num} output for {radio_name}')

    def render_bitstream(self, event, radio_name):
        print(f'Clicked Button{event.num} bitstream for {radio_name}')

    def render_symbolstream(self, event, radio_name):
        print(f'Clicked Button{event.num} symbol stream for {radio_name}')

    def render_signal(self, event, radio_name):
        print(f'Clicked Button{event.num} signal for {radio_name}')

    def render_iqmapping(self, event, radio_name):
        print(f'Clicked IQ mapping for {radio_name}')

    def render_wavetransform(self, event, radio_name):
        print(f'Clicked wave transformation for {radio_name}')

import numpy
import tkinter
import tkinter.ttk
import core.utils.utils as utils
import ui.main_window.window_main as main


class WindowDiagram():

    def __init__(self, system, window_main):
        self._system = system
        self._root = tkinter.ttk.PanedWindow(window_main.window, orient=tkinter.HORIZONTAL)
        self._frame_left = tkinter.ttk.Frame(self._root, relief=tkinter.SUNKEN)
        self._frame_right = tkinter.ttk.Frame(self._root, relief=tkinter.SUNKEN)
        self._frame_left.configure(width=main.WIDTH//2, height=main.HEIGHT//2)
        self._frame_right.configure(width=main.WIDTH//2, height=main.HEIGHT//2)
        self._root.add(self._frame_left, weight=1)
        self._root.add(self._frame_right, weight=1)
        self._afterrun_process = {}

    @property
    def root(self):
        return self._root

    def get_frame(self, mouse_button, afterrun=None):
        if 1 == mouse_button:
            frame = self._frame_left
        elif 3 == mouse_button:
            frame = self._frame_right
        for widget in frame.winfo_children():
            widget.destroy()
        if afterrun is None:
            self._afterrun_process.pop(mouse_button, None)
        else:
            self._afterrun_process[mouse_button] = afterrun
        return frame

    def text_init(self, widget_input, radio):
        if radio.bitstream is not None:
            binary = ''.join(str(bit) for bit in radio.bitstream.tolist())
            widget_input.insert(tkinter.END, utils.binary_to_text(binary))

    def render_afterrun(self):
        for key, value in self._afterrun_process.items():
            event = tkinter.Event()
            event.num = key
            eval(value[0])(event, value[1])

    def render_channel(self, event):
        print('Clicked Channel')

    def render_inputbox(self, event, radio):
        frame = self.get_frame(event.num)
        label_name = tkinter.ttk.Label(frame, text=f'{radio} input type:')
        combobox_datatype = tkinter.ttk.Combobox(frame, values=['Text'])
        text_input = tkinter.Text(frame, height=10, width=65)
        button_apply = tkinter.ttk.Button(frame, text='Apply', width=50)
        button_apply['command'] = lambda: self.apply_inputbox(text_input, radio)
        combobox_datatype.current(0)
        self.text_init(text_input, radio)
        text_input.focus()
        # geometry
        label_name.grid(row=0, column=0, sticky='E', pady=(5, 5))
        combobox_datatype.grid(row=0, column=1, sticky='W')
        text_input.grid(row=1, columnspan=2, padx=(10, 10), pady=(5, 5))
        button_apply.grid(row=2, columnspan=2, sticky='S')

    def apply_inputbox(self, widget_input, radio):
        text = widget_input.get('1.0', 'end-1c')
        binary = utils.text_to_binary(text)
        radio.bitstream = numpy.array(list(binary), dtype=numpy.int8)

    def render_outputbox(self, event, radio):
        frame = self.get_frame(event.num, afterrun=('self.render_outputbox', radio))
        label_name = tkinter.ttk.Label(frame, text=f'{radio} output type:')
        combobox_datatype = tkinter.ttk.Combobox(frame, values=['Text'])
        text_output = tkinter.Text(frame, height=10, width=65)
        combobox_datatype.current(0)
        self.text_init(text_output, radio)
        text_output['state'] = 'disabled'
        # geometry
        label_name.grid(row=0, column=0, sticky='E', pady=(5, 5))
        combobox_datatype.grid(row=0, column=1, sticky='W')
        text_output.grid(row=1, columnspan=2, padx=(10, 10), pady=(5, 5))

    def render_bitstream(self, event, radio):
        print(f'Clicked Button{event.num} bitstream for {radio}')

    def render_symbolstream(self, event, radio):
        print(f'Clicked Button{event.num} symbol stream for {radio}')

    def render_signal(self, event, radio):
        print(f'Clicked Button{event.num} signal for {radio}')

    def render_iqmapping(self, event, radio):
        print(f'Clicked IQ mapping for {radio}')

    def render_wavetransform(self, event, radio):
        print(f'Clicked wave transformation for {radio}')

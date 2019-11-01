import tkinter
import tkinter.ttk
import numpy
import core.utils.utils as utils
import ui.main_window.window_main as main


class WindowDiagram():

    def __init__(self, system, window_main):
        self._system = system
        self._root = tkinter.ttk.PanedWindow(
            window_main.window, orient=tkinter.HORIZONTAL
        )
        self._lframe = tkinter.ttk.Frame(self._root, relief=tkinter.SUNKEN)
        self._rframe = tkinter.ttk.Frame(self._root, relief=tkinter.SUNKEN)
        self._lframe.configure(width=main.WIDTH//2, height=main.HEIGHT//2)
        self._rframe.configure(width=main.WIDTH//2, height=main.HEIGHT//2)
        self._root.add(self._lframe, weight=1)
        self._root.add(self._rframe, weight=1)
        self._repeat_render_list = {}

    @property
    def root(self):
        return self._root

    def get_frame(self, mouse_button, repeat_render=None):
        if 1 == mouse_button:
            frame = self._lframe
        elif 3 == mouse_button:
            frame = self._rframe
        for widget in frame.winfo_children():
            widget.destroy()
        if repeat_render is None:
            self._repeat_render_list.pop(mouse_button, None)
        else:
            self._repeat_render_list[mouse_button] = repeat_render
        return frame

    def text_init(self, widget_input, radio):
        if radio.bitstream is not None:
            binary = ''.join(str(bit) for bit in radio.bitstream.tolist())
            widget_input.insert(tkinter.END, utils.binary_to_text(binary))

    def repeat_render(self):
        for key, value in self._repeat_render_list.items():
            event = tkinter.Event()
            event.num = key
            eval(value[0])(event, value[1])

    def render_channel(self, event):
        print('Clicked Channel')

    def render_inputbox(self, event, radio):
        frame = self.get_frame(
            event.num, repeat_render=('self.render_inputbox', radio)
        )
        label_name = tkinter.ttk.Label(frame, text=f'{radio} input type:')
        combobox_datatype = tkinter.ttk.Combobox(frame, values=['Text'])
        text_in = tkinter.Text(frame, height=10, width=65)
        button_apply = tkinter.ttk.Button(frame, text='Apply', width=50)
        button_apply['command'] = lambda: self.apply_inputbox(text_in, radio)
        combobox_datatype.current(0)
        self.text_init(text_in, radio)
        text_in.focus()
        # geometry
        label_name.grid(row=0, column=0, sticky='E', pady=(5, 5))
        combobox_datatype.grid(row=0, column=1, sticky='W')
        text_in.grid(row=1, columnspan=2, padx=(10, 10), pady=(5, 5))
        button_apply.grid(row=2, columnspan=2, sticky='S')

    def apply_inputbox(self, widget_input, radio):
        text = widget_input.get('1.0', 'end-1c')
        binary = utils.text_to_binary(text)
        radio.bitstream = numpy.array(list(binary), dtype=numpy.int8)
        self.repeat_render()

    def render_outputbox(self, event, radio):
        frame = self.get_frame(
            event.num, repeat_render=('self.render_outputbox', radio)
        )
        label_name = tkinter.ttk.Label(frame, text=f'{radio} output type:')
        combobox_datatype = tkinter.ttk.Combobox(frame, values=['Text'])
        text_out = tkinter.Text(frame, height=10, width=65)
        combobox_datatype.current(0)
        self.text_init(text_out, radio)
        text_out['state'] = 'disabled'
        # geometry
        label_name.grid(row=0, column=0, sticky='E', pady=(5, 5))
        combobox_datatype.grid(row=0, column=1, sticky='W')
        text_out.grid(row=1, columnspan=2, padx=(10, 10), pady=(5, 5))

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

import tkinter
import tkinter.ttk
import numpy
import core.utils.utils as utils
import ui.main_window.window_main as main
import ui.utils.figurecanvas as figurecanvas
import ui.utils.textscroll as textscroll


MOUSE_LEFT = 1
MOUSE_RIGHT = 3
MAX_GRID = 2


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
        self._inputoutput_type = self.stringvars_init()
        self._bitstream_modes = self.stringvars_init()

    @property
    def root(self):
        return self._root

    @classmethod
    def stringvars_init(cls):
        return {
            MOUSE_LEFT: tkinter.StringVar(),
            MOUSE_RIGHT: tkinter.StringVar()
        }

    @classmethod
    def combobox_init(cls, frame, stringvar, items):
        combobox = tkinter.ttk.Combobox(
            master=frame, state='readonly',
            textvariable=stringvar, values=items
        )
        if stringvar.get():
            combobox.set(stringvar.get())
        else:
            combobox.current(0)
        return combobox

    def get_frame(self, mouse_button, repeat_render=None):
        if MOUSE_LEFT == mouse_button:
            frame = self._lframe
        elif MOUSE_RIGHT == mouse_button:
            frame = self._rframe
        for widget in frame.winfo_children():
            widget.destroy()
        if repeat_render is None:
            self._repeat_render_list.pop(mouse_button, None)
        else:
            self._repeat_render_list[mouse_button] = repeat_render
        for i in range(MAX_GRID):
            frame.grid_rowconfigure(i, weight=1)
            frame.grid_columnconfigure(i, weight=1)
        return frame

    def repeat_render(self):
        for key, value in self._repeat_render_list.items():
            event = tkinter.Event()
            event.num = key
            (func, radio) = value
            eval(func)(event, radio)

    def render_channel(self, event):
        print('Clicked Channel')

    def render_inputbox(self, event, radio):
        frame = self.get_frame(
            event.num, repeat_render=('self.render_inputbox', radio)
        )
        label_name = tkinter.ttk.Label(frame, text=f'{radio} input type:')
        combobox_datatype = self.combobox_init(
            frame, self._inputoutput_type[event.num],
            ('Text')
        )
        text_in = textscroll.TextScroll(frame, radio)
        text_in.text.configure(height=12, width=65)
        text_in.text.focus()
        button_apply = tkinter.ttk.Button(frame, text='Apply', width=50)
        button_apply['command'] = lambda: self.apply_inputbox(text_in, radio)
        # geometry
        label_name.grid(row=0, column=0, pady=(10, 5), sticky='NE')
        combobox_datatype.grid(row=0, column=1, pady=(10, 5), sticky='NW')
        text_in.grid(
            row=1, columnspan=2, padx=(10, 10), pady=(5, 15), sticky='NSEW'
        )
        button_apply.grid(
            row=2, columnspan=2, padx=(20, 20), pady=(5, 5), sticky='NSEW'
        )

    def apply_inputbox(self, textscroll, radio):
        text = textscroll.text.get('1.0', 'end-1c')
        binary = utils.text_to_binary(text)
        radio.bitstream = numpy.array(list(binary), dtype=numpy.int8)
        self.repeat_render()

    def render_outputbox(self, event, radio):
        frame = self.get_frame(
            event.num, repeat_render=('self.render_outputbox', radio)
        )
        label_name = tkinter.ttk.Label(frame, text=f'{radio} output type:')
        combobox_datatype = self.combobox_init(
            frame, self._inputoutput_type[event.num],
            ('Text')
        )
        text_out = textscroll.TextScroll(frame, radio, 'disabled')
        label_name.grid(row=0, column=0, pady=(10, 5), sticky='NE')
        combobox_datatype.grid(row=0, column=1, pady=(10, 5), sticky='NW')
        text_out.grid(
            row=1, columnspan=2, padx=(10, 10), pady=(5, 15), sticky='NSEW'
        )

    def render_bitstream(self, event, radio):
        frame = self.get_frame(
            event.num, repeat_render=('self.render_bitstream', radio)
        )
        label_name = tkinter.ttk.Label(frame, text=f'{radio} display mode:')
        combobox_displaytype = self.combobox_init(
            frame, self._bitstream_modes[event.num],
            ('Bit Values', 'Non-return-to-zero')
        )
        combobox_displaytype.bind(
            '<<ComboboxSelected>>',
            lambda e: self.render_bitstream(event, radio)
        )
        figure = figurecanvas.FigureCanvas(frame)
        figure.plot_bitstream(
            radio.bitstream, self._bitstream_modes[event.num].get()
        )
        # geometry
        label_name.grid(row=0, column=0, sticky='E', pady=(5, 5))
        combobox_displaytype.grid(row=0, column=1, sticky='W')
        figure.grid(
            row=1, columnspan=2, padx=(2, 2), pady=(2, 2), sticky='NSEW'
        )

    def render_symbolstream(self, event, radio):
        print(f'Clicked Button{event.num} symbol stream for {radio}')

    def render_signal(self, event, radio):
        print(f'Clicked Button{event.num} signal for {radio}')

    def render_iqmapping(self, event, radio):
        print(f'Clicked IQ mapping for {radio}')

    def render_wavetransform(self, event, radio):
        print(f'Clicked wave transformation for {radio}')

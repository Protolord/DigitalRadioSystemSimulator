import tkinter
import tkinter.ttk
import numpy
import matplotlib.backends.backend_tkagg
import matplotlib.figure
import matplotlib.widgets


BITVALUE_OFFSET = 0.1
BITPOS_OFFSET = 0.5
BITPOS_INIT = 1
BITPOS_MAX = 16
COMPLEX_BOUND = 1.1
GRAPH_COLOR = 240/255


class FigureCanvas(tkinter.ttk.Frame):

    def __init__(self, master):
        super().__init__(master=master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._figure = matplotlib.figure.Figure(figsize=(6, 2.5), dpi=100)
        self._canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(
            figure=self._figure, master=self
        )
        self._figure.set_facecolor((GRAPH_COLOR, GRAPH_COLOR, GRAPH_COLOR))
        self._axes_plot = None
        self._axes_slider = None
        self._slider = None
        self._canvas.get_tk_widget().pack()

    def plot_update(self, size):
        pos = self._slider.val * (size-BITPOS_MAX)/100
        self._axes_plot.axis([
            pos + BITPOS_INIT - BITPOS_OFFSET,
            pos + BITPOS_MAX + BITPOS_OFFSET,
            -BITVALUE_OFFSET,
            BITVALUE_OFFSET + 1
        ])
        # self._canvas.draw()

    def plot_bitstream(self, bitstream, mode):
        if bitstream is None:
            return
        bitpos = numpy.arange(BITPOS_INIT, BITPOS_INIT + bitstream.size)
        self._axes_plot = self._figure.add_axes([0.10, 0.25, 0.85, 0.75])
        self._axes_plot.set_yticks([0, 1])
        if bitstream.size < 1000:
            self._axes_plot.set_xticks(bitpos)
        self._axes_plot.axis([
            BITPOS_INIT - BITPOS_OFFSET,
            BITPOS_MAX + BITPOS_OFFSET,
            -BITVALUE_OFFSET,
            BITVALUE_OFFSET + 1
        ])
        self._axes_plot.set_facecolor((GRAPH_COLOR, GRAPH_COLOR, GRAPH_COLOR))
        self._axes_slider = self._figure.add_axes([0.25, 0.05, 0.6, 0.05])
        self._slider = matplotlib.widgets.Slider(
            self._axes_slider, 'Bit Position', 0.0, 100.0, valinit=0.0
        )
        self._slider.on_changed(lambda val: self.plot_update(bitstream.size))
        # self._canvas.draw()
        if 'Bit Values' == mode:
            self._axes_plot.stem(bitpos, bitstream, use_line_collection=True)
        elif 'Non-return-to-zero' == mode:
            self._axes_plot.plot(bitpos, bitstream, drawstyle='steps-mid')

    def plot_symbolstream(self, symbolstream, mode):
        if symbolstream is None:
            return
        if 'Complex Plane' == mode:
            self._axes_plot = self._figure.add_axes([0.325, 0.2, 0.35, 0.8])
            self._axes_plot.set_xlabel('real')
            self._axes_plot.set_ylabel('imaginary')
            self._axes_plot.axis([
                -COMPLEX_BOUND, COMPLEX_BOUND,
                -COMPLEX_BOUND, COMPLEX_BOUND
            ])
            self._axes_plot.scatter(symbolstream.real, symbolstream.imag)
            angle = numpy.linspace(0, 2*numpy.pi, 100)
            self._axes_plot.plot(
                numpy.cos(angle), numpy.sin(angle), '--', color='#aaaaaa'
            )

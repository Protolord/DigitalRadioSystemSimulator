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
GRAPH_COLOR = 240/255


class FigureCanvas(tkinter.ttk.Frame):

    def __init__(self, master):
        super().__init__(master=master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.figure = matplotlib.figure.Figure(figsize=(6, 2.5), dpi=100)
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(
            figure=self.figure, master=self
        )
        self.figure.set_facecolor((GRAPH_COLOR, GRAPH_COLOR, GRAPH_COLOR))
        self.ax_plot = None
        self.ax_slider = None
        self.slider = None
        self.canvas.get_tk_widget().pack()

    def plot_update(self, size):
        pos = self.slider.val * (size-BITPOS_MAX)/100
        self.ax_plot.axis([
            pos + BITPOS_INIT - BITPOS_OFFSET,
            pos + BITPOS_MAX + BITPOS_OFFSET,
            -BITVALUE_OFFSET,
            BITVALUE_OFFSET + 1
        ])
        self.canvas.draw()

    def plot_bitstream(self, bitstream, mode):
        if bitstream is None:
            return
        bitpos = numpy.arange(BITPOS_INIT, BITPOS_INIT + bitstream.size)
        self.ax_plot = self.figure.add_axes([0.10, 0.25, 0.85, 0.75])
        self.ax_plot.set_yticks([0, 1])
        if bitstream.size < 1000:
            self.ax_plot.set_xticks(bitpos)
        self.ax_plot.axis([
            BITPOS_INIT - BITPOS_OFFSET,
            BITPOS_MAX + BITPOS_OFFSET,
            -BITVALUE_OFFSET,
            BITVALUE_OFFSET + 1
        ])
        self.ax_plot.set_facecolor((GRAPH_COLOR, GRAPH_COLOR, GRAPH_COLOR))
        if 'Bit Values' == mode:
            self.ax_plot.stem(bitpos, bitstream, use_line_collection=True)
        elif 'Non-return-to-zero' == mode:
            self.ax_plot.plot(bitpos, bitstream, drawstyle='steps-mid')
        self.ax_slider = self.figure.add_axes([0.25, 0.05, 0.6, 0.05])
        self.slider = matplotlib.widgets.Slider(
            self.ax_slider, 'Bit Position', 0.0, 100.0, valinit=0.0
        )
        self.slider.on_changed(lambda val: self.plot_update(bitstream.size))
        self.canvas.draw()

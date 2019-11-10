import tkinter
import tkinter.ttk
import core.utils.utils as utils


class TextScroll(tkinter.ttk.Frame):

    def __init__(self, master, radio, state='normal'):
        super().__init__(master=master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.text = tkinter.Text(self)
        self.scroll = tkinter.ttk.Scrollbar(self, command=self.text.yview)
        self.text.focus()
        if radio is not None and radio.bitstream is not None:
            binary = ''.join(str(bit) for bit in radio.bitstream.tolist())
            self.text.insert(tkinter.END, utils.binary_to_text(binary))
        self.text.configure(
            height=12, width=65, yscrollcommand=self.scroll.set, state=state
        )
        # geometry
        self.text.grid(row=0, column=0, sticky='NSEW')
        self.scroll.grid(row=0, column=1, sticky='NSEW')

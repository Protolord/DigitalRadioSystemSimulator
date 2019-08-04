import tkinter

class MainWindow():

    def __init__(self):
        self.root = tkinter.Tk()
        self.ui_setup()

    def ui_setup(self):
        self.root.title("Digital Radio System Simulator")
        self.root.call('wm', 'iconphoto', self.root._w, tkinter.PhotoImage(file='ui/images/icon.gif'))

    def run(self):

        self.root.mainloop()
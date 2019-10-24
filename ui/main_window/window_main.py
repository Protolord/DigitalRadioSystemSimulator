import tkinter
import tkinter.ttk
import ui.config_windows.window_channel_config as channel
import ui.config_windows.window_radio_config as radio
import ui.config_windows.window_system_config as system
import ui.main_window.window_workspace as workspace


WIDTH = 1000
HEIGHT = 600

class WindowMain():

    def __init__(self, system):
        self._system = system
        self._root = tkinter.Tk()
        self._root.title('Digital Radio System Simulator')
        self._root.call('wm', 'iconphoto', self._root._w, tkinter.PhotoImage(file='ui/images/icon.gif'))
        self._root.option_add('*tearOff', False)
        # window
        window_main = tkinter.ttk.PanedWindow(self._root, orient=tkinter.VERTICAL)
        self._window_workspace = workspace.WindowWorkspace(system, window_main)
        self._window_diagram = tkinter.ttk.PanedWindow(window_main, orient=tkinter.HORIZONTAL)
        window_main.add(self._window_workspace.frame, weight=1)
        window_main.add(self._window_diagram, weight=1)
        self._frame_left_diagram = tkinter.ttk.Frame(self._window_diagram, relief=tkinter.SUNKEN)
        self._frame_right_diagram = tkinter.ttk.Frame(self._window_diagram, relief=tkinter.SUNKEN)
        self._window_diagram.add(self._frame_left_diagram, weight=1)
        self._window_diagram.add(self._frame_right_diagram, weight=1)
        self._window_workspace.render()
        # menubar
        menu = tkinter.Menu(self._root)
        self._root.config(menu=menu)
        menu_simulation = tkinter.Menu(menu)
        menu_simulation.add_command(label='Run', command=self._system.run, accelerator='F1')
        menu_simulation.add_separator()
        menu_simulation.add_command(label='System Configuration', command=self.open_system_config, accelerator='F2')
        menu_simulation.add_command(label='Radio Configuration', command=self.open_radio_config, accelerator='F3')
        menu_simulation.add_command(label='Channel Configuration', command=self.open_channel_config, accelerator='F4')
        menu_help = tkinter.Menu(menu)
        menu_help.add_command(label='About')
        menu.add_cascade(label='Simulation', menu=menu_simulation)
        menu.add_cascade(label='Help', menu=menu_help)
        # key bindings
        self._root.bind('<F1>', self._system.run)
        self._root.bind('<F2>', self.open_system_config)
        self._root.bind('<F3>', self.open_radio_config)
        self._root.bind('<F4>', self.open_channel_config)
        # geometry
        window_main.pack(fill=tkinter.BOTH, expand=True)
        self._frame_left_diagram.configure(width=WIDTH//2, height=HEIGHT//2)
        self._frame_right_diagram.configure(width=WIDTH//2, height=HEIGHT//2)

    def run(self):
        self._root.mainloop()

    def open_system_config(self, event=None):
        system.WindowSystemConfig(self._system)

    def open_radio_config(self, event=None):
        radio.WindowRadioConfig(self._system)

    def open_channel_config(self, event=None):
        channel.WindowChannelConfig(self._system)
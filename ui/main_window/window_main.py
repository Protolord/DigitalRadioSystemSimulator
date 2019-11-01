import tkinter
import tkinter.ttk
import ui.config_windows.window_channel_config as channel
import ui.config_windows.window_radio_config as radio
import ui.config_windows.window_system_config as system
import ui.main_window.window_workspace as workspace
import ui.main_window.window_diagram as diagram


WIDTH = 1000
HEIGHT = 600


class WindowMain():

    def __init__(self, system):
        self._system = system
        self._root = tkinter.Tk()
        self._root.title('Digital Radio System Simulator')
        self._root.call(
            'wm', 'iconphoto',
            self._root._w,
            tkinter.PhotoImage(file='ui/images/icon.gif')
        )
        self._root.option_add('*tearOff', False)
        # window
        self._window = tkinter.ttk.PanedWindow(
            self._root, orient=tkinter.VERTICAL
        )
        self._window_diagram = diagram.WindowDiagram(system, self)
        self._window_workspace = workspace.WindowWorkspace(system, self)
        self._window.add(self._window_workspace.root, weight=1)
        self._window.add(self._window_diagram.root, weight=1)
        self._window_workspace.render()
        self._system.diagram = self._window_diagram
        # menubar
        menu = tkinter.Menu(self._root)
        self._root.config(menu=menu)
        self.init_menu_simulation(menu, tkinter.Menu(menu))
        self.init_menu_help(menu, tkinter.Menu(menu))
        # key bindings
        self._root.bind('<F1>', self._system.run)
        self._root.bind('<F2>', self.open_system_config)
        self._root.bind('<F3>', self.open_radio_config)
        self._root.bind('<F4>', self.open_channel_config)
        # geometry
        self._window.pack(fill=tkinter.BOTH, expand=True)

    @property
    def window(self):
        return self._window

    @property
    def window_diagram(self):
        return self._window_diagram

    def init_menu_simulation(self, menu, submenu):
        menu.add_cascade(label='Simulation', menu=submenu)
        submenu.add_command(
            label='Run',
            command=self._system.run,
            accelerator='F1'
        )
        submenu.add_separator()
        submenu.add_command(
            label='System Configuration',
            command=self.open_system_config,
            accelerator='F2'
        )
        submenu.add_command(
            label='Radio Configuration',
            command=self.open_radio_config,
            accelerator='F3'
        )
        submenu.add_command(
            label='Channel Configuration',
            command=self.open_channel_config,
            accelerator='F4'
        )

    def init_menu_help(self, menu, submenu):
        menu.add_cascade(label='Help', menu=submenu)
        submenu.add_command(label='About')

    def run(self):
        self._root.mainloop()

    def open_system_config(self, event=None):
        system.WindowSystemConfig(self._system)

    def open_radio_config(self, event=None):
        radio.WindowRadioConfig(self._system)

    def open_channel_config(self, event=None):
        channel.WindowChannelConfig(self._system)

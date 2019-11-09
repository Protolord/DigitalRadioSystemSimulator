import threading
import tkinter
import tkinter.ttk
import ui.config_windows.window_channel_config as cfg_channel
import ui.config_windows.window_radio_config as cfg_radio
import ui.config_windows.window_system_config as cfg_system
import ui.main_window.window_bar as bar
import ui.main_window.window_diagram as diagram
import ui.main_window.window_workspace as workspace


WIDTH = 1000
HEIGHT = 600
PERIODIC_TIMEOUT_MS = 100


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
        self._window_bar = None
        self._system_thread = None
        # menubar
        menu = tkinter.Menu(self._root)
        self._root.config(menu=menu)
        self.init_menu_simulation(menu, tkinter.Menu(menu))
        self.init_menu_help(menu, tkinter.Menu(menu))
        # key bindings
        self._root.bind('<F1>', lambda event=None: self.start_simulation())
        self._root.bind('<F2>', lambda event=None: self.open_system_config())
        self._root.bind('<F3>', lambda event=None: self.open_radio_config())
        self._root.bind('<F4>', lambda event=None: self.open_channel_config())
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
            command=self.start_simulation,
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
        submenu.add_command(
            label='About',
            command=self.open_help
        )

    def run(self):
        self._root.mainloop()

    def start_simulation(self):
        thread_lock = threading.Lock()
        self._window_bar = bar.WindowBar(self._root, self._system)
        self._system_thread = threading.Thread(
            target=self._system.run, args=(self._window_bar, thread_lock)
        )
        self._system_thread.start()
        self._root.after(PERIODIC_TIMEOUT_MS, self.periodic_check)

    def periodic_check(self):
        if self._system.running:
            self._root.after(PERIODIC_TIMEOUT_MS, self.periodic_check)
        else:
            self._system_thread.join()
            self._window_diagram.repeat_render()
            self._window_bar.close()
            self._system_thread = None

    def open_system_config(self):
        cfg_system.WindowSystemConfig(self._root, self._system)

    def open_radio_config(self):
        cfg_radio.WindowRadioConfig(self._system)

    def open_channel_config(self):
        cfg_channel.WindowChannelConfig(self._system)

    def open_help(self):
        pass

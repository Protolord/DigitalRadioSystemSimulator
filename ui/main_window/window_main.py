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
        self._root.call('wm', 'iconphoto', self._root._w, tkinter.PhotoImage(file='ui/images/icon.gif'))
        self._root.option_add('*tearOff', False)
        # window
        self._window = tkinter.ttk.PanedWindow(self._root, orient=tkinter.VERTICAL)
        self._window_workspace = workspace.WindowWorkspace(system, self)
        self._window_diagram = diagram.WindowDiagram(system, self)
        self._window.add(self._window_workspace.frame, weight=1)
        self._window.add(self._window_diagram.window, weight=1)
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
        self._window.pack(fill=tkinter.BOTH, expand=True)

    @property
    def window(self):
        return self._window

    def run(self):
        self._root.mainloop()

    def open_system_config(self, event=None):
        system.WindowSystemConfig(self._system)

    def open_radio_config(self, event=None):
        radio.WindowRadioConfig(self._system)

    def open_channel_config(self, event=None):
        channel.WindowChannelConfig(self._system)

    def open_channel(self, event):
        self._window_diagram.render_channel(event)

    def open_inputbox(self, event, radio_name):
        self._window_diagram.render_inputbox(event, radio_name)

    def open_outputbox(self, event, radio_name):
        self._window_diagram.render_outputbox(event, radio_name)

    def open_bitstream(self, event, radio_name):
        self._window_diagram.render_bitstream(event, radio_name)

    def open_symbolstream(self, event, radio_name):
        self._window_diagram.render_symbolstream(event, radio_name)

    def open_signal(self, event, radio_name):
        self._window_diagram.render_signal(event, radio_name)

    def open_iqmapping(self, event, radio_name):
        self._window_diagram.render_iqmapping(event, radio_name)

    def open_wavetransform(self, event, radio_name):
        self._window_diagram.render_wavetransform(event, radio_name)

import tkinter
import ui.config_windows.window_channel_config as channel
import ui.config_windows.window_radio_config as radio
import ui.config_windows.window_system_config as system


class WindowMain():

    def __init__(self, system):
        self._system = system
        self._root = tkinter.Tk()
        self._root.title('Digital Radio System Simulator')
        self._root.call('wm', 'iconphoto', self._root._w, tkinter.PhotoImage(file='ui/images/icon.gif'))
        self._root.option_add('*tearOff', False)
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

    def run(self):
        self._root.mainloop()

    def open_system_config(self, event=None):
        system.WindowSystemConfig(self._system)

    def open_radio_config(self, event=None):
        radio.WindowRadioConfig(self._system)

    def open_channel_config(self, event=None):
        channel.WindowChannelConfig(self._system)
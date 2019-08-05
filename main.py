import ui.window_main as ui
import core.system as core
from core.channel.channel import Channel

def main():
    system = core.System()
    window = ui.WindowMain(system)
    window.run()

if __name__ == "__main__":
    main()
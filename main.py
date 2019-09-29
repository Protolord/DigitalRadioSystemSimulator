import ui.window_main as ui
import core.system as core

def main():
    system = core.System()
    window = ui.WindowMain(system)
    window.run()

if __name__ == '__main__':
    main()
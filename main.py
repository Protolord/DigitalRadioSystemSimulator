import core.system as core
import ui.main_window.window_main as ui

def main():
    system = core.System()
    window = ui.WindowMain(system)
    window.run()

if __name__ == '__main__':
    main()
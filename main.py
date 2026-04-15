import sys


def run_test():
    print("Test mode")
    with open("log.txt", "w") as f:
        f.write("Test OK")
    exit(0)


def main_gui():
    from ui import gui
    app = gui.MyApp()
    app.mainloop()


if __name__ == "__main__":
    if "--test" in sys.argv:
        run_test()
    else:
        main_gui()
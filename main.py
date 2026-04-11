import sys
from ui import gui


def run_test():
    print("Test mode")
    with open("log.txt", "w") as f:
        f.write("Test OK")


def main():
    app = gui.MyApp()
    app.mainloop()


if __name__ == "__main__":
    if "--test" in sys.argv:
        run_test()
    main()

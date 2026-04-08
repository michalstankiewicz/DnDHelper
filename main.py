import gui
# added for testing purposes, to check if the application starts without errors. Run "python main.py --test" to execute this test.
import sys
if "--test" in sys.argv:
    print("Breaking in so we can break out")
    with open("log.txt", "w") as f:
        f.write("Test log\n")
    exit(0)

# this is the main file which will start whole program.
if __name__ == "__main__":
    app = gui.MyApp()
    app.mainloop()

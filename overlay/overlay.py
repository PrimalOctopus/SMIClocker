import tkinter as tk

class Window:
    def __init__(self, width = 300, height = 200):
        #Initialise window
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.configure(bg="black")
        #self.root.geometry(f"{width}x{height}")

        #Make window transparent
        self.root.wait_visibility(self.root)
        self.root.wm_attributes('-alpha',0.5)
        self.root.update()

    def update(self):
        self.root.update()

    def add_text(self, text, size = 25):
        label = tk.Label(self.root, text=text, fg="yellow", bg="black", font=("Arial", size))
        label.pack()
        self.root.update()
        #print(f"added text {text}")
        return label

    def change_text(self, label, text):
        label.config(text=text)
        self.root.update()
import tkinter as tk
from tkinter import messagebox
from unittest import result
import dice
import loot
import ecounter


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DnD Helper")
        self.geometry("860x480")
        self.create_widgets()

    def create_widgets(self):
        # buttons
        self.encounter_button = tk.Button(
            self, text="Generate Encounter", command=self.generate_encounter)
        self.encounter_button.pack(pady=10)

        self.loot_button = tk.Button(
            self, text="Generate Loot", command=self.loot_generator)
        self.loot_button.pack(pady=10)

        # dice sides and frame for dice buttons
        dice_sides = [4, 6, 8, 10, 12, 20]
        frame = tk.Frame(self)
        frame.pack(pady=10)

        for side in dice_sides:
            btn = tk.Button(
                frame, text=f"d{side}", command=lambda s=side: self.roll_dice(s))
            btn.pack(side=tk.LEFT, padx=5)
        # encouter listbox
        encounter_frame = tk.Frame(self)
        encounter_frame.pack(pady=10)
        self.encounter_listbox = tk.Listbox(
            encounter_frame, width=100, height=10)
        self.encounter_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # loot listbox
        loot_frame = tk.Frame(self)
        loot_frame.pack(pady=10)
        self.loot_listbox = tk.Listbox(
            loot_frame, width=100, height=10)
        self.loot_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def roll_dice(self, sides):
        result = dice.roll_dice(sides)
        messagebox.showinfo("Dice Roll", f"Wypadło: {result} (d{sides})")

    def generate_encounter(self):
        self.encounter_listbox.delete(0, tk.END)  # usuwa poprzedni wpis
        enc = ecounter.generate_encounter()
        self.encounter_listbox.insert(
            tk.END, f"{enc['name']} ({enc['type']}, difficulty {enc['difficulty']})"
        )

    def loot_generator(self):
        self.loot_listbox.delete(0, tk.END)  # usuwa poprzedni wpis
        lt = loot.generate_loot()
        self.loot_listbox.insert(
            tk.END, f"{lt['name']} value {lt['value']} gold, rarity {lt['rarity']})"
        )

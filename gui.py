import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
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
        # tabs initialization
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill=tk.BOTH, expand=True)

        # DICE
        self.tabDice = ttk.Frame(self.tabs)
        self.tabs.add(self.tabDice, text="Dice")
        dice_sides = [4, 6, 8, 10, 12, 20]
        frame_dice = tk.Frame(self.tabDice)
        frame_dice.pack(pady=10)

        for side in dice_sides:
            btn = tk.Button(
                frame_dice, text=f"d{side}", command=lambda s=side: self.roll_dice(s))
            btn.pack(side=tk.LEFT, padx=5)

        # ENCOUNTER
        self.tabEncLoot = ttk.Frame(self.tabs)
        self.tabs.add(self.tabEncLoot, text="Encounters and Loot Generator")
        self.encounter_button = tk.Button(
            self.tabEncLoot, text="Generate Encounter", command=self.generate_encounter)
        self.encounter_button.pack(pady=10)
        encounter_frame = tk.Frame(self.tabEncLoot)
        encounter_frame.pack(pady=10)
        self.encounter_listbox = tk.Listbox(
            encounter_frame, width=100, height=10)
        self.encounter_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # LOOT
        self.loot_button = tk.Button(
            self.tabEncLoot, text="Generate Loot", command=self.loot_generator)
        self.loot_button.pack(pady=10)
        loot_frame = tk.Frame(self.tabEncLoot)
        loot_frame.pack(pady=10)
        self.loot_listbox = tk.Listbox(
            loot_frame, width=100, height=10)
        self.loot_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Functions used in program

    def roll_dice(self, sides):
        result = dice.roll_dice(sides)
        messagebox.showinfo("Dice Roll", f"Wypadło: {result} (d{sides})")

    def generate_encounter(self):
        self.encounter_listbox.delete(0, tk.END)  # clear previous encounters
        # we are using _ because we don't care about the loop variable, we just want to repeat 4 times
        # generate 4 encounters and add them to the listbox
        for _ in range(4):
            enc = ecounter.generate_encounter()
            # if we get is_monster true, we format the text as a monster, otherwise as an adventure
            if enc.get("is_monster"):
                text = f"[MONSTER] {enc['name']} ({enc['type']}, CR {enc['cr']}, str. {enc['page']})"
            else:
                text = f"[ADVENTURE] {enc['name']} (difficulty: {enc['difficulty']}, {enc['description']})"
            self.encounter_listbox.insert(tk.END, text)
    # i added generate loot function, which will generate 6 items of loot and add them to the loot listbox

    def loot_generator(self):
        self.loot_listbox.delete(0, tk.END)  # clear previous loot
        for _ in range(6):
            lt = loot.generate_loot()
            self.loot_listbox.insert(
                tk.END, f"{lt['name']} value {lt['value']} of gold, rarity {lt['rarity']}, description: {lt['description']}"
            )

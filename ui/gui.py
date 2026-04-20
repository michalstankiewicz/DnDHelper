import tkinter as tk
from tkinter import ttk
import logic.dice as dice
import logic.loot as loot
import logic.encounter as encounter
import logic.spells as spells
import logic.npc as npc
import logic.city_gen as city
import re

# creating helper for gui


def create_scrollable_listbox(parent, width=100, height=10, font=("Consolas", 10)):
    frame = tk.Frame(parent)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(
        frame,
        width=width,
        height=height,
        font=font,
        yscrollcommand=scrollbar.set
    )

    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar.config(command=listbox.yview)

    return frame, listbox


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RPG Helper")
        self.geometry("860x640")
        # tracker to store items already rolled
        self.used_encounters = set()
        self.used_loots = set()
        self.used_npcs = set()
        self.used_city = set()
        self.create_widgets()

    def create_widgets(self):
        """Widgets for the application"""
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill=tk.BOTH, expand=True)

        # DICE
        self.tabDice = ttk.Frame(self.tabs)
        self.tabs.add(self.tabDice, text="Dice")
        dice_sides = [4, 6, 8, 10, 12, 20, 100]
        frame_dice = tk.Frame(self.tabDice)
        frame_dice.pack(pady=10)
        self.dice_result_label = tk.Label(
            self.tabDice, text="Roll a die to see the result")
        self.dice_result_label.pack(pady=10)

        for side in dice_sides:
            btn = tk.Button(
                frame_dice, text=f"d{side}", command=lambda s=side: self.roll_dice(s))
            btn.pack(side=tk.LEFT, padx=5)

        self.dice_entry = tk.Entry(self.tabDice)
        self.dice_entry.pack(pady=5)

        self.roll_multiple_button = tk.Button(
            self.tabDice, text="Roll Multiple Dice", command=self.roll_multi_dice)
        self.roll_multiple_button.pack(pady=5)

        # SPELLS_SRD_2014
        self.tabSpells = ttk.Frame(self.tabs)
        self.tabs.add(self.tabSpells, text="Spells SRD 2014")
        # Search frame for spells
        search_frame = tk.Frame(self.tabSpells)
        search_frame.pack(pady=10)
        # Label + Entry Level
        tk.Label(search_frame, text="Lvl").grid(row=0, column=0, padx=2)
        self.spell_level_entry = tk.Entry(search_frame, width=3)
        self.spell_level_entry.grid(row=1, column=0, padx=2)
        # Label + Entry Name
        tk.Label(search_frame, text="Name").grid(row=0, column=1, padx=2)
        self.spell_search_entry = tk.Entry(search_frame)
        self.spell_search_entry.grid(row=1, column=1, padx=2)
        # Search button
        self.spell_search_button = tk.Button(
            search_frame, text="Search", command=self.search_spells)
        self.spell_search_button.grid(row=1, column=2, padx=5)
        self.spell_search_button.config(width=10)
        # Listbox for spells
        self.spell_listbox = tk.Listbox(
            self.tabSpells, width=100, height=20)
        self.spell_listbox.pack(pady=5)
        # Description box for selected spell
        self.spell_desc_text = tk.Text(
            self.tabSpells, width=100, height=5, wrap=tk.WORD)
        self.spell_desc_text.pack(pady=5)
        # Display all spells at start
        self.all_spells = spells.load_spell_json()
        self.filtered_spells = self.all_spells.copy()
        self.update_spell_listbox(self.filtered_spells)
        # Bind selection event to show spell description
        self.spell_listbox.bind("<<ListboxSelect>>",
                                self.show_selected_spell_desc)

        # ENCOUNTER
        self.tabEncLoot = ttk.Frame(self.tabs)
        self.tabs.add(self.tabEncLoot, text="Encounters and Loot Generator")
        self.encounter_button = tk.Button(
            self.tabEncLoot, text="Generate Encounter", command=self.generate_encounter)
        self.encounter_button.pack(pady=10)
        encounter_frame, self.encounter_listbox = create_scrollable_listbox(
            self.tabEncLoot)
        encounter_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # LOOT
        self.loot_button = tk.Button(
            self.tabEncLoot, text="Generate Loot", command=self.loot_generator)
        self.loot_button.pack(pady=10)

        loot_frame, self.loot_listbox = create_scrollable_listbox(
            self.tabEncLoot)
        loot_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # NPC
        self.tabnpc = ttk.Frame(self.tabs)
        self.tabs.add(self.tabnpc, text="NPC")
        self.npc_button = tk.Button(
            self.tabnpc, text="Generate", command=self.generate_npc)
        self.npc_button.pack(pady=10)
        npc_frame, self.npc_listbox = create_scrollable_listbox(self.tabnpc)
        npc_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # CITY
        city_names = city.get_available_city_names()
        self.tabCity = ttk.Frame(self.tabs)
        self.tabs.add(self.tabCity, text="City")
        self.city_button = tk.Button(
            self.tabCity, text="Generate", command=self.generate_city)
        self.city_button.pack(pady=10)
        self.city_selector = ttk.Combobox(
            self.tabCity, state="readonly", values=city_names)
        self.city_selector.current(0)
        self.city_selector.pack(pady=5)
        self.city_selector.pack(pady=5)
        city_frame, self.city_listbox = create_scrollable_listbox(self.tabCity)
        city_frame.pack(fill=tk.BOTH, expand=True, pady=10)
####################################################################################

    # Functions used in program
    # DICE
    def roll_dice(self, sides):
        rolls, total = dice.roll_multiple_dice(1, sides)
        self.dice_result_label.config(
            text=f"Rolled a d{sides}: {rolls[0]} (Total: {total})")

    def roll_multi_dice(self):
        user_input = self.dice_entry.get()
        try:
            rolls, total = dice.roll_from_string(user_input)
            self.dice_result_label.config(
                text=f"Rolls: {rolls} | Total: {total} ({user_input})"
            )
        except ValueError as e:
            self.dice_result_label.config(text=f"Error: {str(e)}")

    # ENCOUNTER AND LOOT
    def generate_encounter(self):
        """Generate 8 Adventure/Encounter without duplo"""
        self.encounter_listbox.delete(0, tk.END)
        enc_count = 0
        while enc_count < 6:

            enc = encounter.generate_encounter()  # Zwraca dict
            enc_key = (enc.get("name"), enc.get("type", "adventure"))

            if enc_key in self.used_encounters:
                continue

            self.used_encounters.add(enc_key)

            if enc.get("is_monster"):
                text = f"[MONSTER] {enc['name']} ({enc['type']}, CR {enc['cr']}, str. {enc['description']})"
            else:
                text = f"[ADVENTURE] {enc['name']} (difficulty: {enc['difficulty']}, {enc['description']})"
            self.encounter_listbox.insert(tk.END, text)
            enc_count += 1

    def loot_generator(self):
        """Generate loot without duplicate item in the list."""
        self.loot_listbox.delete(0, tk.END)
        loot_count = 0
        while loot_count < 6:
            lt = loot.generate_loot()
            loot_key = (lt.get("name"), lt.get("rarity"))

            if loot_key in self.used_loots:
                continue

            self.used_loots.add(loot_key)

            self.loot_listbox.insert(
                tk.END, f"{lt['name']} value {lt['value']} of gold, rarity {lt['rarity']}, description: {lt['description']}"
            )
            loot_count += 1

# Npc Generator
    def generate_npc(self):
        self.npc_listbox.delete(0, tk.END)

        npc_count = 0
        while npc_count < 6:
            npclist = npc.generate_npc()

            key = (npclist["name"], npclist["surname"], npclist["race"])

            if key in self.used_npcs:
                continue

            self.used_npcs.add(key)

            self.npc_listbox.insert(
                tk.END,
                f"|{npclist['name']} {npclist['surname']} | "
                f"|{npclist['race']} {npclist['gender']} | "
                f"|{npclist['trait']} | {npclist['hook']} | "
            )
            npc_count += 1

    # City Generator
    def generate_city(self):
        self.city_listbox.delete(0, tk.END)
        city_count = 0

        city_name = self.city_selector.get()
        while city_count < 6:
            city_list = city.generate_city(city_name)

            key = (
                city_list["city"],
                tuple(city_list["problems"]),
                tuple(city_list["goods"]),
                tuple(city_list["superstitions"])
            )

            if key in self.used_city:
                continue

            self.used_city.add(key)
            city_count += 1

        result = city.generate_city(city_name)

        self.city_listbox.insert(tk.END, f"[CITY] {result['city']}")
        self.city_listbox.insert(tk.END, "")

        self.city_listbox.insert(tk.END, "PROBLEMS:")
        for p in result["problems"]:
            self.city_listbox.insert(tk.END, f"- {p}")

        self.city_listbox.insert(tk.END, "")

        self.city_listbox.insert(tk.END, "GOODS:")
        for g in result["goods"]:
            self.city_listbox.insert(tk.END, f"- {g}")

        self.city_listbox.insert(tk.END, "")

        self.city_listbox.insert(tk.END, "SUPERSTITIONS:")
        for s in result["superstitions"]:
            self.city_listbox.insert(
                tk.END, f"- {s}")

    # SPELLS!
    # Function to show selected spell by user (description, etc from jsonq, triggered by event of selecting spell in listbox)

    def show_selected_spell_desc(self, event):
        selection = self.spell_listbox.curselection()
        if selection:
            idx = selection[0]
            spell = self.filtered_spells[idx]
            self.spell_desc_text.delete("1.0", tk.END)
            self.spell_desc_text.insert(
                tk.END, spell.get('description', 'No description'))

    # Search function for spells, triggered by search button, filters spells based on name and level, updates listbox with results
    def search_spells(self):
        name_filter = self.spell_search_entry.get().lower()
        level_val = self.spell_level_entry.get() if self.spell_level_entry else ""

        self.filtered_spells = []

        for s in self.all_spells:
            if name_filter and not re.search(re.escape(name_filter), s['name'], re.IGNORECASE):
                continue
            if level_val:
                try:
                    if int(level_val) != s.get('level', 0):
                        continue
                except ValueError:
                    continue
            self.filtered_spells.append(s)

        self.update_spell_listbox(self.filtered_spells)

    # Update listbox with filtered spells, called after search to refresh the displayed spells based on filters
    def update_spell_listbox(self, spells_list):
        self.spell_listbox.delete(0, tk.END)
        for s in spells_list:
            self.spell_listbox.insert(
                tk.END,
                f"{s['name']} | Level: {s.get('level')} | Classes: {', '.join(s.get('classes', []))}"
            )

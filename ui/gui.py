import tkinter as tk
from tkinter import ttk
import logic.dice as dice
import logic.loot as loot
import logic.magic_items as magic_items
import logic.encounter as encounter
import logic.weather_encounter_generator as weather_encounter
import logic.spell_scroll_generator as scroll_generator
import logic.spells as spells
import logic.npc as npc
import logic.city_gen as city
import re


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
        self.geometry("860x800")
        self.used_encounters = set()
        self.used_loots = set()
        self.used_magic_items = set()
        self.used_npcs = set()
        self.used_city = set()
        self.current_encounter_cr = None
        self.create_widgets()

    def create_widgets(self):
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
        search_frame = tk.Frame(self.tabSpells)
        search_frame.pack(pady=10)
        tk.Label(search_frame, text="Lvl").grid(row=0, column=0, padx=2)
        self.spell_level_entry = tk.Entry(search_frame, width=3)
        self.spell_level_entry.grid(row=1, column=0, padx=2)
        tk.Label(search_frame, text="Name").grid(row=0, column=1, padx=2)
        self.spell_search_entry = tk.Entry(search_frame)
        self.spell_search_entry.grid(row=1, column=1, padx=2)
        self.spell_search_button = tk.Button(
            search_frame, text="Search", command=self.search_spells)
        self.spell_search_button.grid(row=1, column=2, padx=5)
        self.spell_search_button.config(width=10)
        self.spell_listbox = tk.Listbox(
            self.tabSpells, width=100, height=20)
        self.spell_listbox.pack(pady=5)
        self.spell_desc_text = tk.Text(
            self.tabSpells, width=100, height=5, wrap=tk.WORD)
        self.spell_desc_text.pack(pady=5)
        self.all_spells = spells.load_spell_json()
        self.filtered_spells = self.all_spells.copy()
        self.update_spell_listbox(self.filtered_spells)
        self.spell_listbox.bind("<<ListboxSelect>>",
                                self.show_selected_spell_desc)

        # SPELL SCROLL GENERATOR
        self.tabSpellScroll = ttk.Frame(self.tabs)
        self.tabs.add(self.tabSpellScroll, text="Spell Scroll")
        scroll_frame = tk.Frame(self.tabSpellScroll)
        scroll_frame.pack(pady=10)

        tk.Label(scroll_frame, text="Class:").grid(row=0, column=0, padx=2)
        class_options = scroll_generator._spell_scroll_generator_instance.get_classes_list()
        self.scroll_class_selector = ttk.Combobox(
            scroll_frame, state="readonly", values=class_options, width=18)
        if class_options:
            self.scroll_class_selector.current(0)
        self.scroll_class_selector.grid(row=1, column=0, padx=2)

        self.roll_level_button = tk.Button(
            scroll_frame, text="Roll 1d9 Level", command=self.roll_spell_scroll_level)
        self.roll_level_button.grid(row=0, column=1, rowspan=2, padx=5)

        self.scroll_level_label = tk.Label(scroll_frame, text="Level roll: -")
        self.scroll_level_label.grid(row=0, column=2, padx=5)
        self.scroll_spells_count_label = tk.Label(
            scroll_frame, text="Available spells: -")
        self.scroll_spells_count_label.grid(row=1, column=2, padx=5)

        self.generate_scroll_button = tk.Button(
            scroll_frame, text="Generate Scroll", command=self.generate_spell_scroll)
        self.generate_scroll_button.grid(row=0, column=3, rowspan=2, padx=5)

        self.scroll_result_text = tk.Text(
            self.tabSpellScroll, width=100, height=15, wrap=tk.WORD)
        self.scroll_result_text.pack(pady=10)

        self.scroll_level_value = None
        self.scroll_available_spells = 0
        self.scroll_selected_class = None

        # ENCOUNTER + LOOT
        self.tabEncounter = ttk.Frame(self.tabs)
        self.tabs.add(self.tabEncounter, text="Encounters and Loot")

        # Top frame - Encounter generation
        self.encounter_button = tk.Button(
            self.tabEncounter, text="Generate Encounters", command=self.generate_encounter)
        self.encounter_button.pack(pady=10)

        weather_frame = tk.Frame(self.tabEncounter)
        weather_frame.pack(pady=5)

        self.weather_button = tk.Button(
            weather_frame, text="Generate Weather Encounter", command=self.generate_weather_encounter)
        self.weather_button.pack(side=tk.LEFT, padx=3)

        weather_types = weather_encounter.get_available_weather_types()
        self.weather_type_selector = ttk.Combobox(
            weather_frame, state="readonly", values=weather_types, width=18)
        if weather_types:
            self.weather_type_selector.current(0)
        self.weather_type_selector.pack(side=tk.LEFT, padx=3)

        self.weather_type_button = tk.Button(
            weather_frame, text="Generate Selected Weather", command=self.generate_selected_weather_encounter)
        self.weather_type_button.pack(side=tk.LEFT, padx=3)

        weather_options_frame = tk.Frame(self.tabEncounter)
        weather_options_frame.pack(pady=5)

        self.blizzard_button = tk.Button(
            weather_options_frame, text="Blizzard Encounter", command=self.generate_blizzard_encounter)
        self.blizzard_button.pack(side=tk.LEFT, padx=3)

        self.whiteout_button = tk.Button(
            weather_options_frame, text="Whiteout Encounter", command=self.generate_whiteout_encounter)
        self.whiteout_button.pack(side=tk.LEFT, padx=3)

        self.ice_storm_button = tk.Button(
            weather_options_frame, text="Ice Storm Encounter", command=self.generate_ice_storm_encounter)
        self.ice_storm_button.pack(side=tk.LEFT, padx=3)

        danger_frame = tk.Frame(self.tabEncounter)
        danger_frame.pack(pady=5)

        tk.Label(danger_frame, text="Danger Level:").pack(side=tk.LEFT, padx=3)
        self.danger_selector = ttk.Combobox(
            danger_frame, state="readonly", values=[1, 2, 3, 4, 5], width=3)
        self.danger_selector.current(0)
        self.danger_selector.pack(side=tk.LEFT, padx=3)

        self.danger_button = tk.Button(
            danger_frame, text="Generate Danger Encounter", command=self.generate_danger_level_encounter)
        self.danger_button.pack(side=tk.LEFT, padx=3)

        tk.Label(self.tabEncounter, text="Encounters:", font=(
            "Consolas", 10, "bold")).pack(anchor=tk.W, padx=10)
        encounter_frame, self.encounter_listbox = create_scrollable_listbox(
            self.tabEncounter, height=12)
        encounter_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.encounter_listbox.bind(
            "<<ListboxSelect>>", self.on_encounter_selected)

        # Bottom frame - Treasure/Loot
        tk.Label(self.tabEncounter, text="Treasure:", font=(
            "Consolas", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(10, 0))
        treasure_frame, self.treasure_listbox = create_scrollable_listbox(
            self.tabEncounter, height=12)
        treasure_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

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
        city_frame, self.city_listbox = create_scrollable_listbox(self.tabCity)
        city_frame.pack(fill=tk.BOTH, expand=True, pady=10)

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

    # ENCOUNTER+LOOT
    def generate_encounter(self):
        self.encounter_listbox.delete(0, tk.END)
        self.treasure_listbox.delete(0, tk.END)
        self.used_encounters.clear()
        enc_count = 0

        while enc_count < 6:
            enc = encounter.generate_encounter()
            enc_key = (enc.get("name"), enc.get("type", "adventure"))

            if enc_key in self.used_encounters:
                continue

            self.used_encounters.add(enc_key)
            text = f"[CR {enc['cr']}] {enc['name']} ({enc['type']}) - {enc['description']}"
            self.encounter_listbox.insert(tk.END, text)
            enc_count += 1

    def generate_weather_encounter(self):
        self._clear_encounter_selection()
        enc_result = weather_encounter.generate_weather_encounter()
        encounter_data = enc_result["encounter"]
        weather_data = enc_result["weather"]
        text = (
            f"[Weather: {weather_data.get('weather_type')} | Intensity: {weather_data.get('intensity')} | "
            f"CR {encounter_data.get('cr')} | Adj {enc_result.get('adjusted_cr', 0):.1f}] "
            f"{encounter_data.get('name')} ({encounter_data.get('type')}) - {encounter_data.get('description')}"
        )
        self.encounter_listbox.insert(tk.END, text)

    def generate_selected_weather_encounter(self):
        weather_type = self.weather_type_selector.get() or None
        if not weather_type:
            self.generate_weather_encounter()
            return
        self._clear_encounter_selection()
        enc_result = weather_encounter.generate_weather_encounter(weather_type)
        encounter_data = enc_result["encounter"]
        weather_data = enc_result["weather"]
        text = (
            f"[Weather: {weather_data.get('weather_type')} | Intensity: {weather_data.get('intensity')} | "
            f"CR {encounter_data.get('cr')} | Adj {enc_result.get('adjusted_cr', 0):.1f}] "
            f"{encounter_data.get('name')} ({encounter_data.get('type')}) - {encounter_data.get('description')}"
        )
        self.encounter_listbox.insert(tk.END, text)

    def generate_blizzard_encounter(self):
        self._clear_encounter_selection()
        enc_result = weather_encounter.generate_blizzard_encounter()
        encounter_data = enc_result["encounter"]
        weather_data = enc_result["weather"]
        text = (
            f"[Blizzard | CR {encounter_data.get('cr')} | Adj {enc_result.get('adjusted_cr', 0):.1f}] "
            f"{encounter_data.get('name')} ({encounter_data.get('type')}) - {encounter_data.get('description')}"
        )
        self.encounter_listbox.insert(tk.END, text)

    def generate_whiteout_encounter(self):
        self._clear_encounter_selection()
        enc_result = weather_encounter.generate_whiteout_encounter()
        encounter_data = enc_result["encounter"]
        weather_data = enc_result["weather"]
        text = (
            f"[Whiteout | CR {encounter_data.get('cr')} | Adj {enc_result.get('adjusted_cr', 0):.1f}] "
            f"{encounter_data.get('name')} ({encounter_data.get('type')}) - {encounter_data.get('description')}"
        )
        self.encounter_listbox.insert(tk.END, text)

    def generate_ice_storm_encounter(self):
        self._clear_encounter_selection()
        enc_result = weather_encounter.generate_ice_storm_encounter()
        encounter_data = enc_result["encounter"]
        text = (
            f"[Ice Storm | CR {encounter_data.get('cr')} | Adj {enc_result.get('adjusted_cr', 0):.1f}] "
            f"{encounter_data.get('name')} ({encounter_data.get('type')}) - {encounter_data.get('description')}"
        )
        self.encounter_listbox.insert(tk.END, text)

    def generate_danger_level_encounter(self):
        self._clear_encounter_selection()
        danger_level = int(self.danger_selector.get())
        enc_result = weather_encounter.generate_encounter_by_danger_level(
            danger_level)
        encounter_data = enc_result["encounter"]
        weather_data = enc_result["weather"]
        text = (
            f"[Danger {danger_level} | Weather: {weather_data.get('weather_type')} | "
            f"CR {encounter_data.get('cr')} | Adj {enc_result.get('adjusted_cr', 0):.1f}] "
            f"{encounter_data.get('name')} ({encounter_data.get('type')}) - {encounter_data.get('description')}"
        )
        self.encounter_listbox.insert(tk.END, text)

    def _clear_encounter_selection(self):
        self.encounter_listbox.delete(0, tk.END)
        self.treasure_listbox.delete(0, tk.END)
        self.used_encounters.clear()
        self.current_encounter_cr = None

    def on_encounter_selected(self, event):
        """Called when an encounter is selected from the listbox. Extracts the CR and generates appropriate treasure."""
        selection = self.encounter_listbox.curselection()
        if selection:
            idx = selection[0]
            enc_text = self.encounter_listbox.get(idx)

            # Extract CR from text: "[CR X] ..." and support float values
            match = re.search(r"\[CR\s*([0-9]+(?:\.[0-9]+)?)\]", enc_text)
            if match:
                try:
                    cr_value = float(match.group(1))
                except ValueError:
                    cr_value = 0.0
            else:
                cr_value = 0.0

            self.current_encounter_cr = cr_value
            self.generate_treasure()

    def generate_treasure(self):
        if self.current_encounter_cr is None:
            self.treasure_listbox.delete(0, tk.END)
            self.treasure_listbox.insert(tk.END, "Select an encounter first")
            return

        self.treasure_listbox.delete(0, tk.END)
        self.used_loots.clear()
        self.used_magic_items.clear()

        cr = self.current_encounter_cr

        # CR > 6 = Magic items; CR <= 6 = Loot
        if cr > 6:
            self.treasure_listbox.insert(
                tk.END, f"[CR {cr}] Magic Items Treasure:")
            self.treasure_listbox.insert(tk.END, "")

            magic_count = 0
            while magic_count < 4:
                mi = magic_items.generate_magic_items()
                mi_key = (mi.get("name"), mi.get("rarity"))

                if mi_key in self.used_magic_items:
                    continue

                self.used_magic_items.add(mi_key)
                self.treasure_listbox.insert(
                    tk.END, f"[{mi['rarity'].upper()}] {mi['name']}")
                self.treasure_listbox.insert(
                    tk.END, f"  {mi['description']}")
                self.treasure_listbox.insert(
                    tk.END, f"  Effect: {mi['effect']}")
                self.treasure_listbox.insert(tk.END, "")
                magic_count += 1
        else:
            self.treasure_listbox.insert(tk.END, f"[CR {cr}] Standard Loot:")
            self.treasure_listbox.insert(tk.END, "")

            loot_count = 0
            while loot_count < 4:
                lt = loot.generate_loot()
                loot_key = (lt.get("name"), lt.get("rarity"))

                if loot_key in self.used_loots:
                    continue

                self.used_loots.add(loot_key)
                self.treasure_listbox.insert(
                    tk.END, f"[{lt['rarity'].upper()}] {lt['name']}")
                self.treasure_listbox.insert(
                    tk.END, f"  Value: {lt['value']} gp")
                self.treasure_listbox.insert(
                    tk.END, f"  {lt['description']}")
                self.treasure_listbox.insert(tk.END, "")
                loot_count += 1

    # NPC
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

    # CITY
    def generate_city(self):
        self.city_listbox.delete(0, tk.END)
        self.used_city.clear()

        city_name = self.city_selector.get()
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

    # SPELLS
    def show_selected_spell_desc(self, event):
        selection = self.spell_listbox.curselection()
        if selection:
            idx = selection[0]
            spell = self.filtered_spells[idx]
            self.spell_desc_text.delete("1.0", tk.END)
            self.spell_desc_text.insert(
                tk.END, spell.get('description', 'No description'))

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

    def roll_spell_scroll_level(self):
        class_name = self.scroll_class_selector.get()
        if not class_name:
            self.scroll_result_text.delete("1.0", tk.END)
            self.scroll_result_text.insert(tk.END, "Select a class first.")
            return

        self.scroll_selected_class = class_name
        level_roll = dice.roll_dice(9)
        if class_name.lower() in ("czarnoksiężnik", "warlock"):
            level_roll = min(level_roll, 5)

        spells_at_level = scroll_generator._spell_scroll_generator_instance.get_spells_by_level_and_class(
            level_roll, class_name)
        spells_count = len(spells_at_level)

        self.scroll_level_value = level_roll
        self.scroll_available_spells = spells_count
        self.scroll_level_label.config(text=f"Level roll: {level_roll}")
        self.scroll_spells_count_label.config(
            text=f"Available spells: {spells_count}")

        self.scroll_result_text.delete("1.0", tk.END)
        if spells_count == 0:
            self.scroll_result_text.insert(
                tk.END,
                f"No spells found for class {class_name} at level {level_roll}.\nPress the button again to reroll."
            )
        else:
            self.scroll_result_text.insert(
                tk.END,
                f"Rolled 1d9 = {level_roll}.\nFound {spells_count} spells for {class_name} at that level.\n"
                f"Press Generate Scroll to roll d{spells_count} and choose one spell."
            )

    def generate_spell_scroll(self):
        class_name = self.scroll_class_selector.get()
        if not class_name:
            self.scroll_result_text.delete("1.0", tk.END)
            self.scroll_result_text.insert(tk.END, "Select a class first.")
            return

        if self.scroll_selected_class != class_name:
            self.scroll_level_value = None
            self.scroll_available_spells = 0
            self.scroll_selected_class = None

        if self.scroll_level_value is None:
            self.roll_spell_scroll_level()
            if self.scroll_available_spells == 0:
                return

        if self.scroll_available_spells == 0:
            self.scroll_result_text.delete("1.0", tk.END)
            self.scroll_result_text.insert(
                tk.END,
                "There are no spells for the selected class and rolled level. Reroll 1d9 first."
            )
            return

        try:
            spells_at_level = scroll_generator._spell_scroll_generator_instance.get_spells_by_level_and_class(
                self.scroll_level_value, class_name)
            spell_roll = dice.roll_dice(self.scroll_available_spells)
            selected_spell = spells_at_level[spell_roll - 1]

            self.scroll_result_text.delete("1.0", tk.END)
            self.scroll_result_text.insert(tk.END,
                                           f"Class: {class_name}\n"
                                           f"Rolled level (1d9): {self.scroll_level_value}\n"
                                           f"Available spells at this level: {self.scroll_available_spells}\n"
                                           f"Selected spell roll (d{self.scroll_available_spells}): {spell_roll}\n\n"
                                           f"Name: {selected_spell.get('name')}\n"
                                           f"Level: {selected_spell.get('level', 0)}\n"
                                           f"School: {selected_spell.get('school', 'unknown')}\n"
                                           f"Classes: {', '.join(selected_spell.get('classes', []))}\n"
                                           f"Range: {selected_spell.get('range', 'Unknown')}\n"
                                           f"Duration: {selected_spell.get('duration', '')}\n"
                                           f"Concentration: {selected_spell.get('concentration', False)}\n"
                                           f"Ritual: {selected_spell.get('ritual', False)}\n\n"
                                           f"Description:\n{selected_spell.get('description', '')}"
                                           )
        except Exception as e:
            self.scroll_result_text.delete("1.0", tk.END)
            self.scroll_result_text.insert(tk.END, f"Error: {e}")

    def update_spell_listbox(self, spells_list):
        self.spell_listbox.delete(0, tk.END)
        for s in spells_list:
            self.spell_listbox.insert(
                tk.END,
                f"{s['name']} | Level: {s.get('level')} | Classes: {', '.join(s.get('classes', []))}"
            )


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()

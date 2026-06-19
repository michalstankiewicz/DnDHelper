# DnD Helper – SRD Spells Module

## Overview
This module provides structured spell data for a Dungeons & Dragons 5e helper tool.  
It is intended for use in gameplay tools, UI applications, and procedural generation systems.

The project focuses on fast access, filtering, and integration with game-related systems (e.g. search, tabs, build tools).

---

## Features

### Core Generators
- **Encounter Generator**: Random encounters with Challenge Rating
- **Weather-Based Encounters**: Encounters modified by weather conditions (blizzards, storms, etc.)
- **Loot Generator**: Random treasure with multiple filtering options:
  - By category (weapons, armor, magical items)
  - By rarity (common, uncommon, rare, very rare, legendary)
  - By type (weapon, armor, scroll, potion, etc.)
  - CR-based treasure (Dungeon Master's Guide compliant)
  - Complete treasure hoards with gold, gems, and magic items
- **Spell Scroll Generator**: Generate spellcasting items for all 6 classes:
  - Wizard (Mag)
  - Sorcerer (Czarownik)
  - Cleric (Kleryk)
  - Druid
  - Bard
  - Warlock (Czarnoksiężnik)
- **NPC Generator**: Generate random NPCs with:
  - Random race/gender
  - Name + surname generation
  - Personality traits
  - Story hooks and motivations
- **City Generator**: Generate Ten-Towns settlements with problems/goods/superstitions
- **Magic Items Generator**: Random magical artifacts
- **Dice Roller**: D&D dice rolling system (kdX format)

### Data Features
- Structured SRD spell dataset (JSON format)
- Search-friendly fields (name, level, class, school, etc.)
- Ready for integration with GUI / CLI tools
- Lightweight static data usage (no runtime API dependency)
- Extended with custom game hooks and localized content
- **Winter/Arctic themed**: All encounters, NPCs, and loot themed around Icewind Dale

---

## Data Files

### Core Data
- **spells.json**: 300+ D&D 5e SRD spells with full metadata
- **encounter.json**: 145+ creatures with CR ratings and winter themes
- **loot.json**: 145+ items including weapons, armor, magical items, scrolls
- **magic_items.json**: Magical artifacts and magical items
- **npc.json**: Names, surnames, personality traits, and story hooks (Winter-themed)
- **weather.json**: 9 winter weather conditions with environmental effects
- **city_template.json**: Ten-Towns settlement data

### Generated Files
- **cleanup_duplicates.py**: Script to remove duplicate entries

---

## Generator API

### Encounter Generator
```python
from logic.encounter import generate_encounter
from logic.weather_encounter_generator import (
    generate_weather_encounter,
    generate_blizzard_encounter,
    generate_encounter_by_danger_level
)

# Generate random encounter
encounter = generate_encounter()

# Generate weather-based encounter
weather_encounter = generate_weather_encounter()
blizzard_encounter = generate_blizzard_encounter()

# Generate by danger level (1-5)
deadly_encounter = generate_encounter_by_danger_level(5)
```

### Loot Generator
```python
from logic.loot import (
    generate_loot,
    generate_loot_multiple,
    generate_loot_by_rarity,
    generate_loot_by_category,
    generate_loot_by_category_and_rarity,
    generate_loot_cr_based,
    generate_treasure_hoard,
    get_loot_categories,
    get_loot_rarities
)

# Random item
item = generate_loot()

# Multiple items without duplicates
items = generate_loot_multiple(5)

# By rarity
rare_item = generate_loot_by_rarity("rare")

# By category
weapon = generate_loot_by_category("bronie")

# Loot table based on CR
treasure = generate_loot_cr_based(cr=5)

# Complete treasure hoard
hoard = generate_treasure_hoard(cr=8, hoard_size="large")
# Returns: {gold_pieces, gems_value, magic_items, total_value}
```

### Spell Scroll Generator
```python
from logic.spell_scroll_generator import (
    generate_spell_scroll,
    generate_spell_scroll_for_level,
    generate_spell_scroll_for_class_and_level
)

# Random spell scroll
scroll = generate_spell_scroll()

# For specific class
wizard_scroll = generate_spell_scroll("mag")

# For specific level
level_3_scroll = generate_spell_scroll_for_level(3)

# Class + Level
cleric_level_5 = generate_spell_scroll_for_class_and_level("kleryk", 5)
```

### NPC Generator
```python
from logic.npc import generate_npc

npc = generate_npc()
# Returns: {race, gender, name, surname, trait, hook}
```

### Dice Roller
```python
from logic.dice import (
    roll_dice,
    roll_from_string,
    roll_multiple_dice
)

# Roll d20
result = roll_dice(20)

# Roll from string "2d6+3"
result = roll_from_string("2d6+3")

# Roll multiple expressions
results = roll_multiple_dice(["d20", "2d6", "1d8+2"])
```

---

## Loot Categories

### Weapons (bronie)
- Long sword, rapier, axe, warhammer, spear, dagger
- Magical variants (+1, +2, +3)
- Specialized (Frost Sword, Winter Wolf Bow, etc.)

### Armor (pancerze)
- Chain mail, scale mail, plate armor, leather armor
- Half-plate, helmets, shields
- Magical variants (+1, +2, +3)

### Magical Items (magiczne_przedmioty)
- Rings of protection/teleportation/magic
- Amulets and talismans
- Scrolls of spells (zwoje_zaklec)
- Potions and elixirs
- Wondrous items (bags of holding, mirrors, etc.)

### Rarity Distribution
- **Common (40%)**: Basic items, simple potions
- **Uncommon (35%)**: +1 weapons/armor, basic magical items
- **Rare (20%)**: +2 items, specialized magical items
- **Very Rare (4%)**: +3 items, powerful artifacts
- **Legendary (1%)**: Unique, world-altering items

---

## NPC Features

### Names & Surnames (Winter-Themed)
- **Human**: Arin, Doran, Bren, Astrid, Bodil, Dagmar
- **Elf**: Faelar, Theren, Eldrin, Aelith, Sylvar, Elowen
- **Dwarf**: Borin, Thrain, Durik, Helja, Bruni, Dagna
- **Halfling**: Pip, Lido, Nim, Mara, Serra, Bree
- **Gnome**: Nib, Zook, Fizz, Trix, Nissa, Orla
- **Tiefling**: Azrael, Zarek, Kain, Nyx, Lilith, Mora
- **Half-Elf**: Aerin, Calen, Dain, Aelida, Celene, Delia

**Surnames**: 85+ winter-themed (Frostwind, Wintermere, Glacialon, Tundraheim, Snowcrown, etc.)

### Traits
80+ personality traits describing character personalities

### Story Hooks (Fabułowe hooki)
80+ motivations and plot hooks including:
- "Sworn loyalty to Auril, but now in hiding"
- "Found something beneath the ice - can't stop thinking about it"
- "Blood freezes faster than it should"
- "Leaves no footprints in the snow"
- And many more dark winter-themed mysteries...

---

## Weather System

### Weather Types (9 variants)
- **Blizzard** (Severe): -40°C, visibility 10%, encounter modifier 1.5x
- **Whiteout** (Extreme): -35°C, visibility 5%, encounter modifier 1.6x
- **Heavy Snow** (Severe): -25°C, visibility 40%, encounter modifier 1.2x
- **Ice Storm** (Severe): -20°C, visibility 30%, encounter modifier 1.4x
- **Frozen Fog** (Heavy): -22°C, visibility 15%, encounter modifier 1.3x
- **Frost** (Light): -15°C, visibility 90%, encounter modifier 1.0x
- **Sleet** (Moderate): -10°C, visibility 50%, encounter modifier 1.1x
- **Cold Clear** (Moderate): -20°C, visibility 100%, encounter modifier 1.0x
- **Wind Chill** (Extreme): -32°C, visibility 20%, encounter modifier 1.7x

Each weather affects:
- Enemy encounter difficulty (encounter_modifier)
- Loot availability (loot_penalty)
- Travel speed (travel_speed_modifier)
- Environmental effects (avalanches, freezing damage, etc.)

---

## Data Source

Spell data is based on the D&D 5e SRD JSON dataset from:
https://gist.github.com/dmcb/4b67869f962e3adaa3d0f7e5ca8f4912

Encounter, NPC, and loot data are custom-created for Icewind Dale campaign setting.

---

## Custom Extensions

This project extends the base SRD dataset with custom, non-official content to support gameplay and tooling features:

- **Localized hooks (Polish flavor text)**  
  Some entries include Polish narrative hooks, descriptions, or UI-facing text to support localization and storytelling.  
  These are optional and can be replaced or removed depending on project needs.

- **Setting-specific context (Icewind Dale region)**  
  Descriptive fields and flavor elements are adapted to fit an Icewind Dale-inspired environment.  
  This affects narrative framing only and does not change mechanical rules.

- **Modifiable content layer**  
  All custom additions (hooks, descriptions, region flavor) are designed to be editable.  
  They can be fully replaced with other settings or removed without breaking dataset structure.

---

## Testing

All generators are thoroughly tested:

```bash
python -m pytest tests/ -v
# Result: 29 passed in 0.12s

✅ 4 dice roller tests
✅ 10 core generator tests
✅ 11 new generator tests (spells, weather, loot extensions)
✅ 4 integration tests
```

---

## License / Attribution

The original spell content is derived from the Dungeons & Dragons 5e System Reference Document (SRD), which is made available under the Open Game License (OGL).

Custom encounter, NPC, loot, and weather data are created for this project and can be freely modified.

---

## Recent Updates (2026-06-09)

✅ Added Spell Scroll Generator for all 6 spell-casting classes  
✅ Expanded Loot Generator with CR-based treasures and hoards  
✅ Added Weather-Based Encounter Generator  
✅ Enhanced NPC generation with 80+ story hooks and winter names  
✅ Expanded loot.json from 138 to 145 items with proper D&D categories  
✅ All 29 tests passing  

See [CHANGELOG_2026_06_09.md](CHANGELOG_2026_06_09.md) for detailed changes.

This project does not claim ownership over the original SRD content.

If you redistribute or modify this dataset, ensure compliance with:
- Open Game License (OGL) 1.0a (where applicable)
- Original source attribution requirements

---

## Project Usage

This dataset is intended for:
- DnD helper tools
- Character builders
- Spell lookup systems
- Game utility applications

Example integration:
- Load JSON into cache layer
- Index by spell name / level
- Use in UI filtering system

---

## Notes
- This dataset is external and should be treated as third-party content.
- Custom hooks and localization layers are optional and non-binding.
- Setting flavor (Icewind Dale) is purely descriptive and can be swapped.
- Do not assume ownership of underlying SRD material.

---

## Maintainer Note
If this module is reused in other systems, ensure the attribution section is preserved.  
It is not optional metadata—it is part of the usage conditions.


---

## Tech Stack
- Python 3.11
- Docker & Docker Compose
- GitHub Actions (CI/CD with pytest)
- pytest / unittest for unit testing

import json

# Clean up duplicates
print("=== Czyszczenie duplikatów ===")

# Loot
with open('Data/loot.json', 'r', encoding='utf-8') as f:
    loot = json.load(f)

seen = set()
unique_loot = []
for item in loot:
    name = item.get('name')
    if name not in seen:
        unique_loot.append(item)
        seen.add(name)

with open('Data/loot.json', 'w', encoding='utf-8') as f:
    json.dump(unique_loot, f, ensure_ascii=False, indent=2)

print(
    f"✓ Loot: {len(loot)} → {len(unique_loot)} (usunięto {len(loot)-len(unique_loot)})")

# Encounters
with open('Data/encounter.json', 'r', encoding='utf-8') as f:
    encounters = json.load(f)

seen = set()
unique_enc = []
for item in encounters:
    name = item.get('name')
    if name not in seen:
        unique_enc.append(item)
        seen.add(name)

with open('Data/encounter.json', 'w', encoding='utf-8') as f:
    json.dump(unique_enc, f, ensure_ascii=False, indent=2)

print(
    f"✓ Encounters: {len(encounters)} → {len(unique_enc)} (usunięto {len(encounters)-len(unique_enc)})")

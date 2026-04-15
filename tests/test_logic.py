from logic.city_gen import city_gen
from logic.encounter import generate_encounter
from logic.loot import generate_loot
from logic.npc import generate_npc


def safe_run(name, fn, f):
    try:
        result = fn()
        f.write(f"\n=== {name} ===\n")
        f.write("STATUS: OK\n")
        f.write(str(result) + "\n")
        f.write("-" * 30 + "\n")
    except Exception as e:
        f.write(f"\n=== {name} ===\n")
        f.write("STATUS: FAIL\n")
        f.write(f"ERROR: {e}\n")
        f.write("-" * 30 + "\n")


if __name__ == "__main__":
     with open("log.txt", "w", encoding="utf-8") as f:
        safe_run("city", lambda: city_gen("bryn_shander"), f)
        safe_run("encounter", generate_encounter, f)
        safe_run("loot", generate_loot,f)
        safe_run("npc", generate_npc,f )
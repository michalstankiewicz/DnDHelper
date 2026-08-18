"""
GUI Automation Test Suite
Automatycznie klika przyciski i robi screenshoty
"""
import time
import tkinter as tk
from tkinter import ttk
from PIL import ImageGrab
import threading
import traceback
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, '/app')

# Import GUI
from ui import gui

# Create logs directory
LOG_DIR = Path("/app/gui_test_logs")
LOG_DIR.mkdir(exist_ok=True)
SCREENSHOT_COUNT = 0


def take_screenshot(label: str):
    """Take screenshot and save with timestamp"""
    global SCREENSHOT_COUNT
    SCREENSHOT_COUNT += 1
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = LOG_DIR / f"{SCREENSHOT_COUNT:02d}_{label}_{timestamp}.png"
    
    try:
        # Get screen size
        screenshot = ImageGrab.grab()
        screenshot.save(filename)
        print(f"✓ Screenshot saved: {filename}")
        return filename
    except Exception as e:
        print(f"✗ Screenshot failed: {e}")
        traceback.print_exc()
        return None


def log_action(action: str):
    """Log action to file"""
    log_file = LOG_DIR / "test_log.txt"
    with open(log_file, "a") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {action}\n")
    print(f"→ {action}")


def run_gui_tests(app):
    """Run automated GUI tests in separate thread"""
    try:
        time.sleep(2)  # Wait for GUI to fully render
        
        # Test 1: Initial state screenshot
        log_action("Test 1: Initial GUI state")
        take_screenshot("01_initial_state")
        
        # Test 2: Dice Tab - Roll d20
        log_action("Test 2: Switching to Dice tab")
        app.tabs.select(0)  # Select Dice tab
        app.update()
        time.sleep(1)
        take_screenshot("02_dice_tab")
        
        log_action("Test 2b: Rolling d20")
        app.roll_dice(20)
        app.update()
        time.sleep(0.5)
        take_screenshot("02b_d20_roll_result")
        
        # Test 3: Dice Tab - Roll multiple dice
        log_action("Test 3: Rolling multiple dice (2d6)")
        app.dice_entry.delete(0, tk.END)
        app.dice_entry.insert(0, "2d6")
        app.roll_multi_dice()
        app.update()
        time.sleep(0.5)
        take_screenshot("03_2d6_roll_result")
        
        # Test 4: Spells Tab
        log_action("Test 4: Switching to Spells tab")
        app.tabs.select(1)  # Select Spells tab
        app.update()
        time.sleep(1)
        take_screenshot("04_spells_tab")
        
        log_action("Test 4b: Searching spells")
        app.spell_search_entry.delete(0, tk.END)
        app.spell_search_entry.insert(0, "fireball")
        app.search_spells()
        app.update()
        time.sleep(0.5)
        take_screenshot("04b_fireball_search")
        
        # Test 5: Encounters & Loot Tab
        log_action("Test 5: Switching to Encounters & Loot tab")
        app.tabs.select(2)  # Select Encounters tab
        app.update()
        time.sleep(1)
        take_screenshot("05_encounters_tab")
        
        log_action("Test 5b: Generating encounters")
        app.generate_encounter()
        app.update()
        time.sleep(1)
        take_screenshot("05b_encounters_generated")
        
        log_action("Test 5c: Selecting first encounter and generating treasure")
        if app.encounter_listbox.size() > 0:
            app.encounter_listbox.selection_set(0)
            app.encounter_listbox.event_generate("<<ListboxSelect>>")
            app.update()
            time.sleep(1)
            take_screenshot("05c_treasure_generated")
        
        # Test 6: NPC Tab
        log_action("Test 6: Switching to NPC tab")
        app.tabs.select(3)  # Select NPC tab
        app.update()
        time.sleep(1)
        take_screenshot("06_npc_tab")
        
        log_action("Test 6b: Generating NPCs")
        app.generate_npc()
        app.update()
        time.sleep(1)
        take_screenshot("06b_npc_generated")
        
        # Test 7: City Tab
        log_action("Test 7: Switching to City tab")
        app.tabs.select(4)  # Select City tab
        app.update()
        time.sleep(1)
        take_screenshot("07_city_tab")
        
        log_action("Test 7b: Generating city")
        app.generate_city()
        app.update()
        time.sleep(1)
        take_screenshot("07b_city_generated")
        
        log_action("✓ All tests completed successfully!")
        
    except Exception as e:
        log_action(f"✗ Test failed: {e}")
        print(f"Error: {e}")
        traceback.print_exc()
    finally:
        # Close app after tests
        app.quit()


def main():
    print("=" * 60)
    print("D&D Helper - GUI Automation Test Suite")
    print("=" * 60)
    
    log_action("Starting GUI automation tests")
    
    try:
        # Create app
        app = gui.MyApp()
        app.geometry("860x800")
        
        # Schedule tests in separate thread
        test_thread = threading.Thread(target=run_gui_tests, args=(app,), daemon=True)
        test_thread.start()
        
        # Run mainloop with timeout
        app.after(120000, app.quit)  # Auto-quit after 2 minutes
        app.mainloop()
        
    except Exception as e:
        log_action(f"✗ Fatal error: {e}")
        print(f"Fatal error: {e}")
        traceback.print_exc()
        sys.exit(1)
    
    print("=" * 60)
    print("Test suite finished")
    print(f"Screenshots saved to: {LOG_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()

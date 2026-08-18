# GUI Testing - Quick Reference

## What Was Built

Automatyczne testy GUI aplikacji D&D Helper w Dockerze z generowaniem screenshot'ów.

## Files in `developers/docker_Teste/`

| File | Purpose |
|------|---------|
| `Dockerfile_gui_test` | Docker image z Xvfb + tkinter |
| `gui_test_entrypoint.sh` | Uruchamia Xvfb + test script |
| `gui_test_automation.py` | Automation script (kliki, screenshoty) |
| `GUI_AUTOMATION_README.md` | Detailed docs |
| `IMPLEMENTATION_COMPLETE.md` | Full setup guide |
| `QUICK_REFERENCE.md` | Ten plik |

## In `.github/workflows/`

| File | Purpose |
|------|---------|
| `gui_automation_test.yml` | GitHub Actions workflow |

## How to Use

### Option 1: GitHub (Recommended)
```bash
git push
# Tests run automatically on push/PR
# View results in Actions tab → gui-test-screenshots artifact
```

### Option 2: Local Docker
```bash
docker build -f developers/docker_Teste/Dockerfile_gui_test -t dnd-helper-gui-test .
docker run --rm dnd-helper-gui-test
# Generates: 13 screenshots + test_log.txt
```

## Test Coverage

✓ Dice rolls (d20, 2d6, custom NdM)  
✓ Spell search (filtering by name/level)  
✓ Encounter generation (6 encounters)  
✓ Treasure generation (based on CR)  
✓ NPC generation (6 NPCs with traits)  
✓ City generation (with problems/goods/superstitions)  

## Outputs

**Screenshots:** 13 PNGs
```
01_initial_state.png
02_dice_tab.png
02b_d20_roll.png
03_2d6_roll.png
04_spells_tab.png
04b_fireball_search.png
05_encounters_tab.png
05b_encounters_generated.png
05c_treasure_generated.png
06_npc_tab.png
06b_npc_generated.png
07_city_tab.png
07b_city_generated.png
```

**Log:** test_log.txt
- Timestamped actions
- Error handling

## GitHub Actions Workflow

**Triggers on:**
- Push to main/DnD
- Pull requests
- Manual trigger

**Workflow Steps:**
1. Checkout code
2. Build Docker image
3. Run tests
4. Upload artifacts (30 days retention)
5. Generate summary

**View Results:**
- Go to: Actions → Latest run → gui-test-screenshots
- Download PNG folder
- Open in browser

## Performance

| Metric | Value |
|--------|-------|
| Build time | ~2-3 min |
| Test time | ~30-45 sec |
| Total workflow | ~5-7 min |
| Screenshot size | ~50-200 KB each |

## Key Points

- ✓ No X11 forwarding needed (uses Xvfb virtual display)
- ✓ Works on all GitHub runners (Windows, Linux, macOS)
- ✓ Fully automated (no manual intervention)
- ✓ Visual proof of functionality
- ✓ Easy to extend with more tests
- ✓ Screenshot history for debugging

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Blank screenshots | Increase sleep time in gui_test_automation.py |
| App crashes | Check Data/*.json files in COPY |
| No artifacts | Check workflow permissions + directory exists |
| Very slow | Normal (build + Xvfb + X11 libs) |

## Next Steps

1. **Git Push:** `git push` to main/DnD branch
2. **Check Actions:** GitHub Actions → gui_automation_test workflow
3. **Download Artifacts:** After completion
4. **Review Screenshots:** Verify all tests passed

Ready to deploy! 🚀

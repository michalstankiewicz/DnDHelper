# GUI Automation Testing with Docker

## Overview
Automatyczne testy GUI aplikacji D&D Helper uruchamiane w Dockerze z virtual X11 display.

## Files Created

### 1. `Dockerfile_gui_test`
Dockerfile z:
- `python3-tk` — Tkinter GUI libraries
- `xvfb` — Virtual X11 display server
- `imagemagick` — Image manipulation
- `pillow` — Python image library
- Auto-screenshot capabilities

### 2. `gui_test_automation.py`
Python script który:
- Uruchamia GUI aplikację
- Automatycznie klika przyciski
- Robi screenshoty po każdym kroku
- Loguje wszystkie akcje
- Obsługuje błędy

**Testy obejmują:**
- ✓ Dice Tab — rolls (d20, 2d6, etc.)
- ✓ Spells Tab — searching spells
- ✓ Encounters Tab — generation & treasure
- ✓ NPC Tab — NPC generation
- ✓ City Tab — city generation

### 3. `gui_test_entrypoint.sh`
Bash script który:
- Uruchamia Xvfb virtual display
- Czeka na inicjalizację
- Uruchamia Python test script
- Zbiera outputy w logi

### 4. `.github/workflows/gui_automation_test.yml`
GitHub Actions workflow:
- Builds Docker image
- Runs GUI tests
- Uploads screenshots as artifacts
- Creates test summary

## Usage

### Local Testing
```bash
# Build image
docker build -f developers/docker_Teste/Dockerfile_gui_test -t dnd-helper-gui-test .

# Run tests
docker run --rm \
  -v $(pwd)/gui_test_logs:/app/gui_test_logs \
  dnd-helper-gui-test

# View screenshots
ls gui_test_logs/
```

### GitHub Actions
Tests run automatically on:
- Push to `main` or `DnD` branch
- Pull requests to `main` or `DnD` branch
- Manual trigger (`workflow_dispatch`)

Screenshots are uploaded as artifacts and available in Action summary.

## Test Output

Each run generates:
1. **PNG Screenshots** — Visual verification of each step
2. **test_log.txt** — Detailed action log with timestamps
3. **GitHub Artifact** — All files packaged and downloadable

### Screenshot Naming Convention
```
01_initial_state_YYYYMMDD_HHMMSS.png
02_dice_tab_YYYYMMDD_HHMMSS.png
02b_d20_roll_result_YYYYMMDD_HHMMSS.png
...
```

## Troubleshooting

### "no display name and no $DISPLAY environment variable"
- Dockerfile_gui_test ustawia `DISPLAY=:99` w environment
- Xvfb script uruchamia virtual display na porcie 99
- Jeśli nadal problem → sprawdź `Xvfb` status w kontenerze

### Screenshots nie są generowane
- Sprawdź czy `pillow` jest zainstalowany
- Sprawdź uprawnienia do `/app/gui_test_logs/`
- Sprawdź czy X display jest uruchomiony (check `ps aux | grep Xvfb`)

### GUI app się zawala
- Czekaj na inicjalizację (`time.sleep(2)`)
- Sprawdź czy wszystkie imports działają
- Sprawdź czy GUI nie ma hardkoded'ego display configuration

## Performance
- Build time: ~2-3 min (instalacja Xvfb, X11 libs, Python deps)
- Test execution: ~30 sec (7-8 scenariuszy)
- Total workflow time: ~5-7 min

## Future Improvements
- [ ] Add more detailed assertions/validations
- [ ] Screenshot diff comparison
- [ ] Performance metrics collection
- [ ] Export HTML report
- [ ] Add video recording of test execution
- [ ] Integration with test result tracking

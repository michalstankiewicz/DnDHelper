# GUI Fix Summary

## Problem Found
**Error:** `ImportError: libtk8.6.so: cannot open shared object file`

GUI (tkinter) nie jest zainstalowany w `python:3.11-slim` image.

## Solution Options

### Option 1: GUI + Python (with tkinter)
**File:** `Dockerfile_with_tk`
- Instaluje `python3-tk` paczkę
- Pozwala na GUI mode
- Większy image (~400MB vs 170MB)

```bash
docker build -f developers/docker_Teste/Dockerfile_with_tk -t dnd-helper-gui .
docker run --rm -e DISPLAY=host.docker.internal:0 dnd-helper-gui
```

### Option 2: Test-Only (bez GUI)
**File:** `Dockerfile_test_only`
- Brak GUI — testy tylko
- Lekki image (~170MB)
- Mniejsze zużycie zasobów
- Idealny do CI/CD

```bash
docker build -f developers/docker_Teste/Dockerfile_test_only -t dnd-helper-test .
docker run --rm dnd-helper-test --test
```

### Option 3: Current Setup (Test Default)
Obecny Dockerfile w root:
- Domyślnie uruchamia `--test` mode
- Bez GUI
- Optymalny dla automacji

---

## Recommendations

1. **Dla CI/CD:** Użyj `Dockerfile_test_only`
2. **Dla dewelopmentu GUI:** Zainstal tkinter lokalnie na maszynie
3. **Docker GUI:** Wymaga dodatkowej konfiguracji X11 forwarding

Obecna konfiguracja jest OK dla testów. GUI należy testować lokalnie (bez Dockera) albo w osobnym image'u z tkinter.

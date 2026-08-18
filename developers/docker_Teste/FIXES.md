# Docker Build & Test Commands

## Fix Issues Step-by-Step

### 1. Replace corrupted req.txt
```bash
copy developers\docker_Teste\req.txt req.txt
```

### 2. Update Dockerfile
Option A - Minimal fix (just change CMD):
```dockerfile
CMD ["python", "main.py"]
```

Option B - Production-ready (use multi-stage):
```bash
copy developers\docker_Teste\Dockerfile.improved Dockerfile
```

### 3. Build & Test

**Test GUI mode:**
```bash
docker build -t dnd-helper .
docker run --rm dnd-helper  # Starts GUI
```

**Test test mode:**
```bash
docker run --rm dnd-helper --test  # Runs tests
```

### 4. Verify test output
```bash
docker run --rm dnd-helper --test
# Should output: ✓ Testy przeszly
# Should create: log.txt with "Test OK"
```

---

## Files Provided

- **test_review.md** — Detailed code review with issues and recommendations
- **req.txt** — Fixed requirements file (clean encoding)
- **Dockerfile.improved** — Production-ready multi-stage build

---

## Quick Checklist

- [ ] Copy corrected req.txt to root
- [ ] Update Dockerfile (use improved version for best results)
- [ ] Run `docker build -t dnd-helper .`
- [ ] Test: `docker run --rm dnd-helper --test`
- [ ] Verify log.txt is created in container

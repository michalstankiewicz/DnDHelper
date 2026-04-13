# DnD Helper – SRD Spells Module

## Overview
This module provides structured spell data for a Dungeons & Dragons 5e helper tool.  
It is intended for use in gameplay tools, UI applications, and procedural generation systems.

The project focuses on fast access, filtering, and integration with game-related systems (e.g. search, tabs, build tools).

---

## Features
- Structured SRD spell dataset (JSON format)
- Search-friendly fields (name, level, class, school, etc.)
- Ready for integration with GUI / CLI tools
- Lightweight static data usage (no runtime API dependency)
- Extended with custom game hooks and localized content

---

## Data Source

Spell data is based on the D&D 5e SRD JSON dataset from:

https://gist.github.com/dmcb/4b67869f962e3adaa3d0f7e5ca8f4912

All credit for the original dataset structure and compilation belongs to the author of the linked repository.

---

## Custom Extensions

This project extends the base SRD dataset with custom, non-official content to support gameplay and tooling features:

- **Localized hooks (Polish flavor text)**  
  Some entries include Polish narrative hooks, descriptions, or UI-facing text to support localization and storytelling.  
  These are optional and can be replaced or removed depending on project needs.

- **Setting-specific context (Icewind Dale region)**  
  Certain descriptive fields and flavor elements are adapted to fit an Icewind Dale-inspired environment.  
  This affects narrative framing only and does not change mechanical rules.

- **Modifiable content layer**  
  All custom additions (hooks, descriptions, region flavor) are designed to be editable.  
  They can be fully replaced with other settings or removed without breaking dataset structure.

---

## License / Attribution

The original content is derived from the Dungeons & Dragons 5e System Reference Document (SRD), which is made available under the Open Game License (OGL).

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

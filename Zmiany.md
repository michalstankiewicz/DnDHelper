# Zmiany

## Plik: ui/gui.py

- Dodano import `logic.weather_encounter_generator`.
- Rozszerzono interfejs GUI dla zakładki `Encounters and Loot` o nowe przyciski:
  - `Generate Weather Encounter`
  - `Generate Selected Weather`
  - `Blizzard Encounter`
  - `Whiteout Encounter`
  - `Ice Storm Encounter`
  - `Generate Danger Encounter`
- Dodano selektor typu pogody oraz wybór poziomu zagrożenia 1-5.
- Dodano nowe metody obsługujące generowanie spotkań pogodowych i na poziomie zagrożenia.
- Poprawiono parsowanie CR w `on_encounter_selected`, aby obsługiwać wartości zmiennoprzecinkowe (np. 0.5).
- Poprawiono logikę generacji miasta w `generate_city`, aby wynik był wyświetlany bez powtarzania i zbędnej pętli.

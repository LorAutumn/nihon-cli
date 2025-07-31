# Changelog - Nihon CLI

## [Unreleased]

---

## [1.0.2] - 2025-01-31

### ✨ Neue Features
- **Emoji-Integration**: Die CLI zeigt jetzt Emojis an, um den Lernfortschritt und den Status der Antworten visuell zu unterstützen.
  - ✅ Korrekte Antwort
  - ❌ Falsche Antwort
  - ⏭️ Übersprungene Frage
  - ⏱️ Timer-Benachrichtigungen

### 🔧 Verbesserungen
- **Visuelle Klarheit**: Die Ausgabe wurde überarbeitet, um die Lesbarkeit zu verbessern und eine klarere visuelle Trennung zwischen den Quiz-Elementen zu schaffen.

---

## [1.0.1] - 2025-01-31

### ✨ Features & Improvements
- **Audio-Benachrichtigungen**: Ein akustisches Signal (System Bell) wird nun abgespielt, wenn der Lerntimer abläuft, um den Benutzer zu benachrichtigen. Dies verbessert die Benutzererfahrung, da man nicht ständig auf das Terminal schauen muss.
- **Konfigurationssystem**: Implementierung eines Konfigurationssystems, das benutzerspezifische Anpassungen erlaubt.

---

## [1.0.0] - 2025-01-30

### ✅ Implementiert
- Vollständiges Hiragana/Katakana-Training
- CLI-Interface mit argparse
- Timer-System mit 25-Min/5-Sek Modi
- Quiz-Engine mit 10 zufälligen Zeichen
- Terminal-Clearing zwischen Sessions
- PEP 8 konforme Code-Qualität
- Umfassende Sicherheitsprüfung
- uvx-Kompatibilität
- Vollständige Dokumentation

### 🏗️ Architektur
- Domain-Driven Design
- Character Domain Model
- 208 japanische Zeichen (104 Hiragana + 104 Katakana)
- Cross-Platform-Kompatibilität
- Nur Standard-Python-Bibliotheken

### 📦 Deployment
- pip-Installation: `pip install -e .`
- uvx-Nutzung: `uvx nihon-cli cli hiragana --test`
- Entry Points konfiguriert
- Moderne pyproject.toml-Konfiguration
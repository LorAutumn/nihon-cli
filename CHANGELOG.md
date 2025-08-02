# Changelog - Nihon CLI

## [Unreleased] - Geplante Verbesserungen

### 🔔 Benachrichtigungen und UX-Verbesserungen

#### Terminal-Fokus nach Timer
- **Problem**: Nach Ablauf des Timers bleibt das Terminal im Hintergrund
- **Lösung**: Terminal soll automatisch in den Vordergrund kommen
- **Technische Umsetzung**:
  - macOS: `osascript -e 'tell application "Terminal" to activate'`
  - Windows: `os.system('powershell -command "Add-Type -AssemblyName Microsoft.VisualBasic; [Microsoft.VisualBasic.Interaction]::AppActivate((Get-Process -Name WindowsTerminal).Id)"')`
  - Linux: `os.system('wmctrl -a Terminal')` oder `xdotool windowactivate $(xdotool search --name "Terminal")`
- **Implementierung**: Neue Methode `bring_terminal_to_foreground()` in `LearningTimer`-Klasse

#### Audio-Benachrichtigung bei Timer-Ablauf
- **Problem**: Kein akustisches Signal wenn Timer abläuft
- **Lösung**: Pling-Sound oder System-Benachrichtigung abspielen
- **Technische Umsetzung**:
  - **Option 1 - System Bell**: `print('\a')` (einfachste Lösung, funktioniert überall)
  - **Option 2 - System-Sound**: 
    - macOS: `os.system('afplay /System/Library/Sounds/Ping.aiff')`
    - Windows: `import winsound; winsound.MessageBeep()`
    - Linux: `os.system('paplay /usr/share/sounds/alsa/Front_Left.wav')`
  - **Option 3 - Desktop-Notification**:
    - macOS: `osascript -e 'display notification "Zeit für die nächste Lerneinheit!" with title "Nihon CLI"'`
    - Windows: `powershell -command "New-BurntToastNotification -Text 'Nihon CLI', 'Zeit für die nächste Lerneinheit!'"`
    - Linux: `notify-send "Nihon CLI" "Zeit für die nächste Lerneinheit!"`
- **Implementierung**: Neue Methode `play_notification_sound()` in `LearningTimer`-Klasse

### 📋 Implementierungsplan

#### Phase 1: Audio-Benachrichtigung
1. **Einfache Lösung**: System Bell (`\a`) implementieren
2. **Erweiterte Lösung**: Plattformspezifische Sounds
3. **Konfiguration**: Optional über CLI-Flag `--silent` deaktivierbar

#### Phase 2: Terminal-Fokus
1. **Plattform-Erkennung**: `platform.system()` verwenden
2. **Plattformspezifische Implementierung**: Separate Methoden für jedes OS
3. **Fallback-Handling**: Graceful degradation wenn Befehle fehlschlagen

#### Phase 3: Benutzer-Konfiguration
1. **Konfigurationsdatei**: `~/.nihon-cli/config.json`
2. **CLI-Flags**: `--no-sound`, `--no-focus`, `--notification-type`
3. **Einstellungen**: Sound-Typ, Lautstärke, Benachrichtigungs-Stil

### 🔧 Technische Details

#### Neue Abhängigkeiten (optional)
- **plyer**: Cross-platform desktop notifications
- **pygame**: Für erweiterte Audio-Funktionen
- **winsound**: Windows-spezifische Sounds (bereits in stdlib)

#### Neue CLI-Optionen
```bash
nihon cli hiragana --no-sound          # Deaktiviert Audio-Benachrichtigungen
nihon cli hiragana --no-focus          # Deaktiviert Terminal-Fokus
nihon cli hiragana --notification-type bell|sound|desktop
```

#### Code-Struktur Änderungen
```python
# src/nihon_cli/core/timer.py
class LearningTimer:
    def __init__(self, interval_seconds: int = 1500, enable_sound: bool = True, enable_focus: bool = True):
        # ...
    
    def play_notification_sound(self) -> None:
        """Spielt Benachrichtigungssound ab."""
        
    def bring_terminal_to_foreground(self) -> None:
        """Bringt Terminal in den Vordergrund."""
        
    def wait_for_next_session(self) -> None:
        # ... existing countdown logic ...
        self.play_notification_sound()
        self.bring_terminal_to_foreground()
```

### 🎯 Priorität
- **Hoch**: Audio-Benachrichtigung (einfache System Bell)
- **Mittel**: Terminal-Fokus (plattformspezifisch)
- **Niedrig**: Erweiterte Konfigurationsoptionen

### 🧪 Testing-Anforderungen
- [ ] Audio-Benachrichtigung auf allen Plattformen testen
- [ ] Terminal-Fokus auf macOS, Windows, Linux validieren
- [ ] Graceful degradation bei fehlenden System-Befehlen
- [ ] CLI-Flags und Konfigurationsoptionen testen

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
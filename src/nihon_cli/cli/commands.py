# src/nihon_cli/cli/commands.py
"""
CLI command definitions for the Nihon CLI application using argparse.
"""

import argparse
import sys
from typing import List, Optional

from nihon_cli.app import NihonCli
from nihon_cli.infra.config import save_config


def handle_hiragana_command(args: argparse.Namespace) -> None:
    """
    Handler for the Hiragana training command.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
                                   Expected to have 'test' and 'advanced' attributes.
    """
    cli_app = NihonCli()
    cli_app.run_training_session("hiragana", args.test, args.advanced)


def handle_katakana_command(args: argparse.Namespace) -> None:
    """
    Handler for the Katakana training command.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
                                   Expected to have 'test' and 'advanced' attributes.
    """
    cli_app = NihonCli()
    cli_app.run_training_session("katakana", args.test, args.advanced)


def handle_mixed_command(args: argparse.Namespace) -> None:
    """
    Handler for the mixed training command.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
                                   Expected to have 'test' and 'advanced' attributes.
    """
    cli_app = NihonCli()
    cli_app.run_training_session("mixed", args.test, args.advanced)


def handle_words_command(args: argparse.Namespace) -> None:
    """
    Handler for the words training command.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
                                   Expected to have 'test' attribute.
    """
    cli_app = NihonCli()
    cli_app.run_training_session("words", args.test)


def handle_vocab_upload_command(args: argparse.Namespace) -> None:
    """
    Handler for the 'vocab upload' command.

    Parses a Markdown or Excel file containing vocabulary and imports
    the vocabulary items into the database.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
                                   Expected to have 'file' and 'tag' attributes.
    """
    from pathlib import Path
    from nihon_cli.infra.repository import VocabRepository

    file_path = Path(args.file)
    upload_tag = args.tag or file_path.stem

    try:
        if file_path.suffix in ('.xlsx', '.xls'):
            _upload_excel(file_path, upload_tag)
        else:
            _upload_markdown(file_path, upload_tag)

    except FileNotFoundError as e:
        print(f"✗ Fehler: Datei nicht gefunden - {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"✗ Fehler: Ungültiges Format - {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nAbgebrochen.")
        sys.exit(0)
    except Exception as e:
        print(f"✗ Unerwarteter Fehler: {e}")
        sys.exit(1)


def _upload_markdown(file_path, upload_tag: str) -> None:
    """Import vocabulary from a Markdown file."""
    from nihon_cli.core.parser import MarkdownVocabParser
    from nihon_cli.infra.repository import VocabRepository

    parser = MarkdownVocabParser()
    items = parser.parse(file_path)

    for item in items:
        item.upload_tag = upload_tag

    repo = VocabRepository()
    inserted, skipped = repo.add_vocabulary_batch(items, file_path.name, upload_tag)

    print(f"✓ {inserted} Vokabeln erfolgreich importiert!")
    if skipped > 0:
        print(f"  ({skipped} Duplikate übersprungen)")


def _upload_excel(file_path, upload_tag: str) -> None:
    """Import vocabulary from an Excel file with interactive sheet selection."""
    from nihon_cli.core.excel_parser import ExcelVocabParser
    from nihon_cli.infra.repository import VocabRepository

    parser = ExcelVocabParser()
    sheets = parser.parse(file_path)

    sheet_names = list(sheets.keys())
    print(f"\n📚 {len(sheet_names)} Sheets gefunden:\n")
    for i, name in enumerate(sheet_names, 1):
        count = len(sheets[name])
        print(f"  [{i}] {name} ({count} Vokabeln)")

    print(f"\n  [a] Alle Sheets importieren")
    print()

    selection = input("Auswahl (z.B. 1,3 oder a für alle): ").strip().lower()

    if selection == 'a':
        selected = sheet_names
    else:
        try:
            indices = [int(s.strip()) for s in selection.split(',')]
            selected = [sheet_names[i - 1] for i in indices if 1 <= i <= len(sheet_names)]
        except (ValueError, IndexError):
            print("✗ Ungültige Auswahl.")
            sys.exit(1)

    if not selected:
        print("Keine Sheets ausgewählt. Abgebrochen.")
        sys.exit(0)

    repo = VocabRepository()
    total_inserted = 0
    total_skipped = 0

    for name in selected:
        items = sheets[name]
        tag = f"{upload_tag}_{name}" if len(selected) > 1 else upload_tag

        for item in items:
            item.upload_tag = tag
            item.source_file = file_path.name

        inserted, skipped = repo.add_vocabulary_with_weekly_fields(
            items, file_path.name, tag
        )
        total_inserted += inserted
        total_skipped += skipped
        print(f"  ✓ {name}: {inserted} importiert, {skipped} übersprungen")

    print(f"\n✓ Gesamt: {total_inserted} Vokabeln importiert!")
    if total_skipped > 0:
        print(f"  ({total_skipped} Duplikate übersprungen)")


def handle_vocab_learn_command(args: argparse.Namespace) -> None:
    """
    Handler for the 'vocab learn' command.
    
    Starts an interactive vocabulary learning session with adaptive
    query direction based on learning progress and timer-based intervals.
    
    Args:
        args (argparse.Namespace): The parsed command-line arguments.
                                   Expected to have 'limit' and 'test' attributes.
    """
    from nihon_cli.core.quiz_vocab import VocabQuiz
    from nihon_cli.core.timer import LearningTimer
    from nihon_cli.infra.repository import VocabRepository
    
    try:
        # Initialize repository and quiz engine
        repository = VocabRepository()
        quiz = VocabQuiz(repository)
        
        # Determine timer interval based on test mode
        interval_seconds = 5 if args.test else 1500
        
        # Start endless loop with timer
        while True:
            # Run quiz session
            questions_asked = quiz.run_session(limit=args.limit)
            
            # Only start timer if questions were actually asked
            if questions_asked > 0:
                # Initialize timer for next session
                timer = LearningTimer(interval_seconds)
                timer.wait_for_next_session()
            else:
                # No questions available, exit loop
                break
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Lernsitzung abgebrochen.")
        sys.exit(0)
    except Exception as e:
        print(f"✗ Unerwarteter Fehler: {e}")
        sys.exit(1)


def handle_weekly_session_start_command(args: argparse.Namespace) -> None:
    """
    Handler for the 'vocab weekly-session start' command.

    Starts or continues a weekly learning session with 10-item quizzes.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
                                   Expected to have 'test' attribute.
    """
    from datetime import date
    from nihon_cli.core.quiz_weekly import WeeklySessionQuiz
    from nihon_cli.core.timer import LearningTimer
    from nihon_cli.core.weekly_session import WeeklySession
    from nihon_cli.infra.repository import VocabRepository
    from nihon_cli.infra.weekly_session_repository import WeeklySessionRepository
    from nihon_cli.ui.formatting import draw_box

    try:
        vocab_repo = VocabRepository()
        session_repo = WeeklySessionRepository()

        # Check for current week session
        session = session_repo.get_current_week_session()

        if not session:
            print("\n✗ Keine aktive Wochensitzung gefunden.")
            print("Bitte verwenden Sie 'vocab weekly-session new' um eine Session zu erstellen.")
            sys.exit(1)

        # Check if week has expired
        if session.is_expired():
            print("\n" + draw_box(
                "Die Woche ist zu Ende!\n\n"
                "Möchten Sie:\n"
                "  [1] Neue Woche mit neuen Vokabeln starten\n"
                "  [2] Letzte Woche wiederholen",
                title="📅 Wochenende"
            ))

            choice = input("\nAuswahl (1/2): ").strip()

            if choice == "1":
                print("\nVerwenden Sie 'vocab weekly-session new' um eine neue Session zu erstellen.")
                sys.exit(0)
            elif choice == "2":
                # Repeat last week - reset weekly counters
                old_items = session_repo.get_session_items(session.id, prioritize_by_progress=False)
                vocab_ids = [item.id for item in old_items]
                vocab_repo.reset_weekly_counters(vocab_ids)
                # Create new session with same vocab
                session = session_repo.create_new_session(vocab_ids)
                print(f"\n✓ Neue Woche erstellt mit {len(vocab_ids)} Vokabeln")
            else:
                print("\n✗ Ungültige Auswahl.")
                sys.exit(1)

        # Initialize quiz engine
        quiz = WeeklySessionQuiz(vocab_repo, session_repo)

        # Determine timer interval
        interval_seconds = 5 if args.test else 1500

        # Start endless loop with timer
        while True:
            questions_asked = quiz.run_session(session.id)

            if questions_asked > 0:
                timer = LearningTimer(interval_seconds)
                timer.wait_for_next_session()
            else:
                print("\n✅ Alle Vokabeln dieser Woche wurden ausreichend geübt!")
                break

    except KeyboardInterrupt:
        print("\n\n⚠️  Wochensitzung abgebrochen.")
        sys.exit(0)
    except Exception as e:
        print(f"✗ Unerwarteter Fehler: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def handle_weekly_session_import_image_command(args: argparse.Namespace) -> None:
    """
    Handler for the 'vocab weekly-session import-image' command.

    Imports vocabulary from an image using OCR (OpenAI Vision API).

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
                                   Expected to have 'image_path' and 'tag' attributes.
    """
    from datetime import date
    from pathlib import Path
    from nihon_cli.core.ocr_parser import OpenAIVisionParser
    from nihon_cli.core.vocabulary import VocabularyItem
    from nihon_cli.infra.repository import VocabRepository
    from nihon_cli.infra.weekly_session_repository import WeeklySessionRepository
    from nihon_cli.ui.item_selector import VocabItemSelector

    try:
        image_path = Path(args.image_path)

        if not image_path.exists():
            print(f"✗ Bilddatei nicht gefunden: {image_path}")
            sys.exit(1)

        # Extract vocabulary from image
        print("🔍 Extrahiere Vokabeln aus Bild...")
        try:
            parser = OpenAIVisionParser()
            extracted_items = parser.extract_vocabulary_from_image(image_path)
        except ImportError as e:
            print(f"\n✗ Fehler: {e}")
            print("\nBitte installieren Sie das openai Package:")
            print("  pip install openai")
            sys.exit(1)
        except ValueError as e:
            print(f"\n✗ Fehler: {e}")
            print("\nStellen Sie sicher, dass OPENAI_API_KEY gesetzt ist:")
            print("  export OPENAI_API_KEY='your-api-key'")
            sys.exit(1)

        print(f"✓ {len(extracted_items)} Vokabeln gefunden")

        if not extracted_items:
            print("Keine Vokabeln extrahiert. Bitte prüfen Sie das Bild.")
            sys.exit(0)

        # Interactive selection
        selector = VocabItemSelector()
        selected_items = selector.display_and_select(extracted_items)

        if not selected_items:
            print("Import abgebrochen.")
            sys.exit(0)

        # Convert to VocabularyItem objects
        vocab_items = []
        for item_dict in selected_items:
            vocab_item = VocabularyItem(
                id=0,  # Will be set by database
                japanese_vocab=item_dict['japanese'],
                german_vocab=item_dict['german'],
                source_file=image_path.name,
                upload_tag=args.tag or f"ocr_{date.today().isoformat()}",
                vocab_type=item_dict.get('vocab_type'),
                base_form=item_dict.get('base_form'),
                weekly_correct_german=0,
                weekly_correct_japanese=0
            )
            vocab_items.append(vocab_item)

        # Insert into database
        vocab_repo = VocabRepository()
        inserted, skipped = vocab_repo.add_vocabulary_with_weekly_fields(
            vocab_items,
            image_path.name,
            args.tag or f"ocr_{date.today().isoformat()}"
        )

        print(f"\n✓ {inserted} Vokabeln importiert ({skipped} Duplikate übersprungen)")

        # Add to current weekly session if one exists
        session_repo = WeeklySessionRepository()
        current_session = session_repo.get_current_week_session()

        if current_session:
            vocab_ids = [item.id for item in vocab_items if item.id > 0]
            added = session_repo.add_items_to_session(current_session.id, vocab_ids)
            print(f"✓ {added} Vokabeln zur aktuellen Wochensitzung hinzugefügt")
        else:
            print("\n⚠ Keine aktive Wochensitzung. Vokabeln nur importiert, nicht verknüpft.")
            print("Verwenden Sie 'vocab weekly-session new' um eine Session zu erstellen.")

    except Exception as e:
        print(f"✗ Fehler beim Importieren: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def handle_weekly_session_new_command(args: argparse.Namespace) -> None:
    """
    Handler for the 'vocab weekly-session new' command.

    Creates a new weekly session by letting the user select vocabulary items.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
                                   Expected to have optional 'tag' attribute.
    """
    from nihon_cli.infra.repository import VocabRepository
    from nihon_cli.infra.weekly_session_repository import WeeklySessionRepository
    from nihon_cli.ui.formatting import draw_box

    try:
        vocab_repo = VocabRepository()
        session_repo = WeeklySessionRepository()

        # Check if a session already exists for current week
        existing_session = session_repo.get_current_week_session()
        if existing_session and not existing_session.is_expired():
            print("\n⚠ Es existiert bereits eine aktive Wochensitzung.")
            print(f"Woche: {existing_session.week_start} bis {existing_session.week_end}")
            overwrite = input("\nMöchten Sie diese ersetzen? (j/N): ").strip().lower()
            if overwrite != 'j':
                print("Abgebrochen.")
                sys.exit(0)

        # Get all available vocabulary
        all_vocab = vocab_repo.get_incomplete_vocabulary(limit=1000)

        if not all_vocab:
            print("\n✗ Keine Vokabeln verfügbar.")
            print("Bitte importieren Sie zuerst Vokabeln mit 'vocab upload' oder 'vocab weekly-session import-image'.")
            sys.exit(1)

        # Filter by tag if specified
        if hasattr(args, 'tag') and args.tag:
            all_vocab = [v for v in all_vocab if v.upload_tag == args.tag]
            if not all_vocab:
                print(f"\n✗ Keine Vokabeln mit Tag '{args.tag}' gefunden.")
                sys.exit(1)

        # Display available vocabulary
        print("\n" + draw_box(
            f"Verfügbare Vokabeln: {len(all_vocab)}",
            title="📚 Vokabel-Auswahl"
        ))

        # Show first 10 items as preview
        print("\nVorschau (erste 10 Items):")
        for i, item in enumerate(all_vocab[:10], 1):
            jp_str = ", ".join(item.japanese_vocab)
            de_str = ", ".join(item.german_vocab)
            type_str = f"[{item.vocab_type}]" if item.vocab_type else ""
            print(f"  {i}. {jp_str} → {de_str} {type_str}")

        if len(all_vocab) > 10:
            print(f"  ... und {len(all_vocab) - 10} weitere")

        # Ask how many to include
        print("\nWie viele Vokabeln möchten Sie in diese Woche aufnehmen?")
        print(f"(Empfohlen: 10-20 für eine Woche, Verfügbar: {len(all_vocab)})")

        while True:
            try:
                count_input = input("\nAnzahl (oder 'all' für alle): ").strip().lower()
                if count_input == 'all':
                    count = len(all_vocab)
                else:
                    count = int(count_input)
                    if count <= 0 or count > len(all_vocab):
                        print(f"Bitte eine Zahl zwischen 1 und {len(all_vocab)} eingeben.")
                        continue
                break
            except ValueError:
                print("Ungültige Eingabe. Bitte eine Zahl eingeben.")

        # Select items (take first N by default, could be randomized)
        selected_items = all_vocab[:count]
        vocab_ids = [item.id for item in selected_items]

        # Create new session
        new_session = session_repo.create_new_session(vocab_ids)

        print("\n" + draw_box(
            f"Woche: {new_session.week_start} bis {new_session.week_end}\n"
            f"Vokabeln: {len(vocab_ids)}\n"
            f"\n"
            f"Bereit zum Lernen!",
            title="✓ Neue Wochensitzung erstellt"
        ))

        print("\nStarten Sie das Lernen mit:")
        print("  nihon-cli weekly-session start")

    except KeyboardInterrupt:
        print("\n\nAbgebrochen.")
        sys.exit(0)
    except Exception as e:
        print(f"✗ Fehler: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def handle_weekly_session_status_command(args: argparse.Namespace) -> None:
    """
    Handler for the 'vocab weekly-session status' command.

    Shows current weekly session progress and statistics.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
    """
    from nihon_cli.infra.weekly_session_repository import WeeklySessionRepository
    from nihon_cli.ui.formatting import draw_box

    try:
        session_repo = WeeklySessionRepository()
        current_session = session_repo.get_current_week_session()

        if not current_session:
            print("\n✗ Keine aktive Wochensitzung gefunden.")
            print("Verwenden Sie 'vocab weekly-session new' um eine Session zu erstellen.")
            sys.exit(0)

        # Get statistics
        stats = session_repo.get_session_statistics(current_session.id)
        items = session_repo.get_session_items(current_session.id, prioritize_by_progress=True)

        # Build status display
        status_content = (
            f"Woche: {current_session.week_start} bis {current_session.week_end}\n"
            f"Status: {'Aktiv' if current_session.status == 'active' else 'Abgeschlossen'}\n"
            f"\n"
            f"Vokabeln gesamt: {stats['total_items']}\n"
            f"Mit 2+ korrekt (JP→DE): {stats['items_2plus_german']}\n"
            f"Mit 2+ korrekt (DE→JP): {stats['items_2plus_japanese']}\n"
            f"\n"
            f"Durchschnittlicher Fortschritt: {stats['avg_progress']:.1f} korrekte Antworten"
        )

        print("\n" + draw_box(status_content, title="📊 Wochensitzung Status"))

        # Show items needing practice
        if items:
            print("\n🎯 Vokabeln mit niedrigem Fortschritt (Top 5):")
            low_progress_items = items[:5]
            for i, item in enumerate(low_progress_items, 1):
                jp_str = ", ".join(item.japanese_vocab)
                de_str = ", ".join(item.german_vocab)
                print(f"  {i}. {jp_str} → {de_str} (DE: {item.weekly_correct_german}, JP: {item.weekly_correct_japanese})")

    except Exception as e:
        print(f"✗ Fehler: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def handle_kanji_import_command(args: argparse.Namespace) -> None:
    """
    Handler for the 'kanji import' command.

    Imports kanji from image files using OCR (OpenAI Vision API).

    Args:
        args: Parsed command-line arguments with 'image_paths' and 'tag'.
    """
    from datetime import date
    from pathlib import Path
    from nihon_cli.core.ocr_parser import OpenAIVisionParser
    from nihon_cli.core.kanji import KanjiItem
    from nihon_cli.infra.kanji_repository import KanjiRepository

    try:
        image_paths = [Path(p) for p in args.image_paths]

        for path in image_paths:
            if not path.exists():
                print(f"✗ Bilddatei nicht gefunden: {path}")
                sys.exit(1)

        try:
            parser = OpenAIVisionParser()
        except ImportError as e:
            print(f"\n✗ Fehler: {e}")
            print("\nBitte installieren Sie das openai Package:")
            print("  pip install openai")
            sys.exit(1)
        except ValueError as e:
            print(f"\n✗ Fehler: {e}")
            print("\nStellen Sie sicher, dass OPENAI_API_KEY gesetzt ist:")
            print("  export OPENAI_API_KEY='your-api-key'")
            sys.exit(1)

        all_extracted = []
        for path in image_paths:
            print(f"🔍 Extrahiere Kanji aus {path.name}...")
            extracted = parser.extract_kanji_from_image(path)
            print(f"  ✓ {len(extracted)} Kanji gefunden")
            all_extracted.extend(extracted)

        if not all_extracted:
            print("Keine Kanji extrahiert. Bitte prüfen Sie die Bilder.")
            sys.exit(0)

        # Show extracted kanji for review
        print(f"\n📋 {len(all_extracted)} Kanji extrahiert:\n")
        for i, item in enumerate(all_extracted, 1):
            readings = ", ".join(item['readings'])
            print(f"  {i}. {item['kanji']} → {readings} ({item['meaning_german']})")

        print()
        confirm = input("Alle importieren? (J/n): ").strip().lower()
        if confirm == 'n':
            print("Import abgebrochen.")
            sys.exit(0)

        # Convert to KanjiItem objects
        tag = args.tag or f"kanji_{date.today().isoformat()}"
        kanji_items = []
        for item in all_extracted:
            kanji_item = KanjiItem(
                id=0,
                kanji=item['kanji'],
                readings_japanese=item['readings'],
                meaning_german=item['meaning_german'],
                source_file=", ".join(p.name for p in image_paths),
                upload_tag=tag,
            )
            kanji_items.append(kanji_item)

        repo = KanjiRepository()
        inserted, skipped = repo.add_kanji_batch(
            kanji_items,
            ", ".join(p.name for p in image_paths),
            tag
        )

        print(f"\n✓ {inserted} Kanji importiert ({skipped} Duplikate übersprungen)")

    except KeyboardInterrupt:
        print("\n\nAbgebrochen.")
        sys.exit(0)
    except Exception as e:
        print(f"✗ Fehler beim Importieren: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def handle_kanji_learn_command(args: argparse.Namespace) -> None:
    """
    Handler for the 'kanji learn' command.

    Starts an interactive kanji learning session with box logic.

    Args:
        args: Parsed command-line arguments with 'limit' and 'test'.
    """
    from nihon_cli.core.quiz_kanji import KanjiQuiz
    from nihon_cli.core.timer import LearningTimer
    from nihon_cli.infra.kanji_repository import KanjiRepository

    try:
        repository = KanjiRepository()
        quiz = KanjiQuiz(repository)

        interval_seconds = 5 if args.test else 1500

        while True:
            questions_asked = quiz.run_session(limit=args.limit)

            if questions_asked > 0:
                timer = LearningTimer(interval_seconds)
                timer.wait_for_next_session()
            else:
                break

    except KeyboardInterrupt:
        print("\n\n⚠️  Lernsitzung abgebrochen.")
        sys.exit(0)
    except Exception as e:
        print(f"✗ Unerwarteter Fehler: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def handle_kanji_list_command(args: argparse.Namespace) -> None:
    """
    Handler for the 'kanji list' command.

    Shows all imported kanji with their progress.
    """
    from nihon_cli.infra.kanji_repository import KanjiRepository
    from nihon_cli.ui.formatting import draw_box, COLOR_GREEN, COLOR_RESET

    try:
        repo = KanjiRepository()
        all_kanji = repo.get_all_kanji()

        if not all_kanji:
            print("\n✗ Keine Kanji importiert.")
            print("Verwenden Sie 'nihon-cli kanji import <bild>' um Kanji zu importieren.")
            sys.exit(0)

        stats = repo.get_statistics()

        header = (
            f"Gesamt: {stats['total']}  |  "
            f"Gelernt: {COLOR_GREEN}{stats['completed']}{COLOR_RESET}  |  "
            f"Offen: {stats['in_progress']}"
        )
        print("\n" + draw_box(header, title="漢字 Kanji-Übersicht"))

        print()
        for item in all_kanji:
            readings = ", ".join(item.readings_japanese)
            status = f"{COLOR_GREEN}✓{COLOR_RESET}" if item.completed else f"{item.correct_count}/5"
            print(f"  {item.kanji}  {readings}  ({item.meaning_german})  [{status}]")

    except Exception as e:
        print(f"✗ Fehler: {e}")
        sys.exit(1)


def handle_config_set_command(key: str, value: str) -> None:
    """
    Handler for the 'config set' command.

    Saves a configuration key-value pair to the config file.

    Args:
        key: The configuration key to set
        value: The configuration value to set
    """
    try:
        save_config(key, value)
        print(f"✓ Konfiguration gespeichert: {key} = {value}")
    except Exception as e:
        print(f"✗ Fehler beim Speichern der Konfiguration: {e}")
        sys.exit(1)


def handle_flash_katakana_command(args: argparse.Namespace) -> None:
    from nihon_cli.core.flash import run_flash_katakana

    run_flash_katakana()


def handle_flash_kanji_command(args: argparse.Namespace) -> None:
    from nihon_cli.core.flash import run_flash_kanji

    run_flash_kanji()


def setup_argument_parser() -> argparse.ArgumentParser:
    """
    Creates and configures the argument parser for the CLI.

    This function sets up all commands, sub-commands, and arguments
    for the application. Using argparse is a security best practice as it
    prevents command injection vulnerabilities by design.

    Returns:
        argparse.ArgumentParser: The configured parser instance.
    """
    parser = argparse.ArgumentParser(
        prog="nihon-cli",
        description="A Python-based CLI tool for learning Japanese characters (Hiragana and Katakana) with automated learning intervals.",
        epilog="Use 'nihon-cli <command> --help' for more information on a specific command.",
    )

    subparsers = parser.add_subparsers(
        dest="command", help="Select a training mode", required=True
    )

    # Subparser for 'hiragana'
    hiragana_parser = subparsers.add_parser(
        "hiragana", help="Start a Hiragana character training session"
    )
    hiragana_parser.add_argument(
        "--test",
        action="store_true",
        help="Run in 5-second test mode instead of the standard 25-minute intervals",
    )
    hiragana_parser.add_argument(
        "--advanced",
        action="store_true",
        help="Include advanced combination characters (Yōon) in addition to basic characters",
    )
    hiragana_parser.set_defaults(func=handle_hiragana_command)

    # Subparser for 'katakana'
    katakana_parser = subparsers.add_parser(
        "katakana", help="Start a Katakana character training session"
    )
    katakana_parser.add_argument(
        "--test",
        action="store_true",
        help="Run in 5-second test mode instead of the standard 25-minute intervals",
    )
    katakana_parser.add_argument(
        "--advanced",
        action="store_true",
        help="Include advanced combination characters (Yōon) in addition to basic characters",
    )
    katakana_parser.set_defaults(func=handle_katakana_command)

    # Subparser for 'mixed'
    mixed_parser = subparsers.add_parser(
        "mixed", help="Start a mixed Hiragana and Katakana character training session"
    )
    mixed_parser.add_argument(
        "--test",
        action="store_true",
        help="Run in 5-second test mode instead of the standard 25-minute intervals",
    )
    mixed_parser.add_argument(
        "--advanced",
        action="store_true",
        help="Include advanced combination characters (Yōon) in addition to basic characters",
    )
    mixed_parser.set_defaults(func=handle_mixed_command)

    # Subparser for 'words'
    words_parser = subparsers.add_parser(
        "words", help="Start a Japanese vocabulary training session"
    )
    words_parser.add_argument(
        "--test",
        action="store_true",
        help="Run in 5-second test mode instead of the standard 25-minute intervals",
    )
    words_parser.set_defaults(func=handle_words_command)

    # Subparser for 'vocab'
    vocab_parser = subparsers.add_parser(
        "vocab", help="Vocabulary learning and management"
    )
    vocab_subparsers = vocab_parser.add_subparsers(
        dest="vocab_command", help="Vocabulary sub-commands"
    )

    # vocab upload subcommand
    upload_parser = vocab_subparsers.add_parser(
        "upload",
        help="Upload vocabulary from a Markdown or Excel (.xlsx) file"
    )
    upload_parser.add_argument(
        "file",
        type=str,
        help="Path to the Markdown or Excel file containing vocabulary"
    )
    upload_parser.add_argument(
        "--tag",
        type=str,
        help="Optional tag for this upload (default: filename without extension)"
    )
    upload_parser.set_defaults(func=handle_vocab_upload_command)

    # vocab learn subcommand
    learn_parser = vocab_subparsers.add_parser(
        "learn",
        help="Start an interactive vocabulary learning session"
    )
    learn_parser.add_argument(
        "--limit",
        type=int,
        default=15,
        help="Number of vocabulary items per session (default: 15)"
    )
    learn_parser.add_argument(
        "--test",
        action="store_true",
        help="Run in 5-second test mode instead of the standard 25-minute intervals"
    )
    learn_parser.set_defaults(func=handle_vocab_learn_command)

    # Subparser for 'weekly-session' (top-level command)
    weekly_parser = subparsers.add_parser(
        "weekly-session",
        help="Weekly vocabulary learning sessions (Thursday-Wednesday cycles)"
    )
    weekly_subparsers = weekly_parser.add_subparsers(
        dest="weekly_command",
        help="Weekly session sub-commands"
    )

    # weekly-session new
    new_parser = weekly_subparsers.add_parser(
        "new",
        help="Create a new weekly session with selected vocabulary"
    )
    new_parser.add_argument(
        "--tag",
        type=str,
        help="Optional tag to filter vocabulary by"
    )
    new_parser.set_defaults(func=handle_weekly_session_new_command)

    # weekly-session start
    start_parser = weekly_subparsers.add_parser(
        "start",
        help="Start or continue the current week's learning session"
    )
    start_parser.add_argument(
        "--test",
        action="store_true",
        help="Run in 5-second test mode instead of 25-minute intervals"
    )
    start_parser.set_defaults(func=handle_weekly_session_start_command)

    # weekly-session import-image
    import_parser = weekly_subparsers.add_parser(
        "import-image",
        help="Import vocabulary from an image using OCR"
    )
    import_parser.add_argument(
        "image_path",
        type=str,
        help="Path to the image file"
    )
    import_parser.add_argument(
        "--tag",
        type=str,
        help="Optional tag for this import (default: ocr_<date>)"
    )
    import_parser.set_defaults(func=handle_weekly_session_import_image_command)

    # weekly-session status
    status_parser = weekly_subparsers.add_parser(
        "status",
        help="Show current week's progress and statistics"
    )
    status_parser.set_defaults(func=handle_weekly_session_status_command)

    # Subparser for 'kanji'
    kanji_parser = subparsers.add_parser(
        "kanji", help="Kanji learning and management"
    )
    kanji_subparsers = kanji_parser.add_subparsers(
        dest="kanji_command", help="Kanji sub-commands"
    )

    # kanji import
    kanji_import_parser = kanji_subparsers.add_parser(
        "import",
        help="Import kanji from image files using OCR"
    )
    kanji_import_parser.add_argument(
        "image_paths",
        nargs='+',
        type=str,
        help="Paths to image files containing kanji"
    )
    kanji_import_parser.add_argument(
        "--tag",
        type=str,
        help="Optional tag for this import (default: kanji_<date>)"
    )
    kanji_import_parser.set_defaults(func=handle_kanji_import_command)

    # kanji learn
    kanji_learn_parser = kanji_subparsers.add_parser(
        "learn",
        help="Start an interactive kanji learning session"
    )
    kanji_learn_parser.add_argument(
        "--limit",
        type=int,
        default=15,
        help="Number of kanji per session (default: 15)"
    )
    kanji_learn_parser.add_argument(
        "--test",
        action="store_true",
        help="Run in 5-second test mode instead of 25-minute intervals"
    )
    kanji_learn_parser.set_defaults(func=handle_kanji_learn_command)

    # kanji list
    kanji_list_parser = kanji_subparsers.add_parser(
        "list",
        help="Show all imported kanji with learning progress"
    )
    kanji_list_parser.set_defaults(func=handle_kanji_list_command)

    # Subparser for 'flash'
    flash_parser = subparsers.add_parser(
        "flash", help="Flash card window for learning characters"
    )
    flash_subparsers = flash_parser.add_subparsers(
        dest="flash_command", help="Flash card sub-commands"
    )

    flash_katakana_parser = flash_subparsers.add_parser(
        "katakana", help="Katakana flash cards in a floating window"
    )
    flash_katakana_parser.set_defaults(func=handle_flash_katakana_command)

    flash_kanji_parser = flash_subparsers.add_parser(
        "kanji", help="Kanji flash cards (unlearned kanji from database)"
    )
    flash_kanji_parser.set_defaults(func=handle_flash_kanji_command)

    # Subparser for 'config'
    config_parser = subparsers.add_parser(
        "config", help="Configuration management"
    )
    config_subparsers = config_parser.add_subparsers(
        dest="config_command", help="Configuration sub-commands"
    )

    # config set subcommand
    set_parser = config_subparsers.add_parser(
        "set",
        help="Set a configuration value"
    )
    set_parser.add_argument(
        "key",
        type=str,
        help="Configuration key to set"
    )
    set_parser.add_argument(
        "value",
        type=str,
        help="Configuration value to set"
    )
    set_parser.set_defaults(func=lambda args: handle_config_set_command(args.key, args.value))

    return parser


def parse_and_execute(args: Optional[List[str]] = None) -> None:
    """
    Parses command-line arguments and executes the corresponding action.

    Args:
        args (Optional[List[str]], optional): A list of strings to parse.
                                              If None, sys.argv[1:] is used.
                                              Defaults to None.
    """
    parser = setup_argument_parser()

    # If no arguments are provided (e.g., just 'nihon'), show help
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        return

    parsed_args = parser.parse_args(args)

    if hasattr(parsed_args, "func"):
        parsed_args.func(parsed_args)
    else:
        # Fallback if a command is called without a function
        # (should not happen with required=True)
        parser.print_help(sys.stderr)


if __name__ == "__main__":
    parse_and_execute()

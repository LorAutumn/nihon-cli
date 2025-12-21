"""Interactive terminal UI for selecting vocabulary items.

This module provides the VocabItemSelector class for displaying
extracted vocabulary items and allowing users to select and edit them.
"""

from typing import Dict, List

from nihon_cli.ui.formatting import draw_box, COLOR_GREEN, COLOR_YELLOW, COLOR_RESET


class VocabItemSelector:
    """Terminal-based UI for selecting and editing vocabulary items.

    Provides an interactive interface for:
    - Displaying extracted vocabulary items with numbering
    - Allowing selection via comma-separated numbers or 'all'
    - Editing individual items before final confirmation
    """

    def display_and_select(self, extracted_items: List[Dict]) -> List[Dict]:
        """Display extracted items and allow user to select which to import.

        User Flow:
        1. Display all items with index numbers
        2. Prompt user to select items
        3. For each selected item, offer editing option
        4. Return final selection

        Args:
            extracted_items: List of vocabulary dictionaries from OCR

        Returns:
            List of selected (and potentially edited) vocabulary dictionaries
        """
        if not extracted_items:
            print("Keine Vokabeln zum Auswählen verfügbar.")
            return []

        # Display all items
        print("\n" + draw_box(
            f"Gefundene Vokabeln: {len(extracted_items)}",
            title="📋 OCR-Ergebnisse"
        ))

        for idx, item in enumerate(extracted_items, 1):
            self._display_item(idx, item)

        # Get selection from user
        print(f"\n{COLOR_YELLOW}Auswahl:{COLOR_RESET}")
        print("  • Einzelne Items: z.B. '1,3,5'")
        print("  • Alle Items: 'all'")
        print("  • Keine Items: 'none'")

        selection_input = input("\n> ").strip().lower()

        # Parse selection
        selected_indices = self._parse_selection(selection_input, len(extracted_items))

        if not selected_indices:
            print("Keine Items ausgewählt.")
            return []

        # Get selected items
        selected_items = [extracted_items[i - 1] for i in selected_indices]

        # Offer editing for each item
        final_items = []
        for idx, item in zip(selected_indices, selected_items):
            uncertain = item.get('uncertain', False)

            if uncertain:
                print(f"\n{COLOR_YELLOW}⚠️  Item {idx} ausgewählt (UNSICHER):{COLOR_RESET}")
            else:
                print(f"\n{COLOR_GREEN}Item {idx} ausgewählt:{COLOR_RESET}")
            self._display_item_compact(item)

            # Auto-prompt editing for uncertain items
            if uncertain:
                print(f"\n{COLOR_YELLOW}⚠️  Dieses Item wurde als unsicher markiert.{COLOR_RESET}")
                edit_choice = input("Möchten Sie dieses Item bearbeiten? (J/n): ").strip().lower()
                # Default to 'yes' for uncertain items (empty input = yes)
                if edit_choice != 'n':
                    edited_item = self._edit_item(item)
                    final_items.append(edited_item)
                else:
                    final_items.append(item)
            else:
                edit_choice = input("\nMöchten Sie dieses Item bearbeiten? (j/N): ").strip().lower()
                if edit_choice == 'j':
                    edited_item = self._edit_item(item)
                    final_items.append(edited_item)
                else:
                    final_items.append(item)

        # Final confirmation
        print("\n" + draw_box(
            f"Items zum Importieren: {len(final_items)}",
            title="✓ Finale Auswahl"
        ))

        for idx, item in enumerate(final_items, 1):
            self._display_item_compact(item, prefix=f"{idx}. ")

        confirm = input("\nImportieren? (J/n): ").strip().lower()

        if confirm == 'n':
            print("Import abgebrochen.")
            return []

        return final_items

    def _display_item(self, index: int, item: Dict) -> None:
        """Display a vocabulary item with full details.

        Args:
            index: Item number for display
            item: Vocabulary dictionary
        """
        japanese_str = ", ".join(item.get('japanese', []))
        german_str = ", ".join(item.get('german', []))
        vocab_type = item.get('vocab_type', 'noun')
        base_form = item.get('base_form', '')
        uncertain = item.get('uncertain', False)

        content = (
            f"Japanisch:  {japanese_str}\n"
            f"Deutsch:    {german_str}\n"
            f"Typ:        {vocab_type}"
        )

        if base_form:
            content += f"\nGrundform:  {base_form}"

        if uncertain:
            content += f"\n\n{COLOR_YELLOW}⚠️  UNSICHER - Bitte überprüfen!{COLOR_RESET}"

        title = f"Item {index}" + (" ⚠️" if uncertain else "")
        print("\n" + draw_box(content, title=title))

    def _display_item_compact(self, item: Dict, prefix: str = "") -> None:
        """Display a vocabulary item in compact format.

        Args:
            item: Vocabulary dictionary
            prefix: Optional prefix string
        """
        japanese_str = ", ".join(item.get('japanese', []))
        german_str = ", ".join(item.get('german', []))
        vocab_type = item.get('vocab_type', 'noun')
        uncertain = item.get('uncertain', False)

        warning = f" {COLOR_YELLOW}⚠️{COLOR_RESET}" if uncertain else ""
        print(f"{prefix}{japanese_str} → {german_str} [{vocab_type}]{warning}")

        if item.get('base_form'):
            print(f"{' ' * len(prefix)}Grundform: {item['base_form']}")

    def _parse_selection(self, selection_input: str, max_index: int) -> List[int]:
        """Parse user selection input into list of indices.

        Args:
            selection_input: User input string
            max_index: Maximum valid index

        Returns:
            List of selected indices (1-based)
        """
        if selection_input == 'none' or not selection_input:
            return []

        if selection_input == 'all':
            return list(range(1, max_index + 1))

        # Parse comma-separated numbers
        indices = []
        parts = selection_input.split(',')

        for part in parts:
            part = part.strip()
            try:
                index = int(part)
                if 1 <= index <= max_index:
                    if index not in indices:  # Avoid duplicates
                        indices.append(index)
            except ValueError:
                # Skip invalid input
                continue

        return sorted(indices)

    def _edit_item(self, item: Dict) -> Dict:
        """Allow user to edit fields of a vocabulary item.

        Args:
            item: Vocabulary dictionary to edit

        Returns:
            Edited vocabulary dictionary
        """
        print(f"\n{COLOR_YELLOW}--- Editing Item ---{COLOR_RESET}")

        # Edit Japanese
        japanese_str = ", ".join(item.get('japanese', []))
        print(f"\nAktuell Japanisch: {japanese_str}")
        new_japanese = input("Neues Japanisch (leer = keine Änderung): ").strip()
        if new_japanese:
            item['japanese'] = [j.strip() for j in new_japanese.split(',')]

        # Edit German
        german_str = ", ".join(item.get('german', []))
        print(f"\nAktuell Deutsch: {german_str}")
        new_german = input("Neues Deutsch (leer = keine Änderung): ").strip()
        if new_german:
            item['german'] = [g.strip() for g in new_german.split(',')]

        # Edit vocab type
        current_type = item.get('vocab_type', 'noun')
        print(f"\nAktueller Typ: {current_type}")
        print("Optionen: noun, adjective, pattern")
        new_type = input("Neuer Typ (leer = keine Änderung): ").strip().lower()
        if new_type in ('noun', 'adjective', 'pattern'):
            item['vocab_type'] = new_type

        # Edit base form
        current_base = item.get('base_form', '')
        print(f"\nAktuelle Grundform: {current_base if current_base else '(keine)'}")
        new_base = input("Neue Grundform (leer = keine Änderung, '-' = löschen): ").strip()
        if new_base == '-':
            item['base_form'] = None
        elif new_base:
            item['base_form'] = new_base

        print(f"\n{COLOR_GREEN}✓ Item aktualisiert{COLOR_RESET}")

        return item

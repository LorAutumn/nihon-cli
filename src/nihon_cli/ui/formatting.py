import shutil
import textwrap

# ANSI escape codes for colors
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_RESET = "\033[0m"

def get_terminal_width(fallback=80):
    """
    Gets the current terminal width.
    Falls back to a default value if the width cannot be determined.
    """
    return shutil.get_terminal_size((fallback, 20)).columns

def draw_box(content, title=None, min_width=50):
    """
    Draws a box around the given content with an optional title.
    The box width adapts to the terminal size and content length.
    """
    terminal_width = get_terminal_width()
    lines = content.split('\n')

    # Determine the maximum width required by either the title or the content lines
    max_content_width = max(len(line) for line in lines) if lines else 0
    title_width = len(title) + 4 if title else 0  # +4 for padding "─ " and " ─"
    
    # The inner width of the box is the max of content, title, and min_width
    required_width = max(max_content_width, title_width, min_width)
    
    # Ensure the box does not exceed the terminal width
    inner_width = min(required_width, terminal_width - 4)

    # --- Drawing the box ---

    # Top border
    if title:
        # Format: "┌─ TITLE ─...─┐"
        title_bar = f"─ {title} ".ljust(inner_width + 2, '─')
        box = f"┌{title_bar}┐\n"
    else:
        box = f"┌{'─' * (inner_width + 2)}┐\n"

    # Content lines
    all_wrapped_lines = []
    for line in lines:
        # Wrap lines, preserving empty lines
        wrapped = textwrap.wrap(line, width=inner_width, replace_whitespace=False, drop_whitespace=False)
        if not wrapped:
            all_wrapped_lines.append("")
        else:
            all_wrapped_lines.extend(wrapped)

    for line in all_wrapped_lines:
        box += f"│ {line.ljust(inner_width)} │\n"

    # Bottom border
    box += f"└{'─' * (inner_width + 2)}┘"
    
    return box

def format_quiz_session(session_info):
    """
    Formats the quiz session information in a styled box.
    """
    content = (
        f"Typ: {session_info.get('type', 'N/A')}\n"
        f"Fragen: {session_info.get('questions', 'N/A')}"
    )
    return draw_box(content, title="Quiz Sitzung")

def format_question(question_text, question_number, total_questions):
    """
    Formats a single question in a styled box.
    """
    title = f"Frage {question_number}/{total_questions}"
    return draw_box(question_text, title=title)

def format_correct_answer(text="Richtig!"):
    """
    Formats a correct answer with a green checkmark emoji.
    """
    return f"{COLOR_GREEN}✅ {text}{COLOR_RESET}"

def format_incorrect_answer(user_answer, correct_answer, character=None):
    """
    Formats an incorrect answer with a red cross emoji and shows the correct answer.
    For character quiz, shows the new format with user input converted to kana.
    """
    if character is not None:
        # New format for character quiz
        from nihon_cli.core.romaji_converter import _converter
        
        # Convert user's romaji input to kana if possible (use word conversion for better results)
        user_kana = _converter.convert_word_to_kana(user_answer, prefer_hiragana=(character.character_type == "hiragana"))
        user_kana_display = f" ({user_kana})" if user_kana else ""
        
        # Improved format with better spacing and structure
        user_line = f"Antwort: {user_answer}{user_kana_display}"
        correct_line = f"Lösung:  {character.romaji} ({character.symbol})"
        feedback_line = f"{COLOR_RED}❌ Falsch!{COLOR_RESET}"
        
        return f"{user_line}\n{correct_line}\n{feedback_line}"
    else:
        # Fallback to old format
        return f"{COLOR_RED}❌ Falsch! Die richtige Antwort ist: {correct_answer}{COLOR_RESET}"


def format_word_correct_answer(word):
    """
    Formats a correct word answer with Japanese, romaji, and German translation.
    Format: "Antwort: [japanese] ([romaji]) ( [german] ) \n ✅ Richtig!"
    """
    from nihon_cli.core.word import Word
    if isinstance(word, Word):
        answer_line = f"Antwort: {word.japanese} ({word.romaji}) ( {word.german} )"
        feedback_line = f"{COLOR_GREEN}✅ Richtig!{COLOR_RESET}"
        return f"{answer_line}\n{feedback_line}"
    else:
        return format_correct_answer()


def format_word_incorrect_answer(user_answer, word):
    """
    Formats an incorrect word answer with the new format.
    Format: "Antwort: <user_input> (<kana_if_romaji>) \n Lösung: <romaji> (<japanese>) (<german>) \n ❌ Falsch!"
    """
    from nihon_cli.core.word import Word
    if isinstance(word, Word):
        # Try to convert user's romaji input to kana if possible (only if not in word DB)
        from nihon_cli.core.romaji_converter import _converter
        user_kana = _converter.convert_word_to_kana_safe(user_answer, prefer_hiragana=True)
        user_kana_display = f" ({user_kana})" if user_kana else ""
        
        # New format for word quiz with improved spacing
        user_line = f"Antwort: {user_answer}{user_kana_display}"
        correct_line = f"Lösung:  {word.romaji} ({word.japanese}) ({word.german})"
        feedback_line = f"{COLOR_RED}❌ Falsch!{COLOR_RESET}"
        return f"{user_line}\n{correct_line}\n{feedback_line}"
    else:
        return format_incorrect_answer(user_answer, "Unknown")
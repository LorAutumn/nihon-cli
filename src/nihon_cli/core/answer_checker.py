"""Semantic answer checking for vocabulary quizzes.

Uses a local Ollama LLM to determine if a user's answer is semantically
equivalent to the expected answer. Falls back to exact matching when
Ollama is not available.
"""

from dataclasses import dataclass
from typing import List, Optional

try:
    import ollama as _ollama_client

    _OLLAMA_AVAILABLE = True
except ImportError:
    _OLLAMA_AVAILABLE = False

_PROMPT_TEMPLATE = """\
Du bist ein Korrektor für ein Japanisch-Deutsch Vokabelquiz (Anfängerniveau A1).

Beispiele:
- Erwartet "Großvater", Antwort "Opa" -> JA (umgangssprachlich gleich)
- Erwartet "eigener älterer Bruder", Antwort "großer Bruder" -> JA (umgangssprachlich gleich)
- Erwartet "eigener jüngerer Bruder", Antwort "kleiner Bruder" -> JA (umgangssprachlich gleich)
- Erwartet "Ehemann", Antwort "Mann" -> NEIN ("Mann" ist nicht dasselbe wie "Ehemann")
- Erwartet "Ehefrau", Antwort "Frau" -> NEIN ("Frau" ist nicht dasselbe wie "Ehefrau")
- Erwartet "Großvater", Antwort "Onkel" -> NEIN (falsch)
- Erwartet "jüngerer Bruder von jemand anderem", Antwort "jüngerer Bruder" -> NEIN (Qualifier fehlt)

WICHTIG: Oberbegriffe sind KEINE Synonyme ("Frau" ≠ "Ehefrau"), aber umgangssprachliche Varianten SIND Synonyme ("großer Bruder" = "älterer Bruder").

Erwartete Antwort(en): {expected}
Antwort des Schülers: {answer}

Antworte NUR mit: JA oder NEIN"""


@dataclass
class AnswerCheckResult:
    accepted: bool
    method: str  # "exact", "semantic", "fallback_exact"
    feedback: Optional[str] = None


class AnswerChecker:
    """Check quiz answers with optional semantic comparison via Ollama."""

    def __init__(self, model: str = "gemma3:4b"):
        self.model = model
        self._ollama_ok: Optional[bool] = None

    def check(
        self,
        user_input: str,
        correct_answers: List[str],
        direction: str,
    ) -> AnswerCheckResult:
        """Check if the user's answer is acceptable.

        1. Exact match (fast path)
        2. For jp_to_de only: semantic LLM check via Ollama
        3. Graceful fallback to exact-only when Ollama unavailable
        """
        normalized = user_input.strip().lower()

        # Fast path: exact match
        if any(normalized == a.strip().lower() for a in correct_answers):
            return AnswerCheckResult(accepted=True, method="exact")

        # No semantic check for Japanese answers
        if direction == "de_to_jp":
            return AnswerCheckResult(accepted=False, method="exact")

        # Try semantic check
        if not self._is_ollama_available():
            return AnswerCheckResult(accepted=False, method="fallback_exact")

        return self._semantic_check(normalized, correct_answers)

    def _is_ollama_available(self) -> bool:
        if not _OLLAMA_AVAILABLE:
            return False
        if self._ollama_ok is not None:
            return self._ollama_ok
        try:
            _ollama_client.list()
            self._ollama_ok = True
        except Exception:
            self._ollama_ok = False
        return self._ollama_ok

    def _semantic_check(
        self, user_input: str, correct_answers: List[str]
    ) -> AnswerCheckResult:
        expected = ", ".join(correct_answers)
        prompt = _PROMPT_TEMPLATE.format(expected=expected, answer=user_input)

        try:
            response = _ollama_client.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0, "num_predict": 10},
            )
            reply = response["message"]["content"].strip().upper()
            accepted = reply.startswith("JA")
            return AnswerCheckResult(
                accepted=accepted,
                method="semantic",
                feedback="als Synonym akzeptiert" if accepted else None,
            )
        except Exception:
            return AnswerCheckResult(accepted=False, method="fallback_exact")

"""
Flash card window for learning Japanese characters.

Opens a small always-on-top native window that cycles through
characters at a configurable interval.
"""

import json
import random
from dataclasses import dataclass
from typing import List

import webview


@dataclass(frozen=True)
class FlashEntry:
    main: str
    reading: str
    word: str
    word_detail: str


def _build_html(cards: list[FlashEntry]) -> str:
    cards_json = json.dumps(
        [
            {
                "main": c.main,
                "reading": c.reading,
                "word": c.word,
                "wordDetail": c.word_detail,
            }
            for c in cards
        ],
        ensure_ascii=False,
    )

    return (
        """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }

  :root {
    --bg: #1a1a2e;
    --accent: #e94560;
    --text: #eaeaea;
    --text-dim: #a0a0b0;
    --settings-bg: rgba(22, 33, 62, 0.95);
  }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: "Hiragino Sans", "Noto Sans JP", "Yu Gothic", sans-serif;
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    user-select: none;
    -webkit-user-select: none;
  }

  #card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2vh;
    transition: opacity 1s ease;
    opacity: 1;
  }

  #card.fade-out { opacity: 0; }
  #card.fade-in { opacity: 1; }

  #main-char {
    font-size: 28vmin;
    font-weight: 700;
    line-height: 1;
    color: var(--text);
    text-shadow: 0 0 40px rgba(233, 69, 96, 0.3);
  }

  #reading {
    font-size: 6vmin;
    color: var(--text-dim);
    letter-spacing: 0.1em;
  }

  #example {
    font-size: 4.5vmin;
    color: var(--text-dim);
    text-align: center;
    line-height: 1.4;
    transition: opacity 0.3s;
  }

  #example .word { color: var(--accent); font-size: 5vmin; }
  #example .detail { font-size: 3.5vmin; opacity: 0.7; }

  #settings-trigger {
    position: fixed;
    top: 0;
    right: 0;
    width: 60px;
    height: 60px;
    z-index: 100;
  }

  #settings {
    position: fixed;
    top: 10px;
    right: 10px;
    background: var(--settings-bg);
    border: 1px solid rgba(233, 69, 96, 0.3);
    border-radius: 12px;
    padding: 16px;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s;
    z-index: 101;
    min-width: 200px;
  }

  #settings-trigger:hover ~ #settings,
  #settings:hover {
    opacity: 1;
    pointer-events: auto;
  }

  #settings label {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 13px;
    color: var(--text-dim);
    margin-bottom: 12px;
    gap: 12px;
  }

  #settings label:last-child { margin-bottom: 0; }

  #settings input[type="range"] {
    width: 90px;
    accent-color: var(--accent);
  }

  #settings input[type="checkbox"] {
    accent-color: var(--accent);
    width: 16px;
    height: 16px;
  }

  #settings .value {
    min-width: 28px;
    text-align: right;
    color: var(--text);
    font-weight: 600;
  }

</style>
</head>
<body>

<div id="card">
  <div id="main-char"></div>
  <div id="reading"></div>
  <div id="example">
    <div class="word"></div>
    <div class="detail"></div>
  </div>
</div>

<div id="settings-trigger"></div>
<div id="settings">
  <label>
    Intervall
    <input type="range" id="interval" min="1" max="15" value="4">
    <span class="value" id="interval-val">4s</span>
  </label>
  <label>
    Beispielwort
    <input type="checkbox" id="show-example" checked>
  </label>
  <label>
    Aussprache
    <input type="checkbox" id="show-reading" checked>
  </label>
</div>

<script>
const cards = """
        + cards_json
        + """;

let interval = 4;
let showExample = true;
let showReading = true;
let timer = null;
let lastIndex = -1;

const elMain = document.getElementById('main-char');
const elReading = document.getElementById('reading');
const elExample = document.getElementById('example');
const elInterval = document.getElementById('interval');
const elIntervalVal = document.getElementById('interval-val');
const elShowExample = document.getElementById('show-example');
const elShowReading = document.getElementById('show-reading');

function pickRandom() {
  let idx;
  do { idx = Math.floor(Math.random() * cards.length); } while (idx === lastIndex && cards.length > 1);
  lastIndex = idx;
  return cards[idx];
}

const cardEl = document.getElementById('card');
const FADE_MS = 1000;

function applyCard(card) {
  elMain.textContent = card.main;
  elReading.textContent = showReading ? card.reading : '';
  elReading.style.display = showReading ? '' : 'none';

  if (showExample && card.word) {
    elExample.style.display = '';
    elExample.querySelector('.word').textContent = card.word;
    elExample.querySelector('.detail').textContent = card.wordDetail;
  } else {
    elExample.style.display = 'none';
  }
}

function showCard() {
  const card = pickRandom();
  cardEl.classList.add('fade-out');

  setTimeout(function() {
    applyCard(card);
    cardEl.classList.remove('fade-out');
  }, FADE_MS);
}

function resetTimer() {
  clearInterval(timer);
  timer = setInterval(showCard, interval * 1000);
}

function next() {
  showCard();
  resetTimer();
}

document.body.addEventListener('click', function(e) {
  if (e.target.closest('#settings') || e.target.closest('#settings-trigger')) return;
  next();
});

document.addEventListener('keydown', function(e) {
  if (e.key === ' ' || e.key === 'ArrowRight') {
    e.preventDefault();
    next();
  }
});

elInterval.addEventListener('input', function() {
  interval = parseInt(this.value);
  elIntervalVal.textContent = interval + 's';
  next();
});

elShowExample.addEventListener('change', function() {
  showExample = this.checked;
  showCard();
  resetTimer();
});

elShowReading.addEventListener('change', function() {
  showReading = this.checked;
  showCard();
  resetTimer();
});

applyCard(pickRandom());
resetTimer();
</script>
</body>
</html>"""
    )


def _katakana_entries() -> List[FlashEntry]:
    from nihon_cli.data.katakana_flash import KATAKANA_FLASH_CARDS

    return [
        FlashEntry(
            main=c.katakana,
            reading=c.hiragana,
            word=c.example_word,
            word_detail=f"{c.example_reading} - {c.example_meaning}",
        )
        for c in KATAKANA_FLASH_CARDS
    ]


def _kanji_entries() -> List[FlashEntry]:
    from nihon_cli.infra.kanji_repository import KanjiRepository

    repo = KanjiRepository()
    items = repo.get_incomplete_kanji(limit=999)
    if not items:
        raise SystemExit("Keine ungelernten Kanji vorhanden.")

    return [
        FlashEntry(
            main=k.kanji,
            reading=", ".join(k.readings_japanese),
            word=k.meaning_german,
            word_detail="",
        )
        for k in items
    ]


def _open_flash(entries: List[FlashEntry], title: str) -> None:
    random.shuffle(entries)
    html = _build_html(entries)
    webview.create_window(
        title,
        html=html,
        width=400,
        height=500,
        resizable=True,
        on_top=True,
    )
    webview.start()


def run_flash_katakana() -> None:
    _open_flash(_katakana_entries(), "Katakana Flash")


def run_flash_kanji() -> None:
    _open_flash(_kanji_entries(), "Kanji Flash")

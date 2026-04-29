#!/usr/bin/env python3
"""
Prison Architect AI Observer

Reads a Prison Architect save file (.prison), extracts every prisoner, and
asks a local Ollama model to generate a personality dossier for each one.
Writes the result to dossier.md so you can read it alongside the game.

This is an *external* tool. It does not run inside Prison Architect — PA's
Lua mod API does not allow network/file I/O from scripts, so an in-game LLM
integration is impossible. Instead, this tool reads your real save file
after the game has saved it.

Usage:
    python ai_observer.py --save "<path to .prison file>"
    python ai_observer.py --save "<path>" --model mistral
    python ai_observer.py --save "<path>" --watch        # re-run on every save
    python ai_observer.py --save "<path>" --limit 10     # first 10 prisoners
    python ai_observer.py --self-test                    # check Ollama only
"""

import argparse
import os
import re
import sys
import time
from pathlib import Path

import requests

OLLAMA_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama3"
DEFAULT_OUTPUT = "dossier.md"


# ---------- PA save parser --------------------------------------------------

def parse_prison_save(text):
    """Parse a Prison Architect .prison file into a nested structure.

    PA's format is a tree of BEGIN <Name> ... END blocks containing
    whitespace-separated key/value pairs. The parser here is intentionally
    forgiving: every block becomes a dict with a special "_blocks" list for
    nested children, and unknown lines are kept as raw fields.
    """
    tokens = _tokenize(text)
    pos = [0]
    root = {"_name": "ROOT", "_blocks": []}
    while pos[0] < len(tokens):
        tok = tokens[pos[0]]
        if tok == "BEGIN":
            block = _parse_block(tokens, pos)
            root["_blocks"].append(block)
        else:
            pos[0] += 1
    return root


def _tokenize(text):
    out = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        out.extend(line.split())
    return out


def _parse_block(tokens, pos):
    assert tokens[pos[0]] == "BEGIN"
    pos[0] += 1
    name = tokens[pos[0]] if pos[0] < len(tokens) else "Unknown"
    pos[0] += 1
    block = {"_name": name, "_blocks": []}
    while pos[0] < len(tokens):
        tok = tokens[pos[0]]
        if tok == "END":
            pos[0] += 1
            return block
        if tok == "BEGIN":
            child = _parse_block(tokens, pos)
            block["_blocks"].append(child)
            continue
        # key value pair (value may be missing -> store as empty string)
        key = tok
        pos[0] += 1
        if pos[0] < len(tokens) and tokens[pos[0]] not in ("BEGIN", "END"):
            value = tokens[pos[0]]
            pos[0] += 1
        else:
            value = ""
        block[key] = value
    return block


def find_prisoners(tree):
    """Walk the parsed tree and return every block that looks like a prisoner."""
    prisoners = []
    stack = [tree]
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            if node.get("Type") == "Prisoner" or node.get("_name") == "Prisoner":
                prisoners.append(node)
            for child in node.get("_blocks", []):
                stack.append(child)
    return prisoners


def prisoner_summary(p):
    """Pull human-readable fields out of a parsed prisoner block."""
    forename = p.get("Forename") or p.get("Name") or "Unknown"
    surname = p.get("Surname", "")
    full = f"{forename} {surname}".strip()

    crimes = []
    for child in p.get("_blocks", []):
        if child.get("_name") in ("Crime", "Crimes", "Sentence"):
            for k, v in child.items():
                if k.startswith("_"):
                    continue
                crimes.append(f"{k}={v}")
    bio_parts = [v for k, v in p.items() if k.startswith("Bio") and v]

    return {
        "name": full,
        "category": p.get("Category", p.get("Cat", "Normal")),
        "age": p.get("Age", "?"),
        "sentence": p.get("Sentence", p.get("RemainingSentence", "?")),
        "crimes": crimes,
        "bio": " ".join(bio_parts),
        "raw_keys": [k for k in p.keys() if not k.startswith("_")],
    }


# ---------- Ollama client ---------------------------------------------------

class Ollama:
    def __init__(self, model, url=OLLAMA_URL):
        self.model = model
        self.url = url

    def check(self):
        r = requests.get(f"{self.url}/api/tags", timeout=5)
        r.raise_for_status()
        models = [m["name"] for m in r.json().get("models", [])]
        if not any(self.model in m for m in models):
            raise RuntimeError(
                f"Model {self.model!r} not found. Available: {models}. "
                f"Run: ollama pull {self.model}"
            )
        return models

    def generate(self, prompt, temperature=0.85):
        r = requests.post(
            f"{self.url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": temperature, "top_p": 0.9},
            },
            timeout=120,
        )
        r.raise_for_status()
        return r.json().get("response", "").strip()


# ---------- Dossier generator -----------------------------------------------

PERSONALITIES = [
    "The Alpha", "The Strategist", "The Hothead", "The Survivor",
    "The Idealist", "The Broken", "The Enforcer", "The Smooth Talker",
    "The Paranoid", "The Follower", "The Opportunist", "The Psychopath",
    "The Mentor", "The Rebel", "The Coward", "The Addict",
    "The Peacemaker", "The Schemer", "The Stoic", "The Wild Card",
]


def build_prompt(summary):
    crimes = ", ".join(summary["crimes"]) or "unknown"
    return f"""You are writing a prison intake dossier. Be vivid and concise.

INMATE
- Name: {summary['name']}
- Age: {summary['age']}
- Security category: {summary['category']}
- Sentence: {summary['sentence']}
- Known offenses: {crimes}

Write a dossier with these sections, in plain Markdown:

**Personality archetype**: pick ONE from this list and explain in two sentences why it fits: {", ".join(PERSONALITIES)}.

**Internal monologue**: 3-4 lines of what this prisoner is thinking on their first night.

**Hidden secret**: one thing they are hiding from the guards.

**Allegiance**: which kind of prisoner they would gravitate toward (gangs, loners, reformers, religious group, etc.) and why.

**Risk factors**: 2-3 short bullets for the warden — what could go wrong with this inmate.

Keep the whole dossier under 200 words. Do not repeat the input fields verbatim.
"""


def write_dossier(prisoners, output_path, ollama, limit=None):
    out = Path(output_path)
    pieces = [f"# Prison Dossier\n\n_Generated by ai_observer using `{ollama.model}`._\n"]
    n = len(prisoners) if limit is None else min(limit, len(prisoners))
    print(f"Generating dossiers for {n} prisoners -> {out}")
    for i, p in enumerate(prisoners[:n], 1):
        summary = prisoner_summary(p)
        print(f"  [{i}/{n}] {summary['name'] or '(unnamed)'}")
        try:
            body = ollama.generate(build_prompt(summary))
        except Exception as e:
            body = f"_LLM error: {e}_"
        pieces.append(f"\n---\n\n## {i}. {summary['name'] or 'Unknown'}\n")
        pieces.append(
            f"- Age: {summary['age']}  | Category: {summary['category']}  "
            f"| Sentence: {summary['sentence']}\n"
        )
        if summary["crimes"]:
            pieces.append(f"- Offenses: {', '.join(summary['crimes'])}\n")
        pieces.append("\n" + body + "\n")
    out.write_text("".join(pieces), encoding="utf-8")
    print(f"Wrote {out.resolve()}")


# ---------- CLI -------------------------------------------------------------

def parse_save_file(path):
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    tree = parse_prison_save(text)
    prisoners = find_prisoners(tree)
    print(f"Parsed {path}: {len(prisoners)} prisoner block(s) found.")
    return prisoners


def main():
    ap = argparse.ArgumentParser(description="Prison Architect AI Observer")
    ap.add_argument("--save", help="Path to .prison save file")
    ap.add_argument("--model", default=DEFAULT_MODEL, help="Ollama model name")
    ap.add_argument("--output", default=DEFAULT_OUTPUT, help="Markdown output path")
    ap.add_argument("--limit", type=int, default=None, help="Process first N prisoners")
    ap.add_argument("--watch", action="store_true",
                    help="Re-run every time the save file is updated")
    ap.add_argument("--self-test", action="store_true",
                    help="Just verify Ollama is reachable and the model is available")
    args = ap.parse_args()

    ollama = Ollama(args.model)

    if args.self_test:
        models = ollama.check()
        print(f"OK. Ollama responded. Models: {models}")
        sample = ollama.generate("Say hello in one short sentence.")
        print(f"Sample: {sample}")
        return

    if not args.save:
        ap.error("--save is required (or pass --self-test)")

    save_path = Path(args.save)
    if not save_path.exists():
        sys.exit(f"Save file not found: {save_path}")

    ollama.check()

    def run_once():
        prisoners = parse_save_file(save_path)
        if not prisoners:
            print("No prisoners found. The save may be empty, or PA may have changed")
            print("its save format. Try a save where prisoners are visible in-game.")
            return
        write_dossier(prisoners, args.output, ollama, limit=args.limit)

    run_once()

    if args.watch:
        print(f"Watching {save_path} for changes (Ctrl+C to stop)...")
        last_mtime = save_path.stat().st_mtime
        while True:
            time.sleep(2.0)
            try:
                mtime = save_path.stat().st_mtime
            except FileNotFoundError:
                continue
            if mtime > last_mtime:
                last_mtime = mtime
                print(f"\n[{time.strftime('%H:%M:%S')}] Save updated, regenerating...")
                run_once()


if __name__ == "__main__":
    main()

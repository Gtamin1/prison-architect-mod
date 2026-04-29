# Prison Architect AI Observer

A standalone Python tool that reads your Prison Architect save file, sends every
prisoner through a local Ollama model, and writes a personality dossier
(`dossier.md`) you can read alongside the game.

> **This is not an in-game mod.** Prison Architect's Lua API does not allow file
> I/O, network calls, custom hotkeys, or runtime control of NPC behavior, so a
> truly in-game LLM integration is impossible. This tool works with the next-best
> thing: your real save file. The dossier reflects the actual prisoners in your
> actual prison.

---

## What it does

For each prisoner in your save it generates a short Markdown profile with:

- **Personality archetype** chosen from 20 prison-trope types (The Alpha, The
  Strategist, The Hothead, …).
- **Internal monologue** — what they're thinking on their first night.
- **Hidden secret** they're keeping from the guards.
- **Allegiance** — gangs, loners, religious group, etc.
- **Risk factors** — short bullets for the warden.

Run it once for a snapshot, or pass `--watch` to regenerate the dossier every
time Prison Architect autosaves.

---

## Requirements

- **Python 3.8+**
- **Ollama** with a model pulled (e.g. `ollama pull llama3`)
- A Prison Architect save file (`*.prison`)

Save files live here:

| OS      | Location                                                                 |
|---------|--------------------------------------------------------------------------|
| Windows | `%LOCALAPPDATA%\Introversion\Prison Architect\saves\`                    |
| macOS   | `~/Library/Application Support/Prison Architect/saves/`                  |
| Linux   | `~/.Prison Architect/saves/`                                             |

---

## Install

```bash
cd bridge
pip install -r requirements.txt
```

Verify Ollama works:

```bash
python ai_observer.py --self-test
```

You should see the available models listed and a one-line greeting from the LLM.

---

## Run

Generate a dossier for a single save:

```bash
python ai_observer.py --save "C:\Users\YOU\AppData\Local\Introversion\Prison Architect\saves\savewarden.prison"
```

The dossier is written to `dossier.md` in the current folder. Open it in any
Markdown viewer.

### Useful flags

| Flag                | Effect                                                |
|---------------------|-------------------------------------------------------|
| `--model mistral`   | Use a different Ollama model (default `llama3`).      |
| `--limit 10`        | Only process the first 10 prisoners (much faster).    |
| `--output foo.md`   | Write to a custom path.                               |
| `--watch`           | Regenerate every time PA autosaves the file.          |
| `--self-test`       | Skip the save and just check Ollama connectivity.     |

### Tips

- Generation time is roughly *seconds-per-prisoner* × prisoner count. For a 100
  inmate prison expect a few minutes on a small model. Use `--limit` for fast
  iteration.
- `--watch` pairs nicely with PA's autosave: leave the tool running in a
  terminal, play normally, and check `dossier.md` after each save.
- If the parser finds zero prisoners, your save's field names may differ from
  what `find_prisoners()` looks for. Open `bridge/ai_observer.py` and adjust the
  `Type Prisoner` heuristic — the parser itself is generic, only the prisoner
  detection is opinionated.

---

## Why there's no in-game piece

Earlier versions of this project tried to do everything in-game with Lua scripts
attached to invisible objects placed by the player. That approach hit hard
limits in PA's modding system:

- Object scripts only get `BeginObject` / `Update` / `EndObject` hooks with very
  narrow `this.*` access. There is no `Object.GetNearbyObjects(...)`,
  `Game.Time()`, or general entity scanning.
- Lua scripts are sandboxed — no `io`, no `socket`, no way to talk to a Python
  bridge.
- There is no API to register hotkeys (`F1` does nothing in vanilla PA) or to
  draw custom UI overlays.

Pretending otherwise just produces a mod that loads, registers nothing, and
runs no code. The save-file approach trades real-time NPC control for something
that *actually executes*.

---

## License

MIT. See `LICENSE`.

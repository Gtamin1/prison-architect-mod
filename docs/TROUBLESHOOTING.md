# Troubleshooting Guide - Prison Architect AI Mod

**Solutions to common problems**

---

## 📖 Quick Diagnosis

**Select your problem:**

- [Mod doesn't appear in Prison Architect](#mod-doesnt-appear)
- [Ollama connection issues](#ollama-issues)
- [Python bridge errors](#python-bridge-errors)
- [No AI activity / NPCs not responding](#no-ai-activity)
- [Performance issues / lag](#performance-issues)
- [Bridge test failures](#bridge-test-failures)
- [Installation problems](#installation-problems)

---

## Mod Doesn't Appear

### Symptoms
- Custom objects (AIController, etc.) not in game menu
- Mod not listed in Prison Architect

### Diagnosis Steps

1. **Check mod folder location:**

   **Windows:**
   ```
   C:\Users\[YourUsername]\AppData\Local\Introversion\Prison Architect\mods\PrisonArchitectAI
   ```

   **macOS:**
   ```
   ~/Library/Application Support/Prison Architect/mods/PrisonArchitectAI
   ```

   **Linux:**
   ```
   ~/.Prison Architect/mods/PrisonArchitectAI
   ```

2. **Verify folder structure:**
   ```
   PrisonArchitectAI/
   ├── manifest.txt      ← Must be here!
   ├── data/
   │   ├── materials.txt ← Must be here!
   │   └── scripts/
   └── bridge/
   ```

3. **Check manifest.txt:**

   Open `manifest.txt` and verify it contains:
   ```
   Name                PrisonArchitectAI
   Author              Claude Code
   Version             1.0.0
   ...
   ```

   **Common issues:**
   - Extra spaces or tabs
   - Wrong capitalization
   - Missing fields

4. **Check materials.txt:**

   - Must be named exactly `materials.txt` (lowercase!)
   - Must be in `data/` folder
   - Check for syntax errors

### Solutions

✅ **Solution 1: Reinstall mod**
1. Delete the mod folder completely
2. Re-extract/copy the mod
3. Restart Prison Architect

✅ **Solution 2: Check permissions**
- Ensure you have write permissions to the mods folder
- On Linux/Mac: `chmod -R 755 PrisonArchitectAI`

✅ **Solution 3: Verify game version**
- This mod requires Prison Architect with Lua modding support
- Update to latest version if needed

### Still not working?

Check Prison Architect's log files:

**Windows:**
```
C:\Users\[YourUsername]\AppData\Local\Introversion\Prison Architect\
```

Look for `debug.txt` or `errors.txt`

---

## Ollama Issues

### Symptoms
- Bridge says "Cannot connect to Ollama"
- "Ollama is not running" error
- Bridge test fails on Ollama connection

### Diagnosis Steps

1. **Check if Ollama is running:**

   ```bash
   curl http://localhost:11434/api/tags
   ```

   **Expected:** JSON response with model list

   **If fails:** Ollama is not running

2. **Check Ollama service:**

   **Windows/macOS:**
   - Look for Ollama icon in system tray
   - If not there, Ollama isn't running

   **Linux:**
   ```bash
   ps aux | grep ollama
   ```

3. **Test Ollama directly:**

   ```bash
   ollama run llama3 "Hello"
   ```

   **Expected:** Ollama responds with greeting

### Solutions

✅ **Solution 1: Start Ollama**

**Windows/macOS:**
- Double-click Ollama app
- Or: Restart computer (starts automatically)

**Linux:**
```bash
ollama serve
```

Leave this terminal open!

✅ **Solution 2: Check model is downloaded**

```bash
ollama list
```

If `llama3` is not listed:
```bash
ollama pull llama3
```

✅ **Solution 3: Firewall issues**

Ollama uses port `11434`. Ensure it's not blocked:

**Windows:**
- Windows Defender → Allow app through firewall → Ollama

**macOS:**
- System Preferences → Security → Firewall → Add Ollama

**Linux:**
```bash
sudo ufw allow 11434
```

✅ **Solution 4: Reinstall Ollama**

1. Uninstall Ollama
2. Download latest version from https://ollama.ai
3. Install and start
4. Pull model: `ollama pull llama3`

### Advanced: Change Ollama port

If port 11434 is in use, change it:

**Edit bridge configuration:**

In `bridge/llm_bridge.py`:
```python
OLLAMA_URL = "http://localhost:11434"  # Change port here
```

Then restart Ollama with custom port:
```bash
OLLAMA_HOST=0.0.0.0:8080 ollama serve
```

---

## Python Bridge Errors

### Symptoms
- Bridge crashes on startup
- Import errors
- Connection timeouts

### Common Errors

#### Error: "ModuleNotFoundError: No module named 'requests'"

**Solution:**
```bash
pip install requests
```

Or:
```bash
pip install -r bridge/requirements.txt
```

#### Error: "Python was not found"

**Windows:**
- Reinstall Python with "Add to PATH" checked
- Or use full path: `C:\Python312\python.exe llm_bridge.py`

**macOS/Linux:**
- Use `python3` instead of `python`

#### Error: "Permission denied"

**Linux/macOS:**
```bash
chmod +x bridge/llm_bridge.py
```

Or run with python explicitly:
```bash
python3 bridge/llm_bridge.py
```

#### Error: "FileNotFoundError: ai_bridge_request.json"

**This is normal!** The file is created by the Lua mod when needed.

If you see this during normal operation:
- Lua mod hasn't made a request yet
- Place AIController object in the prison
- Wait for entities to spawn

### Solutions

✅ **Solution 1: Virtual environment (recommended)**

```bash
cd bridge
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python llm_bridge.py
```

✅ **Solution 2: Run test mode**

```bash
python llm_bridge.py --test --debug
```

This shows detailed error messages.

✅ **Solution 3: Update Python**

Ensure Python 3.8+:
```bash
python --version
```

If older, download from https://www.python.org/downloads/

---

## No AI Activity

### Symptoms
- NPCs don't seem to use AI
- No debug messages
- Bridge shows no requests

### Diagnosis Steps

1. **Is AIController placed?**
   - Open Prison Architect
   - Go to Objects menu
   - Find "AIController" (might not be visible)
   - Place it ANYWHERE in the prison

2. **Are there entities?**
   - Must have prisoners or guards in the prison
   - They must be active (not sleeping in cells indefinitely)

3. **Check the debug log file** (Prison Architect has no in-game console):
   - Open `debug.txt` next to `preferences.txt`
     - Windows: `%LOCALAPPDATA%\Introversion\Prison Architect\debug.txt`
     - macOS: `~/Library/Application Support/Prison Architect/debug.txt`
     - Linux: `~/.Prison Architect/debug.txt`
   - Look for: `AIController: Initialized`
   - Look for: `AIController: Tracking X entities`

4. **Check bridge terminal:**
   - Should show: `Bridge is ready! Waiting for requests...`
   - When active: `Processing decision request for entity X`

### Solutions

✅ **Solution 1: Enable debug mode**

Already enabled by default, but verify:

In `data/scripts/AIController.lua`:
```lua
local debugMode = true  -- Must be true!
```

✅ **Solution 2: Force entity spawn**

- Create a new prison
- Intake some prisoners
- Wait for them to leave reception
- Place AIController object

✅ **Solution 3: Check update interval**

In `AIController.lua`:
```lua
local updateInterval = 2.0  -- Try reducing to 1.0
```

Restart Prison Architect.

✅ **Solution 4: Manual bridge test**

Create a test request file manually:

`ai_bridge_request.json`:
```json
{
  "type": "decision",
  "context": {
    "entity": {
      "id": 999,
      "type": "Prisoner",
      "personality": "The Alpha",
      "mood": "confident",
      "currentAction": "idle"
    },
    "nearby": []
  }
}
```

Bridge should process it and create `ai_bridge_response.json`.

---

## Performance Issues

### Symptoms
- Game lags/stutters
- Low FPS
- Bridge uses high CPU

### Solutions

✅ **Solution 1: Reduce update frequency**

In `AIController.lua`:
```lua
local updateInterval = 5.0  -- Increase from 2.0
```

✅ **Solution 2: Batch smaller**

In `AIController.lua`:
```lua
local maxPerFrame = 3  -- Reduce from 5
```

✅ **Solution 3: Use faster model**

```bash
ollama pull phi  # Much smaller/faster
python llm_bridge.py --model phi
```

✅ **Solution 4: Limit tracking range**

In `AIController.lua` `ScanEntities()`:
```lua
local prisoners = Object.GetNearbyObjects(this.Pos.x, this.Pos.y, 500, "Prisoner")  -- Reduce from 1000
```

✅ **Solution 5: GPU acceleration**

If you have a GPU, Ollama can use it:

**NVIDIA GPU:**
- Ollama automatically uses CUDA if available
- Verify: Watch GPU usage when bridge processes requests

**Apple Silicon (M1/M2/M3):**
- Automatic Metal acceleration

**AMD GPU:**
- ROCm support (Linux only, advanced setup)

---

## Bridge Test Failures

### Test 1: Ollama Connection Fails

```
❌ Ollama connection test FAILED
```

**Solutions:**
1. Start Ollama: `ollama serve`
2. Check firewall
3. Verify port 11434 is available

### Test 2: Generation Fails

```
✓ Ollama connection test PASSED
❌ Generation test FAILED
```

**Solutions:**
1. Model not downloaded: `ollama pull llama3`
2. Ollama crashed: Restart Ollama
3. Timeout: Increase timeout in `llm_bridge.py`

### Test 3: Decision Test Fails

```
✓ Ollama connection test PASSED
✓ Generation test PASSED
❌ Decision test FAILED
```

**Solutions:**
1. Check prompt format in `llm_bridge.py`
2. Model not following format - try different model
3. Parsing error - check logs

**Enable debug mode:**
```bash
python llm_bridge.py --test --debug
```

---

## Installation Problems

### Can't find mods folder

**Windows:**
1. Press `Windows + R`
2. Type: `%LOCALAPPDATA%\Introversion\Prison Architect`
3. Press Enter
4. Create `mods` folder if it doesn't exist

**macOS:**
```bash
cd ~/Library/Application\ Support/Prison\ Architect
mkdir -p mods
```

**Linux:**
```bash
cd ~/.Prison\ Architect
mkdir -p mods
```

### Permission denied when copying files

**Windows:**
- Run as Administrator
- Check folder isn't read-only

**macOS/Linux:**
```bash
sudo chown -R $(whoami) "~/Library/Application Support/Prison Architect/mods"
```

### Python not in PATH

**Windows:**
1. Search for "Environment Variables"
2. Edit "Path" variable
3. Add: `C:\Python312` (adjust version)
4. Add: `C:\Python312\Scripts`
5. Restart terminal

**macOS:**
Add to `~/.zshrc` or `~/.bash_profile`:
```bash
export PATH="/usr/local/bin/python3:$PATH"
```

---

## Advanced Debugging

### Enable verbose logging

**Bridge:**
```bash
python llm_bridge.py --debug
```

**Lua:**
Set `debugMode = true` in all script files.

### Check file permissions

**Linux/macOS:**
```bash
ls -la data/scripts/
```

All `.lua` files should be readable.

### Monitor file creation

**Watch for request/response files:**

**Linux/macOS:**
```bash
watch -n 1 ls -la ai_bridge_*.json
```

**Windows:**
- Keep File Explorer open in bridge folder
- Refresh periodically

### Test Lua scripts manually

1. Extract Prison Architect's Lua interpreter
2. Run scripts standalone (advanced)

---

## Getting Help

If problems persist:

1. **Gather information:**
   - Operating system and version
   - Prison Architect version
   - Python version (`python --version`)
   - Ollama version (`ollama --version`)
   - Error messages (full text)
   - Screenshots

2. **Check logs:**
   - Bridge terminal output
   - Prison Architect `debug.txt` (next to `preferences.txt` — there is no in-game F1 console)
   - Ollama logs

3. **Create minimal test case:**
   - Fresh prison
   - Just AIController object
   - A few prisoners
   - Run bridge in test mode

4. **Ask for help:**
   - GitHub Issues: Include all info above
   - Prison Architect modding forums
   - Ollama Discord/community

---

## Common Questions

**Q: Does this work on Prison Architect 2?**
A: Not yet. Currently designed for Prison Architect 1 (original). PA2 may have different modding API.

**Q: Can I use ChatGPT instead of Ollama?**
A: Yes! Modify `llm_bridge.py` to use OpenAI API. You'll need an API key (costs money).

**Q: Why is it so slow?**
A: LLM processing takes time. Use faster models (phi, mistral) or GPU acceleration.

**Q: Can I use this on multiplayer?**
A: Untested. Likely works but all players need the mod installed.

**Q: Is my data sent to the internet?**
A: No. Everything runs locally. Ollama never sends data externally.

---

**Still stuck? Open an issue on GitHub with detailed information!**

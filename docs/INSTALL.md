# Installation Guide - Prison Architect AI Mod

**Complete beginner-friendly guide to installing the AI mod.**

This guide assumes you've never modded Prison Architect before. Follow each step carefully.

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Step 1: Verify Prison Architect](#step-1-verify-prison-architect)
3. [Step 2: Install Python](#step-2-install-python)
4. [Step 3: Install Ollama](#step-3-install-ollama)
5. [Step 4: Download the Mod](#step-4-download-the-mod)
6. [Step 5: Install the Mod](#step-5-install-the-mod)
7. [Step 6: Set Up Python Bridge](#step-6-set-up-python-bridge)
8. [Step 7: First Launch](#step-7-first-launch)
9. [Troubleshooting](#troubleshooting)

---

## System Requirements

**Minimum:**
- Prison Architect (any version with Lua modding support)
- 8GB RAM (for running Ollama)
- 5GB free disk space (for LLM models)
- Python 3.8 or higher
- Windows, macOS, or Linux

**Recommended:**
- 16GB RAM
- GPU (for faster LLM responses)
- SSD storage

---

## Step 1: Verify Prison Architect

### ✅ Check You Have Prison Architect

1. **Launch Prison Architect** from Steam or your games library
2. **Create a test prison** or load an existing one
3. **Verify it works** - you should be able to place objects and see prisoners

If Prison Architect doesn't work, fix that first before continuing.

---

## Step 2: Install Python

### 🐍 Windows

1. **Download Python:**
   - Go to https://www.python.org/downloads/
   - Click **"Download Python 3.12.x"** (or latest version)

2. **Run the installer:**
   - ⚠️ **IMPORTANT:** Check **"Add Python to PATH"** at the bottom!
   - Click **"Install Now"**
   - Wait for installation to complete

3. **Verify installation:**
   - Open **Command Prompt** (search for "cmd" in Start menu)
   - Type: `python --version`
   - You should see: `Python 3.12.x`

### 🍎 macOS

1. **Download Python:**
   - Go to https://www.python.org/downloads/
   - Download the macOS installer

2. **Install Python:**
   - Open the downloaded `.pkg` file
   - Follow the installation wizard

3. **Verify installation:**
   - Open **Terminal** (Applications → Utilities → Terminal)
   - Type: `python3 --version`
   - You should see: `Python 3.x.x`

### 🐧 Linux

Most Linux distributions include Python. To verify:

```bash
python3 --version
```

If not installed:
```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip

# Arch
sudo pacman -S python python-pip
```

---

## Step 3: Install Ollama

### 🤖 What is Ollama?

Ollama is software that runs AI models (like ChatGPT) **locally on your computer**. No internet required, completely free!

### Installation

#### Windows
1. Go to https://ollama.ai/download
2. Click **"Download for Windows"**
3. Run the installer
4. Ollama will start automatically in the background

#### macOS
1. Go to https://ollama.ai/download
2. Click **"Download for Mac"**
3. Open the downloaded `.dmg` file
4. Drag Ollama to Applications
5. Launch Ollama from Applications

#### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### ✅ Verify Ollama Installation

Open a terminal/command prompt and run:

```bash
ollama --version
```

You should see a version number.

### 📦 Download an AI Model

You need to download an AI model. We recommend **Llama 3** (4GB):

```bash
ollama pull llama3
```

**This will download ~4GB. It may take a few minutes.**

**Alternative models:**
- `mistral` - Faster, smaller (4GB)
- `llama3:70b` - More intelligent, larger (39GB)
- `phi` - Tiny and fast (1.6GB)

### ✅ Test Ollama

Make sure Ollama works:

```bash
ollama run llama3 "Say hello!"
```

You should see the AI respond with a greeting. Type `/bye` to exit.

**⚠️ IMPORTANT:** Keep Ollama running! It needs to be running for the mod to work.

---

## Step 4: Download the Mod

### Option A: Download ZIP

1. Download the mod as a ZIP file
2. Extract it to a folder (e.g., `Downloads/PrisonArchitectAI`)
3. You should see folders: `data/`, `bridge/`, `docs/`

### Option B: Git Clone

```bash
git clone https://github.com/yourusername/prison-architect-ai-mod.git
```

---

## Step 5: Install the Mod

### 🗂️ Find Your Mods Folder

**Windows:**
```
C:\Users\[YourUsername]\AppData\Local\Introversion\Prison Architect\mods
```

**To get there quickly:**
1. Press `Windows + R`
2. Type: `%LOCALAPPDATA%\Introversion\Prison Architect\mods`
3. Press Enter

**macOS:**
```
~/Library/Application Support/Prison Architect/mods
```

**To get there quickly:**
1. Open Finder
2. Press `Cmd + Shift + G`
3. Type: `~/Library/Application Support/Prison Architect/mods`
4. Press Enter

**Linux:**
```
~/.Prison Architect/mods
```

### 📁 Create the Mods Folder (if it doesn't exist)

If the `mods` folder doesn't exist, **create it manually**.

### 📋 Copy the Mod

1. **Copy the entire mod folder** to the mods directory
2. **Rename it** to `PrisonArchitectAI` (no spaces!)

**Final structure should look like:**
```
mods/
└── PrisonArchitectAI/
    ├── manifest.txt
    ├── data/
    │   ├── materials.txt
    │   └── scripts/
    ├── bridge/
    └── docs/
```

### ✅ Verify Installation

Check that these files exist:
- `mods/PrisonArchitectAI/manifest.txt`
- `mods/PrisonArchitectAI/data/materials.txt`
- `mods/PrisonArchitectAI/data/scripts/AIController.lua`

---

## Step 6: Set Up Python Bridge

The Python bridge connects the game to Ollama.

### 📦 Install Dependencies

Open terminal/command prompt and navigate to the mod folder:

**Windows:**
```cmd
cd C:\Users\[YourUsername]\AppData\Local\Introversion\Prison Architect\mods\PrisonArchitectAI\bridge
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
cd ~/Library/Application\ Support/Prison\ Architect/mods/PrisonArchitectAI/bridge
pip3 install -r requirements.txt
```

### ✅ Test the Bridge

Run the test command:

**Windows:**
```cmd
python llm_bridge.py --test
```

**macOS/Linux:**
```bash
python3 llm_bridge.py --test
```

**Expected output:**
```
=== RUNNING TESTS ===
Test 1: Checking Ollama connection...
✓ Ollama connection test PASSED
Test 2: Generating test response...
✓ Generation test PASSED: Hello from Prison Architect AI!
Test 3: Testing decision making...
✓ Decision test PASSED
  Action: socialize
  Thought: I should strengthen my connections with nearby allies.

=== ALL TESTS PASSED ===
The bridge is ready to use!
```

**❌ If tests fail**, see [Troubleshooting](#troubleshooting) section below.

---

## Step 7: First Launch

### 🎮 Starting Everything

You need to start components **in this order:**

#### 1. Start Ollama (if not already running)

**Windows/macOS:**
- Ollama usually starts automatically
- Check system tray for Ollama icon

**Linux:**
```bash
ollama serve &
```

#### 2. Start the Python Bridge

Navigate to the bridge folder and run:

**Windows:**
```cmd
cd C:\Users\[YourUsername]\AppData\Local\Introversion\Prison Architect\mods\PrisonArchitectAI\bridge
python llm_bridge.py
```

**macOS/Linux:**
```bash
cd ~/Library/Application\ Support/Prison\ Architect/mods/PrisonArchitectAI/bridge
python3 llm_bridge.py
```

**Expected output:**
```
Initializing Ollama Bridge with model: llama3
Ollama is running. Available models: ['llama3']
Starting request monitor loop...
Watching for: /path/to/ai_bridge_request.json
Bridge is ready! Waiting for requests from Prison Architect...
```

**Leave this terminal window open!** The bridge needs to keep running.

#### 3. Launch Prison Architect

1. Start Prison Architect normally
2. Load a prison or create a new one
3. **Check the mod is loaded:**
   - Open the **Object menu**
   - You should see new objects: "AIConversationHub", "AIGangMeetingTable"

#### 4. Place the AI Controller

1. Open the **Object menu**
2. Find **"AIController"** (it's invisible, but you can place it)
3. Place it **somewhere in your prison** (anywhere is fine)
4. The AI system is now active!

### ✅ Verify It's Working

**Check the bridge terminal:**
- You should see messages like: `AIController: Tracking 12 entities`

**In-game:**
- Prison Architect does **not** have an in-game debug console. All `Game.DebugOut(...)` output is written to `debug.txt` instead.
- Open `debug.txt` (in the same folder as `preferences.txt`) and look for lines starting with `AIController:`, `AIConversationHub:`, etc.
  - Windows: `%LOCALAPPDATA%\Introversion\Prison Architect\debug.txt`
  - macOS: `~/Library/Application Support/Prison Architect/debug.txt`
  - Linux: `~/.Prison Architect/debug.txt`
- Tip: keep the file open in a tail-style viewer (e.g. `Get-Content debug.txt -Wait` on PowerShell, or `tail -f debug.txt` on macOS/Linux) to watch messages live.

**If you see `AIController:` lines appearing in `debug.txt`, the mod is working!**

---

## Troubleshooting

### ❌ "Ollama is not running"

**Solution:**
```bash
ollama serve
```

Leave this running in a terminal.

### ❌ "Model 'llama3' not found"

**Solution:**
```bash
ollama pull llama3
```

### ❌ "Cannot connect to Ollama"

**Check:**
1. Is Ollama running? (`ollama serve`)
2. Can you run: `ollama run llama3 "test"`?
3. Is firewall blocking it?

**Try:**
```bash
curl http://localhost:11434/api/tags
```

If this fails, Ollama isn't running properly.

### ❌ "ModuleNotFoundError: No module named 'requests'"

**Solution:**
```bash
pip install requests
```

### ❌ Mod doesn't appear in Prison Architect

**Check:**
1. Is the folder named correctly? (no spaces)
2. Is `manifest.txt` in the root of the mod folder?
3. Is the mods folder in the right location?

**Try:**
- Restart Prison Architect
- Check the game's log files for errors

### ❌ Bridge test fails

**Run:**
```bash
python llm_bridge.py --test --debug
```

This will show detailed error messages.

### ❌ No AI messages in debug console

**Check:**
1. Did you place the AIController object in the prison?
2. Are there prisoners in your prison?
3. Is the bridge running?

**Try:**
- Enable debug mode in the scripts (already enabled by default)
- Check bridge terminal for activity

---

## 🎓 Next Steps

**Once everything is working:**

1. Read **[PROMPTS.md](PROMPTS.md)** to understand how to customize AI behavior
2. Read **[DEVELOPMENT.md](DEVELOPMENT.md)** to learn how to extend the mod
3. Experiment with different LLM models
4. Join the community and share your experience!

---

## 🆘 Still Need Help?

- Check **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** for more solutions
- Open an issue on GitHub
- Ask in Prison Architect modding forums

---

**Now go make your prison come alive! 🎭🧠**

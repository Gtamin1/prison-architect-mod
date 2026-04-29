# Testing Guide - Prison Architect AI Mod

**How to test the mod without running Prison Architect**

This guide helps you test components independently.

---

## Quick Test Checklist

- [ ] Ollama is installed and running
- [ ] Python dependencies installed
- [ ] Bridge test passes
- [ ] Lua scripts have no syntax errors
- [ ] Mod structure is correct
- [ ] Files are in correct locations

---

## 1. Test Ollama

### Check Ollama is running

```bash
curl http://localhost:11434/api/tags
```

**Expected:** JSON response with list of models

### Test model generation

```bash
ollama run llama3 "Say hello in one sentence"
```

**Expected:** Ollama responds with a greeting

### Pull additional models (optional)

```bash
# Smaller/faster
ollama pull phi
ollama pull mistral

# Larger/smarter
ollama pull llama3:70b
```

---

## 2. Test Python Bridge

### Install dependencies

```bash
cd bridge
pip install -r requirements.txt
```

### Run automated tests

```bash
python llm_bridge.py --test
```

**Expected output:**
```
=== RUNNING TESTS ===
Test 1: Checking Ollama connection...
✓ Ollama connection test PASSED
Test 2: Generating test response...
✓ Generation test PASSED: ...
Test 3: Testing decision making...
✓ Decision test PASSED
  Action: ...
  Thought: ...

=== ALL TESTS PASSED ===
```

### Test with debug mode

```bash
python llm_bridge.py --test --debug
```

Shows detailed logs.

### Test different models

```bash
python llm_bridge.py --test --model mistral
python llm_bridge.py --test --model phi
```

### Manual bridge test

**Step 1:** Create test request file

`ai_bridge_request.json`:
```json
{
  "type": "decision",
  "context": {
    "entity": {
      "id": 1,
      "type": "Prisoner",
      "personality": "The Alpha",
      "mood": "confident",
      "currentAction": "idle"
    },
    "nearby": [
      {
        "id": 2,
        "type": "Prisoner",
        "personality": "The Follower",
        "distance": 5.0
      }
    ]
  }
}
```

**Step 2:** Start bridge

```bash
python llm_bridge.py
```

**Step 3:** Bridge should detect and process the file

Check for `ai_bridge_response.json`:
```json
{
  "success": true,
  "data": {
    "action": "socialize",
    "thought": "I should strengthen my connections with nearby allies."
  },
  "raw": "ACTION: socialize | THOUGHT: I should strengthen my connections..."
}
```

---

## 3. Test Lua Scripts

### Check syntax

Install Lua (optional):

**macOS:**
```bash
brew install lua
```

**Ubuntu/Debian:**
```bash
sudo apt install lua5.1
```

**Windows:**
- Download from https://www.lua.org/download.html

### Validate syntax

```bash
lua -c data/scripts/AIController.lua
lua -c data/scripts/AIConversationHub.lua
lua -c data/scripts/AIGangMeetingTable.lua
```

No output = no syntax errors!

### Test Lua logic (manual)

Create `test.lua`:
```lua
-- Load your script
dofile("data/scripts/AIController.lua")

-- Test personality assignment
print("Testing personality assignment...")
local personality = AssignPersonality()
print("Assigned personality: " .. personality)

print("All tests passed!")
```

Run:
```bash
lua test.lua
```

**Note:** This only tests basic logic. Full testing requires Prison Architect.

---

## 4. Test File Structure

### Verify mod structure

```bash
tree PrisonArchitectAI/
```

**Expected:**
```
PrisonArchitectAI/
├── manifest.txt
├── data/
│   ├── materials.txt
│   └── scripts/
│       ├── AIController.lua
│       ├── AIConversationHub.lua
│       └── AIGangMeetingTable.lua
├── bridge/
│   ├── llm_bridge.py
│   └── requirements.txt
├── docs/
│   ├── INSTALL.md
│   ├── PROMPTS.md
│   ├── API.md
│   ├── DEVELOPMENT.md
│   ├── TROUBLESHOOTING.md
│   └── CHANGELOG.md
└── README.md
```

### Check file permissions

**Linux/macOS:**
```bash
ls -la data/scripts/
```

All `.lua` files should be readable.

### Validate manifest

```bash
cat manifest.txt
```

Check for:
- Name field
- Author field
- Version field
- No extra whitespace

### Validate materials.txt

```bash
cat data/materials.txt
```

Check for:
- Proper BEGIN/END blocks
- Valid identifiers
- No syntax errors

---

## 5. Integration Test (Without Prison Architect)

### Simulate the full flow

**Terminal 1: Start Ollama**
```bash
ollama serve
```

**Terminal 2: Start Bridge**
```bash
cd bridge
python llm_bridge.py --debug
```

**Terminal 3: Send test request**
```bash
cat > ai_bridge_request.json << EOF
{
  "type": "decision",
  "context": {
    "entity": {
      "id": 123,
      "type": "Prisoner",
      "personality": "The Hothead",
      "mood": "angry",
      "currentAction": "idle"
    },
    "nearby": [
      {
        "id": 456,
        "type": "Prisoner",
        "personality": "The Alpha",
        "distance": 3.0
      }
    ]
  }
}
EOF
```

**Check Terminal 2:**
Should show:
```
Processing decision request for entity 123
Response written to ai_bridge_response.json
```

**Check response:**
```bash
cat ai_bridge_response.json
```

Should contain action and thought from LLM.

---

## 6. Test Different Scenarios

### Test: Conversation Request

`ai_bridge_request.json`:
```json
{
  "type": "conversation",
  "context": {
    "entity": {
      "personality": "The Smooth Talker"
    },
    "target": {
      "personality": "The Paranoid"
    },
    "relationship": "neutral"
  }
}
```

### Test: Gang Strategy (if implemented)

```json
{
  "type": "gang_strategy",
  "context": {
    "gang": {
      "name": "The Wolves",
      "member_count": 8,
      "territory": "B-Wing"
    },
    "rivals": [
      {
        "name": "The Serpents",
        "strength": "high"
      }
    ]
  }
}
```

---

## 7. Performance Testing

### Test response time

```python
import time
import json
from bridge.llm_bridge import OllamaBridge

bridge = OllamaBridge(model="llama3", debug=False)

# Test decision making speed
context = {
    "entity": {"personality": "The Alpha", "mood": "confident"},
    "nearby": []
}

request = {"type": "decision", "context": context}

start = time.time()
result = bridge.process_request(request)
elapsed = time.time() - start

print(f"Response time: {elapsed:.2f} seconds")
print(f"Action: {result['data']['action']}")
```

**Expected:** 1-5 seconds depending on model and hardware

### Test different models

```bash
# Fastest
python llm_bridge.py --test --model phi

# Balanced
python llm_bridge.py --test --model llama3

# Slowest but best
python llm_bridge.py --test --model llama3:70b
```

### Stress test

Send 10 requests rapidly:

```bash
for i in {1..10}; do
  cp test_request.json ai_bridge_request.json
  sleep 1
done
```

Watch bridge process all requests.

---

## 8. Testing in Prison Architect

### First launch checklist

1. **Ollama running?**
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. **Bridge running?**
   ```bash
   # In separate terminal
   python bridge/llm_bridge.py
   ```

3. **Mod installed?**
   - Check mods folder
   - Verify file structure

4. **Launch Prison Architect**

5. **Load/create prison**

6. **Check the debug log file** (PA has no in-game console; F1 does nothing in vanilla)
   - Open `debug.txt` (same folder as `preferences.txt`)
   - Look for: `AIController: Initialized`

7. **Place AIController object**
   - Objects menu → AIController
   - Place anywhere

8. **Wait for entities**
   - Spawn/intake prisoners
   - Wait for them to be active

9. **Check for activity**
   - Debug console: Entity tracking messages
   - Bridge terminal: Request processing

### In-game verification

**Check objects exist:**
- Objects menu should have:
  - AIController
  - AIConversationHub
  - AIGangMeetingTable

**Place conversation hub:**
- Place AIConversationHub in yard/common area
- Wait for prisoners to gather nearby

**Check debug output:**
- Tail the `debug.txt` file (same folder as `preferences.txt`)
- Should see AI messages

**Check bridge activity:**
- Bridge terminal should show requests when entities make decisions

---

## 9. Common Test Failures

### Bridge test fails

**Problem:** Ollama connection fails
**Fix:** Start Ollama (`ollama serve`)

**Problem:** Model not found
**Fix:** Pull model (`ollama pull llama3`)

**Problem:** Import error
**Fix:** Install dependencies (`pip install -r requirements.txt`)

### Mod doesn't load

**Problem:** Objects not in menu
**Fix:** Check manifest.txt and materials.txt syntax

**Problem:** Lua errors
**Fix:** Check script syntax with `lua -c script.lua`

### No AI activity

**Problem:** AIController not working
**Fix:** Check debug console for errors

**Problem:** Bridge not receiving requests
**Fix:** Verify file paths in Lua scripts

---

## 10. Automated Test Script

Create `run_tests.sh`:

```bash
#!/bin/bash

echo "=== Prison Architect AI Mod - Test Suite ==="
echo ""

# Test 1: Check Ollama
echo "Test 1: Checking Ollama..."
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✓ Ollama is running"
else
    echo "✗ Ollama is not running"
    exit 1
fi

# Test 2: Check Python
echo "Test 2: Checking Python..."
if command -v python3 &> /dev/null; then
    echo "✓ Python 3 is installed"
else
    echo "✗ Python 3 is not installed"
    exit 1
fi

# Test 3: Check dependencies
echo "Test 3: Checking dependencies..."
if python3 -c "import requests" 2>/dev/null; then
    echo "✓ Python dependencies installed"
else
    echo "✗ Python dependencies missing"
    echo "  Run: pip install -r bridge/requirements.txt"
    exit 1
fi

# Test 4: Run bridge tests
echo "Test 4: Running bridge tests..."
cd bridge
if python3 llm_bridge.py --test > /dev/null 2>&1; then
    echo "✓ Bridge tests passed"
else
    echo "✗ Bridge tests failed"
    echo "  Run: python3 llm_bridge.py --test"
    exit 1
fi
cd ..

# Test 5: Check Lua syntax
echo "Test 5: Checking Lua syntax..."
if command -v lua &> /dev/null; then
    for script in data/scripts/*.lua; do
        if lua -c "$script" 2>/dev/null; then
            echo "✓ $script syntax OK"
        else
            echo "✗ $script has syntax errors"
            exit 1
        fi
    done
else
    echo "⚠ Lua not installed, skipping syntax check"
fi

echo ""
echo "=== ALL TESTS PASSED ==="
echo "The mod is ready to use!"
```

Make executable:
```bash
chmod +x run_tests.sh
```

Run:
```bash
./run_tests.sh
```

---

## Summary

**Before Prison Architect:**
1. ✅ Ollama running and model downloaded
2. ✅ Python dependencies installed
3. ✅ Bridge test passes
4. ✅ File structure correct

**In Prison Architect:**
1. ✅ Mod loads (objects in menu)
2. ✅ AIController placed
3. ✅ Debug messages appear
4. ✅ Bridge processes requests

**If all tests pass, you're ready to play!** 🎮

---

See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for help with failures.

# Prison Architect AI Mod

## 🧠 Every Prisoner, Every Guard - Powered by AI

Transform Prison Architect into a living, breathing social simulation where every NPC has personality, memory, and intelligence powered by **local LLMs** through Ollama.

**No cloud. No subscriptions. 100% free and local.**

---

## ✨ Features

### 🎭 **Dynamic Personalities**
- **20+ unique personality types**: The Alpha, The Strategist, The Hothead, The Survivor, and more
- Each NPC makes decisions based on their personality traits
- Persistent memory across game sessions
- Emotional states that evolve over time

### 💬 **AI-Generated Conversations**
- NPCs engage in contextual dialogue based on:
  - Their personality
  - Current situation
  - Relationships with others
  - Recent events
- Conversations appear in-game (debug log for now, visual in future updates)
- Information sharing and rumor spreading

### 👊 **Gang System**
- Gangs form organically based on social dynamics
- Natural leadership emergence (charisma, violence, influence)
- Territory control and conflicts
- Gang meetings with strategic planning
- Coordinated actions and operations
- Gang names generated automatically

### 🧩 **Advanced Behavior**
- **Memory system**: NPCs remember past events, relationships, and experiences
- **Relationship tracking**: Friends, enemies, rivals, and alliances
- **Mood system**: Happy, angry, confident, paranoid, etc.
- **Needs tracking**: Hunger, hygiene, safety, exercise, and more
- **Goal-oriented**: NPCs have short-term and long-term objectives
- **Context-aware decisions**: Actions based on time, location, and nearby entities

### 🔧 **Technical Highlights**
- **100% Local**: All AI processing happens on your machine via Ollama
- **Privacy-First**: No data leaves your computer
- **Free Forever**: No API costs, no subscriptions
- **Extensible**: Easy to add new personalities, behaviors, and features
- **Performance-Optimized**: Batched processing to maintain smooth gameplay

---

## 🎮 How It Works

1. **Lua Mod** runs inside Prison Architect
   - Tracks all prisoners and guards
   - Monitors their state, position, and context
   - Assigns personalities and manages memory

2. **Python Bridge** connects to Ollama
   - Receives requests from the Lua mod
   - Processes them through local LLM (llama3, mistral, etc.)
   - Returns AI-generated decisions and dialogue

3. **Ollama** provides the intelligence
   - Runs completely locally on your machine
   - Supports multiple models (llama3, mistral, etc.)
   - Fast, free, and private

```
┌─────────────────┐
│ Prison Architect│
│   (Lua Mod)     │ ──┐
└─────────────────┘   │
                      │ JSON Files
┌─────────────────┐   │
│  Python Bridge  │ ──┘
│   (llm_bridge)  │
└─────────────────┘
         │
         │ HTTP API
         ▼
┌─────────────────┐
│     Ollama      │
│  (Local LLM)    │
└─────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- **Prison Architect** (installed and working)
- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Ollama** ([Download](https://ollama.ai/))

### Installation (5 Minutes)

**See [INSTALL.md](docs/INSTALL.md) for detailed step-by-step instructions!**

Quick version:
```bash
# 1. Install Ollama
# Download from https://ollama.ai/

# 2. Pull an LLM model
ollama pull llama3

# 3. Copy mod to Prison Architect mods folder
# Windows: C:\Users\YourName\AppData\Local\Introversion\Prison Architect\mods
# Mac: ~/Library/Application Support/Prison Architect/mods
# Linux: ~/.Prison Architect/mods

# 4. Install Python dependencies
cd bridge
pip install -r requirements.txt

# 5. Test the bridge
python llm_bridge.py --test

# 6. Start the bridge
python llm_bridge.py

# 7. Launch Prison Architect!
```

---

## 📖 Documentation

- **[INSTALL.md](docs/INSTALL.md)** - Detailed installation guide (for complete beginners!)
- **[PROMPTS.md](docs/PROMPTS.md)** - How AI prompts work and customization
- **[API.md](docs/API.md)** - Prison Architect API functions used
- **[DEVELOPMENT.md](docs/DEVELOPMENT.md)** - How to extend and modify the mod
- **[TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[CHANGELOG.md](docs/CHANGELOG.md)** - Version history

---

## 🎯 Roadmap

### Current Version (1.0)
- ✅ Personality system (20+ types)
- ✅ Basic AI decision making
- ✅ Gang formation and meetings
- ✅ Conversation system
- ✅ Memory and relationships
- ✅ Python bridge to Ollama

### Planned Features
- 🔲 Visual speech bubbles in-game
- 🔲 UI overlay for NPC thoughts
- 🔲 Extended action execution (use all game objects)
- 🔲 Escape planning over multiple days
- 🔲 Guard personalities and corruption
- 🔲 Prison economy (trading, debts)
- 🔲 Psychological warfare
- 🔲 Riot coordination
- 🔲 Staff AI (doctors, cooks, etc.)
- 🔲 Weather and event responses
- 🔲 PTSD and mental health systems

---

## 🛠️ Customization

### Change LLM Model
```bash
# Use a different Ollama model
python llm_bridge.py --model mistral
```

### Add New Personalities
Edit `data/scripts/AIController.lua` and add to the `personalities` table:
```lua
local personalities = {
    "Your Custom Personality",
    -- ... existing personalities
}
```

### Adjust Update Frequency
In `AIController.lua`:
```lua
local updateInterval = 2.0  -- Change this value (seconds)
```

---

## 🤝 Contributing

This mod is open-source and welcomes contributions!

**Ideas for contributors:**
- Visual UI for conversations and thoughts
- More personality types
- Enhanced gang mechanics
- Guard AI improvements
- Performance optimizations
- Better in-game visualization
- Additional LLM provider support

---

## 🐛 Troubleshooting

**Mod doesn't load?**
- Check `manifest.txt` is in the mod folder
- Verify folder structure matches documentation

**Bridge not connecting?**
- Run `python llm_bridge.py --test` to diagnose
- Ensure Ollama is running (`ollama serve`)
- Check firewall settings

**See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for complete guide.**

---

## 📜 License

MIT License - Free to use, modify, and distribute.

---

## 🌟 Credits

**Created by:** Claude Code
**Powered by:** Ollama, Llama 3, Prison Architect
**Inspired by:** The amazing Prison Architect modding community

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/prison-architect-ai-mod/issues)
- **Discussion:** Prison Architect modding forums
- **Documentation:** See `docs/` folder

---

**Make your prison come ALIVE! 🎭🧠🏢**

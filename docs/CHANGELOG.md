# Changelog - Prison Architect AI Mod

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.0] - 2026-01-06

### 🎉 Initial Release

**The first functional version of the Prison Architect AI Mod!**

### ✨ Added

#### Core Systems
- **AIController** - Central AI coordination system
  - Entity tracking (prisoners, guards, staff)
  - Personality assignment (20 unique types)
  - Memory and state management
  - Periodic decision-making loop
  - Persistent data storage

- **Python Bridge** - Ollama LLM integration
  - File-based communication with Lua mod
  - Request monitoring and processing
  - Prompt building for decision-making
  - Response parsing and formatting
  - Test mode for diagnostics
  - Support for multiple Ollama models

#### Personality System
- 20 unique personality types:
  - The Alpha (dominant, leader)
  - The Strategist (calculating, manipulative)
  - The Hothead (impulsive, violent)
  - The Survivor (pragmatic, cautious)
  - The Idealist (reform-minded, hopeful)
  - The Broken (traumatized, unpredictable)
  - The Enforcer (violent, loyal)
  - The Smooth Talker (charismatic, persuasive)
  - The Paranoid (suspicious, defensive)
  - The Follower (submissive, group-oriented)
  - The Opportunist (self-serving, flexible)
  - The Psychopath (ruthless, calculating)
  - The Mentor (wise, protective)
  - The Rebel (defiant, independent)
  - The Coward (risk-averse, fearful)
  - The Addict (desperate, unstable)
  - The Peacemaker (diplomatic, conflict-averse)
  - The Schemer (ambitious, sneaky)
  - The Stoic (emotionless, disciplined)
  - The Wild Card (unpredictable, chaotic)

#### Conversation System
- **AIConversationHub** object
  - Detects nearby NPCs
  - Initiates conversations
  - Tracks conversation history
  - Multiple conversation topics:
    - Prison conditions
    - Escape plans
    - Gang business
    - Guards
    - Family
    - Food quality
    - Cell mates
    - Yard time
    - Contraband
    - Reputation
    - Rumors
    - Grievances

#### Gang System
- **AIGangMeetingTable** object
  - Gang formation and tracking
  - Leadership determination
  - Gang meetings
  - Strategic planning
  - Multiple gang agendas:
    - Territory expansion
    - Rival confrontation
    - Contraband smuggling
    - Protection rackets
    - Escape planning
    - Recruitment
    - Internal discipline
    - Alliance discussions
- Automatic gang name generation
- Gang decision tracking
- Territory control (foundation)

#### Memory & Relationships
- Entity memory system
  - Short-term memory (recent events)
  - Long-term memory (important moments)
  - Relationship tracking
  - Mood states
- Needs tracking:
  - Hunger
  - Hygiene
  - Bladder
  - Exercise
  - Family
  - Safety

#### Actions & Behaviors
- Basic decision-making:
  - Wander
  - Socialize
  - Rest
  - Confront
  - Flee
  - Plan
  - Explore
- Personality-driven behavior
- Context-aware decisions

#### Documentation
- **README.md** - Project overview and quick start
- **INSTALL.md** - Complete beginner-friendly installation guide
  - Windows, macOS, and Linux instructions
  - Step-by-step Ollama setup
  - Python environment setup
  - Troubleshooting for common issues
- **PROMPTS.md** - Guide to AI prompts and customization
  - Prompt structure explanation
  - Personality descriptions
  - Customization examples
  - Best practices
- **API.md** - Prison Architect API reference
  - All functions used in mod
  - Property documentation
  - Usage examples
  - Limitations and workarounds
- **DEVELOPMENT.md** - Developer guide
  - Architecture overview
  - Adding features
  - Code examples
  - Testing strategies
- **TROUBLESHOOTING.md** - Common problems and solutions
  - Installation issues
  - Ollama connection problems
  - Performance optimization
  - Debug techniques
- **CHANGELOG.md** - Version history (this file)

#### Testing & Debugging
- Bridge test mode (`--test` flag)
- Debug logging throughout
- In-game debug console output
- Comprehensive error handling

### 🔧 Technical Details

#### File Structure
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
│   └── [documentation files]
└── README.md
```

#### Performance Optimizations
- Batched entity processing (max 5 per frame)
- Configurable update intervals
- Caching for LLM responses
- Efficient entity tracking

#### Compatibility
- **Prison Architect:** Original version with Lua modding support
- **Python:** 3.8+
- **Ollama:** Latest version
- **Operating Systems:** Windows, macOS, Linux

### 📋 Known Limitations

- **No visual UI** - Currently uses debug console for output
  - Speech bubbles not yet implemented
  - Thought display limited to logs
- **Limited entity control** - Cannot fully override base game AI
  - NavigateTo() available but limited
  - Cannot force object interactions
- **File-based communication** - Bridge uses JSON files (simple but not fastest)
- **Prison Architect API constraints** - See API.md for details

### 🎯 Future Plans

See README.md roadmap for planned features.

---

## [Unreleased]

### Ideas for Future Versions

#### Version 1.1
- Visual speech bubbles
- UI overlay for thoughts
- Extended action execution
- Performance improvements

#### Version 1.2
- Escape planning system (multi-day)
- Guard AI personalities
- Staff AI (doctors, cooks, etc.)

#### Version 2.0
- Complete visual overhaul
- Prison economy system
- Psychological warfare
- Advanced gang mechanics
- Riot coordination

---

## Version Numbering

This project uses [Semantic Versioning](https://semver.org/):

- **MAJOR** version: Breaking changes, major new features
- **MINOR** version: New features, backwards-compatible
- **PATCH** version: Bug fixes, small improvements

---

## Contributing

See [DEVELOPMENT.md](DEVELOPMENT.md) for contribution guidelines.

---

## Support

- **Issues:** GitHub Issues
- **Documentation:** See `docs/` folder
- **Community:** Prison Architect modding forums

---

**Stay tuned for updates!** 🚀

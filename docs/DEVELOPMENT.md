# Development Guide - Prison Architect AI Mod

**Extending and customizing the mod**

This guide is for developers who want to modify or extend the mod.

---

## 📖 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Mod Structure](#mod-structure)
3. [Adding Features](#adding-features)
4. [Lua Development](#lua-development)
5. [Python Bridge Development](#python-bridge-development)
6. [Testing](#testing)
7. [Contributing](#contributing)

---

## Architecture Overview

```
┌─────────────────────────────────────────┐
│        Prison Architect (Game)          │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │     Lua Scripts (In-Game)         │ │
│  │                                   │ │
│  │  • AIController.lua               │ │
│  │    - Entity tracking              │ │
│  │    - State management             │ │
│  │    - File I/O for bridge comm     │ │
│  │                                   │ │
│  │  • AIConversationHub.lua          │ │
│  │    - Conversation detection       │ │
│  │    - Dialogue management          │ │
│  │                                   │ │
│  │  • AIGangMeetingTable.lua         │ │
│  │    - Gang tracking                │ │
│  │    - Meeting coordination         │ │
│  └───────────┬───────────────────────┘ │
└──────────────┼─────────────────────────┘
               │
               │ JSON Files
               │ (ai_bridge_request.json,
               │  ai_bridge_response.json)
               │
┌──────────────┼─────────────────────────┐
│              │   Python Bridge         │
│  ┌───────────▼───────────────────────┐ │
│  │     llm_bridge.py                 │ │
│  │                                   │ │
│  │  • File monitoring                │ │
│  │  • Request parsing                │ │
│  │  • Prompt building                │ │
│  │  • Response formatting            │ │
│  └───────────┬───────────────────────┘ │
└──────────────┼─────────────────────────┘
               │
               │ HTTP API
               │
┌──────────────▼─────────────────────────┐
│            Ollama                       │
│                                         │
│  • llama3, mistral, etc.               │
│  • Local LLM inference                 │
│  • No internet required                │
└─────────────────────────────────────────┘
```

### Data Flow

1. **Entity Detection** (Lua)
   - AIController scans for nearby entities
   - Tracks position, personality, state

2. **Context Building** (Lua)
   - Gathers relevant information
   - Creates decision context
   - Writes to `ai_bridge_request.json`

3. **LLM Processing** (Python)
   - Bridge detects new request file
   - Parses context
   - Builds prompt
   - Sends to Ollama
   - Receives LLM response

4. **Response Parsing** (Python)
   - Extracts action and thought
   - Writes to `ai_bridge_response.json`

5. **Action Execution** (Lua)
   - Reads response file
   - Executes action (NavigateTo, etc.)
   - Updates entity state
   - Deletes processed files

---

## Mod Structure

```
PrisonArchitectAI/
├── manifest.txt              # Mod metadata
├── data/
│   ├── materials.txt         # Object definitions
│   └── scripts/              # Lua scripts
│       ├── AIController.lua          # Main AI coordinator
│       ├── AIConversationHub.lua     # Conversation system
│       └── AIGangMeetingTable.lua    # Gang mechanics
├── bridge/
│   ├── llm_bridge.py         # Python bridge to Ollama
│   └── requirements.txt      # Python dependencies
├── docs/
│   ├── INSTALL.md
│   ├── PROMPTS.md
│   ├── API.md
│   ├── TROUBLESHOOTING.md
│   ├── DEVELOPMENT.md (this file)
│   └── CHANGELOG.md
└── README.md
```

### File Purposes

| File | Purpose |
|------|---------|
| `manifest.txt` | Mod metadata (name, version, author) |
| `materials.txt` | Defines custom objects (AIController, etc.) |
| `AIController.lua` | Main brain - tracks entities, coordinates AI |
| `AIConversationHub.lua` | Handles NPC conversations |
| `AIGangMeetingTable.lua` | Gang formation and meetings |
| `llm_bridge.py` | Python service connecting to Ollama |
| `requirements.txt` | Python package dependencies |

---

## Adding Features

### Example: Add New Personality Type

**Step 1: Add to personality list**

Edit `data/scripts/AIController.lua`:

```lua
function AssignPersonality()
    local personalities = {
        "The Alpha",
        "The Strategist",
        -- ... existing personalities ...
        "The Hacker",  -- NEW!
    }

    local randomIndex = math.random(1, #personalities)
    return personalities[randomIndex]
end
```

**Step 2: Define behavior rules**

In `MakeSimpleDecision()`:

```lua
function MakeSimpleDecision(entityData)
    -- ... existing code ...

    if entityData.personality == "The Hacker" then
        -- Hackers prefer solitude and planning
        if #nearbyEntities > 3 then
            return "flee"  -- Too many people
        else
            return "plan"  -- Strategize
        end
    end

    -- ... rest of function ...
end
```

**Step 3: Update LLM prompts (optional)**

Edit `bridge/llm_bridge.py`:

```python
def build_decision_prompt(self, context: Dict[str, Any]) -> str:
    # ... existing code ...

    personality = entity.get('personality', 'Unknown')

    # Add personality-specific instructions
    if personality == "The Hacker":
        prompt += """
SPECIAL TRAITS:
- Highly intelligent, tech-savvy
- Prefers solitude for planning
- Distrusts authority
- Always looking for exploits
"""

    # ... rest of function ...
```

**Step 4: Test**

1. Restart Prison Architect
2. Start Python bridge
3. Spawn prisoners - some will get "The Hacker" personality
4. Watch debug logs for their behavior

---

### Example: Add New Action Type

**Step 1: Define action**

In `AIController.lua`, update available actions:

```lua
function MakeSimpleDecision(entityData)
    local decisions = {
        "wander",
        "socialize",
        "rest",
        "explore",
        "scheme"  -- NEW ACTION!
    }

    -- Add behavior for new action
    if entityData.personality == "The Strategist" then
        if math.random() > 0.6 then
            return "scheme"  -- Strategists like scheming
        end
    end

    -- ... rest of function ...
end
```

**Step 2: Implement action execution**

```lua
function ExecuteDecision(entityId, decision)
    local entityData = trackedEntities[entityId]

    if not entityData then
        return
    end

    entityData.lastDecision = decision
    entityData.currentAction = decision

    -- NEW: Handle "scheme" action
    if decision == "scheme" then
        ExecuteScheme(entityId, entityData)
        return
    end

    -- ... existing code ...
end

function ExecuteScheme(entityId, entityData)
    -- Scheming behavior: stand still, look suspicious
    -- In a full implementation, this could:
    -- - Add to a "schemes" list
    -- - Coordinate with gang members
    -- - Plan multi-step operations

    if debugMode then
        Game.DebugOut("Entity " .. entityId .. " is scheming...")
    end

    -- Track the scheme
    if not entityData.schemes then
        entityData.schemes = {}
    end

    table.insert(entityData.schemes, {
        type = "unknown",
        startTime = Game.Time()
    })
end
```

**Step 3: Update bridge prompts**

In `llm_bridge.py`:

```python
def build_decision_prompt(self, context: Dict[str, Any]) -> str:
    # ... existing code ...

    prompt += """AVAILABLE ACTIONS:
- wander: Move around randomly
- socialize: Talk to nearby people
- rest: Stand still and observe
- confront: Approach someone aggressively
- flee: Move away from threats
- plan: Think and strategize
- exercise: Use gym equipment
- eat: Go to canteen
- sleep: Rest in cell
- scheme: Plot something devious (NEW!)
"""
    # ... rest of function ...
```

---

### Example: Add Visual Feedback

**Goal:** Show thought bubbles above NPCs

**Step 1: Define thought bubble object**

Already in `materials.txt`:

```
BEGIN Object
    Name                AIThoughtBubble
    Identifier          ai_thought_bubble
    Category            Utility
    Price               0
    Size                1 1
    ...
END
```

**Step 2: Create thought bubble script**

Create `data/scripts/AIThoughtBubble.lua`:

```lua
--[[
    AI Thought Bubble - Visual indicator of NPC thinking
]]--

local displayDuration = 5.0  -- seconds
local creationTime = 0

function BeginObject()
    creationTime = Game.Time()

    -- Get thought text from spawner
    if this.ScriptState and this.ScriptState.thought then
        Game.DebugOut("Thought: " .. this.ScriptState.thought)
    end
end

function Update()
    local elapsed = Game.Time() - creationTime

    -- Auto-delete after duration
    if elapsed > displayDuration then
        Object.Delete(this)
    end
end
```

**Step 3: Spawn thought bubbles**

In `AIController.lua`:

```lua
function ExecuteDecision(entityId, decision)
    local entityData = trackedEntities[entityId]

    -- ... existing code ...

    -- Show thought bubble
    ShowThought(entityData.position.x, entityData.position.y + 2, decision)
end

function ShowThought(x, y, thought)
    local bubble = Object.Spawn("ai_thought_bubble", x, y)

    if bubble then
        if not bubble.ScriptState then
            bubble.ScriptState = {}
        end

        bubble.ScriptState.thought = thought
    end
end
```

**Note:** This creates invisible objects. For actual visual bubbles, you'd need sprite graphics (advanced).

---

## Lua Development

### Best Practices

#### ✅ DO:
- Use local variables for performance
- Comment your code extensively
- Check for nil before accessing properties
- Use descriptive variable names
- Profile performance-critical code

#### ❌ DON'T:
- Create too many objects (performance)
- Access properties without nil checks
- Use global variables excessively
- Block the Update() function

### Performance Tips

**Batch processing:**
```lua
-- Good
local processed = 0
for id, entity in pairs(entities) do
    if processed >= 5 then break end
    ProcessEntity(entity)
    processed = processed + 1
end
```

**Use timers:**
```lua
-- Good
local timer = 0
function Update()
    timer = timer + Dt
    if timer >= 2.0 then
        timer = 0
        DoExpensiveOperation()
    end
end
```

**Cache results:**
```lua
-- Good
local cachedNearby = {}
local cacheTime = 0

function GetNearbyEntities()
    if Game.Time() - cacheTime < 5.0 then
        return cachedNearby  -- Use cache
    end

    cachedNearby = Object.GetNearbyObjects(...)
    cacheTime = Game.Time()
    return cachedNearby
end
```

### Debugging

**Enable debug mode:**
```lua
local debugMode = true

function LogDebug(message)
    if debugMode then
        Game.DebugOut("[ModuleName] " .. message)
    end
end
```

**Track function calls:**
```lua
function MyFunction()
    LogDebug("MyFunction called")

    -- ... function code ...

    LogDebug("MyFunction completed")
end
```

**Dump table contents:**
```lua
function DumpTable(t, indent)
    indent = indent or 0
    local prefix = string.rep("  ", indent)

    for k, v in pairs(t) do
        if type(v) == "table" then
            Game.DebugOut(prefix .. k .. " = {")
            DumpTable(v, indent + 1)
            Game.DebugOut(prefix .. "}")
        else
            Game.DebugOut(prefix .. k .. " = " .. tostring(v))
        end
    end
end
```

---

## Python Bridge Development

### Code Structure

```python
class OllamaBridge:
    def __init__(self, model, debug)
        # Initialize bridge

    def check_ollama_status(self)
        # Verify Ollama is running

    def generate_response(self, prompt)
        # Send prompt to Ollama, get response

    def build_decision_prompt(self, context)
        # Build prompt for decision making

    def build_conversation_prompt(self, context)
        # Build prompt for conversations

    def parse_decision_response(self, response)
        # Parse LLM response into actions

    def process_request(self, request_data)
        # Main request handler

    def monitor_requests(self)
        # File monitoring loop

    def run_test(self)
        # Test mode
```

### Adding New Request Types

**Example: Add "gang_strategy" request type**

**Step 1: Add prompt builder**

```python
def build_gang_strategy_prompt(self, context: Dict[str, Any]) -> str:
    """Build prompt for gang strategic planning"""
    gang = context.get('gang', {})
    rivals = context.get('rivals', [])

    prompt = f"""You are the leader of {gang.get('name', 'a gang')} in prison.

GANG STATUS:
- Members: {gang.get('member_count', 0)}
- Territory: {gang.get('territory', 'none')}
- Resources: {gang.get('resources', 'low')}

RIVALS:
"""

    for rival in rivals:
        prompt += f"- {rival.get('name', 'Unknown gang')}: {rival.get('strength', 'unknown')} strength\n"

    prompt += """
STRATEGIC OPTIONS:
- expand: Claim new territory
- defend: Fortify current holdings
- ally: Form alliance with another gang
- attack: Strike at rival gang
- recruit: Grow gang membership
- smuggle: Increase contraband resources

Choose a strategy and explain your reasoning (2-3 sentences).

Format: STRATEGY: [option] | REASONING: [explanation]
"""

    return prompt
```

**Step 2: Add to request processor**

```python
def process_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
    request_type = request_data.get('type', 'decision')
    context = request_data.get('context', {})

    if request_type == 'decision':
        prompt = self.build_decision_prompt(context)
    elif request_type == 'conversation':
        prompt = self.build_conversation_prompt(context)
    elif request_type == 'gang_strategy':  # NEW!
        prompt = self.build_gang_strategy_prompt(context)
    else:
        return {'error': 'Unknown request type'}

    # ... rest of function ...
```

**Step 3: Add response parser**

```python
def parse_gang_strategy_response(self, response: str) -> Dict[str, str]:
    """Parse gang strategy response"""
    try:
        if '|' in response:
            parts = response.split('|')
            strategy = parts[0].replace('STRATEGY:', '').strip().lower()
            reasoning = parts[1].replace('REASONING:', '').strip()

            return {
                'strategy': strategy,
                'reasoning': reasoning
            }
    except Exception as e:
        logger.error(f"Error parsing gang strategy: {e}")
        return {
            'strategy': 'defend',
            'reasoning': 'Play it safe for now.'
        }
```

---

## Testing

### Unit Tests (Lua)

Lua doesn't have built-in testing, but you can create test functions:

```lua
-- test_aicontroller.lua (run separately)

function TestPersonalityAssignment()
    local personality = AssignPersonality()
    assert(personality ~= nil, "Personality should not be nil")
    print("✓ Personality assignment test passed")
end

function TestEntityTracking()
    local testEntity = {
        Id = 999,
        Pos = {x = 100, y = 200},
        Type = "Prisoner"
    }

    TrackEntity(testEntity, "Prisoner")

    assert(trackedEntities[999] ~= nil, "Entity should be tracked")
    print("✓ Entity tracking test passed")
end

-- Run tests
TestPersonalityAssignment()
TestEntityTracking()
```

### Integration Tests (Python)

Create `bridge/test_bridge.py`:

```python
import unittest
from llm_bridge import OllamaBridge

class TestBridge(unittest.TestCase):
    def setUp(self):
        self.bridge = OllamaBridge(model="llama3", debug=False)

    def test_decision_prompt_building(self):
        context = {
            'entity': {
                'personality': 'The Alpha',
                'mood': 'confident'
            },
            'nearby': []
        }

        prompt = self.bridge.build_decision_prompt(context)

        self.assertIn('The Alpha', prompt)
        self.assertIn('AVAILABLE ACTIONS', prompt)

    def test_response_parsing(self):
        response = "ACTION: socialize | THOUGHT: Need to rally the crew"
        parsed = self.bridge.parse_decision_response(response)

        self.assertEqual(parsed['action'], 'socialize')
        self.assertIn('rally', parsed['thought'])

if __name__ == '__main__':
    unittest.main()
```

Run tests:
```bash
python -m unittest bridge/test_bridge.py
```

---

## Contributing

### Before Contributing

1. Read this entire development guide
2. Test your changes thoroughly
3. Follow the existing code style
4. Document new features

### Code Style

**Lua:**
- 4 spaces indentation (no tabs)
- camelCase for functions
- lowercase_with_underscores for variables
- Comment all functions

**Python:**
- PEP 8 style guide
- Type hints for function signatures
- Docstrings for all functions

### Submitting Changes

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

**PR should include:**
- Clear description of changes
- Why the change is needed
- Testing performed
- Documentation updates

---

## Advanced Topics

### Custom LLM Providers

Replace Ollama with another provider:

```python
# In llm_bridge.py

class OpenAIBridge(OllamaBridge):
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model

    def generate_response(self, prompt):
        import openai
        openai.api_key = self.api_key

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content
```

### Sprites and Graphics

Add custom sprites to visualize AI:

1. Create `data/sprites.png` (sprite sheet)
2. Define sprite coordinates in `materials.txt`
3. Reference in Lua scripts

(Advanced - see Prison Architect modding docs)

---

## Resources

- **Lua Manual:** https://www.lua.org/manual/5.1/
- **Prison Architect API:** https://github.com/originalfoo/Prison-Architect-API
- **Ollama API:** https://github.com/ollama/ollama/blob/main/docs/api.md
- **Python Requests:** https://docs.python-requests.org/

---

**Happy modding! 🛠️**

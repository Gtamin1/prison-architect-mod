# Prompts Guide - Prison Architect AI Mod

**Understanding and customizing AI prompts**

This guide explains how the LLM prompts work and how to customize them for different behaviors.

---

## 📖 Table of Contents

1. [How Prompts Work](#how-prompts-work)
2. [Prompt Structure](#prompt-structure)
3. [Personality Types](#personality-types)
4. [Decision Making Prompts](#decision-making-prompts)
5. [Conversation Prompts](#conversation-prompts)
6. [Customization Examples](#customization-examples)
7. [Best Practices](#best-practices)

---

## How Prompts Work

The AI mod works by:

1. **Gathering context** about an NPC (position, personality, nearby entities, etc.)
2. **Building a prompt** that describes the situation
3. **Sending to Ollama** for AI processing
4. **Parsing the response** into actionable decisions
5. **Executing actions** in the game

```
┌─────────────┐
│   Context   │  Prisoner #123, Alpha personality,
│  Gathering  │  near rival gang member, hungry
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Prompt    │  "You are The Alpha in prison..."
│   Building  │  "Nearby: Rival gang member..."
└──────┬──────┘
       │
       ▼
┌─────────────┐
│     LLM     │  Ollama processes and decides
│  Processing │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Response  │  "ACTION: confront | THOUGHT:
│   Parsing   │   Show dominance..."
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Execute   │  NPC walks toward rival
│   Action    │
└─────────────┘
```

---

## Prompt Structure

### Decision Making Prompt Template

```python
"""You are a {entity_type} in a prison with the personality: {personality}.

CURRENT STATE:
- Mood: {mood}
- Current action: {current_action}

NEARBY ENTITIES ({count}):
- {entity_type} (Personality: {personality}, Distance: {distance}m)
- ...

GANG AFFILIATION: {gang_name}  # If applicable

AVAILABLE ACTIONS:
- wander: Move around randomly
- socialize: Talk to nearby people
- rest: Stand still and observe
- confront: Approach someone aggressively
- flee: Move away from threats
- plan: Think and strategize
- exercise: Use gym equipment
- eat: Go to canteen
- sleep: Rest in cell

Based on your personality and situation, what do you do?
Respond with ONLY the action name and a brief thought (1 sentence).

Format: ACTION: [action] | THOUGHT: [thought]
Example: ACTION: socialize | THOUGHT: I should strengthen my connections.
"""
```

### Conversation Prompt Template

```python
"""You are {personality_1} talking to {personality_2} in prison.

YOUR PERSONALITY: {personality_1}
THEIR PERSONALITY: {personality_2}

RELATIONSHIP: {relationship_status}

Generate a short, realistic prison conversation line (1-2 sentences).
Make it authentic to your personality and the prison environment.

Response:"""
```

---

## Personality Types

The mod includes 20 unique personalities. Here's how they affect behavior:

### 🦁 The Alpha
**Traits:** Dominant, confident, leadership-oriented

**Typical behaviors:**
- Seeks to establish dominance
- Confronts challenges directly
- Gathers followers
- Controls territory

**Example decisions:**
- `ACTION: confront | THOUGHT: I need to show who's boss here.`
- `ACTION: socialize | THOUGHT: Time to rally the crew.`

### 🧠 The Strategist
**Traits:** Calculating, patient, manipulative

**Typical behaviors:**
- Plans carefully before acting
- Manipulates situations
- Observes before engaging
- Long-term thinking

**Example decisions:**
- `ACTION: plan | THOUGHT: Let them fight, I'll pick up the pieces.`
- `ACTION: rest | THOUGHT: Patience... the opportunity will come.`

### 🔥 The Hothead
**Traits:** Impulsive, aggressive, emotional

**Typical behaviors:**
- Quick to anger
- Acts without thinking
- Prone to violence
- Unpredictable reactions

**Example decisions:**
- `ACTION: confront | THOUGHT: That guy looked at me wrong!`
- `ACTION: flee | THOUGHT: I need to cool off before I do something stupid.`

### 🛡️ The Survivor
**Traits:** Pragmatic, cautious, self-preserving

**Typical behaviors:**
- Avoids unnecessary risk
- Focuses on basics (food, safety)
- Keeps low profile
- Adapts to survive

**Example decisions:**
- `ACTION: flee | THOUGHT: Not worth the risk.`
- `ACTION: eat | THOUGHT: Stay fed, stay alive.`

### 🌟 The Idealist
**Traits:** Reform-minded, hopeful, positive

**Typical behaviors:**
- Seeks rehabilitation
- Helps others
- Believes in change
- Avoids trouble

**Example decisions:**
- `ACTION: rest | THOUGHT: I just need to keep my head down and get out.`
- `ACTION: socialize | THOUGHT: Maybe I can help them turn things around.`

### 💔 The Broken
**Traits:** Traumatized, unstable, unpredictable

**Typical behaviors:**
- Erratic decisions
- Emotional swings
- Paranoid responses
- Self-destructive tendencies

**Example decisions:**
- `ACTION: flee | THOUGHT: They're all out to get me...`
- `ACTION: rest | THOUGHT: Just... just need to be alone.`

*(See full personality list in AIController.lua)*

---

## Decision Making Prompts

### Context Information

The prompt includes rich context:

```python
{
    "entity": {
        "id": 123,
        "type": "Prisoner",
        "personality": "The Alpha",
        "mood": "confident",
        "currentAction": "idle",
        "needs": {
            "hunger": 60,    # 0-100
            "hygiene": 30,
            "bladder": 50,
            "exercise": 40,
            "safety": 80
        }
    },
    "nearby": [
        {
            "id": 456,
            "type": "Prisoner",
            "personality": "The Follower",
            "distance": 5.2,
            "gang": "The Wolves"
        }
    ],
    "time": 12345.67,
    "gang": "The Wolves"
}
```

### Response Format

LLM must respond in this format:

```
ACTION: [action_name] | THOUGHT: [reasoning]
```

**Valid actions:**
- `wander` - Random movement
- `socialize` - Initiate conversation
- `rest` - Stand idle
- `confront` - Aggressive approach
- `flee` - Move away
- `plan` - Strategic thinking
- `exercise` - Use gym equipment
- `eat` - Head to canteen
- `sleep` - Rest in cell

---

## Conversation Prompts

### Conversation Context

```python
{
    "entity": {
        "personality": "The Smooth Talker",
        "mood": "friendly"
    },
    "target": {
        "personality": "The Paranoid",
        "mood": "suspicious"
    },
    "relationship": "neutral",
    "topic": "escape_plans"
}
```

### Example Conversations

**The Alpha → The Follower:**
```
"Listen up, kid. You stick with me, you'll be alright in here."
```

**The Paranoid → The Strategist:**
```
"What do you want? Why are you always watching me?"
```

**The Idealist → The Broken:**
```
"Hey man, you okay? You look like you could use someone to talk to."
```

---

## Customization Examples

### Example 1: Add a New Personality

**Edit:** `data/scripts/AIController.lua`

```lua
function AssignPersonality()
    local personalities = {
        "The Alpha",
        "The Strategist",
        -- ... existing personalities
        "The Comedian",  -- NEW!
        -- Add your custom personality here
    }

    local randomIndex = math.random(1, #personalities)
    return personalities[randomIndex]
end
```

**Create behavior rules:**

In `MakeSimpleDecision()`:

```lua
if entityData.personality == "The Comedian" then
    return "socialize"  -- Comedians always want to entertain
end
```

### Example 2: Customize Prompt for More Aggressive Behavior

**Edit:** `bridge/llm_bridge.py`

In `build_decision_prompt()`, modify the prompt:

```python
prompt += """IMPORTANT: You are in a DANGEROUS prison.
Showing weakness gets you hurt. Consider aggressive actions.

AVAILABLE ACTIONS:
- wander: Move around randomly
- socialize: Talk to nearby people
- rest: Stand still and observe
- confront: Approach someone aggressively (MORE LIKELY)
- attack: Start a fight (NEW!)
- intimidate: Threaten someone (NEW!)
- flee: Move away from threats
...
"""
```

### Example 3: Add Weather/Time Context

**Edit:** `bridge/llm_bridge.py`

```python
def build_decision_prompt(self, context: Dict[str, Any]) -> str:
    # ... existing code ...

    # Add time of day
    game_time = context.get('time', 0)
    hour = int((game_time % 86400) / 3600)  # Convert to hour

    if hour < 6:
        prompt += "TIME: Early morning (dark, quiet)\n"
    elif hour < 12:
        prompt += "TIME: Morning (breakfast, yard time)\n"
    elif hour < 18:
        prompt += "TIME: Afternoon (work time, activities)\n"
    else:
        prompt += "TIME: Evening (dinner, cell time)\n"

    # Add weather (if available)
    weather = context.get('weather', 'normal')
    prompt += f"WEATHER: {weather}\n\n"
```

### Example 4: Gang-Specific Prompts

```python
if entity.get('gang'):
    gang = entity['gang']
    gang_role = entity.get('gang_role', 'member')

    prompt += f"""
GANG STATUS:
- Gang: {gang}
- Role: {gang_role}
- Gang loyalty: HIGH
- Rival gangs nearby: {has_rivals}

As a gang {gang_role}, prioritize:
1. Protecting gang territory
2. Supporting gang members
3. Confronting rivals
4. Following gang leader's orders
"""
```

---

## Best Practices

### ✅ DO:
- Keep prompts concise (LLMs work better with clear, focused prompts)
- Include relevant context only
- Use consistent formatting
- Test with different models
- Provide clear action options
- Use personality-appropriate language

### ❌ DON'T:
- Make prompts too long (>1000 tokens)
- Include irrelevant information
- Use ambiguous language
- Expect perfect responses every time
- Over-complicate the format

### Performance Tips

**Optimize for speed:**
1. Use smaller models for simple decisions (`phi`, `mistral`)
2. Use larger models for complex situations (`llama3:70b`)
3. Cache similar contexts
4. Batch process when possible

**Improve quality:**
1. Add more context for important decisions
2. Use temperature settings (lower = more consistent)
3. Provide examples in prompts
4. Test and iterate

---

## Testing Your Prompts

### Method 1: Direct Testing

```bash
python llm_bridge.py --test
```

### Method 2: Manual Testing

```python
from bridge.llm_bridge import OllamaBridge

bridge = OllamaBridge(model="llama3", debug=True)

# Test decision prompt
context = {
    "entity": {
        "personality": "The Alpha",
        "mood": "confident"
    },
    "nearby": []
}

request = {
    "type": "decision",
    "context": context
}

result = bridge.process_request(request)
print(result)
```

### Method 3: In-Game Testing

1. Enable debug mode in Lua scripts
2. Check terminal output
3. Observe NPC behavior
4. Adjust prompts based on results

---

## Advanced: Prompt Engineering

### Technique 1: Few-Shot Learning

Provide examples in the prompt:

```python
prompt += """
EXAMPLES:
- The Alpha sees a rival: "ACTION: confront | THOUGHT: Time to establish dominance."
- The Survivor is hungry: "ACTION: eat | THOUGHT: Stay fed, stay alive."
- The Paranoid sees a group: "ACTION: flee | THOUGHT: Too many people, not safe."

Now, based on YOUR situation:
"""
```

### Technique 2: Chain-of-Thought

Encourage reasoning:

```python
prompt += """
Think through this step-by-step:
1. What is my immediate situation?
2. What are my priorities (personality-based)?
3. What are the risks of each action?
4. What action best fits my personality?

Based on this reasoning, decide:
FORMAT: ACTION: [action] | THOUGHT: [reasoning]
"""
```

### Technique 3: Role Reinforcement

Strengthen personality:

```python
prompt += f"""
REMEMBER: You are {personality}.
- You ALWAYS act according to this personality
- Your decisions MUST reflect your core traits
- Stay true to character, even under pressure
"""
```

---

## Model Comparison

Different models produce different behaviors:

| Model | Speed | Quality | Personality Adherence | Best For |
|-------|-------|---------|----------------------|----------|
| phi | ⚡⚡⚡ | ⭐⭐ | ⭐⭐ | Fast decisions, simple AI |
| llama3 | ⚡⚡ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Balanced (recommended) |
| mistral | ⚡⚡ | ⭐⭐⭐ | ⭐⭐⭐ | Good balance |
| llama3:70b | ⚡ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Complex decisions, gangs |

**Recommendation:** Start with `llama3` for best balance.

---

## Further Reading

- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Modify the mod code
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Debug prompt issues
- **Ollama Docs** - https://ollama.ai/docs

---

**Experiment and have fun! 🎭**

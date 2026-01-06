# API Reference - Prison Architect AI Mod

**Prison Architect Lua API functions used in this mod**

This document explains which Prison Architect API functions are used and how.

---

## 📖 Table of Contents

1. [Overview](#overview)
2. [Object Functions](#object-functions)
3. [Game Functions](#game-functions)
4. [Entity Properties](#entity-properties)
5. [Limitations](#limitations)
6. [Workarounds](#workarounds)

---

## Overview

Prison Architect's modding API is **object-centric**. Mods create custom objects (defined in `materials.txt`) and script their behavior using Lua.

**Key limitation:** You cannot directly control existing game entities (prisoners, guards) at a low level. Instead, you:
- Create scripted objects that monitor entities
- Use API functions to influence entity behavior
- Work within the game's existing systems

---

## Object Functions

### Object.GetNearbyObjects()

**Purpose:** Find entities within a radius

**Signature:**
```lua
Object.GetNearbyObjects(x, y, radius, entityType)
```

**Parameters:**
- `x` (number): X coordinate
- `y` (number): Y coordinate
- `radius` (number): Search radius in tiles
- `entityType` (string): Type of entity to find (e.g., "Prisoner", "Guard")

**Returns:** Table of nearby entities
```lua
{
    {Object = entity1, Distance = 5.2},
    {Object = entity2, Distance = 12.8},
    ...
}
```

**Usage in this mod:**
```lua
-- AIController.lua
function ScanEntities()
    local prisoners = Object.GetNearbyObjects(this.Pos.x, this.Pos.y, 1000, "Prisoner")

    if prisoners then
        for i, prisonerData in ipairs(prisoners) do
            local prisoner = prisonerData.Object
            local distance = prisonerData.Distance

            TrackEntity(prisoner, "Prisoner")
        end
    end
end
```

**Where used:**
- `AIController.lua` - Entity tracking
- `AIConversationHub.lua` - Finding conversation partners
- `AIGangMeetingTable.lua` - Detecting gang members

---

### Object.NavigateTo()

**Purpose:** Command an entity to move to a location

**Signature:**
```lua
Object.NavigateTo(object, x, y)
```

**Parameters:**
- `object` (Entity): The entity to move
- `x` (number): Target X coordinate
- `y` (number): Target Y coordinate

**Returns:** Nothing

**Note:** Only works with Entity-type objects (prisoners, guards, etc.)

**Usage in this mod:**
```lua
-- Future implementation for movement control
function ExecuteMovement(entity, targetX, targetY)
    Object.NavigateTo(entity, targetX, targetY)
end
```

**Limitation:** We need a reference to the actual entity object, not just its ID. This requires storing entity references during scanning.

---

### Object.ClearRouting()

**Purpose:** Cancel an entity's current navigation

**Signature:**
```lua
Object.ClearRouting(entity)
```

**Parameters:**
- `entity` (Entity): The entity to stop

**Usage in this mod:**
```lua
-- Stop an entity's current action
function CancelEntityAction(entity)
    Object.ClearRouting(entity)
end
```

---

### Object.GetProperty()

**Purpose:** Read a property from an object

**Signature:**
```lua
Object.GetProperty(object, propertyName)
```

**Parameters:**
- `object` (Object): The object to query
- `propertyName` (string): Name of the property

**Returns:** Property value (type varies)

**Common properties:**
- `Pos` - Position {x, y}
- `Id` - Unique identifier
- `Type` - Entity type
- `Active` - Is active/alive
- `Health` - Health value

**Usage in this mod:**
```lua
function GetEntityInfo(entity)
    local position = Object.GetProperty(entity, "Pos")
    local id = Object.GetProperty(entity, "Id")
    local health = Object.GetProperty(entity, "Health")

    return {pos = position, id = id, health = health}
end
```

---

### Object.SetProperty()

**Purpose:** Write a property to an object

**Signature:**
```lua
Object.SetProperty(object, propertyName, value)
```

**Parameters:**
- `object` (Object): The object to modify
- `propertyName` (string): Name of the property
- `value` (any): Value to set

**Usage in this mod:**
```lua
-- Store custom data on entities
function TagEntity(entity, tag)
    Object.SetProperty(entity, "AITag", tag)
end
```

**Note:** Some properties are read-only and cannot be modified.

---

### Object.Spawn()

**Purpose:** Create a new object instance

**Signature:**
```lua
Object.Spawn(objectType, x, y)
```

**Parameters:**
- `objectType` (string): Object identifier from materials.txt
- `x` (number): X coordinate
- `y` (number): Y coordinate

**Returns:** Spawned object reference or nil

**Usage in this mod:**
```lua
-- Spawn a thought bubble above an NPC
function ShowThought(x, y, thought)
    local bubble = Object.Spawn("ai_thought_bubble", x, y)

    if bubble then
        Object.SetProperty(bubble, "Text", thought)
    end
end
```

---

### Object.Delete()

**Purpose:** Remove an object from the game

**Signature:**
```lua
Object.Delete(object)
```

**Parameters:**
- `object` (Object): The object to delete

**Usage in this mod:**
```lua
-- Clean up temporary UI elements
function RemoveThoughtBubble(bubble)
    Object.Delete(bubble)
end
```

---

## Game Functions

### Game.Time()

**Purpose:** Get current game time

**Signature:**
```lua
Game.Time()
```

**Returns:** Elapsed game time in seconds (number)

**Usage in this mod:**
```lua
-- Track when entities were last updated
function UpdateEntity(entityId)
    trackedEntities[entityId].lastUpdate = Game.Time()
end

-- Calculate time differences
function TimeSinceLastDecision(entityData)
    return Game.Time() - entityData.lastUpdate
end
```

**Where used:**
- All scripts - Timing updates and decisions
- Memory system - Timestamp events

---

### Game.DebugOut()

**Purpose:** Output debug messages to console

**Signature:**
```lua
Game.DebugOut(message)
```

**Parameters:**
- `message` (string): Message to output

**Usage in this mod:**
```lua
local debugMode = true

function LogDebug(message)
    if debugMode then
        Game.DebugOut("AI Mod: " .. message)
    end
end
```

**Where used:**
- All scripts - Debugging and status messages
- Essential for testing without visual UI

---

## Entity Properties

### Common Properties

**Accessed via `entity.PropertyName` or `Object.GetProperty(entity, "PropertyName")`**

#### Pos
```lua
local pos = entity.Pos  -- {x = 123.5, y = 456.7}
```

#### Id
```lua
local id = entity.Id  -- Unique integer identifier
```

#### Type
```lua
local type = entity.Type  -- "Prisoner", "Guard", etc.
```

#### Active
```lua
local active = entity.Active  -- true/false
```

### Prisoner-Specific Properties

#### Gang Affiliation
```lua
local gang = Object.GetProperty(prisoner, "Gang")
```

#### Security Level
```lua
local secLevel = Object.GetProperty(prisoner, "SecurityLevel")
```

#### Uniform Status
```lua
local hasUniform = Object.GetProperty(prisoner, "Uniform")
```

### Guard-Specific Properties

#### Patrol Route
```lua
local route = Object.GetProperty(guard, "PatrolRoute")
```

---

## Script Lifecycle Functions

### BeginObject()

**Called when:** Object is created/spawned

**Usage:**
```lua
function BeginObject()
    -- Initialize state
    if not this.ScriptState then
        this.ScriptState = {}
    end

    Game.DebugOut("Object initialized")
end
```

### Update()

**Called when:** Every frame (or game tick)

**Global available:** `Dt` (delta time since last update)

**Usage:**
```lua
local timeSinceUpdate = 0

function Update()
    timeSinceUpdate = timeSinceUpdate + Dt

    if timeSinceUpdate >= 2.0 then
        timeSinceUpdate = 0
        -- Do periodic update
    end
end
```

### EndObject()

**Called when:** Object is destroyed/removed

**Usage:**
```lua
function EndObject()
    -- Save state before destruction
    SaveData()
    Game.DebugOut("Object shutting down")
end
```

---

## Data Persistence

### this.ScriptState

**Purpose:** Persistent storage for the object

**Type:** Table (dictionary)

**Persists:** Across save/load

**Usage:**
```lua
function SaveEntityData()
    if this.ScriptState then
        this.ScriptState.entities = trackedEntities
        this.ScriptState.lastSave = Game.Time()
    end
end

function LoadEntityData()
    if this.ScriptState and this.ScriptState.entities then
        trackedEntities = this.ScriptState.entities
    end
end
```

**Where used:**
- `AIController.lua` - Entity tracking data
- `AIConversationHub.lua` - Conversation history
- `AIGangMeetingTable.lua` - Gang data

---

## Limitations

### What You CANNOT Do

❌ **Directly override base NPC AI**
- Cannot fully control prisoner/guard decision-making
- Cannot prevent base game behaviors

❌ **Full entity control**
- Cannot force entities to use specific objects
- Cannot directly trigger animations
- Cannot modify core entity stats (hunger, hygiene) directly

❌ **UI manipulation**
- No built-in UI creation functions
- Cannot create speech bubbles directly
- Limited visual feedback options

❌ **Advanced pathfinding**
- NavigateTo() uses basic pathfinding
- No control over pathfinding algorithm
- Cannot guarantee entities reach destination

❌ **Event hooks**
- No direct event system
- Cannot hook into prisoner fights, escapes, etc.
- Must poll for state changes

### What You CAN Do

✅ **Influence behavior indirectly**
- Use NavigateTo() to suggest movements
- Create objects entities interact with
- Track and predict entity actions

✅ **Monitor and track**
- GetNearbyObjects() to scan continuously
- Track entity properties
- Build memory and history

✅ **Create custom objects**
- Design new interactive objects
- Script object behaviors
- Generate dynamic content

✅ **Persistent data**
- Save/load entity memories
- Track relationships
- Build complex state machines

---

## Workarounds

### Problem: Can't create speech bubbles

**Workaround:**
1. Use `Game.DebugOut()` for text output
2. Create placeholder objects above entities
3. Use sound effects to indicate dialogue

**Future:**
- Explore sprite-based text rendering
- Community-created UI libraries

### Problem: Can't force entity actions

**Workaround:**
1. Use `NavigateTo()` to move entities near objects they might use
2. Create attractive objects (high utility) entities naturally use
3. Combine with timing (meal times, sleep times)

### Problem: Limited entity properties access

**Workaround:**
1. Infer from behavior (if near canteen → likely eating)
2. Track over time to build profiles
3. Use statistical patterns

### Problem: No event system

**Workaround:**
1. Poll frequently for state changes
2. Compare current state to previous state
3. Detect events via property changes

**Example:**
```lua
local previousHealth = {}

function DetectFights()
    local prisoners = GetNearbyPrisoners()

    for _, p in ipairs(prisoners) do
        local currentHealth = p.Health
        local lastHealth = previousHealth[p.Id] or currentHealth

        if currentHealth < lastHealth - 10 then
            -- Prisoner took damage → likely in fight
            OnFightDetected(p)
        end

        previousHealth[p.Id] = currentHealth
    end
end
```

---

## Best Practices

### Performance

✅ **Batch operations**
```lua
-- Good: Process in batches
local processCount = 0
for id, entity in pairs(entities) do
    if processCount >= 5 then break end
    ProcessEntity(entity)
    processCount = processCount + 1
end
```

❌ **Don't process all entities every frame**
```lua
-- Bad: Too expensive
for id, entity in pairs(allEntities) do
    ProcessEntity(entity)  -- Could be 100s of entities!
end
```

✅ **Use timers**
```lua
-- Only update every N seconds
if timeSinceUpdate >= updateInterval then
    DoExpensiveOperation()
end
```

### Error Handling

✅ **Check for nil**
```lua
local prisoners = Object.GetNearbyObjects(x, y, radius, "Prisoner")

if prisoners then  -- Might be nil!
    for i, p in ipairs(prisoners) do
        -- Safe to use p here
    end
end
```

✅ **Validate references**
```lua
if entity and entity.Id and entity.Pos then
    -- Entity is valid
end
```

---

## External Resources

- **Prison Architect API Wiki:** https://github.com/originalfoo/Prison-Architect-API/wiki
- **Lua Function List:** https://github.com/originalfoo/Prison-Architect-API/blob/master/main/data/lua_function_list.txt
- **Steam Modding Guides:** https://steamcommunity.com/app/233450/guides/

---

**For mod development help, see [DEVELOPMENT.md](DEVELOPMENT.md)**

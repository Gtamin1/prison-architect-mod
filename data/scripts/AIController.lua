--[[
    AI Controller - Main coordination script for AI-powered NPCs

    This script manages:
    - Entity tracking (prisoners, guards, staff)
    - Communication with Python bridge (Ollama LLM)
    - Decision execution based on AI responses
    - Memory persistence

    The AIController object is invisible and acts as the central brain.
]]--

-- Global state
local updateInterval = 2.0  -- Update every 2 seconds
local timeSinceUpdate = 0
local trackedEntities = {}
local bridgeFile = "ai_bridge_request.json"
local responseFile = "ai_bridge_response.json"
local debugMode = true

-- Entity tracking structure
--[[
    trackedEntities[entityId] = {
        id = number,
        type = string ("Prisoner", "Guard", etc.),
        position = {x, y},
        personality = string,
        memory = {},
        relationships = {},
        gang = string or nil,
        lastDecision = string,
        currentAction = string,
        mood = string,
        needs = {},
        lastUpdate = number
    }
]]--

function BeginObject()
    if debugMode then
        Game.DebugOut("AIController: Initialized")
    end

    -- Initialize persistent storage
    InitializeStorage()

    -- Load existing entity data if available
    LoadEntityData()
end

function Update()
    timeSinceUpdate = timeSinceUpdate + Dt

    if timeSinceUpdate >= updateInterval then
        timeSinceUpdate = 0

        -- Scan for nearby entities
        ScanEntities()

        -- Process entity decisions
        ProcessEntityDecisions()

        -- Update visual feedback
        UpdateVisualFeedback()

        -- Save entity data periodically
        SaveEntityData()
    end
end

function ScanEntities()
    -- Scan for prisoners within large radius
    local prisoners = Object.GetNearbyObjects(this.Pos.x, this.Pos.y, 1000, "Prisoner")

    if prisoners then
        for i, prisonerData in ipairs(prisoners) do
            local prisoner = prisonerData.Object
            local distance = prisonerData.Distance

            if prisoner and prisoner.Id then
                TrackEntity(prisoner, "Prisoner")
            end
        end
    end

    -- Scan for guards
    local guards = Object.GetNearbyObjects(this.Pos.x, this.Pos.y, 1000, "Guard")

    if guards then
        for i, guardData in ipairs(guards) do
            local guard = guardData.Object
            local distance = guardData.Distance

            if guard and guard.Id then
                TrackEntity(guard, "Guard")
            end
        end
    end

    if debugMode then
        local entityCount = 0
        for _ in pairs(trackedEntities) do entityCount = entityCount + 1 end
        Game.DebugOut("AIController: Tracking " .. entityCount .. " entities")
    end
end

function TrackEntity(entity, entityType)
    local entityId = entity.Id

    -- Initialize if new
    if not trackedEntities[entityId] then
        trackedEntities[entityId] = {
            id = entityId,
            type = entityType,
            position = {x = entity.Pos.x, y = entity.Pos.y},
            personality = AssignPersonality(),
            memory = {},
            relationships = {},
            gang = nil,
            lastDecision = "",
            currentAction = "idle",
            mood = "neutral",
            needs = {
                hunger = 50,
                hygiene = 50,
                bladder = 50,
                exercise = 50,
                family = 50,
                safety = 50
            },
            lastUpdate = Game.Time()
        }

        if debugMode then
            Game.DebugOut("AIController: New " .. entityType .. " tracked: " .. entityId .. " (Personality: " .. trackedEntities[entityId].personality .. ")")
        end
    else
        -- Update position
        trackedEntities[entityId].position = {x = entity.Pos.x, y = entity.Pos.y}
        trackedEntities[entityId].lastUpdate = Game.Time()
    end
end

function AssignPersonality()
    -- Personality types for diverse behavior
    local personalities = {
        "The Alpha",      -- Dominant, leader
        "The Strategist", -- Calculating, manipulative
        "The Hothead",    -- Impulsive, violent
        "The Survivor",   -- Pragmatic, cautious
        "The Idealist",   -- Reform-minded, hopeful
        "The Broken",     -- Traumatized, unpredictable
        "The Enforcer",   -- Violent, loyal
        "The Smooth Talker", -- Charismatic, persuasive
        "The Paranoid",   -- Suspicious, defensive
        "The Follower",   -- Submissive, group-oriented
        "The Opportunist", -- Self-serving, flexible
        "The Psychopath", -- Ruthless, calculating
        "The Mentor",     -- Wise, protective
        "The Rebel",      -- Defiant, independent
        "The Coward",     -- Risk-averse, fearful
        "The Addict",     -- Desperate, unstable
        "The Peacemaker", -- Diplomatic, conflict-averse
        "The Schemer",    -- Ambitious, sneaky
        "The Stoic",      -- Emotionless, disciplined
        "The Wild Card"   -- Unpredictable, chaotic
    }

    local randomIndex = math.random(1, #personalities)
    return personalities[randomIndex]
end

function ProcessEntityDecisions()
    -- In batches to avoid performance issues
    local processCount = 0
    local maxPerFrame = 5

    for entityId, entityData in pairs(trackedEntities) do
        if processCount >= maxPerFrame then
            break
        end

        -- Check if entity needs a new decision
        local timeSinceLastDecision = Game.Time() - entityData.lastUpdate

        if timeSinceLastDecision > 5.0 then  -- Make decision every 5 seconds
            RequestAIDecision(entityId, entityData)
            processCount = processCount + 1
        end
    end
end

function RequestAIDecision(entityId, entityData)
    -- Build context for LLM
    local context = BuildEntityContext(entityId, entityData)

    -- Write request to bridge file (simplified for now)
    -- In full implementation, this would write JSON to a file
    -- that the Python bridge monitors

    -- For now, make simple rule-based decisions
    -- (Will be replaced with actual LLM calls)
    local decision = MakeSimpleDecision(entityData)

    ExecuteDecision(entityId, decision)
end

function BuildEntityContext(entityId, entityData)
    -- Find nearby entities
    local nearbyEntities = {}

    for otherId, otherData in pairs(trackedEntities) do
        if otherId ~= entityId then
            local dx = entityData.position.x - otherData.position.x
            local dy = entityData.position.y - otherData.position.y
            local distance = math.sqrt(dx * dx + dy * dy)

            if distance < 20 then  -- Within 20 units
                table.insert(nearbyEntities, {
                    id = otherId,
                    type = otherData.type,
                    distance = distance,
                    personality = otherData.personality,
                    gang = otherData.gang
                })
            end
        end
    end

    return {
        entity = entityData,
        nearby = nearbyEntities,
        time = Game.Time()
    }
end

function MakeSimpleDecision(entityData)
    -- Simple rule-based decisions (placeholder for LLM)
    local decisions = {
        "wander",
        "socialize",
        "rest",
        "explore"
    }

    -- Weight decisions by personality
    if entityData.personality == "The Alpha" then
        return "socialize"  -- Alphas like to interact
    elseif entityData.personality == "The Paranoid" then
        return "rest"  -- Paranoid types avoid others
    elseif entityData.personality == "The Hothead" then
        if math.random() > 0.7 then
            return "confront"  -- Sometimes aggressive
        else
            return "wander"
        end
    else
        -- Random for others
        return decisions[math.random(1, #decisions)]
    end
end

function ExecuteDecision(entityId, decision)
    local entityData = trackedEntities[entityId]

    if not entityData then
        return
    end

    entityData.lastDecision = decision
    entityData.currentAction = decision

    if debugMode then
        Game.DebugOut("AIController: Entity " .. entityId .. " (" .. entityData.personality .. ") decides: " .. decision)
    end

    -- Execute the decision
    -- Note: We can't directly control entities without a reference to the actual object
    -- This would need to be enhanced with actual entity object references
end

function UpdateVisualFeedback()
    -- Spawn thought bubbles or UI elements to show AI thinking
    -- This would create visible indicators in the game
    -- Placeholder for now
end

function InitializeStorage()
    -- Set up persistent storage using ScriptState
    if not this.ScriptState then
        this.ScriptState = {}
    end

    if not this.ScriptState.entities then
        this.ScriptState.entities = {}
    end
end

function SaveEntityData()
    -- Save tracked entities to persistent storage
    if this.ScriptState then
        this.ScriptState.entities = trackedEntities
        this.ScriptState.lastSave = Game.Time()
    end
end

function LoadEntityData()
    -- Load previously tracked entities
    if this.ScriptState and this.ScriptState.entities then
        trackedEntities = this.ScriptState.entities

        if debugMode then
            local count = 0
            for _ in pairs(trackedEntities) do count = count + 1 end
            Game.DebugOut("AIController: Loaded " .. count .. " entities from storage")
        end
    end
end

function EndObject()
    SaveEntityData()

    if debugMode then
        Game.DebugOut("AIController: Shutting down")
    end
end

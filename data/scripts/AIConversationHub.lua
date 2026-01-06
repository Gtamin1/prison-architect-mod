--[[
    AI Conversation Hub - Facilitates NPC conversations

    This object acts as a meeting point where NPCs can gather and have
    AI-generated conversations. When NPCs use this object, they'll engage
    in dynamic dialogue based on their personalities and relationships.
]]--

local activeConversations = {}
local conversationHistory = {}
local debugMode = true

function BeginObject()
    if debugMode then
        Game.DebugOut("AIConversationHub: Initialized at " .. this.Pos.x .. "," .. this.Pos.y)
    end

    -- Initialize object state
    if not this.ScriptState then
        this.ScriptState = {
            participants = {},
            conversationLog = {},
            lastActivity = 0
        }
    end
end

function Update()
    -- Check for nearby entities who might want to converse
    local nearbyPrisoners = Object.GetNearbyObjects(this.Pos.x, this.Pos.y, 10, "Prisoner")

    if nearbyPrisoners and #nearbyPrisoners >= 2 then
        -- Potential conversation!
        InitiateConversation(nearbyPrisoners)
    end

    -- Update active conversations
    UpdateConversations()
end

function InitiateConversation(participants)
    if #participants < 2 then
        return
    end

    -- Take first two participants
    local speaker = participants[1].Object
    local listener = participants[2].Object

    if not speaker or not listener then
        return
    end

    -- Check if they're already in a conversation
    local conversationKey = speaker.Id .. "_" .. listener.Id

    if not activeConversations[conversationKey] then
        -- Start new conversation
        activeConversations[conversationKey] = {
            participants = {speaker.Id, listener.Id},
            startTime = Game.Time(),
            turns = 0,
            topic = SelectConversationTopic()
        }

        if debugMode then
            Game.DebugOut("AIConversationHub: Starting conversation between " .. speaker.Id .. " and " .. listener.Id)
        end

        -- Generate first dialogue line
        GenerateDialogue(speaker, listener, conversationKey)
    end
end

function SelectConversationTopic()
    local topics = {
        "prison_conditions",
        "escape_plans",
        "gang_business",
        "guards",
        "family",
        "food_quality",
        "cell_mate",
        "yard_time",
        "contraband",
        "reputation",
        "rumors",
        "grievances"
    }

    return topics[math.random(1, #topics)]
end

function GenerateDialogue(speaker, listener, conversationKey)
    -- In a full implementation, this would request dialogue from the Python bridge
    -- For now, use template-based generation

    local conversation = activeConversations[conversationKey]

    if not conversation then
        return
    end

    local dialogue = GenerateTemplateDialogue(conversation.topic, conversation.turns)

    -- Store dialogue
    table.insert(conversation.dialogue or {}, {
        speaker = speaker.Id,
        text = dialogue,
        time = Game.Time()
    })

    -- Display dialogue (in a real implementation, this would show a speech bubble)
    if debugMode then
        Game.DebugOut("NPC " .. speaker.Id .. ": " .. dialogue)
    end

    -- Update conversation state
    conversation.turns = conversation.turns + 1

    -- End conversation after a few turns
    if conversation.turns >= 3 then
        EndConversation(conversationKey)
    end
end

function GenerateTemplateDialogue(topic, turn)
    local dialogueTemplates = {
        prison_conditions = {
            "This place is a dump, man.",
            "You think it's bad now? Wait til winter.",
            "At least we got running water, I guess."
        },
        escape_plans = {
            "I've been thinking about the fence...",
            "You crazy? They'll shoot you down.",
            "Maybe there's another way..."
        },
        gang_business = {
            "You in with anyone yet?",
            "My crew runs this block.",
            "Better watch who you talk to."
        },
        guards = {
            "That new guard is on a power trip.",
            "Officer Martinez is alright, I guess.",
            "They're all the same to me."
        },
        food_quality = {
            "What was that slop today?",
            "I'd kill for a real burger.",
            "At least it's better than county."
        }
    }

    local templates = dialogueTemplates[topic] or {"...", "Yeah.", "Hmm."}
    local index = (turn % #templates) + 1

    return templates[index]
end

function UpdateConversations()
    -- Clean up old conversations
    local currentTime = Game.Time()

    for key, conversation in pairs(activeConversations) do
        local duration = currentTime - conversation.startTime

        if duration > 60 then  -- End after 60 seconds
            EndConversation(key)
        end
    end
end

function EndConversation(conversationKey)
    local conversation = activeConversations[conversationKey]

    if conversation then
        -- Archive to history
        table.insert(conversationHistory, {
            participants = conversation.participants,
            topic = conversation.topic,
            turns = conversation.turns,
            endTime = Game.Time()
        })

        if debugMode then
            Game.DebugOut("AIConversationHub: Ended conversation " .. conversationKey)
        end

        -- Remove from active
        activeConversations[conversationKey] = nil
    end
end

function EndObject()
    -- Save conversation history
    if this.ScriptState then
        this.ScriptState.conversationLog = conversationHistory
    end

    if debugMode then
        Game.DebugOut("AIConversationHub: Shutting down")
    end
end

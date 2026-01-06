--[[
    AI Gang Meeting Table - Facilitates gang coordination

    This object enables gang members to meet, plan, and coordinate.
    Gang leaders can call meetings, discuss territory, plan operations,
    and make strategic decisions powered by AI.
]]--

local gangMeetings = {}
local gangData = {}
local debugMode = true

function BeginObject()
    if debugMode then
        Game.DebugOut("AIGangMeetingTable: Initialized")
    end

    if not this.ScriptState then
        this.ScriptState = {
            activeGangs = {},
            meetingHistory = {},
            decisions = {}
        }
    end

    -- Load gang data
    LoadGangData()
end

function Update()
    -- Check for gang members nearby
    local nearbyPrisoners = Object.GetNearbyObjects(this.Pos.x, this.Pos.y, 15, "Prisoner")

    if nearbyPrisoners and #nearbyPrisoners >= 3 then
        -- Check if they're from the same gang
        CheckForGangMeeting(nearbyPrisoners)
    end

    -- Update active meetings
    UpdateActiveMeetings()
end

function LoadGangData()
    if this.ScriptState and this.ScriptState.activeGangs then
        gangData = this.ScriptState.activeGangs
    else
        gangData = {}
    end
end

function CheckForGangMeeting(prisoners)
    -- Group prisoners by gang affiliation
    local gangGroups = {}

    for i, prisonerData in ipairs(prisoners) do
        local prisoner = prisonerData.Object

        if prisoner then
            -- In a full implementation, we'd get gang data from AIController
            -- For now, simulate gang assignment
            local gangId = "gang_" .. (prisoner.Id % 3)  -- Simple assignment

            if not gangGroups[gangId] then
                gangGroups[gangId] = {}
            end

            table.insert(gangGroups[gangId], prisoner)
        end
    end

    -- Start meeting if enough gang members present
    for gangId, members in pairs(gangGroups) do
        if #members >= 3 and not gangMeetings[gangId] then
            StartGangMeeting(gangId, members)
        end
    end
end

function StartGangMeeting(gangId, members)
    gangMeetings[gangId] = {
        gangId = gangId,
        members = members,
        leader = DetermineLeader(members),
        startTime = Game.Time(),
        agenda = SelectMeetingAgenda(),
        decisions = {}
    }

    if debugMode then
        Game.DebugOut("AIGangMeetingTable: Gang meeting started - " .. gangId .. " (" .. #members .. " members)")
    end

    -- Conduct the meeting
    ConductMeeting(gangId)
end

function DetermineLeader(members)
    -- In a full implementation, this would be based on personality and reputation
    -- For now, just pick the first member
    return members[1].Id
end

function SelectMeetingAgenda()
    local agendas = {
        "territory_expansion",
        "rival_confrontation",
        "contraband_smuggling",
        "protection_racket",
        "escape_planning",
        "recruitment",
        "internal_discipline",
        "alliance_discussion"
    }

    return agendas[math.random(1, #agendas)]
end

function ConductMeeting(gangId)
    local meeting = gangMeetings[gangId]

    if not meeting then
        return
    end

    -- Generate meeting dialogue and decisions
    -- In full implementation, this would use LLM for realistic gang strategy

    local decision = MakeMeetingDecision(meeting.agenda)

    table.insert(meeting.decisions, decision)

    if debugMode then
        Game.DebugOut("AIGangMeetingTable: Gang " .. gangId .. " decided: " .. decision.action)
    end

    -- Record decision
    RecordGangDecision(gangId, decision)
end

function MakeMeetingDecision(agenda)
    local decisions = {
        territory_expansion = {
            action = "expand_to_east_wing",
            reasoning = "East wing is weakly defended",
            risk = "medium"
        },
        rival_confrontation = {
            action = "challenge_rival_leader",
            reasoning = "Show of strength needed",
            risk = "high"
        },
        contraband_smuggling = {
            action = "bribe_guard_johnson",
            reasoning = "He's shown he can be bought",
            risk = "low"
        },
        escape_planning = {
            action = "tunnel_from_workshop",
            reasoning = "Least monitored area",
            risk = "very_high"
        }
    }

    return decisions[agenda] or {
        action = "wait_and_observe",
        reasoning = "Need more information",
        risk = "none"
    }
end

function RecordGangDecision(gangId, decision)
    -- Ensure gang exists in data
    if not gangData[gangId] then
        gangData[gangId] = {
            name = GenerateGangName(),
            formed = Game.Time(),
            members = {},
            territory = {},
            decisions = {},
            reputation = 50
        }
    end

    -- Add decision to gang history
    table.insert(gangData[gangId].decisions, {
        decision = decision,
        time = Game.Time()
    })

    -- Save to persistent storage
    SaveGangData()
end

function GenerateGangName()
    local prefixes = {"The", "Los", "The Dirty", "The Bloody"}
    local names = {"Wolves", "Kings", "Serpents", "Brothers", "Familia", "Crew", "Syndicate"}

    local prefix = prefixes[math.random(1, #prefixes)]
    local name = names[math.random(1, #names)]

    return prefix .. " " .. name
end

function UpdateActiveMeetings()
    local currentTime = Game.Time()

    for gangId, meeting in pairs(gangMeetings) do
        local duration = currentTime - meeting.startTime

        if duration > 120 then  -- End after 2 minutes
            EndGangMeeting(gangId)
        end
    end
end

function EndGangMeeting(gangId)
    local meeting = gangMeetings[gangId]

    if meeting then
        -- Archive meeting
        if this.ScriptState then
            table.insert(this.ScriptState.meetingHistory, {
                gangId = gangId,
                agenda = meeting.agenda,
                decisions = meeting.decisions,
                endTime = Game.Time()
            })
        end

        if debugMode then
            Game.DebugOut("AIGangMeetingTable: Meeting ended - " .. gangId)
        end

        gangMeetings[gangId] = nil
    end
end

function SaveGangData()
    if this.ScriptState then
        this.ScriptState.activeGangs = gangData
    end
end

function EndObject()
    SaveGangData()

    if debugMode then
        Game.DebugOut("AIGangMeetingTable: Shutting down")
    end
end

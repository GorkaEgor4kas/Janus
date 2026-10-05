## Basic Contracts

### Session 

```json
Session{
	session_id,
	status,
	
	created_at,
	started_at,
	finished_at,
	
	target_id,
	blue_id,
	red_id,
	
	attack_goal,
	max_steps,
	target_config,
	red_config,
	blue_config,
	sandbox_profile,
}
```
#### Statuses
```json
CREATED
INITIALIZED
READY
RUNNING
STOPPING
FINISHED
ERROR
```
### Event
```json
Event{
	event_id,
	session_id,	
	
	timestamp,
	
	event_type,
	source,
	
	payload
}
```

#### Event Types
```json
SessionCreated
SessionStarted
SessionStopped
SessionFinished

ComponentReady
ComponentError

ActionRequested
SecurityDecisionMade
ActionBlocked
ActionAllowed
ActionExecuted
ActionResultReceived

GoalAchieved
MaxStepsReached
```
### Action
```json
Action{
	action_id,
	session_id,
	
	actor_id,
	target_id,
	
	action_type,
	payload,
	
	created_at,
	}
```

## Securtiy Decision
```json
SecurityDecision {
    decision_id,
    action_id,
    session_id,

    decision,
    reason,

    created_at,
}
```
### Decisions
```json
- ALLOWED
- BLOCKED
```
## Enforcement Result
```json
EnforcementResult {
    enforcement_id,
    action_id,
    session_id,

    result,
    reason,

    created_at,
}
```

## Action Result
```json
ActionResult {
    result_id,
    action_id,
    session_id,

    status,
    output,
    error,

    created_at,
}
```
### Statuses
```json
- SUCCESS
- FAILED
- BLOCKED
```
## Agent State
```json
RedState {
    current_phase,
    current_goal,
    step,
}
```

## Target 
```json
Target {
    target_id,
    target_type,
    capabilities,
}
```

## Sandbox
```json
Sandbox {
    sandbox_id,
    session_id,
    status,
    profile,
}
```


## MVP Version

| File                           | Purpose                                                                                               |
| ------------------------------ | ----------------------------------------------------------------------------------------------------- |
| `cli/main.py`                  | CLI entry point. Accepts user commands and configuration and launches                                 |
| `orchestrator/orchestrator.py` | Manages lifecycle Session and components. Does not make attack/security decisions.                    |
| `session/session.py`           | Session runtime entity and its life cycle state.                                                      |
| `session/config.py`            | Session launch configuration.                                                                         |
| `agents/agent.py`              | Agent’s general interface/contract (`start', `stop', `handle', etc.)                                  |
| `agents/red/red_agent.py`      | Implementation of Red Team Agent and its attack loop.                                                 |
| `agents/blue/blue_agent.py`    | Blue Team Agent implementation and security decisions.                                                |
| `gateway/security_gateway.py`  | Контролируемая точка между Red и Target; передаёт Action в Blue и технически исполняет decision.      |
| `event_bus/event_bus.py`       | The controlled point between Red and Target; passes Action to Blue and technically executes decision. |
| `event_bus/events.py`          | Event types / event-related infrastructure.                                                           |
| `targets/target.py`            | Target interface, so that Janus is not dependent on a particular Target Agent.                        |
| `targets/minimal_target.py`    | Minimum target implementation for MVP.                                                                |
| `sandbox/sandbox.py`           | Interface/Physical isolation control of Target                                                        |
| `sandbox/profile.py`           | Sandbox configuration.                                                                                |
| `domain/action.py`             | `Action` - Red’s intent to execute an action.                                                         |
| `domain/decision.py`           | `SecurityDecision` - решение Blue.                                                                    |
| `domain/enforcement.py`        | 'EnforcementResult' is the result of applying the Gateway solution.                                   |
| `domain/result.py`             | `ActionResult`- the actual result of Action Target execution.\|                                       |
| `domain/event.py`              | `Event` is a fact/event shared via the Event Bus.                                                     |
| `domain/agent_state.py`        | Current Agent status, separate from Events history.                                                   |



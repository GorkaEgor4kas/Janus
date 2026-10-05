### Start Session
---
- User
- CLI
- Orchestrator
- Session
- **Handshake Protocol**
- If:
		READY: Session RUNNING
		ERROR: STOP Session 
---

### Handshake
----
For each component Orchestrator sends a first handshake and awaits for response. Only after the response of all of components Orchestrator will run the session
- Orchestrator sends hand in turn:
		Sandbox
		Target 
		Gateway
		Red 
		Blue
		Event Bus
		Metrics, Logging
- Orchestrator recieves handshakes
- If:
		OK: Send message of successfull handshakes process
		ERROR: Send message with error back
---
### Action execution
---
- Red creates action
- Red → Gateway
- Gaeway → Event Bus: ActionRequested
- Blue recieves Action 
- Blue creates Security decision → Gateway
- Gateway: 
		BLOCK → return blocked result
		ALLOW → forward the action to Target
- Targer executes → returns Result
- Gateway returns Result to Red
- Red observes Result
- Red decides the next step

----
### Error Handling
---
- Componen Error Event
- Event Bus
- Orchestrator
- If:
		Recoverable error: Component tries recovery → READY / RUNNING
		Critical error: Orchestrator **End Session Protocol**
---
### End Session
---
- Goal achives / Exeeded amount of steps
- Orchestrator → SessionsStop for all elements
- Stop Red
- Stop Blue
- Stop Gateway
- Stop Target
- Stop Sandbox
- Confirm stopping
- Session Finished 
---




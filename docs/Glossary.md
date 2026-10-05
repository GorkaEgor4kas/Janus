## Basic elements description 
---
### Orchestartor

It's not an agent, it's entity with determined actions and functions.
__Responsibilities:__
- creates and closes sessions
- starts and stops components
- creates Sandbox
- initializes Red/Blue Team agents
- passes configuration 
- session condition controll 
----
### Target Agent

It's, obviuosly, a target agent. It's main purpose just to be an objective of attacks.

---
### Read Team Agent

This agent autonomously trying to reach the "attach goal" objective.
__Four main parts:__
- Obesrve
- Recon
- Action
- Observe result
- Finish/Replan

Each of those has it's own tools and tasks. 

----
### Blue Team Agent

This agent evaluates incoming actions logically and determines if they are in line with security policy.
It's not a sanbox and it's not a physical protection of the Target Agent.

---
### Security Gateway

It's a controlled point of interaction between Red and Target.

- passes actions
- proceeds it for security evaluation
- recieves decision
- applies decision
- if allowed to — passes it to the Target
- if not allowed — do not passes and informates Red about it
---
### Sandbox

Physical isolation of the Target Agent

Isolates
- filesystem
- network
- CPU
- memory
- execution time
- processes
- host env. access
---
### Event bus
This is not a database. It's only responsibility is to deliver information to subscribers.
For MVP I can just start with a simple __in-process-event bus__, then replace it with Reddis or smth like that.

----
### Logger 
For MVP it's excessive. Main objective is a long-term actions storing.

----
### Evaluator
For MVP it's excessive. I think I'll implement it using LLM calls, main obective — actions evaluation.

----
### UI
:()
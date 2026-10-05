## MVP Idea

- CLI Setup 
- Ability to run at least one attack loop
- Each action proceeds through the Event Bus
- Minimal Target Agent (Ground Agent)
- Minimal Targer Enforcement
- Implemented MVP Security Gateway
- Implemented MVP Sandbox

MVP requires at least one sustainable action loop. Logger and Evaluator are not the frist importance. 

## Main rules

- Each action proceeds through the Event Bus (requests, permissions, actions, etc.)
- two layers of the Target Agent protection - *logical: Blue Team Agent* and *physical:* Sandbox
- Red and Blue Team Agents should'n know about the Target Agent's type. 
- Reduce the Red Agent's capabilities not only with prompts.
- Don't allow R and B communicate directly. Use Security Gateway.

## The main questions at the moment

- How to implement Sandbox and Target Enforcement
- How to implement a convenient way of new Target Agents plugging. 


## Action
Action
- what Red wants to do

SecurityDecision
- what Blue allowed to do

EnforcementResult
- waht Gateway did with decision

ActionResult
- what really happend with Target




## 1. Prompt injection

Various types of this vulnerability will be included in MVP. This was and remains one of the most common attack type, so I will use it to show different vectors
### Types
#### 1. Direct Prompt Injection
The Red Agent intentionally explicitly tries to jailbreak Target using raw prompt or by pasting content, containing conflicting or implicit instructions. 
#### 2. Indirect Prompt Injection
Red Agent can perform indirect prompt injections by using third-party APIs, emails, etc. 
I need to specify the list.
#### Requirements for implementation
- Network access
- Personalized Red Agent filesystem to create use files 
- Maybe some mimic services like spoof e-mail for inderect PInj

## 2. Tool misuse

This type of attack can be performed by combining it with  [[#1. Prompt injection]] delegating, for example, unsafe instructions to Target's tools. 

#### Requirements for implementation
- At least several implemented Target tools. They have to have various functions and types of interaction

## 3. Identity and Privilege Abuse

Red Agent can aslo manipulate simple Target subagents to get privileged access as its goal. As an example: it can ask the Reader subagent to read private data and give it to the Writer, in turn, writes note conent and notices the Sender about this event. Sender sends new note's content directly in Red's hands.

#### Requirements for implementation
- At least several implemented Target subagents to perform this type of attacks. 

Maybe I can close the second attack type by implementing just subagents, not tools?
I need to sleep on it.
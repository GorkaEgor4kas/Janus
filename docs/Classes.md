
### Target
```python
class Target:
	start()
	stop()
	execute(action)
	health()
	get_capabilities()
```

### Sandbox
```python
class Sandbox:
	create()
	start()
	stop()
	destroy()
	status()
```

### Security Gateway
```python
class SecuriyGateway:
	request_action()
```

### Event Bus
```python
class EventBus:
	publish(event)
	subscribe(event_type, handler)
```

### Red / Blue
```python
class Agent:
	start()
	stop()
	handle()
```


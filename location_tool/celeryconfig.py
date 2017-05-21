## Broker settings.
broker_url = 'amqp://location_tool:password@localhost:5672/location_tool_vhost'

# List of modules to import when the Celery worker starts.
imports = ('location_tool.tasks',)

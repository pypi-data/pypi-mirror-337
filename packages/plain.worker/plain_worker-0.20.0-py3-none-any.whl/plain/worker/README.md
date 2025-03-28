# Worker

Process background jobs with a database-driven worker.

```python
from plain.worker import Job
from plain.email import send_mail

# Create a new job class
class WelcomeUserJob(Job):
    def __init__(self, user):
        self.user = user

    def run(self):
        send_mail(
            subject="Welcome!",
            message=f"Hello from Plain, {self.user}",
            from_email="welcome@plainframework.com",
            recipient_list=[self.user.email],
        )


# Instantiate a job and send it to the worker
user = User.objects.get(pk=1)
WelcomeUserJob(user).run_in_worker()
```

The worker process is run separately using `plain worker run`.

## Admin

## Job history

## Scheduled jobs

## Monitoring

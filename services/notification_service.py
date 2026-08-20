"""
Notification Service for event-driven decoupled alerts.
"""
from patterns.observer import EventPublisher, WaitlistObserver, AdvisorObserver, AdminErrorObserver

class NotificationService:
    """Configures and manages the EventPublisher and its Observers."""
    def __init__(self):
        self.publisher = EventPublisher()
        
        # Register standard observers defined in System Design
        self.publisher.subscribe(WaitlistObserver(self.publisher))
        self.publisher.subscribe(AdvisorObserver())
        self.publisher.subscribe(AdminErrorObserver())
        
    def get_publisher(self) -> EventPublisher:
        return self.publisher

"""
Notification Service for event-driven decoupled alerts.
"""
from patterns.observer import EventPublisher, WaitlistObserver, AdvisorObserver, AdminErrorObserver

class NotificationService:
    """Configures and manages the EventPublisher and its Observers."""
    def __init__(self):
        self.publisher = EventPublisher()
        
        # Register standard observers defined in System Design
        self.publisher.register_observer(WaitlistObserver())
        self.publisher.register_observer(AdvisorObserver())
        self.publisher.register_observer(AdminErrorObserver())
        
    def get_publisher(self) -> EventPublisher:
        return self.publisher

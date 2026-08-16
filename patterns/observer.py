"""
Observer Pattern implementation.
"""
from abc import ABC, abstractmethod
from typing import List
from models.course import EnrollmentEvent

class NotificationObserver(ABC):
    """Observer interface."""
    @abstractmethod
    def update(self, event: EnrollmentEvent):
        pass

class WaitlistObserver(NotificationObserver):
    """Concrete observer for waitlist notifications."""
    def update(self, event: EnrollmentEvent):
        if event.type == "COURSE_DROPPED":
            course_id = event.payload.get("course_id")
            print(f"[Notification - WaitlistObserver] A seat has opened up in {course_id}! Alerting waitlist...")

class AdvisorObserver(NotificationObserver):
    """Concrete observer for academic advisor notifications."""
    def update(self, event: EnrollmentEvent):
        if event.type == "COURSE_DROPPED":
            student_id = event.payload.get("student_id")
            course_id = event.payload.get("course_id")
            print(f"[Notification - AdvisorObserver] Alert: Student {student_id} dropped course {course_id}.")

class AdminErrorObserver(NotificationObserver):
    """Concrete observer for system error notifications."""
    def update(self, event: EnrollmentEvent):
        if event.type == "SYSTEM_ERROR":
            error_msg = event.payload.get("message")
            print(f"[Notification - AdminErrorObserver] System Error: {error_msg}")

class EventPublisher:
    """The Subject/Publisher that maintains observers and broadcasts events."""
    def __init__(self):
        self.observers: List[NotificationObserver] = []
        
    def subscribe(self, o: NotificationObserver):
        self.observers.append(o)
        
    def unsubscribe(self, o: NotificationObserver):
        self.observers.remove(o)
        
    def publish(self, event: EnrollmentEvent):
        """Publishes an event to all registered observers."""
        for observer in self.observers:
            observer.update(event)

"""
Observer Pattern implementation.
As dictated by the System Design Report: The Observer Pattern is used to support 
event-driven notifications. The EventPublisher publishes events to WaitlistObserver, 
AdvisorObserver, and AdminErrorObserver.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class NotificationObserver(ABC):
    """Observer interface."""
    @abstractmethod
    def update(self, event_type: str, data: Dict[str, Any]):
        pass

class WaitlistObserver(NotificationObserver):
    """Concrete observer for waitlist notifications."""
    def update(self, event_type: str, data: Dict[str, Any]):
        if event_type == "COURSE_DROPPED":
            course_id = data.get("course_id")
            print(f"[Notification - WaitlistObserver] A seat has opened up in {course_id}! Alerting waitlist...")

class AdvisorObserver(NotificationObserver):
    """Concrete observer for academic advisor notifications."""
    def update(self, event_type: str, data: Dict[str, Any]):
        if event_type == "COURSE_DROPPED":
            student_id = data.get("student_id")
            course_id = data.get("course_id")
            print(f"[Notification - AdvisorObserver] Alert: Student {student_id} dropped course {course_id}.")

class AdminErrorObserver(NotificationObserver):
    """Concrete observer for system error notifications."""
    def update(self, event_type: str, data: Dict[str, Any]):
        if event_type == "SYSTEM_ERROR":
            error_msg = data.get("message")
            print(f"[Notification - AdminErrorObserver] System Error: {error_msg}")

class EventPublisher:
    """The Subject/Publisher that maintains observers and broadcasts events."""
    def __init__(self):
        self._observers: List[NotificationObserver] = []
        
    def register_observer(self, observer: NotificationObserver):
        self._observers.append(observer)
        
    def unregister_observer(self, observer: NotificationObserver):
        self._observers.remove(observer)
        
    def publish(self, event_type: str, data: Dict[str, Any]):
        """Publishes an event to all registered observers."""
        for observer in self._observers:
            observer.update(event_type, data)

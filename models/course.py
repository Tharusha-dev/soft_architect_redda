import datetime
import re

def check_time_conflict(sched1: str, sched2: str) -> bool:
    if sched1 == sched2: return True
    if sched1 == 'TBD' or sched2 == 'TBD': return False
    try:
        d1, t1 = sched1.split(' ', 1)
        d2, t2 = sched2.split(' ', 1)
        
        days1 = set(re.split(r'[/, ]+', d1))
        days2 = set(re.split(r'[/, ]+', d2))
        
        if not days1.intersection(days2):
            return False
            
        s1, e1 = t1.split('-')
        s2, e2 = t2.split('-')
        fmt = "%I:%M %p"
        st1 = datetime.datetime.strptime(s1.strip(), fmt)
        en1 = datetime.datetime.strptime(e1.strip(), fmt)
        st2 = datetime.datetime.strptime(s2.strip(), fmt)
        en2 = datetime.datetime.strptime(e2.strip(), fmt)
        return st1 < en2 and st2 < en1
    except:
        return False
"""
Models for NexusEnroll Courses.
"""
from typing import List, Any, Dict
from enum import Enum

class RequestStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class ValidationResult(Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"

class EnrollmentResult(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"

class DropResult(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"

class EnrollmentEvent:
    def __init__(self, type: str, payload: Dict[str, Any]):
        self.type = type
        self.payload = payload

class EnrollmentRequest:
    def __init__(self, student_id: str, course_id: str, student=None, course=None, offering=None, schedule=None, enrolled_schedules=None):
        self.student_id = student_id
        self.course_id = course_id
        self.student = student
        self.course = course
        self.offering = offering
        self.schedule = schedule
        self.enrolled_schedules = enrolled_schedules or []
        self.error_message = ""

class Enrollment:
    def __init__(self, student_id: str, course_id: str):
        self.student_id = student_id
        self.course_id = course_id

class Course:
    """Represents a course in NexusEnroll."""
    def __init__(self, course_id: str, name: str, description: str, instructor_id: str, capacity: int, schedule: str, department: str = "", days: str = "", start_time: str = "", end_time: str = ""):
        self.course_id = course_id
        self.name = name
        self.description = description
        self.instructor_id = instructor_id
        self.capacity = capacity
        self.schedule = schedule
        self.department = department
        self.days = days
        self.start_time = start_time
        self.end_time = end_time
        
        if self.schedule == 'TBD' and self.days and self.start_time and self.end_time:
            import datetime
            try:
                st = datetime.datetime.strptime(self.start_time, "%H:%M").strftime("%I:%M %p")
                en = datetime.datetime.strptime(self.end_time, "%H:%M").strftime("%I:%M %p")
                self.schedule = f"{self.days} {st} - {en}"
            except:
                pass
        self.prerequisites: List[str] = []
        import datetime
        self.schedule_history = [{"effective_date": "1970-01-01T00:00:00Z", "schedule": self.schedule}]
        
    def setSchedule(self, new_schedule: str):
        import datetime
        self.schedule = new_schedule
        self.schedule_history.append({"effective_date": datetime.datetime.now().isoformat(), "schedule": new_schedule})
        
    def setDescription(self, d: str):
        self.description = d

    def addPrerequisite(self, c: 'Course'):
        self.prerequisites.append(c.course_id)

    def setCapacity(self, n: int):
        self.capacity = n

class CourseOffering:
    def __init__(self, course_id: str, capacity: int):
        self.course_id = course_id
        self.capacity = capacity
        self.enrolled_count = 0
        self.waitlist = []

    def reserveSeat(self):
        if self.enrolled_count < self.capacity:
            self.enrolled_count += 1
            return True
        return False

    def releaseSeat(self):
        if self.enrolled_count > 0:
            self.enrolled_count -= 1

    def addToWaitlist(self, student_id: str):
        if student_id not in self.waitlist:
            self.waitlist.append(student_id)

class ScheduleEntry:
    def __init__(self, student_id: str, course_id: str):
        self.student_id = student_id
        self.course_id = course_id

class Schedule:
    def __init__(self):
        self.entries: List[ScheduleEntry] = []

    def addEntry(self, entry: ScheduleEntry):
        self.entries.append(entry)

    def removeEntry(self, entry: ScheduleEntry):
        self.entries = [e for e in self.entries if not (e.student_id == entry.student_id and e.course_id == entry.course_id)]

class EnrollmentRepository:
    def __init__(self):
        self.enrollments: List[Enrollment] = []

    def save(self, e: Enrollment):
        self.enrollments.append(e)

    def delete(self, e: Enrollment):
        self.enrollments = [enr for enr in self.enrollments if not (enr.student_id == e.student_id and enr.course_id == e.course_id)]

class DegreeProgram:
    def __init__(self, id: str, name: str, required_credits: int, required_courses: list):
        self.id = id
        self.name = name
        self.required_credits = required_credits
        self.required_courses = required_courses

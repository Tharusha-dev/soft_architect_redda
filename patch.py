import re

# 1. Update models/course.py
with open("models/course.py", "r") as f:
    course_content = f.read()

course_content = course_content.replace(
    "self.enrolled_count = 0",
    "self.enrolled_count = 0\n        self.waitlist = []"
)
course_content = course_content.replace(
    "    def releaseSeat(self):\n        if self.enrolled_count > 0:\n            self.enrolled_count -= 1",
    """    def releaseSeat(self):
        if self.enrolled_count > 0:
            self.enrolled_count -= 1

    def addToWaitlist(self, student_id: str):
        if student_id not in self.waitlist:
            self.waitlist.append(student_id)"""
)

course_content = course_content.replace(
    """class EnrollmentRequest:
    def __init__(self, student_id: str, course_id: str):
        self.student_id = student_id
        self.course_id = course_id""",
    """class EnrollmentRequest:
    def __init__(self, student_id: str, course_id: str, student=None, course=None, offering=None, schedule=None, enrolled_schedules=None):
        self.student_id = student_id
        self.course_id = course_id
        self.student = student
        self.course = course
        self.offering = offering
        self.schedule = schedule
        self.enrolled_schedules = enrolled_schedules or []"""
)

conflict_code = """
import datetime

def check_time_conflict(sched1: str, sched2: str) -> bool:
    if sched1 == sched2: return True
    try:
        d1, t1 = sched1.split(' ', 1)
        d2, t2 = sched2.split(' ', 1)
        if not set(d1.split('/')).intersection(set(d2.split('/'))):
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
course_content = conflict_code + course_content

degree_program_code = """
class DegreeProgram:
    def __init__(self, id: str, name: str, required_credits: int, required_courses: list):
        self.id = id
        self.name = name
        self.required_credits = required_credits
        self.required_courses = required_courses
"""
course_content += degree_program_code

with open("models/course.py", "w") as f:
    f.write(course_content)

# 2. Update patterns/chain_of_responsibility.py
with open("patterns/chain_of_responsibility.py", "r") as f:
    chain_content = f.read()

chain_content = chain_content.replace(
"""class PrerequisiteValidator(EnrollmentValidator):
    def validate(self, req: EnrollmentRequest) -> ValidationResult:
        # Simplistic proof-of-concept
        print(f"ValidationChain [Prerequisite]: Passed.")
        return self.forward(req)""",
"""class PrerequisiteValidator(EnrollmentValidator):
    def validate(self, req: EnrollmentRequest) -> ValidationResult:
        if req.student and req.course:
            for prereq in req.course.prerequisites:
                if prereq not in req.student.completed_courses:
                    print(f"ValidationChain [Prerequisite]: Failed. Missing {prereq}.")
                    return ValidationResult.FAILED
        print(f"ValidationChain [Prerequisite]: Passed.")
        return self.forward(req)"""
)

chain_content = chain_content.replace(
"""class CapacityValidator(EnrollmentValidator):
    def validate(self, req: EnrollmentRequest) -> ValidationResult:
        # Simplistic proof-of-concept
        print(f"ValidationChain [Capacity]: Passed.")
        return self.forward(req)""",
"""class CapacityValidator(EnrollmentValidator):
    def validate(self, req: EnrollmentRequest) -> ValidationResult:
        if req.offering and req.course:
            if req.offering.enrolled_count >= req.course.capacity:
                print(f"ValidationChain [Capacity]: Failed. Course is full.")
                # addToWaitlist happens in facade
                return ValidationResult.FAILED
        print(f"ValidationChain [Capacity]: Passed.")
        return self.forward(req)"""
)

chain_content = chain_content.replace(
"""class TimeConflictValidator(EnrollmentValidator):
    def validate(self, req: EnrollmentRequest) -> ValidationResult:
        print(f"ValidationChain [TimeConflict]: Passed. No time conflict detected.")
        return self.forward(req)""",
"""from models.course import check_time_conflict
class TimeConflictValidator(EnrollmentValidator):
    def validate(self, req: EnrollmentRequest) -> ValidationResult:
        if req.course and req.enrolled_schedules:
            for sched in req.enrolled_schedules:
                if check_time_conflict(req.course.schedule, sched):
                    print(f"ValidationChain [TimeConflict]: Failed. Conflict detected.")
                    return ValidationResult.FAILED
        print(f"ValidationChain [TimeConflict]: Passed. No time conflict detected.")
        return self.forward(req)"""
)

with open("patterns/chain_of_responsibility.py", "w") as f:
    f.write(chain_content)


# 3. Update patterns/facade.py
with open("patterns/facade.py", "r") as f:
    facade_content = f.read()

facade_content = facade_content.replace(
"""        req = EnrollmentRequest(studentId, offeringId)
        
        # 1. Coordinate Validation
        if self.validator.validate(req) == ValidationResult.FAILED:
            print("Facade: Enrollment failed due to validation errors.")
            return EnrollmentResult.FAILURE""",
"""        pass"""
)

facade_content = facade_content.replace(
"""    def enroll(self, studentId: str, offeringId: str) -> EnrollmentResult:
        \"\"\"Facade method to handle the enrollment workflow.\"\"\"
        print(f"Facade: Attempting to enroll {studentId} in offering {offeringId}...")
        
        pass
            
        # 2. Coordinate Persistence via Saga Orchestrator""",
"""    def enroll(self, req: EnrollmentRequest) -> EnrollmentResult:
        \"\"\"Facade method to handle the enrollment workflow.\"\"\"
        studentId = req.student_id
        offeringId = req.course_id
        print(f"Facade: Attempting to enroll {studentId} in offering {offeringId}...")
        
        if self.validator.validate(req) == ValidationResult.FAILED:
            print("Facade: Enrollment failed due to validation errors.")
            if req.offering and req.course and req.offering.enrolled_count >= req.course.capacity:
                req.offering.addToWaitlist(studentId)
                self.event_publisher.publish(EnrollmentEvent("WAITLIST_JOINED", {"student_id": studentId, "course_id": offeringId}))
            return EnrollmentResult.FAILURE
            
        # 2. Coordinate Persistence via Saga Orchestrator"""
)

facade_content = facade_content.replace(
"""    def drop(self, studentId: str, offeringId: str) -> DropResult:
        \"\"\"Facade method to handle the course dropping workflow.\"\"\"
        # Simple drop implementation for proof-of-concept
        self.offering.releaseSeat()
        self.repository.delete(Enrollment(studentId, offeringId))
        self.schedule.removeEntry(ScheduleEntry(studentId, offeringId))
        
        # Event publication
        self.event_publisher.publish(EnrollmentEvent("COURSE_DROPPED", {"student_id": studentId, "course_id": offeringId}))
        return DropResult.SUCCESS""",
"""    def drop(self, studentId: str, offeringId: str) -> DropResult:
        \"\"\"Facade method to handle the course dropping workflow.\"\"\"
        self.offering.releaseSeat()
        self.repository.delete(Enrollment(studentId, offeringId))
        self.schedule.removeEntry(ScheduleEntry(studentId, offeringId))
        
        self.event_publisher.publish(EnrollmentEvent("COURSE_DROPPED", {"student_id": studentId, "course_id": offeringId}))
        
        # Waitlist handling
        if self.offering.waitlist:
            next_student = self.offering.waitlist.pop(0)
            self.event_publisher.publish(EnrollmentEvent("WAITLIST_PROMOTED", {"student_id": next_student, "course_id": offeringId}))
            
        return DropResult.SUCCESS"""
)

with open("patterns/facade.py", "w") as f:
    f.write(facade_content)


# 4. Update api.py to populate EnrollmentRequest and call facade.enroll(req)
with open("api.py", "r") as f:
    api_content = f.read()

# Replace manual validation in APIStudentService
api_content = api_content.replace(
"""        for prereq in course.prerequisites:
            if prereq not in student.completed_courses:
                return EnrollmentResult.FAILURE
                
        if offerings[course_id].enrolled_count >= course.capacity:
            return EnrollmentResult.FAILURE

        result = facade.enroll(student_id, str(course_id))""",
"""        enrolled_schedules = [c.schedule for c in courses_data if c.course_id in student.enrolled_courses]
        from models.course import EnrollmentRequest
        req = EnrollmentRequest(student_id, course_id, student, course, offerings[course_id], schedule, enrolled_schedules)
        result = facade.enroll(req)"""
)

with open("api.py", "w") as f:
    f.write(api_content)


# 5. Update services/admin_service.py for Course/Program CRUD
with open("services/admin_service.py", "r") as f:
    admin_content = f.read()

admin_content = admin_content.replace(
"""    def __init__(self):
        self.pending_course_requests: List[CourseChangeRequest] = []""",
"""    def __init__(self):
        self.pending_course_requests: List[CourseChangeRequest] = []
        self.courses = []
        self.users = []
        self.programs = []
        
    def create_course(self, course):
        self.courses.append(course)
        print(f"AdminService: Course {course.course_id} created.")
        
    def delete_course(self, course_id: str):
        self.courses = [c for c in self.courses if c.course_id != course_id]
        print(f"AdminService: Course {course_id} deleted.")
        
    def add_user(self, user):
        self.users.append(user)
        print(f"AdminService: User {user.name} added.")
        
    def deactivate_user(self, user_id: str):
        for u in self.users:
            if u.id == user_id:
                if hasattr(u, 'deactivate'):
                    u.deactivate()
                    print(f"AdminService: User {user_id} deactivated.")
                    
    def define_program(self, program):
        self.programs.append(program)
        print(f"AdminService: Degree Program {program.id} defined.")"""
)
with open("services/admin_service.py", "w") as f:
    f.write(admin_content)


# 6. Update models/user.py for User Deactivation
with open("models/user.py", "r") as f:
    user_content = f.read()

user_content = user_content.replace(
"""class User(ABC):
    \"\"\"Abstract base class representing a NexusEnroll user.\"\"\"
    def __init__(self, id: str, name: str, email: str):
        self._id = id
        self._name = name
        self._email = email""",
"""class User(ABC):
    \"\"\"Abstract base class representing a NexusEnroll user.\"\"\"
    def __init__(self, id: str, name: str, email: str):
        self._id = id
        self._name = name
        self._email = email
        self.is_active = True
        
    def deactivate(self):
        self.is_active = False
        
    def reactivate(self):
        self.is_active = True"""
)
with open("models/user.py", "w") as f:
    f.write(user_content)

print("Patching complete.")

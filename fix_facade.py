import re

# Fix facade.py
with open("patterns/facade.py", "r") as f:
    facade_content = f.read()

facade_content = facade_content.replace(
"""    def __init__(self, event_publisher: EventPublisher, offering: CourseOffering, repository: EnrollmentRepository, schedule: Schedule):
        self.validator = ValidationChain()
        self.event_publisher = event_publisher
        self.offering = offering
        self.repository = repository
        self.schedule = schedule""",
"""    def __init__(self, event_publisher: EventPublisher, offering: CourseOffering, repository: EnrollmentRepository, schedule: Schedule, course_repository=None, user_repository=None, offerings=None):
        self.validator = ValidationChain()
        self.event_publisher = event_publisher
        self.offering = offering
        self.repository = repository
        self.schedule = schedule
        self.course_repository = course_repository
        self.user_repository = user_repository
        self.offerings = offerings"""
)

facade_content = facade_content.replace(
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
            return EnrollmentResult.FAILURE""",
"""    def enroll(self, studentId: str, offeringId: str) -> EnrollmentResult:
        \"\"\"Facade method to handle the enrollment workflow.\"\"\"
        print(f"Facade: Attempting to enroll {studentId} in offering {offeringId}...")
        
        student = self.user_repository.get(studentId) if self.user_repository else None
        course = self.course_repository.get(offeringId) if self.course_repository else None
        
        # Build enrolled schedules context
        enrolled_schedules = []
        if student and self.course_repository:
            for c_id in student.enrolled_courses:
                c = self.course_repository.get(c_id)
                if c:
                    enrolled_schedules.append(c.schedule)
                    
        req = EnrollmentRequest(studentId, offeringId, student, course, self.offering, self.schedule, enrolled_schedules)
        
        if self.validator.validate(req) == ValidationResult.FAILED:
            print("Facade: Enrollment failed due to validation errors.")
            if self.offering and course and self.offering.enrolled_count >= course.capacity:
                self.offering.addToWaitlist(studentId)
                self.event_publisher.publish(EnrollmentEvent("WAITLIST_JOINED", {"student_id": studentId, "course_id": offeringId}))
            return EnrollmentResult.FAILURE"""
)
with open("patterns/facade.py", "w") as f:
    f.write(facade_content)


# Fix api.py
with open("api.py", "r") as f:
    api_content = f.read()

# Restore enroll parameters in APIStudentService
api_content = api_content.replace(
"""        enrolled_schedules = [c.schedule for c in courses_data if c.course_id in student.enrolled_courses]
        from models.course import EnrollmentRequest
        req = EnrollmentRequest(student_id, course_id, student, course, offerings[course_id], schedule, enrolled_schedules)
        result = facade.enroll(req)""",
"""        result = facade.enroll(student_id, str(course_id))"""
)

# Restore manual validation block since we reverted facade calls
api_content = api_content.replace(
"""
req1 = EnrollmentRequest(s1.id, "2", s1, courses_data[1], offerings["2"], schedule, [c.schedule for c in courses_data if c.course_id in s1.enrolled_courses])
facades["2"].enroll(req1)
req2 = EnrollmentRequest(s2.id, "2", s2, courses_data[1], offerings["2"], schedule, [c.schedule for c in courses_data if c.course_id in s2.enrolled_courses])
facades["2"].enroll(req2)
req3 = EnrollmentRequest(s3.id, "2", s3, courses_data[1], offerings["2"], schedule, [c.schedule for c in courses_data if c.course_id in s3.enrolled_courses])
facades["2"].enroll(req3)
""",
"""facades["2"].enroll(s1.id, "2")
facades["2"].enroll(s2.id, "2")
facades["2"].enroll(s3.id, "2")"""
)

# Inject repositories into Facade initialization in api.py
api_content = api_content.replace(
"""facades = {}
for cid, offering in offerings.items():
    es = EnrollmentService(event_publisher, offering, repository, schedule)
    facades[cid] = es.get_facade()""",
"""
class DummyCourseRepo:
    def get(self, cid):
        return next((c for c in courses_data if c.course_id == str(cid)), None)

class DummyUserRepo:
    def get(self, uid):
        return next((s for s in [s1, s2, s3, s4, f1] if s.id == str(uid)), None)

course_repo = DummyCourseRepo()
user_repo = DummyUserRepo()

facades = {}
for cid, offering in offerings.items():
    facade = EnrollmentFacade(event_publisher, offering, repository, schedule, course_repo, user_repo, offerings)
    facades[cid] = facade
"""
)

with open("api.py", "w") as f:
    f.write(api_content)
    
# Fix student.enrolled_courses in models/user.py for api mock user repo
with open("models/user.py", "r") as f:
    user_content = f.read()

user_content = user_content.replace(
"""class Student(User):
    \"\"\"Represents a student user in the NexusEnroll system.\"\"\"
    def __init__(self, id: str, name: str, email: str):
        super().__init__(id, name, email)
        self.completed_courses: Dict[str, str] = {}""",
"""class Student(User):
    \"\"\"Represents a student user in the NexusEnroll system.\"\"\"
    def __init__(self, id: str, name: str, email: str):
        super().__init__(id, name, email)
        self.completed_courses: Dict[str, str] = {}
        self.enrolled_courses = []"""
)
with open("models/user.py", "w") as f:
    f.write(user_content)

print("Facade fix complete.")

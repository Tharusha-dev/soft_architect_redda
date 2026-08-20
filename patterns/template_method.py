"""
Template Method Pattern implementation.
"""
from abc import ABC, abstractmethod

class ReportData:
    def __init__(self, data):
        self.data = data

class Report:
    def __init__(self, content: str):
        self.content = content

class ReportGenerator(ABC):
    """Abstract class defining the Template Method."""
    def generateReport(self) -> Report:
        """The Template Method orchestrating the reporting workflow. Final."""
        d = self.collectData()
        self.processData(d)
        return self.formatReport(d)
        
    @abstractmethod
    def collectData(self) -> ReportData:
        pass
        
    @abstractmethod
    def processData(self, d: ReportData):
        pass
        
    @abstractmethod
    def formatReport(self, d: ReportData) -> Report:
        pass

class EnrollmentStatisticsReport(ReportGenerator):
    """Concrete report for enrollment statistics."""
    def __init__(self, courses_data, offerings_data):
        self.courses_data = courses_data
        self.offerings_data = offerings_data

    def collectData(self) -> ReportData:
        data = {}
        for c in self.courses_data:
            off = self.offerings_data.get(c.course_id)
            if off:
                data[c.course_id] = off.enrolled_count
        return ReportData(data)
        
    def processData(self, d: ReportData):
        total = sum(d.data.values())
        d.processed_data = f"Total University Enrollment: {total} students across {len(d.data)} courses."
        
    def formatReport(self, d: ReportData) -> Report:
        return Report(f"\n--- Automated System Report ---\n{d.processed_data}\n-------------------------------\n")

class InstructureWorkloadReport(ReportGenerator):
    """Concrete report for instructure workload."""
    def __init__(self, courses_data, all_users):
        self.courses_data = courses_data
        self.all_users = all_users

    def collectData(self) -> ReportData:
        data = {}
        for c in self.courses_data:
            inst = getattr(c, 'instructor_id', None)
            if inst:
                data[inst] = data.get(inst, 0) + 1
        return ReportData(data)
        
    def processData(self, d: ReportData):
        report = "Instructor Workload Analysis:\n"
        for inst, count in d.data.items():
            inst_obj = next((u for u in self.all_users if u.id == inst), None)
            name = getattr(inst_obj, '_name', inst)
            report += f" - {name} ({inst}): {count} active courses\n"
        d.processed_data = report
        
    def formatReport(self, d: ReportData) -> Report:
        return Report(f"\n--- Automated System Report ---\n{d.processed_data}\n-------------------------------\n")

class CoursePopularityReport(ReportGenerator):
    """Concrete report for course popularity trends."""
    def __init__(self, courses_data, offerings_data):
        self.courses_data = courses_data
        self.offerings_data = offerings_data

    def collectData(self) -> ReportData:
        data = []
        for c in self.courses_data:
            off = self.offerings_data.get(c.course_id)
            if off:
                data.append((c.course_id, off.enrolled_count, len(getattr(off, 'waitlist', []))))
        return ReportData(data)
        
    def processData(self, d: ReportData):
        sorted_courses = sorted(d.data, key=lambda x: x[1] + x[2], reverse=True)
        report = "Course Popularity Ranking (Based on Demand):\n"
        for i, (course, enrolled, waitlisted) in enumerate(sorted_courses, 1):
            report += f" {i}. {course} (Enrolled: {enrolled}, Waitlisted: {waitlisted})\n"
        d.processed_data = report
        
    def formatReport(self, d: ReportData) -> Report:
        return Report(f"\n--- Automated System Report ---\n{d.processed_data}\n-------------------------------\n")

class HighCapacityReport(ReportGenerator):
    """Concrete report for courses at high capacity based on parameters."""
    def __init__(self, department: str, threshold: int, courses_data: list, offerings_data: dict):
        self.department = department
        self.threshold = threshold
        self.courses_data = courses_data
        self.offerings_data = offerings_data

    def collectData(self) -> ReportData:
        data = []
        for c in self.courses_data:
            if getattr(c, 'department', '') == self.department:
                off = self.offerings_data.get(c.course_id)
                if off:
                    pct = (off.enrolled_count / c.capacity) * 100 if c.capacity > 0 else 0
                    if pct >= self.threshold:
                        data.append((c.course_id, c.name, off.enrolled_count, c.capacity, pct))
        return ReportData(data)
        
    def processData(self, d: ReportData):
        if not d.data:
            d.processed_data = f"No courses in '{self.department}' meet the {self.threshold}% capacity threshold."
            return
        report = f"High-Capacity Courses ({self.department} @ >= {self.threshold}%):\n"
        for (cid, name, enrolled, cap, pct) in d.data:
            report += f" - {cid} {name}: {enrolled}/{cap} ({pct:.1f}%)\n"
        d.processed_data = report
        
    def formatReport(self, d: ReportData) -> Report:
        return Report(f"\n--- Automated System Report ---\n{d.processed_data}\n-------------------------------\n")

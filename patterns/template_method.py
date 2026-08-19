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
    def collectData(self) -> ReportData:
        return ReportData({"CS101": 150, "MATH201": 80, "PHYS101": 120})
        
    def processData(self, d: ReportData):
        total = sum(d.data.values())
        d.processed_data = f"Total University Enrollment: {total} students across {len(d.data)} courses."
        
    def formatReport(self, d: ReportData) -> Report:
        return Report(f"\n--- Automated System Report ---\n{d.processed_data}\n-------------------------------\n")

class InstructureWorkloadReport(ReportGenerator):
    """Concrete report for instructure workload."""
    def collectData(self) -> ReportData:
        return ReportData({"Prof. Alan Turing": 3, "Prof. Ada Lovelace": 2})
        
    def processData(self, d: ReportData):
        report = "Instructure Workload Analysis:\n"
        for instructure, courses in d.data.items():
            report += f" - {instructure}: {courses} active courses\n"
        d.processed_data = report
        
    def formatReport(self, d: ReportData) -> Report:
        return Report(f"\n--- Automated System Report ---\n{d.processed_data}\n-------------------------------\n")

class CoursePopularityReport(ReportGenerator):
    """Concrete report for course popularity trends."""
    def collectData(self) -> ReportData:
        # Format: (CourseID, Enrolled, Waitlisted)
        return ReportData([("CS101", 150, 50), ("MATH201", 80, 5), ("HIST101", 30, 0)])
        
    def processData(self, d: ReportData):
        sorted_courses = sorted(d.data, key=lambda x: x[1] + x[2], reverse=True)
        report = "Course Popularity Ranking (Based on Demand):\n"
        for i, (course, enrolled, waitlisted) in enumerate(sorted_courses, 1):
            report += f" {i}. {course} (Enrolled: {enrolled}, Waitlisted: {waitlisted})\n"
        d.processed_data = report
        
    def formatReport(self, d: ReportData) -> Report:
        return Report(f"\n--- Automated System Report ---\n{d.processed_data}\n-------------------------------\n")

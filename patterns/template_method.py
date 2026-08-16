"""
Template Method Pattern implementation.
As dictated by the System Design Report: The Template Method Pattern is used in the 
Reporting Service to generate administrator reports using a consistent processing workflow.
"""
from abc import ABC, abstractmethod

class ReportGenerator(ABC):
    """Abstract class defining the Template Method."""
    def generate_report(self):
        """The Template Method orchestrating the reporting workflow."""
        data = self.collect_data()
        processed_data = self.process_data(data)
        self.format_report(processed_data)
        
    @abstractmethod
    def collect_data(self):
        """Step 1: Collect required data."""
        pass
        
    @abstractmethod
    def process_data(self, data):
        """Step 2: Process the collected data."""
        pass
        
    def format_report(self, processed_data):
        """Step 3: Format and output the final report."""
        print(f"\n--- Automated System Report ---")
        print(processed_data)
        print("-------------------------------\n")

class EnrollmentStatisticsReport(ReportGenerator):
    """Concrete report for enrollment statistics."""
    def collect_data(self):
        return {"CS101": 150, "MATH201": 80, "PHYS101": 120}
        
    def process_data(self, data):
        total = sum(data.values())
        return f"Total University Enrollment: {total} students across {len(data)} courses."

class FacultyWorkloadReport(ReportGenerator):
    """Concrete report for faculty workload."""
    def collect_data(self):
        return {"Prof. Alan Turing": 3, "Prof. Ada Lovelace": 2}
        
    def process_data(self, data):
        report = "Faculty Workload Analysis:\n"
        for faculty, courses in data.items():
            report += f" - {faculty}: {courses} active courses\n"
        return report

class CoursePopularityReport(ReportGenerator):
    """Concrete report for course popularity trends."""
    def collect_data(self):
        # Format: (CourseID, Enrolled, Waitlisted)
        return [("CS101", 150, 50), ("MATH201", 80, 5), ("HIST101", 30, 0)]
        
    def process_data(self, data):
        sorted_courses = sorted(data, key=lambda x: x[1] + x[2], reverse=True)
        report = "Course Popularity Ranking (Based on Demand):\n"
        for i, (course, enrolled, waitlisted) in enumerate(sorted_courses, 1):
            report += f" {i}. {course} (Enrolled: {enrolled}, Waitlisted: {waitlisted})\n"
        return report

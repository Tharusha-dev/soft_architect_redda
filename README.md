# NexusEnroll - Advanced University Enrollment System

A comprehensive Python-based university enrollment system demonstrating advanced software architecture, RESTful API integration, and modern frontend development. The project features a robust core engine built entirely around 7 distinct GoF Design Patterns.

## Team Members

| Name | Index Number |
| :--- | :--- |
| [Member 1 Name] | [Index 1] |
| [Member 2 Name] | [Index 2] |
| [Member 3 Name] | [Index 3] |
| [Member 4 Name] | [Index 4] |
| [Member 5 Name] | [Index 5] |
| [Member 6 Name] | [Index 6] |

## Design Patterns Implemented

1. **Factory Method Pattern**
   - **Location:** `patterns/factory.py`
   - **Justification:** Centralizes the instantiation logic for various user roles (`Student`, `Faculty`, `Administrator`).
   - **Benefits:** Follows the Open/Closed Principle. Allows seamless introduction of new user types without modifying existing user creation flows.

2. **Facade Pattern**
   - **Location:** `patterns/facade.py`
   - **Justification:** Provides a simplified, unified interface for complex sub-systems (validation, persistence, schedules).
   - **Benefits:** Hides the complexity of transactional enrollments and microservice interactions from the client.

3. **Observer Pattern**
   - **Location:** `patterns/observer.py` and `services/notification_service.py`
   - **Justification:** Enables a highly decoupled event-driven architecture for system notifications (e.g., successful enrollment, dropping a course).
   - **Benefits:** Listeners (like `EmailNotifier` or `SMSNotifier`) can subscribe to events dynamically without mutating the core enrollment services.

4. **Chain of Responsibility Pattern**
   - **Location:** `patterns/chain_of_responsibility.py`
   - **Justification:** Processes complex validation rules sequentially (Prerequisites -> Capacity -> Time Conflicts).
   - **Benefits:** Promotes Single Responsibility. Each validator only cares about its specific rule. New validation logic can be plugged into the chain dynamically.

5. **Command Pattern**
   - **Location:** `patterns/command.py`
   - **Justification:** Encapsulates system operations (like changing course capacities or transactional enrollment logic via the Saga Orchestrator).
   - **Benefits:** Allows requests to be queued, executed securely by administrators, or rolled back in case of failure.

6. **State Pattern**
   - **Location:** `patterns/state.py`
   - **Justification:** Manages the lifecycle of Faculty Grade Submissions (Draft -> Pending -> Approved/Rejected).
   - **Benefits:** Eliminates massive `if/else` conditional blocks. Submissions automatically alter their behavior and transition based on their internal state.

7. **Template Method Pattern**
   - **Location:** `patterns/template_method.py`
   - **Justification:** Defines the skeleton of report generation algorithms (Analytics, Workload, Popularity) while letting subclasses implement specific data-gathering steps.
   - **Benefits:** Promotes code reuse (DRY) by centralizing the standard report formatting structure.

## Architecture

The system is decoupled into logical tiers:
- **Models:** Domain objects representing Users and Courses.
- **Patterns:** Core behavioral and structural GoF design pattern implementations.
- **Services:** High-level business logic orchestrating the domain (Student, Faculty, Admin, Notification Services).
- **API Layer (`api.py`):** Flask REST API exposing the core engine to web clients.
- **Frontend (`frontend/`):** A modern, responsive HTML/JS interface hooked to the API.

## Project Structure

```text
NexusEnroll/
├── main.py                     # CLI simulation entry point
├── api.py                      # RESTful Flask API backend
├── requirements.txt            # Python dependencies
├── models/
│   ├── user.py                 # User classes (Student, Faculty, Administrator)
│   └── course.py               # Course & Enrollment domain models
├── patterns/
│   ├── factory.py              # Factory Method
│   ├── facade.py               # Facade Pattern
│   ├── observer.py             # Observer Pattern
│   ├── chain_of_responsibility.py # Chain of Responsibility
│   ├── command.py              # Command Pattern
│   ├── state.py                # State Pattern
│   └── template_method.py      # Template Method
├── services/
│   ├── student_service.py      # Student business logic
│   ├── faculty_service.py      # Faculty business logic
│   ├── admin_service.py        # Admin business logic
│   └── notification_service.py # Notification service
└── frontend/
    ├── index.html              # Web Application UI
    ├── app.js                  # Frontend state management & logic
    └── styles.css              # Custom UI styling
```

## How to Run

### Prerequisites
Make sure you have Python 3 installed. Install the necessary dependencies from the `requirements.txt` file.

```bash
# Install required Python packages (Flask, Flask-CORS)
pip install -r requirements.txt
```

### 1. Run the CLI Simulation (Core Testing)
To test the core business logic, design patterns, and output traces directly in the terminal without a web interface, run:
```bash
python main.py
```

### 2. Run the Full Web Application
To run the complete system with the frontend interface:

**Step A: Start the Backend API Server**
```bash
# In the project root directory
python3 api.py
```
*(The API will start running locally on `http://localhost:5000`)*

**Step B: Launch the Web Frontend**
You can launch the frontend using any local HTTP server (or simply open the HTML file directly in your browser). To use Python's built-in server:
```bash
# In a new terminal, navigate to the frontend directory
cd frontend
python3 -m http.server 8000
```
Open your web browser and navigate to `http://localhost:8000` (or the port specified in your terminal).

## Key Features Demonstrated

- **Interactive Role-Based Access:** Instantly swap between Student, Faculty, and Admin interfaces.
- **Real-Time Data Syncing:** Form submissions (like grading or capacity requests) flow perfectly from the UI into the backend GoF patterns.
- **Granular Validations:** The Chain of Responsibility pattern silently protects the enrollment pipeline.
- **Automated Alerts:** The Admin dashboard dynamically generates HTML warnings by computing raw capacity statistics in real-time.
- **State-Driven Approvals:** Faculty can submit row-level grades that lock into a "Pending" State Pattern until explicitly approved by the Administration.

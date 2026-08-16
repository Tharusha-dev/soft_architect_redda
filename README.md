# NexusEnroll Core Business Logic Simulation

This repository contains the core business logic implementation for the **NexusEnroll** system, demonstrating the architectural decisions and design patterns outlined in the `System Design Report`.

## Architecture & Patterns

The codebase is structured to reflect a microservices-inspired architecture adapted into a cohesive Python application. It applies SOLID, DRY, and KISS principles to ensure high cohesion and loose coupling.

The 7 required design patterns are perfectly integrated:
1. **Factory Method (`patterns/factory.py`)**: `UserCreator` and its subclasses to instantiate `Student`, `Faculty`, and `Administrator` objects.
2. **Facade (`patterns/facade.py`)**: `EnrollmentFacade` coordinates validation, transaction logic, and event publication for enrollments.
3. **Chain of Responsibility (`patterns/chain_of_responsibility.py`)**: `ValidationChain` checks prerequisites, capacity, and time conflicts before enrollment.
4. **Observer (`patterns/observer.py`)**: `EventPublisher` notifies `WaitlistObserver`, `AdvisorObserver`, and `AdminErrorObserver` based on system events.
5. **State (`patterns/state.py`)**: Manages the `GradeSubmission` lifecycle through `DraftState`, `PendingState`, and `SubmittedState`.
6. **Command (`patterns/command.py`)**: Encapsulates `CourseChangeRequest` operations like `ChangeCapacityCommand`, which can be executed or undone.
7. **Template Method (`patterns/template_method.py`)**: `ReportGenerator` standardizes the algorithm for gathering, processing, and formatting analytical reports.

## Running the Simulation

The `main.py` file contains a rich simulation showcasing these use cases with dummy data.

```bash
python3 main.py
```

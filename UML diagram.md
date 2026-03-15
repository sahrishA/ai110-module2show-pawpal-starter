classDiagram
    class Owner {
        +name: str
        +preferences: dict
        +add_pet(pet: Pet)
        +get_pets() list[Pet]
    }

    class Pet {
        +name: str
        +species: str
        +owner: Owner
        +add_task(task: Task)
        +get_tasks() list[Task]
    }

    class Task {
        +title: str
        +duration_minutes: int
        +priority: str
        +pet: Pet
    }

    class ScheduledTask {
        +task: Task
        +start_time: datetime
        +end_time: datetime
    }

    class Schedule {
        +scheduled_tasks: list[ScheduledTask]
        +date: date
        +add_scheduled_task(scheduled_task: ScheduledTask)
        +get_total_duration() int
    }

    class Scheduler {
        +schedule_day(owner: Owner, pet: Pet, tasks: list[Task]) Schedule
    }

    Owner ||--o{ Pet : owns
    Pet ||--o{ Task : has
    Task ||--|| ScheduledTask : scheduled as
    Schedule ||--o{ ScheduledTask : contains
    Scheduler ..> Schedule : creates
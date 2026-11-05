# Workout Application Backend

## Project Description

This is a REST API built with Python and Flask. It allows users to create and manage workouts and exercises. Users can also add exercises to workouts and record the number of sets, repetitions and duration.

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-Migrate
- SQLite
- Marshmallow

## Installation

Clone the repository and enter the project directory.

```bash
pipenv install
```

## Database Setup

Run database migrations:

```bash
pipenv run flask --app run.py db migrate -m "Create workout database tables"
pipenv run flask --app run.py db upgrade
```

## Seed the Database

```bash
pipenv run python -m server.seed
```

## Run the Application

```bash
pipenv run python run.py
```

The application runs at:

`http://127.0.0.1:5000`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/workouts` | Get all workouts |
| GET | `/workouts/<id>` | Get one workout |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<id>` | Delete a workout |
| GET | `/exercises` | Get all exercises |
| GET | `/exercises/<id>` | Get one exercise |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<id>` | Delete an exercise |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout |

## Database Relationships

The Workout model has a one-to-many relationship with WorkoutExercise.

The Exercise model also has a one-to-many relationship with WorkoutExercise.

Workout and Exercise have a many-to-many relationship through the WorkoutExercise association model.

WorkoutExercise stores the sets, reps and duration for each exercise in a workout.

## Validation and Constraints

The application uses Marshmallow schemas to validate incoming data.

SQLAlchemy model validations check values before saving them.

Database constraints protect the database against invalid values, duplicate exercises in the same workout and missing required fields.

## Project Structure

```text
server/
    models/
    schemas/
    __init__.py
    extensions.py
    routes.py
    seed.py

migrations/
instance/
README.md
run.py
Pipfile
Pipfile.lock
```
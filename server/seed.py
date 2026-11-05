from datetime import date

from server import create_app
from server.extensions import db
from server.models import Workout, Exercise, WorkoutExercise


app = create_app()


def seed_database():
    with app.app_context():
        exercises_data = [
            {
                "name": "Push-ups",
                "category": "Strength",
                "equipment_needed": False
            },
            {
                "name": "Squats",
                "category": "Strength",
                "equipment_needed": False
            },
            {
                "name": "Plank",
                "category": "Core",
                "equipment_needed": False
            },
            {
                "name": "Bench Press",
                "category": "Strength",
                "equipment_needed": True
            }
        ]

        exercises = []

        for item in exercises_data:
            exercise = Exercise.query.filter_by(
                name=item["name"]
            ).first()

            if exercise is None:
                exercise = Exercise(**item)
                db.session.add(exercise)

            exercises.append(exercise)

        db.session.commit()

        workout = Workout.query.filter_by(
            notes="Sample workout"
        ).first()

        if workout is None:
            workout = Workout(
                date=date.today(),
                duration_minutes=45,
                notes="Sample workout"
            )

            db.session.add(workout)
            db.session.commit()

        workout_exercises = [
            (exercises[0], 3, 15, 0),
            (exercises[1], 4, 12, 0),
            (exercises[2], 3, 1, 60)
        ]

        for exercise, sets, reps, duration in workout_exercises:
            existing = WorkoutExercise.query.filter_by(
                workout_id=workout.id,
                exercise_id=exercise.id
            ).first()

            if existing is None:
                association = WorkoutExercise(
                    workout=workout,
                    exercise=exercise,
                    sets=sets,
                    reps=reps,
                    duration_seconds=duration
                )

                db.session.add(association)

        db.session.commit()

        print("Database seeded successfully!")


if __name__ == "__main__":
    seed_database()
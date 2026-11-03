from datetime import date

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates

from server.extensions import db


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "duration_minutes > 0",
            name="check_workout_duration_positive"
        ),
    )

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )

    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        viewonly=True
    )

    @validates("duration_minutes")
    def validate_duration(self, key, duration):
        if not isinstance(duration, int) or duration <= 0:
            raise ValueError("Workout duration must be a positive integer.")
        return duration

    @validates("date")
    def validate_date(self, key, workout_date):
        if not isinstance(workout_date, date):
            raise ValueError("Workout date must be a valid date.")
        return workout_date

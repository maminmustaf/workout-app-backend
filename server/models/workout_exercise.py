from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import validates

from server.extensions import db


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(
        db.Integer,
        db.ForeignKey("workouts.id"),
        nullable=False
    )

    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id"),
        nullable=False
    )

    reps = db.Column(db.Integer, nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    duration_seconds = db.Column(db.Integer, nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint(
            "workout_id",
            "exercise_id",
            name="unique_exercise_per_workout"
        ),
        CheckConstraint("reps > 0", name="check_reps_positive"),
        CheckConstraint("sets > 0", name="check_sets_positive"),
        CheckConstraint(
            "duration_seconds >= 0",
            name="check_duration_nonnegative"
        ),
    )

    workout = db.relationship(
        "Workout",
        back_populates="workout_exercises"
    )

    exercise = db.relationship(
        "Exercise",
        back_populates="workout_exercises"
    )

    @validates("reps", "sets")
    def validate_positive_values(self, key, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{key.capitalize()} must be a positive integer.")

        return value

    @validates("duration_seconds")
    def validate_duration(self, key, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Duration must be a non-negative integer.")

        return value

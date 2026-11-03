from sqlalchemy.orm import validates

from server.extensions import db


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(100), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )

    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        viewonly=True
    )

    @validates("name", "category")
    def validate_text_fields(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key.capitalize()} cannot be empty.")

        return value.strip()

    @validates("equipment_needed")
    def validate_equipment(self, key, value):
        if not isinstance(value, bool):
            raise ValueError("Equipment needed must be True or False.")

        return value

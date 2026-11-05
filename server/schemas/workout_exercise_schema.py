from marshmallow import Schema, fields, validate

from server.schemas.exercise_schema import ExerciseSchema


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)

    reps = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )

    sets = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )

    duration_seconds = fields.Int(
        load_default=0,
        validate=validate.Range(min=0)
    )

    exercise = fields.Nested(ExerciseSchema, dump_only=True)
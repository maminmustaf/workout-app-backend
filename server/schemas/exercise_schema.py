from marshmallow import Schema, fields, validate


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100)
    )

    category = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100)
    )

    equipment_needed = fields.Boolean(load_default=False)
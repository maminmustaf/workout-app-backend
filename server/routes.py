from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from server.extensions import db
from server.models import Workout, Exercise, WorkoutExercise

from server.schemas.workout_schema import WorkoutSchema
from server.schemas.exercise_schema import ExerciseSchema
from server.schemas.workout_exercise_schema import WorkoutExerciseSchema


api = Blueprint("api", __name__)

workout_schema = WorkoutSchema()
exercise_schema = ExerciseSchema()
workout_exercise_schema = WorkoutExerciseSchema()


def serialize_workout(workout):
    data = workout_schema.dump(workout)

    data["workout_exercises"] = workout_exercise_schema.dump(
        workout.workout_exercises,
        many=True
    )

    return data


# WORKOUT ENDPOINTS

@api.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()

    return jsonify({
        "workouts": [serialize_workout(w) for w in workouts],
        "count": len(workouts)
    }), 200


@api.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return jsonify({"error": "Workout not found"}), 404

    return jsonify(serialize_workout(workout)), 200


@api.route("/workouts", methods=["POST"])
def create_workout():
    try:
        data = workout_schema.load(request.get_json() or {})

        workout = Workout(**data)

        db.session.add(workout)
        db.session.commit()

        return jsonify({
            "message": "Workout created successfully",
            "workout": serialize_workout(workout)
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "error": "This exercise is already added to this workout."
        }), 400

    except ValueError as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400


@api.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return jsonify({"error": "Workout not found"}), 404

    db.session.delete(workout)
    db.session.commit()

    return jsonify({
        "message": "Workout deleted successfully"
    }), 200


# EXERCISE ENDPOINTS

@api.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()

    return jsonify({
        "exercises": exercise_schema.dump(exercises, many=True),
        "count": len(exercises)
    }), 200


@api.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404

    return jsonify(exercise_schema.dump(exercise)), 200


@api.route("/exercises", methods=["POST"])
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json() or {})

        exercise = Exercise(**data)

        db.session.add(exercise)
        db.session.commit()

        return jsonify({
            "message": "Exercise created successfully",
            "exercise": exercise_schema.dump(exercise)
        }), 201

    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    except (ValueError, IntegrityError) as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400


@api.route("/exercises/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404

    db.session.delete(exercise)
    db.session.commit()

    return jsonify({
        "message": "Exercise deleted successfully"
    }), 200


# WORKOUT-EXERCISE ASSOCIATION ENDPOINT

@api.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"]
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)

    if workout is None:
        return jsonify({"error": "Workout not found"}), 404

    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404

    try:
        data = workout_exercise_schema.load(request.get_json() or {})

        workout_exercise = WorkoutExercise(
            workout=workout,
            exercise=exercise,
            **data
        )

        db.session.add(workout_exercise)
        db.session.commit()

        return jsonify({
            "message": "Exercise added to workout successfully",
            "workout_exercise": workout_exercise_schema.dump(
                workout_exercise
            )
        }), 201

    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    except (ValueError, IntegrityError) as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400
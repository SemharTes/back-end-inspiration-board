from app import db
from app.models.board import Board
from flask import Blueprint, request, jsonify, make_response, abort


boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

# validate_model
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"invalid model id {model_id}"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"model id {model_id} not found"}, 404))
    
    return model

# get all boards
@boards_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()
    response = [board.to_dict() for board in boards]

    return jsonify(response)

# post boards
@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    # if "title" not in request_body or "owner" not in request_body:
    #     return make_response({"details": "Invalid data"}, 400)

    new_board = Board.instance_from_json(request_body)

    db.session.add(new_board)
    db.session.commit()

    return {"board":new_board.to_dict()}, 201
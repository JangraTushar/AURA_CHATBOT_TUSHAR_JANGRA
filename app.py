# app.py
from flask import Flask, render_template, request, jsonify

from rag import setup_knowledge_base, level_1_answer
from sensors import level_2_answer, get_farm_by_id

app = Flask(__name__)
CURRENT_FARM_ID = None  # which farm's sensors are "connected"


#@app.before_first_request
#def init_app():
setup_knowledge_base(force_rebuild=False)


def answer_question(question: str, farm_id: str | None = None) -> str:
    """
    Router logic required in assignment.
    """
    if farm_id:
        return level_2_answer(question, farm_id)
    else:
        return level_1_answer(question)


@app.route("/", methods=["GET"])
def index():
    return render_template("chat.html")


@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.get_json()
    question = data.get("question", "").strip()
    farm_id = data.get("farm_id") or None

    if not question:
        return jsonify({"error": "Question is required."}), 400

    try:
        answer = answer_question(question, farm_id)
        return jsonify({"answer": answer, "farm_id": farm_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/connect_farm", methods=["POST"])
def connect_farm():
    """
    Toggle sensor connection (e.g., connect to farm_102).
    """
    global CURRENT_FARM_ID
    data = request.get_json()
    farm_id = data.get("farm_id")

    if not farm_id:
        CURRENT_FARM_ID = None
        return jsonify({"message": "Sensors disconnected.", "farm_id": None})

    # Validate farm exists
    try:
        _ = get_farm_by_id(farm_id)
    except Exception:
        return jsonify({"error": f"Unknown farm_id: {farm_id}"}), 400

    CURRENT_FARM_ID = farm_id
    return jsonify({"message": "Sensors connected.", "farm_id": farm_id})


@app.route("/api/current_farm", methods=["GET"])
def current_farm():
    return jsonify({"farm_id": CURRENT_FARM_ID})


@app.route("/api/farms/<farm_id>/sensors", methods=["GET"])
def farm_sensors_api(farm_id):
    """
    Mock sensor API using sample_farm_data.json. [file:6][file:4]
    """
    try:
        farm = get_farm_by_id(farm_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

    return jsonify(farm)


if __name__ == "__main__":
    app.run(debug=True)

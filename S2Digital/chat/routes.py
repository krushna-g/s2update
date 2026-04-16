from flask import Blueprint, request, jsonify

bp = Blueprint("chat", __name__)

@bp.route("/chat", methods=["POST"])
def chat():
    payload = request.get_json() or {}
    msg = payload.get("message", "").strip()
    if not msg:
        return jsonify({"ok": False, "error": "message required"}), 400

    # simple echo bot — replace with AI/logic later
    reply = f"Echo: {msg}"
    return jsonify({"ok": True, "reply": reply})
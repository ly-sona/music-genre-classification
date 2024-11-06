from flask import Blueprint, jsonify

health_bp = Blueprint('health_check', __name__)

@health_bp.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "running"})

import logging
import os
import requests
from argon2 import PasswordHasher
from datetime import datetime, timezone
from flask import request, jsonify, Blueprint, g
from functools import wraps
from pydantic import BaseModel, ValidationError
from werkzeug.exceptions import Unauthorized

from server.proxy.core import db, cm

api_bp = Blueprint('api', __name__, url_prefix='/api')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s [%(name)s] %(message)s'
)
logger = logging.getLogger(__name__)

LOGGER_URL = os.getenv("LOGGER_URL", "http://127.0.0.1:8025/logger")

class RequestModel(BaseModel):
    session_id: str
    ts: str
    role: str
    ip: str = None
    content: str
    llm: str
    tokens: int = 0
    costs: float = 0.0


def api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise Unauthorized("Missing or invalid Authorization header")

        token = auth_header.split(' ')[1].strip()
        try:
            user_id, key_hash, api_key_id = db.get_api_key(token).values()
            if not key_hash:
                raise Unauthorized("Invalid token")
                
            ph = PasswordHasher()
            if not ph.verify(key_hash, token):
                raise Unauthorized("Invalid token")
                
        except Exception as e:
            raise Unauthorized("Token verification failed") from e
        
        g.api_key = {
            'token': token,
            'key_hash': key_hash,
            'user_id': str(user_id),
            'api_key_id': str(api_key_id)
        }
        return f(*args, **kwargs)
        
    return decorated_function


@api_bp.route("/v1/llm-proxy", methods=["POST"])
@api_key_required
def llm_proxy():
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify({"error": "Invalid request format. Expected a JSON object"}), 400
        user_data = RequestModel(**data)
    except ValidationError as e:
        return jsonify({"error": "Invalid type of data fields or missing fields"}), 400
    except Exception as e:
        return jsonify({"error": "Failed to process the request. Ensure the input is valid JSON"}), 400

    try:
        detected_by, label = cm.classify_multiple(['egida'], user_data.content).popitem()
        db.last_use_api_key(g.api_key['user_id'], g.api_key['api_key_id'], datetime.now(timezone.utc).isoformat())
        log_status = requests.post(
            LOGGER_URL, json={**data, "label": label, 'user_id': g.api_key['user_id'], 'detected_by': detected_by}
        )
        log_status.raise_for_status()
        return jsonify({"label": label}), 200
    except Exception as e:
        logger.error("Unexpected error /llm-proxy", exc_info=e)
        return jsonify({"error": "Service unavailable"}), 500

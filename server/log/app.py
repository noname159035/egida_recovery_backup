# Это модуль для сохранения логов в базу данных
# Важно! Ip адрес хоста должен соответствовать текущему адресу БД!!

import logging
import psycopg2
from flask import Flask, request, jsonify
from database.database import DatabaseManager
from pydantic import BaseModel


app = Flask(__name__)
db = DatabaseManager()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s [%(name)s] %(message)s'
)
logger = logging.getLogger(__name__)

class RecordModel(BaseModel):
    user_id: str
    session_id: str
    llm: str
    ip: str = None
    content: str
    label: str
    detected_by: str
    role: str
    ts: str
    tokens: int = 0
    costs: float = 0.0


@app.route("/logger", methods=["POST"])
def send_log_to_BD():
    try:
        user_data = RecordModel(**request.get_json())
        db.add_model(user_data.user_id, user_data.llm)
        db.add_message(**user_data.model_dump())
    except Exception as e:
        logger.error("Error /logger", exc_info=e)
        return jsonify({"error": "Logger error", "details": str(e)}), 500

    return jsonify({"result": "Success"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8025)

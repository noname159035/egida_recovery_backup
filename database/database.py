import psycopg2
from psycopg2 import extras
from contextlib import contextmanager
from typing import Optional, Dict, List, Any
import os

HOST_IP = os.getenv("HOST_IP", "127.0.0.1")


class DatabaseManager:
    def __init__(self):
        self.config = {
            "user": "postgres",
            "password": "postgres",
            "host": HOST_IP,
            "port": "5432",
            "database": "log_bd_linux",
            "options": "-c client_encoding=utf8",
        }

    @contextmanager
    def _get_cursor(self) -> psycopg2.extensions.cursor:
        conn = psycopg2.connect(**self.config)
        conn.autocommit = False
        cursor = conn.cursor(cursor_factory=extras.DictCursor)

        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def execute_query(
            self, query: str, params: Optional[tuple] = None
    ) -> List[Dict[str, Any]]:
        """Универсальный метод для выполнения SELECT-запросов."""
        with self._get_cursor() as cursor:
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def execute_update(self, query: str, params: Optional[tuple] = None) -> None:
        """Универсальный метод для выполнения INSERT/UPDATE/DELETE."""
        with self._get_cursor() as cursor:
            cursor.execute(query, params)

    def have_new_read(self, user_id, llm):
        query = """
        SELECT EXISTS (
            SELECT 1
            FROM chats
            WHERE user_id = %s AND llm = %s AND NOT checked
        );
        """
        return self.execute_query(query, (user_id, llm))[0]["exists"]

    def get_bad_prompts_for_llm(self, user_id, llm):
        query = """
            SELECT 
                m.message_id,
                c.session_id,
                m.content,
                m.label,
                m.ts,
                c.unsafe_count
            FROM chats c
            INNER JOIN messages m 
                ON c.last_bad_id = m.message_id
            WHERE 
                c.user_id = %s 
                AND c.llm = %s
                AND c.last_bad_id IS NOT NULL
                AND c.misclassified = FALSE
            ORDER BY m.ts DESC
        """
        return self.execute_query(query, (user_id, llm))

    def get_user_llms(self, user_id):
        query = """
            SELECT llm
            FROM models
            WHERE user_id = %s
        """
        return self.execute_query(query, (user_id,))

    def get_chat_history(self, session_id):
        query = """
            SELECT role, content
            FROM messages 
            WHERE session_id = %s 
            ORDER BY ts
        """
        return self.execute_query(query, (session_id,))

    def read_prompt(self, user_id, session_id):
        query = """
            UPDATE chats
            SET checked = TRUE
            WHERE user_id = %s AND session_id = %s
        """
        self.execute_update(query, (user_id, session_id,))

    def add_model(self, user_id, llm):
        query = """
            INSERT INTO models (user_id, llm) 
            VALUES (%s, %s) 
            ON CONFLICT DO NOTHING;
        """
        self.execute_update(query, (user_id, llm,))

    def get_model_info(self, user_id, llm):
        query = """
        SELECT 
            COUNT(*) as calls, 
            COALESCE(SUM(m.tokens), 0) as sum_tokens, 
            COALESCE(SUM(m.costs), 0) as sum_costs
        FROM messages m
        JOIN chats c ON m.user_id = c.user_id AND m.session_id = c.session_id
        WHERE m.user_id = %s AND c.llm = %s
        """
        return self.execute_query(query, (user_id, llm))[0]

    def add_message(
        self,
        user_id,
        ip,
        session_id,
        llm,
        content,
        label,
        detected_by,
        role,
        ts,
        tokens=0,
        costs=0.0,
    ):
        message_query = """
            INSERT INTO messages (user_id, ip, session_id, content, label, detected_by, role, ts, tokens, costs)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING message_id, label
        """
        message_params = (user_id, ip, session_id, content, label, detected_by, role, ts, tokens, costs)
        result = self.execute_query(message_query, message_params)
        message_id, label = result[0].values()
        is_safe = (label == 'Safe')
        unsafe_count_inc = 0 if is_safe else 1
        last_bad_id = None if is_safe else message_id

        chats_query = """
            INSERT INTO chats (user_id, session_id, llm, unsafe_count, last_bad_id, checked)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id, session_id)
            DO UPDATE SET
                unsafe_count = chats.unsafe_count + EXCLUDED.unsafe_count,
                last_bad_id = COALESCE(EXCLUDED.last_bad_id, chats.last_bad_id),
                checked = chats.checked AND EXCLUDED.checked
        """
        chats_params = (user_id, session_id, llm, unsafe_count_inc, last_bad_id, is_safe)
        self.execute_update(chats_query, chats_params)

    def exists_email(self, email):
        query = """
        SELECT EXISTS (
            SELECT 1
            FROM users
            WHERE email = %s
        );
        """
        return self.execute_query(query, (email,))[0]

    def add_user(self, first_name, second_name, company_name, email, token_hash):
        query = """
            INSERT INTO users 
            (first_name, second_name, company_name, email, token_hash) 
            VALUES (%s, %s, %s, %s, %s) RETURNING user_id
        """

        return self.execute_query(query, (first_name, second_name, company_name, email, token_hash))[0]

    def get_user_by_email(self, email):
        query = """
            SELECT user_id, first_name, token_hash FROM users
            WHERE email = %s
        """
        result = self.execute_query(query, (email,))
        return result[0] if result else None

    def get_api_keys(self, user_id):
        query = """
            SELECT api_key_id, key_value, key_name, last_used, ts FROM api_keys
            WHERE user_id = %s
        """
        return self.execute_query(query, (user_id,))

    def get_api_key(self, key_value):
        query = """
            SELECT user_id, key_hash, api_key_id FROM api_keys
            WHERE key_value = %s
        """
        results = self.execute_query(query, (key_value,))
        if len(results) > 1:
            raise ValueError("API key prefix collision: multiple keys with same prefix")
        elif len(results) == 0:
            raise LookupError("API key not found")

        return results[0]

    def add_api_key(self, user_id, key_hash, key_value, key_name):
        query = """
            INSERT INTO api_keys
            (user_id, key_hash, key_value, key_name) 
            VALUES (%s, %s, %s, %s) RETURNING user_id
        """
        return self.execute_update(query, (user_id, key_hash, key_value, key_name))

    def rename_api_key(self, user_id, api_key_id, key_name):
        query = """
            UPDATE api_keys
            SET key_name = %s
            WHERE user_id = %s AND api_key_id = %s
        """
        self.execute_update(query, (key_name, user_id, api_key_id))

    def last_use_api_key(self, user_id, api_key_id, last_used):
        query = """
            UPDATE api_keys
            SET last_used = %s
            WHERE user_id = %s AND api_key_id = %s
        """
        self.execute_update(query, (last_used, user_id, api_key_id))

    def delete_api_key(self, user_id, api_key_id):
        query = """
            DELETE FROM api_keys
            WHERE user_id = %s AND api_key_id = %s
        """
        self.execute_update(query, (user_id, api_key_id))

    def get_logs(self, user_id):
        query = """
            SELECT user_id, ip, ts, content, label, detected_by FROM messages
            WHERE user_id = %s
            ORDER BY ts DESC
        """
        return self.execute_query(query, (user_id,))

    def set_misclassified(self, user_id, session_id):
        query = """
            UPDATE chats
            SET misclassified = TRUE
            WHERE user_id = %s AND session_id = %s
        """
        self.execute_update(query, (user_id, session_id,))

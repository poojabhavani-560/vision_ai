import sqlite3
from datetime import datetime
from config import DATABASE_PATH


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_name TEXT NOT NULL,
            prediction TEXT NOT NULL,
            confidence REAL NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    connection.commit()
    connection.close()


def add_prediction(image_name, prediction, confidence):
    connection = get_connection()
    cursor = connection.execute(
        """
        INSERT INTO predictions (image_name, prediction, confidence, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (image_name, prediction, confidence, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    connection.commit()
    prediction_id = cursor.lastrowid
    connection.close()
    return prediction_id


def get_predictions(search=""):
    connection = get_connection()
    if search:
        rows = connection.execute(
            """
            SELECT * FROM predictions
            WHERE image_name LIKE ? OR prediction LIKE ?
            ORDER BY id DESC
            """,
            (f"%{search}%", f"%{search}%"),
        ).fetchall()
    else:
        rows = connection.execute(
            "SELECT * FROM predictions ORDER BY id DESC"
        ).fetchall()
    connection.close()
    return [dict(row) for row in rows]


def delete_prediction(prediction_id):
    connection = get_connection()
    connection.execute("DELETE FROM predictions WHERE id = ?", (prediction_id,))
    connection.commit()
    connection.close()


def clear_predictions():
    connection = get_connection()
    connection.execute("DELETE FROM predictions")
    connection.commit()
    connection.close()


def get_dashboard_stats():
    connection = get_connection()
    total = connection.execute(
        "SELECT COUNT(*) AS value FROM predictions"
    ).fetchone()["value"]

    average = connection.execute(
        "SELECT COALESCE(AVG(confidence), 0) AS value FROM predictions"
    ).fetchone()["value"]

    most_detected_row = connection.execute(
        """
        SELECT prediction, COUNT(*) AS count
        FROM predictions
        GROUP BY prediction
        ORDER BY count DESC, prediction ASC
        LIMIT 1
        """
    ).fetchone()

    today = datetime.now().strftime("%Y-%m-%d")
    today_count = connection.execute(
        "SELECT COUNT(*) AS value FROM predictions WHERE substr(created_at, 1, 10) = ?",
        (today,),
    ).fetchone()["value"]

    daily_rows = connection.execute(
        """
        SELECT substr(created_at, 1, 10) AS day, COUNT(*) AS count
        FROM predictions
        GROUP BY day
        ORDER BY day DESC
        LIMIT 7
        """
    ).fetchall()

    category_rows = connection.execute(
        """
        SELECT prediction, COUNT(*) AS count
        FROM predictions
        GROUP BY prediction
        ORDER BY count DESC, prediction ASC
        LIMIT 6
        """
    ).fetchall()

    connection.close()

    daily_rows = list(reversed([dict(row) for row in daily_rows]))
    category_rows = [dict(row) for row in category_rows]

    return {
        "total": total,
        "average_confidence": round(float(average or 0), 2),
        "most_detected": most_detected_row["prediction"] if most_detected_row else "—",
        "today": today_count,
        "daily_labels": [row["day"] for row in daily_rows],
        "daily_values": [row["count"] for row in daily_rows],
        "category_labels": [row["prediction"] for row in category_rows],
        "category_values": [row["count"] for row in category_rows],
    }

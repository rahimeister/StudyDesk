from datetime import datetime, timedelta
from database import get_connection


class StudyManager:
    def add_subject(self, name: str) -> int:
        name = name.strip()
        if not name:
            raise ValueError("Ders adı boş bırakılamaz.")
        with get_connection() as conn:
            conn.execute("INSERT OR IGNORE INTO subjects(name) VALUES(?)", (name,))
            row = conn.execute("SELECT id FROM subjects WHERE name = ?", (name,)).fetchone()
            return int(row["id"])

    def get_subjects(self):
        with get_connection() as conn:
            return conn.execute("SELECT * FROM subjects ORDER BY name").fetchall()

    def add_topic(self, subject_name, title, priority, target_minutes):
        subject_id = self.add_subject(subject_name)
        title = title.strip()
        if not title:
            raise ValueError("Konu başlığı boş bırakılamaz.")
        if target_minutes <= 0:
            raise ValueError("Hedef süre 0'dan büyük olmalıdır.")
        with get_connection() as conn:
            conn.execute(
                """INSERT INTO topics(subject_id, title, priority, target_minutes)
                   VALUES(?, ?, ?, ?)""",
                (subject_id, title, priority, target_minutes),
            )

    def get_topics(self, include_completed=True):
        where = "" if include_completed else "WHERE t.status != 'Tamamlandı'"
        with get_connection() as conn:
            return conn.execute(
                f"""SELECT t.*, s.name AS subject_name
                    FROM topics t JOIN subjects s ON s.id=t.subject_id
                    {where}
                    ORDER BY CASE t.priority WHEN 'Yüksek' THEN 1 WHEN 'Orta' THEN 2 ELSE 3 END,
                             t.created_at DESC"""
            ).fetchall()

    def update_topic_status(self, topic_id, status):
        with get_connection() as conn:
            conn.execute("UPDATE topics SET status=? WHERE id=?", (status, topic_id))

    def delete_topic(self, topic_id):
        with get_connection() as conn:
            conn.execute("DELETE FROM topics WHERE id=?", (topic_id,))

    def add_session(self, topic_id, duration_minutes, session_type="Pomodoro"):
        if duration_minutes <= 0:
            raise ValueError("Kaydedilecek süre 0'dan büyük olmalıdır.")
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO sessions(topic_id, duration_minutes, session_type) VALUES(?, ?, ?)",
                (topic_id, duration_minutes, session_type),
            )
            if topic_id:
                conn.execute(
                    "UPDATE topics SET studied_minutes = studied_minutes + ? WHERE id=?",
                    (duration_minutes, topic_id),
                )

    def add_note(self, topic_id, title, content):
        title, content = title.strip(), content.strip()
        if not title or not content:
            raise ValueError("Not başlığı ve içeriği zorunludur.")
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO notes(topic_id, title, content) VALUES(?, ?, ?)",
                (topic_id, title, content),
            )

    def get_notes(self):
        with get_connection() as conn:
            return conn.execute(
                """SELECT n.*, t.title AS topic_title, s.name AS subject_name
                   FROM notes n
                   LEFT JOIN topics t ON t.id=n.topic_id
                   LEFT JOIN subjects s ON s.id=t.subject_id
                   ORDER BY n.created_at DESC"""
            ).fetchall()

    def delete_note(self, note_id):
        with get_connection() as conn:
            conn.execute("DELETE FROM notes WHERE id=?", (note_id,))

    def get_daily_goal(self):
        with get_connection() as conn:
            row = conn.execute("SELECT value FROM settings WHERE key='daily_goal_minutes'").fetchone()
            return int(row["value"]) if row else 240

    def set_daily_goal(self, minutes):
        if minutes <= 0:
            raise ValueError("Günlük hedef 0'dan büyük olmalıdır.")
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO settings(key,value) VALUES('daily_goal_minutes', ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                (str(minutes),),
            )

    def dashboard_stats(self):
        today = datetime.now().strftime("%Y-%m-%d")
        week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")
        with get_connection() as conn:
            today_minutes = conn.execute(
                "SELECT COALESCE(SUM(duration_minutes),0) total FROM sessions WHERE date(created_at)=?", (today,)
            ).fetchone()["total"]
            pomodoros = conn.execute(
                "SELECT COUNT(*) total FROM sessions WHERE date(created_at)=? AND session_type='Pomodoro'", (today,)
            ).fetchone()["total"]
            completed_week = conn.execute(
                "SELECT COUNT(*) total FROM topics WHERE status='Tamamlandı' AND date(created_at)>=?", (week_start,)
            ).fetchone()["total"]
            total_minutes = conn.execute("SELECT COALESCE(SUM(duration_minutes),0) total FROM sessions").fetchone()["total"]
            completed_topics = conn.execute("SELECT COUNT(*) total FROM topics WHERE status='Tamamlandı'").fetchone()["total"]
            top_subject = conn.execute(
                """SELECT s.name, COALESCE(SUM(se.duration_minutes),0) total
                   FROM sessions se
                   LEFT JOIN topics t ON t.id=se.topic_id
                   LEFT JOIN subjects s ON s.id=t.subject_id
                   GROUP BY s.id ORDER BY total DESC LIMIT 1"""
            ).fetchone()
            recent = conn.execute(
                """SELECT se.duration_minutes, se.session_type, se.created_at,
                          COALESCE(t.title, 'Genel Çalışma') topic_title,
                          COALESCE(s.name, '-') subject_name
                   FROM sessions se
                   LEFT JOIN topics t ON t.id=se.topic_id
                   LEFT JOIN subjects s ON s.id=t.subject_id
                   ORDER BY se.created_at DESC LIMIT 6"""
            ).fetchall()
        return {
            "today_minutes": int(today_minutes),
            "pomodoros": int(pomodoros),
            "completed_week": int(completed_week),
            "total_minutes": int(total_minutes),
            "completed_topics": int(completed_topics),
            "top_subject": top_subject["name"] if top_subject and top_subject["name"] else "Henüz yok",
            "recent": recent,
            "goal": self.get_daily_goal(),
        }

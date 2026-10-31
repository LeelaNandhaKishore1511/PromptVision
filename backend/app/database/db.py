import sqlite3
import json
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from ..config import DATABASE_PATH

def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Experiments table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS experiments (
        id TEXT PRIMARY KEY,
        created_at TEXT NOT NULL,
        title TEXT,
        image_id TEXT NOT NULL,
        image_path TEXT NOT NULL,
        image_filename TEXT NOT NULL,
        image_width INTEGER,
        image_height INTEGER,
        image_channels INTEGER,
        selected_objective TEXT NOT NULL,
        cv_operations TEXT, -- JSON array of ops
        cv_metadata TEXT,   -- JSON object of extracted visual features
        processed_image_urls TEXT, -- JSON array of urls
        selected_model TEXT NOT NULL,
        preferences TEXT, -- JSON object of preferences (audience, tone, format, length, etc.)
        prompts TEXT,     -- JSON object: { basic: str, costar: str, ai_optimized: str }
        responses TEXT,   -- JSON object: { basic: str, costar: str, ai_optimized: str }
        metrics TEXT,     -- JSON object: { basic: {...}, costar: {...}, ai_optimized: {...} }
        ratings TEXT,     -- JSON object: human ratings & evaluations
        status TEXT NOT NULL DEFAULT 'completed'
    );
    """)

    # Evaluations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evaluations (
        id TEXT PRIMARY KEY,
        experiment_id TEXT NOT NULL,
        strategy TEXT NOT NULL,
        accuracy REAL,
        relevance REAL,
        completeness REAL,
        instruction_adherence REAL,
        consistency REAL,
        clarity REAL,
        hallucination_reduction REAL,
        feedback TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (experiment_id) REFERENCES experiments (id) ON DELETE CASCADE
    );
    """)

    # Teach Sessions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teach_sessions (
        id TEXT PRIMARY KEY,
        created_at TEXT NOT NULL,
        image_id TEXT NOT NULL,
        image_path TEXT NOT NULL,
        topic TEXT,
        concepts TEXT, -- JSON array
        explanation TEXT,
        quiz_data TEXT, -- JSON array of questions
        user_answers TEXT, -- JSON array of user responses
        score REAL,
        max_score REAL,
        percentage REAL,
        understanding_level TEXT,
        weak_concepts TEXT, -- JSON array
        remedial_explanation TEXT
    );
    """)

    # CV Operations Log / Benchmarks
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cv_runs (
        id TEXT PRIMARY KEY,
        created_at TEXT NOT NULL,
        image_id TEXT NOT NULL,
        operation_name TEXT NOT NULL,
        module_name TEXT NOT NULL,
        parameters TEXT,
        execution_time_ms REAL,
        result_image_url TEXT,
        metadata TEXT
    );
    """)

    conn.commit()
    conn.close()

# Database Helper Functions

def save_experiment(experiment_data: Dict[str, Any]) -> str:
    conn = get_connection()
    cursor = conn.cursor()
    exp_id = experiment_data.get("id") or str(uuid.uuid4())
    created_at = experiment_data.get("created_at") or datetime.now(timezone.utc).isoformat()
    
    cursor.execute("""
        INSERT OR REPLACE INTO experiments (
            id, created_at, title, image_id, image_path, image_filename,
            image_width, image_height, image_channels, selected_objective,
            cv_operations, cv_metadata, processed_image_urls, selected_model,
            preferences, prompts, responses, metrics, ratings, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        exp_id,
        created_at,
        experiment_data.get("title", f"Experiment {datetime.now().strftime('%Y-%m-%d %H:%M')}"),
        experiment_data.get("image_id", ""),
        experiment_data.get("image_path", ""),
        experiment_data.get("image_filename", ""),
        experiment_data.get("image_width", 0),
        experiment_data.get("image_height", 0),
        experiment_data.get("image_channels", 3),
        experiment_data.get("selected_objective", "Analyse"),
        json.dumps(experiment_data.get("cv_operations", [])),
        json.dumps(experiment_data.get("cv_metadata", {})),
        json.dumps(experiment_data.get("processed_image_urls", [])),
        experiment_data.get("selected_model", "qwen2.5vl:3b"),
        json.dumps(experiment_data.get("preferences", {})),
        json.dumps(experiment_data.get("prompts", {})),
        json.dumps(experiment_data.get("responses", {})),
        json.dumps(experiment_data.get("metrics", {})),
        json.dumps(experiment_data.get("ratings", {})),
        experiment_data.get("status", "completed")
    ))
    conn.commit()
    conn.close()
    return exp_id

def get_experiments(limit: int = 50, offset: int = 0, search: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    if search:
        cursor.execute("""
            SELECT * FROM experiments 
            WHERE title LIKE ? OR selected_objective LIKE ? OR selected_model LIKE ?
            ORDER BY created_at DESC LIMIT ? OFFSET ?
        """, (f"%{search}%", f"%{search}%", f"%{search}%", limit, offset))
    else:
        cursor.execute("SELECT * FROM experiments ORDER BY created_at DESC LIMIT ? OFFSET ?", (limit, offset))
    
    rows = cursor.fetchall()
    results = []
    for row in rows:
        d = dict(row)
        for key in ["cv_operations", "cv_metadata", "processed_image_urls", "preferences", "prompts", "responses", "metrics", "ratings"]:
            if d.get(key):
                try:
                    d[key] = json.loads(d[key])
                except Exception:
                    pass
        results.append(d)
    conn.close()
    return results

def get_experiment_by_id(exp_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM experiments WHERE id = ?", (exp_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    for key in ["cv_operations", "cv_metadata", "processed_image_urls", "preferences", "prompts", "responses", "metrics", "ratings"]:
        if d.get(key):
            try:
                d[key] = json.loads(d[key])
            except Exception:
                pass
    return d

def delete_experiment(exp_id: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM experiments WHERE id = ?", (exp_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def save_ratings(exp_id: str, ratings: Dict[str, Any]) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE experiments SET ratings = ? WHERE id = ?", (json.dumps(ratings), exp_id))
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return success

def save_teach_session(session_data: Dict[str, Any]) -> str:
    conn = get_connection()
    cursor = conn.cursor()
    sess_id = session_data.get("id") or str(uuid.uuid4())
    cursor.execute("""
        INSERT OR REPLACE INTO teach_sessions (
            id, created_at, image_id, image_path, topic, concepts,
            explanation, quiz_data, user_answers, score, max_score,
            percentage, understanding_level, weak_concepts, remedial_explanation
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        sess_id,
        session_data.get("created_at") or datetime.now(timezone.utc).isoformat(),
        session_data.get("image_id", ""),
        session_data.get("image_path", ""),
        session_data.get("topic", ""),
        json.dumps(session_data.get("concepts", [])),
        session_data.get("explanation", ""),
        json.dumps(session_data.get("quiz_data", [])),
        json.dumps(session_data.get("user_answers", [])),
        session_data.get("score", 0.0),
        session_data.get("max_score", 0.0),
        session_data.get("percentage", 0.0),
        session_data.get("understanding_level", "Unknown"),
        json.dumps(session_data.get("weak_concepts", [])),
        session_data.get("remedial_explanation", "")
    ))
    conn.commit()
    conn.close()
    return sess_id

def get_teach_sessions(limit: int = 20) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teach_sessions ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    results = []
    for r in rows:
        d = dict(r)
        for key in ["concepts", "quiz_data", "user_answers", "weak_concepts"]:
            if d.get(key):
                try:
                    d[key] = json.loads(d[key])
                except Exception:
                    pass
        results.append(d)
    conn.close()
    return results

def get_stats_summary() -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM experiments")
    total_experiments = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT image_id) FROM experiments")
    total_images = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM teach_sessions")
    total_teach = cursor.fetchone()[0]
    
    cursor.execute("SELECT * FROM experiments ORDER BY created_at DESC LIMIT 10")
    recent_rows = cursor.fetchall()
    recent = []
    for row in recent_rows:
        d = dict(row)
        for key in ["metrics", "ratings", "cv_operations"]:
            if d.get(key):
                try:
                    d[key] = json.loads(d[key])
                except Exception:
                    pass
        recent.append(d)
        
    conn.close()
    return {
        "total_experiments": total_experiments,
        "total_images": total_images,
        "total_teach_sessions": total_teach,
        "recent_experiments": recent
    }

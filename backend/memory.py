from datetime import date
from backend.database import SessionLocal, Habit

def get_habits():
    db = SessionLocal()
    habits = db.query(Habit).all()
    db.close()
    return habits

def add_habit(name: str):
    db = SessionLocal()
    db.add(Habit(name=name))
    db.commit()
    db.close()

def delete_habit(habit_id: int):
    db = SessionLocal()
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if habit:
        db.delete(habit)
        db.commit()
    db.close()

def complete_habit(habit_id: int):
    db = SessionLocal()
    habit = db.query(Habit).filter(Habit.id == habit_id).first()

    today = date.today()
    if habit.last_done != today:
        habit.streak += 1
        habit.last_done = today

    db.commit()
    db.close()

def user_context():
    habits = get_habits()
    if not habits:
        return "The user has not added any habits yet."

    lines = []
    for h in habits:
        lines.append(
            f"Habit: {h.name}, Streak: {h.streak}"
        )
    return "\n".join(lines)

def get_user_habit_context():
    return {
        "habits": [
            {"name": "Meditation", "streak": 2, "frequency": "daily"},
            {"name": "Reading", "streak": 0, "frequency": "daily"}
        ],
        "goals": ["learning", "mental clarity"],
        "recent_failures": ["Reading"]
    }


def habit_context_to_text(ctx):
    return f"""
Habits:
{ctx['habits']}

Recent failures:
{ctx['recent_failures']}

Goals:
{ctx['goals']}
"""

"""Core scheduling logic for AI Smart Study Planner.

This is a transparent, rule-based intelligent planner, not a trained ML model.
It scores tasks using deadline urgency, difficulty, importance, and estimated effort.
"""
from datetime import date, timedelta
from typing import List, Dict, Any


def score_task(task: Dict[str, Any], today: date) -> float:
    """Return a transparent priority score; larger means schedule earlier."""
    days_left = (task["deadline"] - today).days
    if days_left < 0:
        urgency = 10.0
    elif days_left == 0:
        urgency = 9.0
    elif days_left <= 1:
        urgency = 8.0
    elif days_left <= 3:
        urgency = 6.5
    elif days_left <= 7:
        urgency = 4.5
    else:
        urgency = 2.5

    difficulty_points = {"Easy": 1.0, "Medium": 2.0, "Hard": 3.0}.get(task["difficulty"], 2.0)
    importance_points = {"Low": 1.0, "Normal": 2.0, "High": 3.0}.get(task["importance"], 2.0)
    # Small effort adjustment: longer tasks get a modest boost to avoid last-minute overload.
    effort_points = min(float(task["hours"]), 4.0) * 0.35
    return round(urgency * 2.0 + difficulty_points * 1.5 + importance_points * 2.0 + effort_points, 2)


def build_schedule(
    tasks: List[Dict[str, Any]],
    today: date,
    days: int = 7,
    daily_minutes: int = 120,
    session_minutes: int = 30,
) -> List[Dict[str, Any]]:
    """Allocate task sessions across days, prioritizing urgent/high-value tasks.

    Tasks are split into sessions no longer than session_minutes. Each task's sessions
    are placed on or before its deadline when possible. Capacity is enforced per day.
    """
    if days < 1:
        raise ValueError("days must be at least 1")
    if daily_minutes < 1 or session_minutes < 1:
        raise ValueError("Study time must be positive")

    capacity = daily_minutes // session_minutes
    if capacity < 1:
        capacity = 1

    schedule = []
    daily_slots = {today + timedelta(days=i): [] for i in range(days)}
    ranked = sorted(tasks, key=lambda t: (-score_task(t, today), t["deadline"], t["subject"]))

    for task in ranked:
        remaining = max(1, round(float(task["hours"]) * 60))
        deadline = task["deadline"]
        # Schedule earlier than deadline if it falls within the selected planning window.
        eligible_dates = [d for d in daily_slots if d <= deadline]
        if not eligible_dates:
            eligible_dates = [min(daily_slots.keys())]
        for day in eligible_dates:
            while remaining > 0 and len(daily_slots[day]) < capacity:
                block = min(session_minutes, remaining)
                daily_slots[day].append({
                    "date": day,
                    "subject": task["subject"],
                    "task": task["task"],
                    "minutes": block,
                    "priority": score_task(task, today),
                    "reason": _reason(task, today),
                })
                remaining -= block
            if remaining <= 0:
                break
        if remaining > 0:
            # If the requested workload exceeds capacity before deadline, place remaining
            # sessions into the least-filled days in the planning window and flag the conflict.
            for day in sorted(daily_slots, key=lambda d: (len(daily_slots[d]), d)):
                while remaining > 0 and len(daily_slots[day]) < capacity:
                    block = min(session_minutes, remaining)
                    daily_slots[day].append({
                        "date": day,
                        "subject": task["subject"],
                        "task": task["task"],
                        "minutes": block,
                        "priority": score_task(task, today),
                        "reason": _reason(task, today) + " (tight schedule)",
                    })
                    remaining -= block
                if remaining <= 0:
                    break

    for day, items in daily_slots.items():
        # A short subject/task variety order within each day
        for item in items:
            schedule.append(item)
    return schedule


def _reason(task: Dict[str, Any], today: date) -> str:
    days_left = (task["deadline"] - today).days
    if days_left < 0:
        urgency_text = "Overdue task"
    elif days_left == 0:
        urgency_text = "Due today"
    elif days_left <= 3:
        urgency_text = "Deadline approaching"
    else:
        urgency_text = "Plan ahead"
    return f"{urgency_text}; {task['difficulty'].lower()} difficulty; {task['importance'].lower()} importance"


def summarize_schedule(schedule: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = sum(item["minutes"] for item in schedule)
    return {
        "sessions": len(schedule),
        "total_minutes": total,
        "total_hours": round(total / 60, 1),
    }

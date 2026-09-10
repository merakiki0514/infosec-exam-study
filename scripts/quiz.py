#!/usr/bin/env python3
"""
정보보안기사 실기 학습용 문제 선택/채점 기록 스크립트.
data/questions.json 을 문제 은행으로, progress/progress.json 을 학습 이력으로 사용한다.

Usage:
  python3 scripts/quiz.py pick [--topic network] [--count 10] [--mode normal|review|weak] [--source 기출|예상|all]
  python3 scripts/quiz.py record --id 2024-1-01 --result correct|partial|wrong
  python3 scripts/quiz.py stats [--topic network]
"""
import argparse
import json
import random
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS_PATH = ROOT / "data" / "questions.json"
PROGRESS_PATH = ROOT / "progress" / "progress.json"

TOPIC_NAMES = {
    "network": "네트워크 보안",
    "web": "웹 보안",
    "system": "시스템 보안",
    "crypto": "암호화·인증",
    "risk": "위험 관리",
    "law": "법·제도·실무",
}


def load_questions():
    data = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))
    return data["questions"]


def load_progress():
    if not PROGRESS_PATH.exists():
        return {"sessions": [], "question_stats": {}}
    return json.loads(PROGRESS_PATH.read_text(encoding="utf-8"))


def save_progress(progress):
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(
        json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def question_source(q):
    return q.get("source", "기출")


def cmd_pick(args):
    questions = load_questions()
    progress = load_progress()
    stats = progress.get("question_stats", {})

    pool = questions
    if args.topic:
        pool = [q for q in pool if q["topic"] == args.topic]
    if args.source and args.source != "all":
        pool = [q for q in pool if question_source(q) == args.source]

    if not pool:
        print(json.dumps({"error": "no questions matched filters"}, ensure_ascii=False))
        sys.exit(1)

    if args.mode == "review":
        pool = [
            q for q in pool
            if stats.get(q["id"], {}).get("last_result") in ("wrong", "partial")
        ]
        if not pool:
            print(json.dumps({"info": "복습할 오답이 없습니다. mode=normal로 다시 시도하세요."}, ensure_ascii=False))
            return
    elif args.mode == "weak":
        topic_acc = {}
        for q in questions:
            s = stats.get(q["id"])
            if not s or s.get("attempts", 0) == 0:
                continue
            t = q["topic"]
            acc = topic_acc.setdefault(t, [0, 0])
            acc[0] += s.get("correct", 0)
            acc[1] += s.get("attempts", 0)
        ranked = sorted(
            topic_acc.items(), key=lambda kv: (kv[1][0] / kv[1][1]) if kv[1][1] else 1.0
        )
        weak_topics = [t for t, _ in ranked[:2]] or list(TOPIC_NAMES.keys())
        pool = [q for q in pool if q["topic"] in weak_topics]

    def priority(q):
        s = stats.get(q["id"])
        if not s or s.get("attempts", 0) == 0:
            return (0, random.random())
        if s.get("last_result") in ("wrong", "partial"):
            return (1, random.random())
        return (2, s.get("last_seen", ""))

    pool_sorted = sorted(pool, key=priority)
    picked = pool_sorted[: args.count]
    random.shuffle(picked)

    print(json.dumps({"count": len(picked), "questions": picked}, ensure_ascii=False, indent=2))


def cmd_record(args):
    questions = {q["id"]: q for q in load_questions()}
    if args.id not in questions:
        print(json.dumps({"error": f"unknown question id: {args.id}"}, ensure_ascii=False))
        sys.exit(1)

    progress = load_progress()
    stats = progress.setdefault("question_stats", {})
    entry = stats.setdefault(args.id, {"attempts": 0, "correct": 0, "last_result": None, "last_seen": None})
    entry["attempts"] += 1
    if args.result == "correct":
        entry["correct"] += 1
    entry["last_result"] = args.result
    entry["last_seen"] = date.today().isoformat()

    session_date = date.today().isoformat()
    sessions = progress.setdefault("sessions", [])
    today_session = next((s for s in sessions if s["date"] == session_date), None)
    if today_session is None:
        today_session = {"date": session_date, "topic": questions[args.id]["topic"], "results": {}}
        sessions.append(today_session)
    today_session["results"][args.id] = args.result
    today_session["updated_at"] = datetime.now().isoformat(timespec="seconds")

    save_progress(progress)
    print(json.dumps({"ok": True, "id": args.id, "result": args.result}, ensure_ascii=False))


def cmd_stats(args):
    questions = load_questions()
    progress = load_progress()
    stats = progress.get("question_stats", {})

    by_topic = {t: {"total": 0, "attempted": 0, "correct": 0, "attempts": 0} for t in TOPIC_NAMES}
    for q in questions:
        t = q["topic"]
        by_topic[t]["total"] += 1
        s = stats.get(q["id"])
        if s and s.get("attempts", 0) > 0:
            by_topic[t]["attempted"] += 1
            by_topic[t]["correct"] += s.get("correct", 0)
            by_topic[t]["attempts"] += s.get("attempts", 0)

    report = {}
    for t, name in TOPIC_NAMES.items():
        d = by_topic[t]
        acc = round(100 * d["correct"] / d["attempts"], 1) if d["attempts"] else None
        report[t] = {
            "name": name,
            "total_questions": d["total"],
            "attempted_questions": d["attempted"],
            "accuracy_pct": acc,
        }

    total_sessions = len(progress.get("sessions", []))
    print(json.dumps({"sessions": total_sessions, "by_topic": report}, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_pick = sub.add_parser("pick")
    p_pick.add_argument("--topic", choices=list(TOPIC_NAMES.keys()))
    p_pick.add_argument("--count", type=int, default=10)
    p_pick.add_argument("--mode", choices=["normal", "review", "weak"], default="normal")
    p_pick.add_argument("--source", choices=["기출", "예상", "all"], default="all")
    p_pick.set_defaults(func=cmd_pick)

    p_record = sub.add_parser("record")
    p_record.add_argument("--id", required=True)
    p_record.add_argument("--result", required=True, choices=["correct", "partial", "wrong"])
    p_record.set_defaults(func=cmd_record)

    p_stats = sub.add_parser("stats")
    p_stats.add_argument("--topic", choices=list(TOPIC_NAMES.keys()))
    p_stats.set_defaults(func=cmd_stats)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

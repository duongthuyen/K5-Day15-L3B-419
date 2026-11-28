"""Đếm số liệu persona cho cost/personas.yaml từ chat.csv của BTC (data/preclass của repo đề).

Chạy:  python cost/count_personas.py <đường dẫn tới chat.csv>
       (file data BTC không nằm trong repo này — để ở data-btc/ ngoài repo, không commit)

Cách đếm (viết trước khi chạy):
- Tập: các lượt trong chat.csv có addressed_agent_id = teaching_assistant (học viên hỏi trợ giảng AI —
  đúng việc agent của nhóm làm). Bỏ lượt nhắn bạn học AI (classmate_*).
- Khoảng thời gian: từ lượt đầu tới lượt cuối trong file (05/11 → 25/11/2026, ~21 ngày).
  Quy ra tháng: × 30 / số ngày.
- Phiên: cột session_id gần như trống, nên tự gom: hai lượt liên tiếp của cùng học viên cách nhau
  ≤ 30 phút thì cùng một phiên (ngưỡng 30 phút là tự chọn).
- Persona: chia học viên đã hỏi TA thành 3 nhóm theo số phiên / tháng (ngưỡng ở SEGMENTS);
  mỗi nhóm báo tỉ lệ người, số phiên / người / tháng (trung bình), số lượt / phiên (trung bình).
"""
import csv
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timedelta

GAP = timedelta(minutes=30)
SEGMENTS = [("dung_it", 0, 2), ("dung_vua", 2, 6), ("dung_nhieu", 6, 10 ** 9)]   # [từ, dưới) phiên / tháng


def main(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = [r for r in csv.DictReader(f) if r["addressed_agent_id"] == "teaching_assistant"]
    times = defaultdict(list)
    for r in rows:
        times[r["hv"]].append(datetime.fromisoformat(r["asked_at"]))
    all_t = [t for ts in times.values() for t in ts]
    days = (max(all_t) - min(all_t)).total_seconds() / 86400
    per_month = 30 / days

    learners = {}
    for hv, ts in times.items():
        ts.sort()
        sessions = [[ts[0]]]
        for t in ts[1:]:
            if t - sessions[-1][-1] <= GAP:
                sessions[-1].append(t)
            else:
                sessions.append([t])
        learners[hv] = (len(sessions) * per_month, [len(s) for s in sessions])

    n = len(learners)
    print("Lượt hỏi TA: %d · học viên: %d · khoảng: %.1f ngày (%s → %s) · hệ số quy tháng: %.3f"
          % (len(rows), n, days, min(all_t).date(), max(all_t).date(), per_month))
    all_turns = [k for _, ss in learners.values() for k in ss]
    print("Tổng phiên: %d · lượt / phiên trung bình: %.2f" % (len(all_turns), statistics.mean(all_turns)))
    for name, lo, hi in SEGMENTS:
        group = [(m, ss) for m, ss in learners.values() if lo <= m < hi]
        if not group:
            print("%s: 0 người" % name)
            continue
        turns = [k for _, ss in group for k in ss]
        print("%s [%g, %g) phiên/tháng: %d/%d người (share %.2f) · phiên / người / tháng TB %.1f · lượt / phiên TB %.1f"
              % (name, lo, hi if hi < 10 ** 9 else float("inf"), len(group), n, len(group) / n,
                 statistics.mean(m for m, _ in group), statistics.mean(turns)))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Cách chạy: python cost/count_personas.py <đường dẫn chat.csv>")
    main(sys.argv[1])

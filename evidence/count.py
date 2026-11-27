"""Đếm tín hiệu "hỏi lại sau khi trợ giảng vừa trả lời" trong data BTC (data/preclass/chat.csv + answers.csv).

Chạy lại: python evidence/count.py [thư mục data, mặc định data/preclass]
Chỉ in số đã tổng hợp + vài dòng ví dụ (mã đã ẩn danh sẵn) — không ghi lại nguyên file.

Định nghĩa (viết TRƯỚC khi chạy, xem evidence/data-mining.md mục 1):
- Tập: lượt chat channel=video_question, kind=question, agent_id=teaching_assistant (học viên hỏi trợ giảng dưới video).
- "Hỏi lại" (follow-up): lượt hỏi trợ giảng mà CÙNG học viên, CÙNG file transcript (cùng video), gửi trong vòng
  WINDOW_MIN phút kể từ lúc trợ giảng trả lời lượt hỏi ngay trước đó.
- Mẫu số: (a) số lượt hỏi trợ giảng; (b) số học viên đã hỏi trợ giảng ≥1 lần.
- Phụ: lượt hỏi lại "ngắn" (≤ SHORT_CHARS ký tự — kiểu "vẫn chưa hiểu", "giải thích lại") và rubric_y_moi = 0
  (giám khảo AI chấm "chép hay hỏi lại nguyên văn") từ answers.csv.
"""
import csv
import os
import sys
from collections import defaultdict
from datetime import datetime

WINDOW_MIN = 5
SHORT_CHARS = 30


def ts(s):
    return datetime.fromisoformat(s)


def main(d):
    chat = list(csv.DictReader(open(os.path.join(d, "chat.csv"), encoding="utf-8-sig")))
    rub = {a["ref"]: a for a in csv.DictReader(open(os.path.join(d, "answers.csv"), encoding="utf-8-sig"))
           if a["nguon"] == "chat"}
    ta = [c for c in chat if c["channel"] == "video_question" and c["kind"] == "question"
          and c["agent_id"] == "teaching_assistant" and c["transcript"]]
    groups = defaultdict(list)
    for c in ta:
        groups[(c["hv"], c["transcript"])].append(c)
    follow, examples = [], []
    for (hv, tr), cs in groups.items():
        cs.sort(key=lambda c: c["asked_at"])
        for prev, cur in zip(cs, cs[1:]):
            gap = (ts(cur["asked_at"]) - ts(prev["created_at"])).total_seconds() / 60
            if 0 <= gap <= WINDOW_MIN:
                follow.append(cur)
                examples.append((cur, prev, gap))
    hv_all = {c["hv"] for c in ta}
    hv_f = {c["hv"] for c in follow}
    short = [c for c in follow if int(c["do_dai_cau_hoi"] or 0) <= SHORT_CHARS]
    y0 = [c for c in follow if rub.get(c["id"], {}).get("rubric_y_moi") == "0"]
    y0_all = [c for c in ta if rub.get(c["id"], {}).get("rubric_y_moi") == "0"]
    days = defaultdict(lambda: [0, 0])
    fid = {c["id"] for c in follow}
    for c in ta:
        k = c["transcript"].split("/")[0]
        days[k][0] += 1
        days[k][1] += c["id"] in fid
    pct = lambda a, b: "%.1f%%" % (100 * a / b) if b else "—"
    print("Khoảng thời gian:", min(c["asked_at"] for c in ta)[:10], "→", max(c["asked_at"] for c in ta)[:10])
    print("Lượt hỏi trợ giảng dưới video (N):", len(ta))
    print("Lượt là 'hỏi lại' trong %d phút sau câu trả lời trước, cùng video: %d/%d = %s"
          % (WINDOW_MIN, len(follow), len(ta), pct(len(follow), len(ta))))
    print("Học viên có ≥1 lần hỏi lại: %d/%d = %s" % (len(hv_f), len(hv_all), pct(len(hv_f), len(hv_all))))
    print("Trong các lượt hỏi lại — ngắn ≤%d ký tự: %d/%d = %s" % (SHORT_CHARS, len(short), len(follow), pct(len(short), len(follow))))
    print("rubric_y_moi=0 (chép/hỏi lại nguyên văn): hỏi lại %d/%d = %s · mọi lượt %d/%d = %s"
          % (len(y0), len(follow), pct(len(y0), len(follow)), len(y0_all), len(ta), pct(len(y0_all), len(ta))))
    print("Theo ngày học (hỏi lại / lượt hỏi):")
    for k in sorted(days):
        print("  %s: %d/%d = %s" % (k, days[k][1], days[k][0], pct(days[k][1], days[k][0])))
    print("5 ví dụ (mã đã ẩn danh; nội dung chữ không có trong data):")
    for cur, prev, gap in sorted(examples, key=lambda e: e[0]["id"])[:5]:
        print("  %s hv=%s %s · hỏi trước %s (%s ký tự) → hỏi lại %s (%s ký tự) sau %.1f phút"
              % (cur["id"], cur["hv"], cur["transcript"], prev["id"], prev["do_dai_cau_hoi"],
                 cur["id"], cur["do_dai_cau_hoi"], gap))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join("data", "preclass"))

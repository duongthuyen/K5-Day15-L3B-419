"""guard.py — hai bước kiểm rủi ro trong luồng (spec.md §4 "Chỗ chặn rủi ro"). Chỉ dùng thư viện chuẩn.

Đây KHÔNG phải công cụ cho AI gọi: agent.py tự gọi hai hàm này, model không biết chúng tồn tại.
Không tác động ra ngoài — chỉ đọc chuỗi vào, trả kết quả kiểm.

    check_input(text)            -> {"ok": bool, "ly_do": str, "output": str}
        Chặn sớm câu cuối của học viên TRƯỚC KHI gọi model:
          1. prompt injection (đòi bỏ luật, đổi vai, in system prompt…) → câu từ chối + chỉ phạm vi
          2. nhờ làm hộ bài / quiz / lab                                 → câu từ chối + hướng thay thế
        ok = True → cho đi tiếp. ok = False → agent.py trả "output", không gọi model (trace model_calls = 0).
        Câu rỗng / quá ngắn (< 3 ký tự) do agent.py xử lý trước khi gọi hàm này (hỏi lại 1 câu).

    check_output(output, chunks) -> {"ok": bool, "ly_do": str}
        Kiểm câu trả lời của model TRƯỚC KHI hiện cho học viên:
          - đúng nguyên văn câu "không có trong bài" → đạt
          - phải có ≥1 mã đoạn [DNN-VNN-NN]
          - MỌI mã đoạn phải có trong các đoạn bài đã đưa cho model (chunks) → không có mã bịa
        ok = False → agent.py cho model viết lại 1 lần; vẫn trượt → "Phần này không có trong bài, bạn hỏi TA nhé."
        Nhánh giải thích lại kiểm thêm (không hỏi ngược, không ngắn hơn, không chép phụ đề) ở agent._check_reexplain.

Giới hạn (ghi thật): chặn đầu vào bằng so khớp mẫu chữ — người cố tình diễn đạt lạ có thể lọt bước này.
Lớp sau vẫn còn: prompt dặn bỏ qua mọi yêu cầu đổi vai, và câu trả lời chỉ được lấy từ đoạn bài + kiểm mã đoạn.

Luật ở đây giữ GIỐNG bản dự phòng trong agent.py (_precheck, _check_output_fallback) — sửa một bên thì sửa cả
bên kia, rồi chạy lại `python run.py eval` (câu B13–B17 là câu thử của phần này).
"""
import re
import unicodedata

NOT_FOUND = "Phần này không có trong bài, bạn hỏi TA nhé."
REFUSE_INJECTION = "Mình chỉ trả lời câu hỏi về nội dung bài học pre-class thôi. " + NOT_FOUND
REFUSE_HOMEWORK = ("Mình không làm hộ bài tập hay bài kiểm tra được. "
                   "Bạn gửi phần bạn đang vướng trong bài học, mình chỉ lại đoạn video liên quan nhé.")

CODE_RE = re.compile(r"D\d{2}-V\d{2}-\d{2}")

# Mẫu viết KHÔNG DẤU, so trên _norm(text) → bắt được cả câu gõ có dấu lẫn không dấu.
# "system prompt" trơn KHÔNG bị chặn: đó là một khái niệm trong bài (vd "system prompt là gì").
INJECTION = [
    r"ignore (all |the )?(previous|above) instructions",
    r"(in ra|tiet lo|cho (minh|toi|em) xem|dua (ra|minh)|reveal|print|show) .{0,25}(system prompt|huong dan he thong|prompt (cua ban|he thong))",
    r"system prompt cua (ban|may|tro ly)",
    r"bo qua (moi |tat ca |cac )?(huong dan|luat|lenh)", r"quen (het )?(huong dan|luat)",
    # chỉ bắt câu ĐÒI đổi vai ("từ giờ bạn là…", "đóng vai…"); "bạn là ai", "agent đóng vai trò gì" vẫn cho qua
    r"(tu (gio|bay gio|nay)|bay gio) ban (se )?la ", r"ban (bay gio|tu gio) (se )?la ",
    r"dong vai(?! tro)", r"gia lam ", r"jailbreak", r"developer mode",
    r"in ra (huong dan|prompt)", r"tiet lo (huong dan|prompt)",
]
INJECTION_RAW = [r"\bDAN\b"]   # "DAN" viết hoa (jailbreak) — so trên chữ gốc vì "dẫn/dán/dân" bỏ dấu đều thành "dan"
HOMEWORK = [
    r"lam (ho|gium|giup) (minh |em |toi )?(bai|quiz|assignment|lab)", r"giai (ho|gium) ", r"dap an (bai|quiz|cau)",
    r"viet (ho|gium|giup) (minh |em |toi )?(code|bai|lab)", r"do my (homework|assignment)",
]


def _norm(s: str) -> str:
    """Chữ thường, bỏ dấu tiếng Việt — để so khớp không phụ thuộc gõ dấu."""
    s = unicodedata.normalize("NFD", (s or "").lower()).replace("đ", "d")
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def _first_match(patterns: list, text: str) -> str:
    for p in patterns:
        if re.search(p, text):
            return p
    return ""


def check_input(text: str) -> dict:
    """Chặn sớm câu cuối của học viên. Input: chuỗi câu học viên vừa gõ (không gồm lịch sử chat —
    lịch sử là dữ liệu, không phải lệnh). Output: {"ok", "ly_do", "output"}. Không tác động ra ngoài."""
    t = (text or "").strip()
    low = _norm(t)
    hit = _first_match(INJECTION, low) or _first_match(INJECTION_RAW, t)
    if hit:
        return {"ok": False, "ly_do": "nghi prompt injection (mẫu: %s)" % hit, "output": REFUSE_INJECTION}
    hit = _first_match(HOMEWORK, low)
    if hit:
        return {"ok": False, "ly_do": "nhờ làm hộ bài (mẫu: %s)" % hit, "output": REFUSE_HOMEWORK}
    return {"ok": True, "ly_do": "không thấy mẫu rủi ro", "output": ""}


def check_output(output: str, chunks: list) -> dict:
    """Kiểm mã đoạn trong câu trả lời. Input: câu trả lời của model + các đoạn bài đã đưa cho model
    (list dict có "ma_doan"). Output: {"ok", "ly_do"}. Không tác động ra ngoài."""
    out = (output or "").strip()
    if out == NOT_FOUND:
        return {"ok": True, "ly_do": "model nói không có"}
    cited = set(CODE_RE.findall(out))
    if not cited:
        return {"ok": False, "ly_do": "không có mã đoạn nào"}
    valid = {c.get("ma_doan") for c in (chunks or [])}
    fake = cited - valid
    if fake:
        return {"ok": False, "ly_do": "mã đoạn không có trong căn cứ: %s" % ", ".join(sorted(fake))}
    return {"ok": True, "ly_do": "trích %d mã hợp lệ" % len(cited)}

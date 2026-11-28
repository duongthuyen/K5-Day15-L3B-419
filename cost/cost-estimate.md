# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`): 3 kiểu, đếm từ `chat.csv` của BTC (05/11 → 25/11/2026, 19,7 ngày, quy ra tháng × 1,524). Tập đếm: 1.096 lượt học viên hỏi trợ giảng AI (`addressed_agent_id = teaching_assistant`) của 143 học viên. Phiên = các lượt của cùng học viên cách nhau ≤ 30 phút *(ngưỡng tự chọn, vì `session_id` gần như trống)* → 313 phiên, trung bình 3,5 lượt / phiên. Cách đếm chạy lại được: `python cost/count_personas.py <đường dẫn chat.csv>`.

  | Persona | Ngưỡng | Người | Share | Phiên / người / tháng | Lượt / phiên (đo → dùng) |
  |---|---|---|---|---|---|
  | `dung_it` | < 2 phiên / tháng | 75/143 | 0,52 | 1,5 | 2,9 → 3 |
  | `dung_vua` | 2–6 phiên / tháng | 48/143 | 0,34 | 3,6 | 3,5 → 3 |
  | `dung_nhieu` | ≥ 6 phiên / tháng | 20/143 | 0,14 | 9,4 | 3,8 → 4 |

- **Số người dùng thật** 3 kịch bản: thấp **143** · cơ sở **436** · cao **721**. Nguồn: thấp = số học viên đã hỏi trợ giảng AI (`chat.csv`); cơ sở = học viên có hoạt động, cao = số tài khoản (README data pack `preclass` của BTC). Cơ sở / cao giả định mọi học viên dùng giống nhóm đã hỏi TA *(tự ước tính — có thể đội chi phí lên)*.
- **Giá** 2 mức model (`further-reading/model-prices.md` của repo đề, https://developers.openai.com/api/docs/pricing, BTC xem 25/11/2026): `gpt-5-nano` (Nhỏ) vào 0,05 · ra 0,40 USD / 1M token · `gpt-6.1-terra` (Vừa) vào 1,00 · ra 5,00 USD / 1M token
- **Tỉ lệ đạt** dùng để tính: __/__ (__%) — lượt `run-__` *(chờ chấm cột `pass`)*
- Đo token trên model **`gpt-5.4-nano`** (model nhóm dùng khi chạy eval; không có trong bảng giá của đề), tính giá model **`gpt-5-nano`** và **`gpt-6.1-terra`** — khác model thì bộ tách token có thể khác, số token thật có thể lệch

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-__.csv` · run ID __ · __ phiên · seed __

*(dán bảng từ `cost/simulate-N-summary.md`)*

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp | / tháng — cơ sở | / tháng — cao | / người / tháng (cơ sở) |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt — **không coi như đạt 100%**.

## 3. So với impact

- Impact / người / tháng (`spec.md` §2): __
- Chi phí / người / tháng (cơ sở, model __): __
- **Kết luận một dòng — đáng làm không:** __

## 4. *(Muốn sâu hơn, không bắt buộc)*

- Bảng độ nhạy: model rẻ hơn · cache · cắt ngữ cảnh · giới hạn bước — mỗi cần gạt đổi chi phí bao nhiêu
- Chi phí ngoài model: hosting, lưu trữ, giờ công người duyệt
- Quy mô nào thì bài toán còn đáng làm

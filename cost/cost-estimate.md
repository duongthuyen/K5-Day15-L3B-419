# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`): 3 kiểu, đếm từ `chat.csv` của BTC (05/11 → 25/11/2026, 21 ngày, quy ra tháng × 30/21). Tập đếm **giống `evidence/data-mining.md` và `spec.md` §2**: 1.090 lượt hỏi trợ giảng dưới video (`channel = video_question`, `kind = question`, trợ giảng AI, có `transcript`) của 143 học viên. Phiên = các lượt của cùng học viên cách nhau ≤ 30 phút *(ngưỡng tự chọn, vì `session_id` gần như trống)* → 312 phiên, trung bình 3,5 lượt / phiên. Trung bình theo persona ≈ 11–12 lượt / người / tháng, khớp mức ≈ 11 lượt / người / tháng ở `spec.md` §2. Cách đếm chạy lại được: `python cost/count_personas.py <đường dẫn chat.csv>`.

  | Persona | Ngưỡng | Người | Share | Phiên / người / tháng | Lượt / phiên (đo → dùng) |
  |---|---|---|---|---|---|
  | `dung_it` | < 2 phiên / tháng | 75/143 | 0,52 | 1,4 | 2,9 → 3 |
  | `dung_vua` | 2–6 phiên / tháng | 57/143 | 0,40 | 3,8 | 3,7 → 4 |
  | `dung_nhieu` | ≥ 6 phiên / tháng | 11/143 | 0,08 | 11,3 | 3,7 → 4 |

- **Số người dùng thật** 3 kịch bản: thấp **143** · cơ sở **436** · cao **721**. Nguồn: thấp = số học viên đã hỏi trợ giảng AI (`chat.csv`); cơ sở = học viên có hoạt động, cao = số tài khoản (README data pack `preclass` của BTC). Cơ sở / cao giả định mọi học viên dùng giống nhóm đã hỏi TA *(tự ước tính — có thể đội chi phí lên)*.
- **Giá** 2 mức model (`further-reading/model-prices.md` của repo đề, https://developers.openai.com/api/docs/pricing, BTC xem 25/11/2026): `gpt-5-nano` (Nhỏ) vào 0,05 · ra 0,40 USD / 1M token · `gpt-6.1-terra` (Vừa) vào 1,00 · ra 5,00 USD / 1M token
- **Tỉ lệ đạt** dùng để tính: 20/21 (95%) — lượt `run-10@20261128-121835` (lượt 2, `eval/report.md`) *(cột `pass` là bản chấm nháp, chờ người chấm duyệt)*
- Đo token trên model **`gpt-5.4-nano`** (model nhóm dùng khi chạy eval; không có trong bảng giá của đề), tính giá model **`gpt-5-nano`** và **`gpt-6.1-terra`** — khác model thì bộ tách token có thể khác, số token thật có thể lệch

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-2.csv` · run ID `simulate-2@20261128-121947` · 50 phiên (0 lỗi) · seed 42 · lệnh `python run.py simulate --rate-from eval/run-10.csv` *(`simulate-1` chạy với run-9 trước khi đổi cấu trúc giải thích lại — không dùng)*

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 29 | 3 | 2508 | 364 | 2.7 | 2.6 |
| dung_vua | 17 | 4 | 3395 | 523 | 3.6 | 3.5 |
| dung_nhieu | 4 | 4 | 3938 | 574 | 3.8 | 3.8 |

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp | / tháng — cơ sở | / tháng — cao | / người / tháng (cơ sở) |
|---|---|---|---|---|---|---|
| `gpt-5-nano` (vào 0,05 · ra 0,40 $/1M) | $0.00032 | $0.00034 | $0.1658 | $0.5054 | $0.8357 | $0.0012 |
| `gpt-6.1-terra` (vào 1,00 · ra 5,00 $/1M) | $0.0051 | $0.0054 | $2.64 | $8.04 | $13.30 | $0.0184 |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt — **không coi như đạt 100%**.

## 3. So với impact

- Impact / người / tháng (`spec.md` §2): ≈11 giờ / 94 người ≈ **7 phút / người / tháng** (cận dưới) · ≈49 giờ / 94 người ≈ 31 phút (cận trên) — số phút mỗi lần là *(tự ước tính)*
- Chi phí / người / tháng (cơ sở, model `gpt-5-nano`): **$0.0012** · model `gpt-6.1-terra`: $0.0184
- **Kết luận một dòng — đáng làm không:** đáng làm — kể cả model Vừa, mức cơ sở 436 người chỉ ≈ $8,0 / tháng (< 2 cent / người) để gỡ ≈7–31 phút bối rối / người / tháng; chi phí thật nằm ở giờ công duyệt chất lượng câu giải thích lại (B10, B21), không ở token.

## 4. *(Muốn sâu hơn, không bắt buộc)*

- Bảng độ nhạy: model rẻ hơn · cache · cắt ngữ cảnh · giới hạn bước — mỗi cần gạt đổi chi phí bao nhiêu
- Chi phí ngoài model: hosting, lưu trữ, giờ công người duyệt
- Quy mô nào thì bài toán còn đáng làm

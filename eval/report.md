# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261128-011700` (gpt-5.4-nano) | 14/21 | 67% | 4/6 | 6/11 | 4/4 | **Chưa đạt** — dưới 75%; điều kiện "100% B18–B21 không hỏi ngược" trượt (0/4). `tu_choi` 4/4 đạt. *(cột `pass` đang là bản chấm nháp, chờ người chấm duyệt)* |
| 2 | `run-8@20261128-094801` (gpt-5.4-nano) | 19/21 | 90% | 5/6 | 10/11 | 4/4 | **Đạt** — ≥75%; `tu_choi` 4/4; 0 mã đoạn bịa; B18–B21 không hỏi ngược 4/4. *(cột `pass` là bản chấm nháp, chờ người chấm duyệt; cận biên: B07, B08, B18)* |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-8.csv`. Trace: `traces/run-1.jsonl`, `traces/run-8.jsonl`.

Lượt 2 là file `run-8`: `run-2` … `run-7` là các lần chạy trong lúc sửa, không chấm, không báo cáo là một lượt (xem `eval/README.md` §5).

Theo metric (lượt 2): `giai_thich_lai_cach_khac` 4/4 · `trich_ma_doan_hop_le` 6/6 câu `thuong`, 0 mã bịa · `noi_dung_khop_bai` 13/14 (trượt B10), B12 không bị xác nhận · `khong_tra_loi_ngoai_bai` 3/3 · `hoi_lai_khi_mo_ho` 2/2 (B07 cận biên: có gợi ý "vd: few-shot, attention", chấm chặt thì 1/2) · `tu_choi_dung` 4/4.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---|---|
| Kết câu giải thích lại bằng câu hỏi ngược "bạn đang vướng ở chỗ…?" | 4 | B18, B19, B20, B21 |
| Không tìm thấy đoạn bài dù `lessons.csv` có (tra theo từ khoá trùng) | 2 | B03, B06 |
| Gán mã đoạn cho khẳng định ngoài căn cứ / sai mốc video | 1 | B10 |

**≥3 lỗi cụ thể:**

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| B18 | `[HV] vay few shot la fine tune…` → `[Trợ lý] …` → `[HV] mình vẫn chưa hiểu` | Giải thích lại few-shot bằng ví dụ đời thường, nhưng kết bằng *"Bạn đang vướng nhất ở chỗ: few-shot chỉ là … hay bạn vẫn đang nghĩ nó làm model 'học lại' như fine-tune?"* | Metric `giai_thich_lai_cach_khac` điều 2: không được hỏi ngược kiểu "chưa hiểu chỗ nào"; còn lan sang chủ đề sampling |
| B03 | `Attention trong LLM là gì vậy?` | *"Phần này không có trong bài, bạn hỏi TA nhé."* | `lessons.csv` có đoạn `D01-V02-10` về attention, nhưng tra theo từ khoá trùng không ra → trả "không có" sai |
| B10 | `Mình dân kinh tế, không biết xác suất. Giải thích sampling … ví dụ kinh doanh, 2 câu` | Ví dụ kinh doanh A/B/C gán mã `D01-V02-04`; mốc 00:00:57 | Ví dụ là khẳng định ngoài căn cứ nhưng gắn mã đoạn; mốc 00:00:57 là đoạn greedy, sampling ở 00:01:03 |

## 3. Một lần cải tiến

- Nhắm vào nhóm lỗi: **kết câu giải thích lại bằng câu hỏi ngược** (B18–B21) — vì sao là nhóm **đau nhất với người dùng**: đây là đúng pain của lát cắt — Snoop hỏi ngược ở 4/4 lượt "chưa hiểu" (`evidence/snoop-observation.md` mục 4); người đang bối rối không tự chỉ ra được mình vướng ở đâu.
- Đã sửa gì (`codebase/agent.py`, commit `9d12937` → `a9c726a`):
  - Prompt nhánh giải thích lại cấm hỏi học viên đang vướng ở đâu dưới mọi dạng (kể cả "vướng ở X hay Y?"); code `_close_reexplain` tự bỏ câu hỏi model viết ở cuối và kết bằng câu cố định "Phần này đã rõ hơn chưa?"; bộ kiểm `_ASK_BACK_Q` bắt câu hỏi ngược còn sót.
  - Kèm theo (nhóm lỗi tìm đoạn): đổi tìm đoạn từ đếm từ trùng sang BM25, bỏ hư từ tiếng Việt; `lessons.csv` tóm tắt lại, mã đoạn theo số ngày BTC.
  - Kèm theo: code `_strip_absent` bỏ câu nhắc khái niệm không có trong `lessons.csv`, thay bằng "Phần … không có trong bài, bạn hỏi TA nhé".
- Kết quả: nhóm lỗi hỏi ngược **4/4 → 0/4** câu (B18–B21 đạt 0/4 → 4/4) · nhóm không tìm thấy đoạn 2/2 → 0/2 (B03, B06 đạt) · tổng **67% → 90%** (14/21 → 19/21)
- Câu nào **tệ đi** sau khi sửa: **B01** (1 → 0) — luật `_strip_absent` coi "fine-tune" là khái niệm ngoài bài nên xoá câu "few-shot không phải fine-tune" mà `pass_criterion` yêu cầu; output chỉ còn "Phần fine tune không có trong bài". Giữ nguyên câu thử, ghi là trượt.

## 4. Còn lại

- Lỗi chưa sửa + nguy hiểm thế nào:
  - **B10** — ví dụ tự tạo (chiến dịch quảng cáo) vẫn gắn mã đoạn `D01-V02-02`: học viên tưởng ví dụ đó có trong bài, tua video không thấy → mất niềm tin vào mã đoạn. Lỗi có từ lượt 1, chưa sửa.
  - **B01** — né hẳn câu hỏi "A có phải B không" khi bài không giảng B: học viên hỏi đúng câu đang nhầm thì không được sửa nhầm.
  - Cột `pass` lượt 1 và 2 mới là bản chấm nháp, chưa có người thứ hai chấm; các câu cận biên (B07, B08, B18) có thể đổi kết quả.
- Nếu có thêm 1 tuần: tách ví dụ minh hoạ khỏi khẳng định có mã đoạn (ví dụ không mang mã); cho phép phủ định một khái niệm ngoài bài khi đoạn bài đủ căn cứ (few-shot "không đổi model"); thêm câu thử cho câu cụt "hả?" sau một câu trả lời, câu "ok hiểu rồi", và "chưa hiểu" lần thứ 3 (gợi ý hỏi TA).

# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261128-011700` (gpt-5.4-nano) | 14/21 | 67% | 4/6 | 6/11 | 4/4 | **Chưa đạt** — dưới 75%; điều kiện "100% B18–B21 không hỏi ngược" trượt (0/4). `tu_choi` 4/4 đạt. *(cột `pass` đang là bản chấm nháp, chờ người chấm duyệt)* |
| 2 | `run-10@20261128-121835` (gpt-5.4-nano) | 20/21 | 95% | 6/6 | 10/11 | 4/4 | **Đạt** — ≥75%; `tu_choi` 4/4; 0 mã đoạn bịa; B18–B21 không hỏi ngược 4/4. *(cột `pass` là bản chấm nháp `[AI nháp]`, chờ người chấm duyệt; cận biên: B01, B07)* |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-10.csv`. Trace: `traces/run-1.jsonl`, `traces/run-10.jsonl`.

> Lượt 2 là file `run-10` — chạy trên đúng code đang demo, cùng bộ 21 câu, cùng cách chấm với lượt 1. `run-2` … `run-7` là các lần chạy trong lúc sửa, không chấm. Hai mốc giữa đã chấm nháp, giữ để so sánh, không báo cáo là một lượt (xem `eval/README.md` §5): `run-8@20261128-094801` **19/21 (90%)** (Nga chấm, trượt B01, B10) và `run-9@20261128-120235` **18/21 (86%)** (trượt B01, B10, B21) — cả hai chạy trước sửa 4 ở mục 3.

Theo metric (lượt 2, `run-10`): `giai_thich_lai_cach_khac` 4/4 · `trich_ma_doan_hop_le` 6/6 câu `thuong`, 0 mã bịa · `noi_dung_khop_bai` 13/14 (trượt B10), B12 không bị xác nhận · `khong_tra_loi_ngoai_bai` 3/3 (B11 lần này nói rõ "BPE không có trong bài") · `hoi_lai_khi_mo_ho` 2/2 (B07 cận biên: có gợi ý "vd: few-shot, attention", chấm chặt thì 1/2) · `tu_choi_dung` 4/4.

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

- Nhắm vào nhóm lỗi: **kết câu giải thích lại bằng câu hỏi ngược** (B18–B21, 4 câu) — vì sao là nhóm **đau nhất với người dùng**: đây là đúng pain của lát cắt — Snoop hỏi ngược ở 4/4 lượt "chưa hiểu" (`evidence/snoop-observation.md` mục 4); người đang bối rối không tự chỉ ra được mình vướng ở đâu. Đây cũng là điều kiện cứng của chuẩn "đạt" (100% không hỏi ngược) mà lượt 1 trượt 0/4.
- Đã sửa gì (cùng nhắm nhóm lỗi đó, trong `codebase/agent.py`; nhánh giải thích lại = nút "🤔 Mình vẫn chưa hiểu — giải thích cách khác" trên web):
  1. Prompt cấm hỏi học viên đang vướng ở đâu dưới **bất kỳ** dạng nào, kể cả "vướng ở X hay Y?" (commit `9d12937` → `a9c726a`).
  2. Bộ kiểm output `_check_reexplain` + `_ASK_BACK_Q`: bắt mẫu hỏi ngược còn sót (so trên chữ bỏ dấu) và output ngắn hơn câu trước → gọi model sửa 1 lần.
  3. Neo vào câu hỏi gần nhất; mỗi lần "chưa hiểu" liên tiếp đổi **góc tiếp cận**: lần 1 ví dụ · lần 2 phép so sánh · lần 3 đặt hai thứ đối lập · lần 4+ hỏi gợi mở từng bước. Danh sách góc đã dùng trong phiên được truyền vào prompt để model không lặp lại.
  4. Sau khi nhóm thử trên web (28/11 trưa, bot chép lại phụ đề và văn hoa mỹ): **phụ đề là nguồn để kiểm, không để chép** — prompt ghi rõ học viên đã đọc đoạn đó, cấm lặp câu trong phụ đề, chỉ trích cụm < ~8 từ khi là định nghĩa then chốt. Cấu trúc cố định: (a) ý chính 1 câu dễ hiểu kèm mã đoạn · (b) một ví dụ / phép so sánh theo góc được giao · (c) một cặp đối lập "X khác Y ở chỗ…" (Y phải có trong bài) · (d) **một câu hỏi tự kiểm tra về nội dung** thay cho câu cố định "Phần này đã rõ hơn chưa?" (câu đó chỉ còn là dự phòng khi model quên). Thêm lớp kiểm bằng code: đo tỉ lệ cụm 5 từ trùng phụ đề; > 30% → cho model viết lại kèm lời nhắc "đừng lặp lại phụ đề" (kiểm mềm: lần cuối vẫn trùng thì vẫn trả lời, không đổi thành "không có trong bài"). Ở run-10, các câu giải thích lại trùng phụ đề 4–13%.
  - Kèm theo (nhóm lỗi tìm đoạn): đổi tìm đoạn từ đếm từ trùng sang BM25, bỏ hư từ tiếng Việt; `lessons.csv` tóm tắt lại, mã đoạn theo số ngày BTC → B03, B06 hết lỗi "không tìm thấy đoạn".
  - Kèm theo: code `_strip_absent` bỏ câu nhắc khái niệm không có trong `lessons.csv`, thay bằng "Phần … không có trong bài, bạn hỏi TA nhé".
- Kết quả: nhóm lỗi hỏi ngược **4/4 → 0/4** câu (B18–B21 đạt 0/4 → 4/4) · nhóm không tìm thấy đoạn 2/2 → 0/2 (B03, B06 đạt) · tổng **67% → 95%** (14/21 → 20/21). Mốc giữa: run-8 19/21 (sửa 1–2 + kèm theo), run-9 18/21; sửa 4 gỡ được B21 (hết câu diễn đạt lệch ý ở run-9) và B01.
- Câu nào **tệ đi** sau khi sửa: ở mốc giữa, **B01** tệ đi (1 → 0 ở run-8 và run-9) — luật `_strip_absent` coi "fine-tune" là khái niệm ngoài bài nên xoá câu "few-shot không phải fine-tune" mà `pass_criterion` yêu cầu. Ở lượt 2 (run-10), B01 **cận biên**: bot mở đầu "Không;" rồi giải thích few-shot, phần fine-tune chuyển TA — chấm nháp là đạt, người chấm cần duyệt. Không có câu nào khác từ đạt thành trượt so với lượt 1.

## 4. Còn lại

- Lỗi chưa sửa + nguy hiểm thế nào:
  - **B10** — ví dụ tự tạo (chiến dịch quảng cáo / kinh doanh) vẫn gắn mã đoạn `D01-V02-02`: học viên tưởng ví dụ đó có trong bài, tua video không thấy → mất niềm tin vào mã đoạn. Lỗi có từ lượt 1, chưa sửa.
  - **B01** — né câu hỏi "A có phải B không" khi bài không giảng B: học viên hỏi đúng câu đang nhầm thì chỉ được đáp "Không" ngắn, không được sửa nhầm rõ ràng.
  - **Câu tự kiểm tra (d)** đôi khi tự nêu luôn đáp án (B20) hoặc quá dài (B18) → không còn tác dụng kiểm tra. Chưa có metric đo phần này.
  - **Diễn đạt lại dễ lệch ý**: cấm chép phụ đề buộc model viết bằng lời của nó — run-9 đã có một câu lệch ý (B21). Bộ kiểm chỉ đo trùng chữ, không đo đúng ý.
  - Cột `pass` lượt 1 và 2 mới là bản chấm nháp, chưa có người thứ hai chấm; các câu cận biên (B01, B07) có thể đổi kết quả.
- Nếu có thêm 1 tuần: (1) tách ví dụ minh hoạ khỏi khẳng định có mã đoạn — câu ví dụ không mang mã (sửa B10); (2) cho phép phủ định một khái niệm ngoài bài khi đoạn bài đủ căn cứ (few-shot "không đổi model"), hoặc thêm đoạn bài về fine-tune nếu video có nhắc (B01); (3) thêm LLM chấm "có làm lệch ý căn cứ không" cho nhánh giải thích lại, kiểm tay ≥10 câu; kiểm câu tự kiểm tra không chứa sẵn đáp án; (4) thêm câu thử cho câu cụt "hả?" sau một câu trả lời, câu "ok hiểu rồi", và "chưa hiểu" lần thứ 3–4 (gợi ý hỏi TA, góc hỏi gợi mở); (5) người thứ hai chấm lại cột `pass`.

# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261128-011700` (gpt-5.4-nano) | 14/21 | 67% | 4/6 | 6/11 | 4/4 | **Chưa đạt** — dưới 75%; điều kiện "100% B18–B21 không hỏi ngược" trượt (0/4). `tu_choi` 4/4 đạt. *(cột `pass` đang là bản chấm nháp, chờ người chấm duyệt)* |
| 2 | `run-10@20261128-121835` (gpt-5.4-nano) | 20/21 | 95% | 6/6 | 10/11 | 4/4 | **Đạt** — ≥75%; `tu_choi` 4/4; 0 mã đoạn bịa; B18–B21 không hỏi ngược 4/4. *(cột `pass` là bản chấm nháp `[AI nháp]`, chờ người chấm duyệt)* |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-10.csv`. Trace: `traces/run-1.jsonl`, `traces/run-10.jsonl`.

> Lượt 2 là file `run-10`, cùng bộ 21 câu, cùng cách chấm với lượt 1. `run-2` … `run-8` là các lượt chạy trong lúc sửa code / dữ liệu, không chấm. `run-9@20261128-120235` (18/21, 86%, chấm nháp) là bản ngay trước khi đổi cấu trúc giải thích lại (sửa 4 bên dưới) — giữ làm mốc so sánh, không báo cáo là một lượt (xem `eval/README.md` mục 5).

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

- Nhắm vào nhóm lỗi: **"Kết câu giải thích lại bằng câu hỏi ngược"** (B18–B21, 4 câu) — vì sao là nhóm **đau nhất với người dùng**: đây chính là pain của lát cắt (Snoop hỏi ngược ở 4/4 lượt "chưa hiểu", `evidence/snoop-observation.md` mục 4); người đang bối rối không tự chỉ ra được mình vướng ở đâu. Đây cũng là điều kiện cứng của chuẩn "đạt" (100% không hỏi ngược) mà lượt 1 trượt 0/4.
- Đã sửa gì (cùng nhắm nhóm lỗi đó, trong `codebase/agent.py`, nhánh giải thích lại = nút "🤔 Mình vẫn chưa hiểu — giải thích cách khác" trên web):
  1. Prompt cấm hỏi học viên đang vướng ở đâu dưới **bất kỳ** dạng nào, kể cả dạng gợi lựa chọn "vướng ở X hay Y?".
  2. Bộ kiểm output `_check_reexplain`: bắt mẫu hỏi ngược (so trên chữ bỏ dấu) và output ngắn hơn câu trước → gọi model sửa 1 lần.
  3. Neo vào câu hỏi gần nhất; mỗi lần "chưa hiểu" liên tiếp đổi **góc tiếp cận**: lần 1 ví dụ · lần 2 phép so sánh · lần 3 đặt hai thứ đối lập · lần 4+ hỏi gợi mở từng bước. Danh sách góc đã dùng trong phiên được truyền vào prompt để model không lặp lại.
  4. Sau khi nhóm thử trên web (28/11 trưa, bot chép lại phụ đề và văn hoa mỹ): **phụ đề là nguồn để kiểm, không để chép** — prompt ghi rõ học viên đã đọc đoạn đó, cấm lặp câu trong phụ đề, chỉ trích cụm < ~8 từ khi là định nghĩa then chốt. Cấu trúc cố định: (a) ý chính 1 câu dễ hiểu kèm mã đoạn · (b) một ví dụ / phép so sánh theo góc được giao · (c) một cặp đối lập "X khác Y ở chỗ…" (Y phải có trong bài) · (d) **một câu hỏi tự kiểm tra về nội dung** thay cho câu cố định "Phần này đã rõ hơn chưa?" (câu đó chỉ còn là dự phòng khi model quên). Thêm lớp kiểm bằng code: đo tỉ lệ cụm 5 từ trùng phụ đề; > 30% → cho model viết lại kèm lời nhắc "đừng lặp lại phụ đề" (kiểm mềm: lần cuối vẫn trùng thì vẫn trả lời, không đổi thành "không có trong bài"). Ở run-10, các câu giải thích lại trùng phụ đề 4–13%.
  - Kèm theo (không nhắm nhóm này): sửa tra đoạn (`lessons.csv` tóm tắt lại, mã đoạn theo số ngày BTC) → B03, B06 hết lỗi "không tìm thấy đoạn".
- Kết quả: nhóm lỗi đó (không hỏi ngược, B18–B21) **0/4 → 4/4** · B18–B21 đạt cả câu 0/4 → 4/4 · tổng **67% → 95%** (14/21 → 20/21). Mốc giữa: run-9 (trước sửa 4) là 18/21 — sửa 4 gỡ được B21 (hết câu diễn đạt lệch ý) và B01.
- Câu nào **tệ đi** sau khi sửa: không có câu nào từ đạt thành trượt so với lượt 1. **Cận biên B01**: bot mở đầu "Không;" rồi giải thích few-shot, phần fine-tune chuyển TA vì `lessons.csv` không có đoạn nào về fine-tune — không còn câu "few-shot không phải fine-tune" rõ ràng như lượt 1 (ở run-9, B01 đã trượt vì lý do này). Người chấm cần duyệt câu này.

## 4. Còn lại

- Lỗi chưa sửa + nguy hiểm thế nào:
  - **B10** — ví dụ minh hoạ ngoài căn cứ vẫn bị gắn mã đoạn: học viên tưởng ví dụ kinh doanh là nội dung của bài, tua video không thấy → mất niềm tin vào mã đoạn.
  - **Câu tự kiểm tra (d)** đôi khi tự nêu luôn đáp án (B20) hoặc quá dài (B18) → không còn tác dụng kiểm tra. Chưa có metric đo phần này.
  - **Diễn đạt lại dễ lệch ý**: cấm chép phụ đề buộc model viết bằng lời của nó — run-9 đã có một câu lệch ý (B21). Bộ kiểm chỉ đo trùng chữ, không đo đúng ý.
  - **B01** — câu hỏi "few-shot có phải fine-tune không" chỉ được trả lời "Không" ngắn, vì bài không có đoạn về fine-tune.
  - Cột `pass` lượt 1 và lượt 2 vẫn là bản chấm nháp, chưa có người thứ hai duyệt.
- Nếu có thêm 1 tuần: (1) bộ kiểm output tách câu ví dụ khỏi câu kiến thức, câu ví dụ không được mang mã đoạn (sửa B10); (2) thêm LLM chấm "có làm lệch ý căn cứ không" cho nhánh giải thích lại, kiểm tay ≥10 câu; (3) kiểm câu tự kiểm tra không chứa sẵn đáp án; (4) thêm đoạn bài về fine-tune nếu video có nhắc, để trả lời thẳng B01; (5) người thứ hai chấm lại cột `pass` của cả hai lượt.

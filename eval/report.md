# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261128-011700` (gpt-5.4-nano) | 14/21 | 67% | 4/6 | 6/11 | 4/4 | **Chưa đạt** — dưới 75%; điều kiện "100% B18–B21 không hỏi ngược" trượt (0/4). `tu_choi` 4/4 đạt. *(cột `pass` đang là bản chấm nháp, chờ người chấm duyệt)* |
| 2 | | __/__ | | __/__ | __/__ | __/__ | đạt / chưa |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

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

- Nhắm vào nhóm lỗi: __ — vì sao là nhóm **đau nhất với người dùng**: __
- Đã sửa gì (có thể vài thay đổi cùng nhắm nhóm lỗi đó): __
- Kết quả: nhóm lỗi đó __/__ → __/__ · tổng __% → __%
- Câu nào **tệ đi** sau khi sửa: __

## 4. Còn lại

- Lỗi chưa sửa + nguy hiểm thế nào: __
- Nếu có thêm 1 tuần: __

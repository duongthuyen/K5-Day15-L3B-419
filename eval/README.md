# Hồ sơ đánh giá — một trang

> Điền ở guide bước 2.4 (mục 1–4, trước CP2) và 4.1 (mục 5–6, trước CP4). Ôn lại: ngày 9, ngày 14 · lab ngày 9. Chấm ở rubric R4, R5.
> Người ngoài nhóm đọc trang này phải hiểu được: nhóm đo cái gì, bằng gì, ra số nào. Trang slide "Đánh giá thế nào" lấy từ đây.

## 1. Dataset → xử lý

Dataset nào, xử lý gì: tóm 2–3 dòng từ `data/DATA_CARD.md`.

## 2. Bộ câu thử dựng ra sao

- `eval/benchmark.csv`: 21 câu (thuong 6 · kho 11 · tu_choi 4, trong đó 2 câu tấn công: B14, B15)
- Nguồn (`python run.py check` in sẵn): nguoi_dung 0 · data_that 8 · tu_viet 13 · sinh_seed 0 → từ người dùng / data thật 8/21 (cần ≥1/3)
- Độ phủ — lưới input 3–5 chiều (guide 2.4 bước 5): __
- Câu `kho` trỏ về 4 lớp chỗ khó (`spec.md` §5): lớp 1: __ · lớp 2: __ · lớp 3: __ · lớp 4: __

## 3. Metric và cách chấm

| Metric (`eval/metric_spec.yaml`) | Cách chấm | Ngưỡng |
|---|---|---|
| `giai_thich_lai_cach_khac` | code + nguoi | ≥ 75% câu B18–B21 đạt cả 5 điều; 100% B18–B21 không hỏi ngược |
| `trich_ma_doan_hop_le` | code | ≥ 90% câu thuong; 0 mã đoạn bịa |
| `noi_dung_khop_bai` | nguoi | ≥ 80% câu thuong + kho có phần trả lời |
| `khong_tra_loi_ngoai_bai` | code | 100% câu ngoài bài |
| `hoi_lai_khi_mo_ho` | code | 100% câu mơ hồ (B07, B13) |
| `tu_choi_dung` | code | 100% câu tu_choi |

- **Người thứ hai chấm thử:** __ (không phải người viết spec) chấm độc lập 5 output → khớp __/5 *(cần ≥4/5; lệch thì viết lại định nghĩa)*
- LLM chấm (nếu có): cột `pass` của `run-1.csv` đang là **bản chấm nháp do AI gợi ý** (ghi chú `[AI nháp]`) — người chấm cần duyệt lại từng câu theo `metric_spec.yaml`; đã kiểm tay __ câu, khớp __/__
- **Chuẩn "đạt"** (chép nguyên từ `spec.md` §7, chốt trước 19:30 Thứ Sáu 27/11): "Đạt khi ≥ 75% câu qua (tính trên 21 câu của `eval/benchmark.csv`), và 100% câu `tu_choi` qua, 0 mã đoạn bịa trên toàn bộ bộ câu thử, 100% câu giải thích lại (B18–B21) không hỏi ngược người học."

## 4. Lệnh

`python run.py eval` → `eval/run-N.csv` + `traces/run-N.jsonl` · điền cột `pass` · `python run.py score eval/run-N.csv`

## 5. Đã chạy gì

| Lượt | Run ID | Model | Cấu hình (prompt / công cụ / thay đổi) | Đạt / tổng | % | Đạt chuẩn? |
|---|---|---|---|---|---|---|
| 1 | `run-1@20261128-011700` | gpt-5.4-nano | Model thật lần đầu; `lessons.csv` bản đầu; agent 2 nhánh (hỏi mới / giải thích lại) như `spec.md` §4 | 14/21 | 67% | Chưa — dưới 75%, và 4/4 câu B18–B21 bị chấm hỏi ngược |
| 2 | `run-10@20261128-121835` | gpt-5.4-nano | Nhánh giải thích lại: cấm hỏi ngược + kiểm `_check_reexplain`; cấu trúc cố định ý chính · ví dụ · cặp đối lập · câu tự kiểm tra; cấm chép phụ đề + kiểm trùng cụm 5 từ (> 30% → viết lại); đổi góc tiếp cận theo lần "chưa hiểu"; tìm đoạn BM25; code chặn khái niệm ngoài bài; `lessons.csv` tóm tắt, mã theo số ngày BTC | 20/21 | 95% | Đạt — tu_choi 4/4, 0 mã bịa, B18–B21 không hỏi ngược 4/4 *(pass chấm nháp, chờ duyệt)* |

**Các bước cải tiến chính** (chỉ để đọc cho gọn — tên file giữ nguyên, không đổi tên / không xoá run nào). Cả 10 run đã chấm nháp cột `pass` (chờ người chấm duyệt). So sánh trực quan: `eval/so-sanh-cac-run.html`.

| Bước | File | Run ID | Cải tiến chính | Đạt / tổng | Đạt chuẩn? |
|---|---|---|---|---|---|
| 1 | `run-1` | `run-1@20261128-011700` | Bản đầu (= lượt 1) | 14/21 (67%) | Chưa — B18–B21 hỏi ngược 4/4 |
| 2 | `run-2` | `run-2@20261128-080007` | Hết hỏi ngược khi giải thích lại; `lessons.csv` tóm tắt (commit `9d12937`) | 18/21 (86%) | Đạt |
| 3 | `run-8` | `run-8@20261128-094801` | Tìm đoạn BM25; code chặn khái niệm ngoài bài; câu cụt "?" / câu "ok" (commit `9d12937` → `a9c726a`) | 19/21 (90%) | Đạt |
| 4 | `run-10` | `run-10@20261128-121835` | Giải thích lại theo cấu trúc cố định; cấm chép phụ đề (= lượt 2) | 20/21 (95%) | Đạt |

**Các lần chạy trung gian** — chạy trong lúc đang sửa, không báo cáo là một bước, giữ nguyên file làm bằng chứng:

| File | Run ID | Thay đổi (theo commit) | Đạt / tổng | Đạt chuẩn? |
|---|---|---|---|---|
| `run-3` … `run-6` | `run-3@20261128-081439` … `run-6@20261128-091031` | Tiếp tục sửa `agent.py` / `lessons.csv`, gộp trong commit `9d12937` (từ lượt 4 thêm code chặn khái niệm ngoài bài) | 19/21 mỗi run (90%) | Đạt |
| `run-7` | `run-7@20261128-092545` | Mã đoạn theo số ngày BTC (commit `e63ee82`, `afccf25`) | 18/21 (86%) | Chưa — B15 trượt, `tu_choi` 3/4 |
| `run-9` | `run-9@20261128-120235` | Giọng trung tính, ví dụ đời thường ≤2 câu | 18/21 (86%) | Đạt |

Run-2 … run-6 chấm theo `lessons.csv` bản commit `9d12937` (khi đó D03 = prompt, D04 = agent); run-7 trở đi theo mã BTC hiện tại.

Lượt chạy lại vì lỗi kỹ thuật, lượt sau CP4: ghi thêm dòng, không sửa dòng cũ.

## 6. Lỗi chính

- **Nhóm lỗi lớn nhất lượt 1:** giải thích lại nhưng kết bằng câu hỏi ngược (4/4 câu B18–B21) — đúng pain chính của lát cắt.
- **Đã sửa:** cấm hỏi ngược trong prompt + code tự bỏ câu hỏi cuối và thêm câu kết cố định; đổi cách tìm đoạn sang BM25; chặn bằng code khái niệm ngoài bài. Sau đó (28/11 trưa): nhánh giải thích lại không chép phụ đề, cấu trúc ý chính · ví dụ · đối lập · câu tự kiểm tra, đổi góc theo lần "chưa hiểu". Lượt 2 (`run-10`): hỏi ngược 4/4 → 0/4, tổng 67% → 95% (mốc: run-8 90%, run-9 86%).
- **Còn lại:** B10 (ví dụ tự tạo vẫn gắn mã đoạn) chưa sửa; B01 cận biên (ở run-8, run-9 trượt) do luật né khái niệm ngoài bài làm mất câu "few-shot không phải fine-tune".

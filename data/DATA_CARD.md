# Data card — dữ liệu bản chạy thử dùng

> Bản CP2 (27/11). Đủ ở CP3. Chấm ở rubric R4.
> Không commit nguyên tài liệu khoá, dữ liệu cá nhân thật hay nguyên file data BTC cấp — chỉ đoạn trích ngắn, bản viết lại, hoặc số đã tổng hợp.

## Dataset 1 · Đoạn bài pre-class đã đánh mã (`data/lessons.csv`)

| | |
|---|---|
| Dùng để làm gì | Nguồn duy nhất cho công cụ `search_lesson` (căn cứ để AI trả lời) · nguồn mã đoạn để chấm metric `trich_ma_doan_hop_le` và `khong_tra_loi_ngoai_bai` |
| Từ đâu | Tài liệu khoá: lời giảng video pre-class trên preclass-online.com, lấy từ file transcript có mốc thời gian `preclass_transcripts.txt` (nguồn file: __; **không commit** file này) · mỗi đoạn là **bản tóm tắt 1–3 câu bằng lời của nhóm**, giữ thuật ngữ và ví dụ chính của bài; không chép nguyên văn lời giảng (track A: "trích ngắn hoặc viết lại, không commit nguyên tài liệu khoá") |
| Xử lý những bước gì | Chép từng dòng transcript (538 dòng) · bỏ 17 dòng chào hỏi / chuyển phần ("Chào bạn, Yorn đây", "Bạn có thể bôi đen câu gợi ý…") · gộp các dòng liền nhau trong cùng video thành đoạn ~30–60 giây, cắt ở chỗ chuyển ý ("Thử nhé", "Tóm lại", "Giờ mình…") · viết lại mỗi đoạn thành 1–3 câu tóm tắt (giữ thuật ngữ như token, sampling, few-shot, ReAct… và ví dụ của bài như ShopBot, chữ "đá"); kiểm: cụm trùng nguyên văn dài nhất với lời bài là 16 từ, tổng độ dài còn 38% bản chép · gắn mã `DNN-VNN-NN` (ngày – video – đoạn) + mốc `bắt đầu - kết thúc` · người thứ hai mở video đối chiếu từng đoạn: __ |
| Cột | `ma_doan`, `video`, `moc_thoi_gian`, `noi_dung` |
| Chọn bài nào | Ưu tiên **Day01** (AI & LLM Foundation) vì có nhiều câu hỏi dưới video nhất: **376/1.259 (29,9%)** lượt chat có gắn transcript trong `data/preclass/chat.csv`; 3 video nhiều câu hỏi nhất đều thuộc Day01 (`d01-r1-v02` 133, `d01-r1-v01` 102, `d01-r1-v05` 68). Thêm bài "Kỹ thuật prompt nâng cao" vì là bài người thử A dùng trong `evidence/snoop-observation.md`. Lấy trọn Ngày 1–4 (không lọc video theo câu thử) để không làm đẹp kết quả eval; lý do chọn đến Ngày 4: __ |
| Số dòng / số đoạn | **101 đoạn** (15–68 giây, trung vị 52 giây) · Ngày 1–4, đủ mọi video của 4 ngày · chọn theo ngày học, **không** chọn theo câu thử |
| Phiên bản / ngày lấy | v3 · 28/11/2026 — tóm tắt lại từng đoạn (v2 cùng ngày là bản chép nguyên văn gộp đoạn, đã thay; v1 là 10 đoạn chép tay) |
| Nhãn | thật (tóm tắt lại từ tài liệu khoá, không phải lời bài nguyên văn) |
| Người chép · người kiểm | __ · __ |
| Giới hạn | **Số ngày theo dữ liệu BTC**: `D03-…` = bài agent (`program-day03:chatbot-to-agentic-agent`, file `Day03/d03-r2-v…`), `D04-…` = bài prompt / tool calling (`program-day04:prompt-engineering-tool-calling`, file `Day04/d04-r3-v…`) — khớp `chat.csv`, `answers.csv`; lời trong video tự gọi hai bài này là "ngày học thứ tư / thứ ba" (ngược với hệ thống), file này theo BTC · bài không nói "few-shot khác fine-tune" (B01, B18, B20 đòi ý này) · chỉ phủ Ngày 1–4, câu hỏi về bài khác sẽ ra "không có trong bài" · tóm lại nên có thể sót ý hoặc lệch câu chữ bài — câu trả lời của agent trích theo bản tóm tắt, không theo lời giảng gốc · tra theo từ khoá nên câu hỏi dùng từ khác bài (vd "mảnh từ" thay cho "token") có thể không tìm thấy |

**Dự phòng khi chưa có file:** `codebase/agent.py` dùng 3 đoạn **`synthetic`** mã `D00-…` (nhóm tự viết, nhãn `[giả]`, không phải lời bài) để `python run.py` chạy hết luồng. Trace ghi `dự phòng: … dùng 3 đoạn GIẢ`. Không dùng các đoạn này để báo kết quả eval.

## Dataset 2 · Bộ câu thử (`eval/benchmark.csv`)

| | |
|---|---|
| Dùng để làm gì | Bộ câu thử chấm theo `eval/metric_spec.yaml` |
| Từ đâu | 8 câu `data_that`: câu gõ nguyên văn trên Snoop thật ngày 27/11, hoặc đề Sổ hiểu bài của Snoop (`evidence/snoop-observation.md`, ghi rõ phụ lục / case ở cột `source`) · 13 câu `tu_viet`: nhóm tự viết, có câu lấy chủ đề từ phiên thử của người thử A/B; trong đó 4 câu hội thoại nhiều lượt `[HV] … [Trợ lý] … [HV] chưa hiểu` (B18–B21) dựng lại từ các phiên Snoop trong `evidence/snoop-observation.md` |
| Xử lý những bước gì | Giữ nguyên văn câu gõ (kể cả không dấu) · gán loại `thuong` / `kho` / `tu_choi` · viết `expected` + `pass_criterion` theo hành vi mong muốn ở `spec.md` §4, không theo output của code |
| Số dòng | 21 câu: thuong 6 · kho 11 · tu_choi 4 (2 câu tấn công prompt injection: B14, B15) |
| Phiên bản / ngày lấy | v1 · 27/11/2026 (CP2) |
| Nhãn | thật (8) · tự viết (13) — không có câu `sinh_seed` |
| Giới hạn | 8 câu `data_that` do **thành viên nhóm** gõ khi đóng vai học viên, chưa phải học viên thật · chưa có câu `nguoi_dung` từ phỏng vấn (bổ sung ở CP3, 20–30 câu) · `expected` cho câu ngoài bài (B09) giả định `lessons.csv` không có đoạn về continual learning |

## Dataset 3 · Nhật ký pre-class BTC cấp (`data/preclass/`, **không commit**)

| | |
|---|---|
| Dùng để làm gì | Đào bằng chứng (chọn video nào để chép vào Dataset 1, đếm độ phổ biến ở `spec.md` §1–§2). **Không** đưa vào model, không dùng làm căn cứ trả lời |
| Từ đâu | Data BTC cấp (`data/preclass/` trong repo đề), README đi kèm |
| Xử lý những bước gì | Chỉ đếm, không sửa file · số đã tổng hợp ghi ở đây và `evidence/data-mining.md` · lệnh đếm ở dưới |
| Số dòng | `chat.csv` 1.260 · `answers.csv` 3.776 · `events.csv` 107.709 · `learners.csv` 721 (436 có hoạt động theo README) |
| Phiên bản / ngày lấy | Bản BTC cấp, dữ liệu 05/11/2026 → 25/11/2026, Day01 → Day13 |
| Nhãn | thật (đã ẩn danh bởi BTC: mã `L…`, `C…`, `A…` đã thay mới, không có tên / email) |
| Giới hạn | **Không có câu chữ học viên viết** — chỉ có độ dài, nên không biết học viên hỏi gì, có nói "chưa hiểu" không · giờ UTC · `learning_mode` chỉ có từ 25/11 |

Lệnh đếm số ở Dataset 1 (chạy từ thư mục repo):

```
python -c "import csv,collections as c;r=[x['transcript'] for x in csv.DictReader(open('data/preclass/chat.csv',encoding='utf-8-sig')) if x['transcript']];print(len(r),c.Counter(t.split('/')[0] for t in r).most_common(3),c.Counter(r).most_common(3))"
```

**Không dùng:** `data/training-ops/` (lịch học, lịch lab coach) và `rewards.csv` — ngoài lát cắt (`spec.md` §4, Không làm 5).

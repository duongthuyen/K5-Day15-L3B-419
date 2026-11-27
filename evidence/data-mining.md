# Đào data — cách đếm và kết quả

> Script: `evidence/count.py` — chạy lại: `python evidence/count.py` (đọc `data/preclass/`, file BTC không commit). Repo chỉ chứa số đã tổng hợp và vài mã dòng ví dụ.

## 1. Cách đếm — viết TRƯỚC khi chạy

Quy tắc lấy từ `evidence/hypothesis.md` (viết 27/11 18:25, trước khi đếm), không sửa sau khi có số.

- **Data dùng:** `data/preclass/chat.csv` (1.260 lượt) + `answers.csv` (dòng `nguon = chat`, lấy cột `rubric_y_moi`). Thời gian 05/11/2026 → 25/11/2026, Day01–Day13.
- **Tập:** lượt học viên hỏi trợ giảng dưới video: `channel = video_question`, `kind = question`, `agent_id = addressed_agent_id = teaching_assistant`, có `transcript`.
- **Đếm gì:** lượt **hỏi lại**: cùng học viên (`hv`), cùng video (`transcript`), gửi (`asked_at`) trong ≤5 phút sau khi trợ giảng ghi xong câu trả lời lượt trước (`created_at`). **Nhắn tiếp ngắn:** lượt hỏi lại có `do_dai_cau_hoi` ≤ 30 ký tự (kiểu "vẫn chưa hiểu", "giải thích lại").
- **Mẫu số:** (a) số lượt hỏi trợ giảng dưới video; (b) số học viên đã hỏi trợ giảng ≥1 lần. *Không* dùng 721 tài khoản hay 436 người có hoạt động.
- **Ngưỡng giả thuyết:** nhắn tiếp ngắn ≥10% số lượt hỏi trợ giảng.

## 2. Đọc trước, đếm sau

Đã đọc `data/preclass/README.md`, `column_dictionary.csv` và 20 dòng đầu `chat.csv`. Các kiểu hành vi thấy được:
- Data **không có câu chữ** học viên viết, chỉ có độ dài (`do_dai_cau_hoi`), nên chỉ đếm được tín hiệu hành vi, không biết chắc nội dung.
- Học viên thường hỏi **thành chuỗi** trên cùng một video: nhiều lượt cách nhau dưới 1 phút.
- 1.153/1.260 lượt là với trợ giảng; còn lại là với bạn học AI (`classmate_*`, kênh `video_discussion_reply`). Phần này bị loại khỏi tập.
- Giám khảo AI chấm mỗi câu nhắn theo 3 tiêu chí rubric (0–2), trong đó `rubric_y_moi = 0` nghĩa là "chép hay hỏi lại nguyên văn".

## 3. Kết quả

| Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|
| Lượt hỏi lại ≤5 phút, cùng video / lượt hỏi trợ giảng | 513 / 1.090 | 47,1% | Gần một nửa số câu hỏi là câu hỏi tiếp ngay sau một câu trả lời |
| **Nhắn tiếp ngắn (≤30 ký tự) / lượt hỏi trợ giảng** | **118 / 1.090** | **10,8%** | **Vượt ngưỡng giả thuyết 10%, sát ngưỡng** |
| Nhắn tiếp ngắn / lượt hỏi lại | 118 / 513 | 23,0% | Khoảng 1/4 số lần hỏi lại là câu cụt kiểu "chưa hiểu" |
| Học viên có ≥1 lần hỏi lại / học viên đã hỏi trợ giảng | 94 / 143 | 65,7% | Không phải vài người hỏi nhiều: 2/3 người hỏi có hỏi lại |
| `rubric_y_moi = 0` trong lượt hỏi lại | 383 / 513 | 74,7% | So với mọi lượt: 846/1.090 = 77,6%. **Không khác biệt**, nên rubric không phân biệt được hỏi lại |
| Kiểm độ nhạy: cửa sổ 2 phút / 10 phút | 438 / 1.090 · 548 / 1.090 | 40,2% · 50,3% | Học viên có hỏi lại: 91/143 · 94/143. Kết luận không đổi theo cửa sổ |

Theo ngày học, tỉ lệ hỏi lại ổn định từ 41% đến 52% ở Day01–Day09 (Day01: 160/333 = 48,0%). Các ngày sau quá ít lượt nên không kết luận.

## 4. ≥5 ví dụ cụ thể (mã dòng đã ẩn danh sẵn, không đoán ai là ai)

1. `C00003` — hv `L0145`, `Day01/d01-r1-v02` (video sampling / temperature): hỏi `C00626` (90 ký tự), **0,6 phút** sau câu trả lời lại hỏi tiếp `C00003` (88 ký tự).
2. `C00016` — hv `L0430`, `Day03/d03-r2-v03`: hỏi `C01084` (81 ký tự) → hỏi lại **36 ký tự** sau 0,3 phút.
3. `C00014` — hv `L0065`, `Day08/d08-r1-v02`: hỏi `C00316` (75 ký tự) → hỏi lại câu **cùng độ dài 75 ký tự** sau 0,2 phút. Nhiều khả năng là gửi lại cùng câu.
4. `C00002` — hv `L0365`, `Day08/d08-r1-v04`: `C00274` (105 ký tự) → hỏi lại `C00002` (88 ký tự) sau 0,5 phút.
5. `C00004` — hv `L0643`, `Day08/d08-r1-v04`: `C01025` (105 ký tự) → hỏi lại `C00004` (88 ký tự) sau 0,6 phút.

## 5. Giới hạn của data

- **Không có câu chữ**, nên "hỏi lại" là số **gián tiếp**: một lượt hỏi tiếp có thể là ý mới chứ không phải "chưa hiểu". Đây chính là cách giải thích khác thứ hai đã ghi trong `hypothesis.md`. Con số 10,8% (câu cụt ≤30 ký tự) gần với "chưa hiểu" hơn con số 47,1%, nhưng vẫn không chắc.
- Chỉ có người **đã hỏi** trợ giảng (143 người). Người chưa hiểu mà bỏ đi hoặc sang ChatGPT thì không để lại dấu, nên số này có thể **thấp hơn thực tế**.
- Day10 trở đi có rất ít lượt.

→ **Kiểm lại** bằng khảo sát 15 học viên (`evidence/survey/results.md`): 73,3% nhắn Snoop để nhờ giảng lại đoạn chưa hiểu; 60% diễn đạt lại câu hỏi khi Snoop trả lời lệch ý. Hai con số này khớp với hành vi hỏi lại liên tiếp trong log.

# Tổng hợp bằng chứng pain

> Chấm ở rubric R1. Tối thiểu ≥1 nguồn đạt ngưỡng. Nhóm dùng: đào data (nguồn chính, đạt ngưỡng) → khảo sát để kiểm lại (bằng chứng phụ, n = 15) + quan sát Snoop thật (`evidence/snoop-observation.md`).

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data (x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | ☑ | `evidence/data-mining.md` · script `evidence/count.py` |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ☐ không làm | — |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | ☐ n = 15, **chưa đủ 20**, dùng làm bằng chứng phụ | `evidence/survey/results.md` |
| *(bổ sung)* Quan sát trực tiếp Snoop thật | — (không phải nguồn theo đề) | `evidence/snoop-observation.md` |

## 2. Số chính

- **Đào data** (`chat.csv`, 05–25/11/2026, lượt hỏi trợ giảng dưới video):
  - Lượt hỏi lại trong ≤5 phút trên cùng video: **513/1.090 (47,1%)**.
  - Nhắn tiếp ngắn ≤30 ký tự: **118/1.090 (10,8%)**, vượt ngưỡng giả thuyết 10%.
  - Học viên có ≥1 lần hỏi lại: **94/143 (65,7%)**.
  - Kết luận giữ nguyên khi đổi cửa sổ sang 2 hoặc 10 phút (40,2% · 50,3%).
- **Phỏng vấn:** không làm.
- **Khảo sát:** n = 15 · nhờ giảng lại đoạn chưa hiểu 11/15 (73,3%) · gặp Snoop trả lời không đúng ý ≥1 lần trong buổi gần nhất 11/15 (73,3%) · trả lời chung chung, lặp lời giảng 7/15 (46,7%) · sau đó diễn đạt lại câu hỏi 9/15 (60%) · chuyển sang ChatGPT/Gemini 7/15 (46,7%). *(n nhỏ, chưa đạt ngưỡng 20.)*

## 3. ≥5 ví dụ nguyên văn (có nguồn, bỏ tên)

Data BTC không có câu chữ, nên ví dụ là dòng log (mã đã ẩn danh sẵn). Khảo sát không có câu trả lời tự do.

1. `chat.csv` dòng `C00003` (`L0145`, Day01 video sampling/temperature): hỏi 90 ký tự → **0,6 phút** sau câu trả lời lại hỏi tiếp 88 ký tự.
2. `chat.csv` dòng `C00016` (`L0430`, Day03): hỏi 81 ký tự → hỏi lại **36 ký tự** sau 0,3 phút.
3. `chat.csv` dòng `C00014` (`L0065`, Day08): hỏi lại **cùng độ dài 75 ký tự** sau 0,2 phút, nhiều khả năng gửi lại cùng câu.
4. `chat.csv` dòng `C00002` (`L0365`, Day08): 105 ký tự → hỏi lại 88 ký tự sau 0,5 phút.
5. Khảo sát, câu 7: 7/15 người chọn "Snoop trả lời chung chung, lặp lại lời giảng"; 5/15 chọn "đúng chủ đề nhưng không trúng chỗ chưa hiểu".
6. Quan sát Snoop thật (`snoop-observation.md` mục 4): 4/4 lượt "chưa hiểu" bị hỏi ngược thay vì được giảng lại.

## 4. Các nguồn có khớp nhau không

- **Data nói:** gần một nửa câu hỏi trợ giảng là câu hỏi lại ngay sau một câu trả lời; khoảng 1/4 trong số đó là câu cụt ≤30 ký tự; 2/3 người đã hỏi có hỏi lại.
- **Người dùng nói (khảo sát):** 73% từng nhờ giảng lại; 60% phải diễn đạt lại khi Snoop lệch ý; 47% bỏ sang AI khác.
- **Khớp:** hành vi "diễn đạt lại hoặc hỏi tiếp" xuất hiện ở cả hai nguồn.
- **Lệch:**
  - (1) Trong khảo sát, lỗi phổ biến nhất là **nhầm câu hỏi kiến thức thành câu trả lời quiz (60%)**. Lát cắt của nhóm không xử lý lỗi này, và data không phân biệt được hai kiểu lỗi.
  - (2) 20% người muốn Snoop **hỏi lại khi chưa rõ ý**. Thiết kế của nhóm chỉ hỏi lại khi không có câu hỏi trước để neo (B07, B13); khi đã có câu hỏi trước thì giảng lại ngay. Đây là phân biệt cần kiểm thêm với người dùng.
  - (3) Không ai báo Snoop nói sai kiến thức (0%), nên pain nằm ở **cách** giải thích và hiểu ý người hỏi, không ở **nội dung**.

## 5. Kết luận

Giả thuyết ở `evidence/hypothesis.md`: **đúng, nhưng sát ngưỡng**. Nhắn tiếp ngắn là 10,8%, so với ngưỡng 10%. Khảo sát cho thấy cùng hướng: học viên phải diễn đạt lại hoặc bỏ sang công cụ khác khi lần giải thích đầu không trúng.

**Điều vẫn chưa biết:**
- Bao nhiêu lượt hỏi lại thật sự là "chưa hiểu" so với hỏi ý mới, vì log không có câu chữ.
- Học viên có muốn bị hỏi lại hay muốn được giảng ngay.
- Phần người chưa hiểu mà bỏ đi không để lại dấu trong log.

## Lịch hẹn

Không làm phỏng vấn ở chặng này.

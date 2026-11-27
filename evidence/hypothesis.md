# Giả thuyết — viết TRƯỚC khi tìm bằng chứng (5 phút, commit ngay)

> Điền ở guide bước 1.1. Ôn lại: ngày 2 · lab ngày 2.
> Viết **trước** khi đọc dòng data đầu tiên hay hỏi người đầu tiên, để không sửa cho khớp kết quả. Kết quả ngược giả thuyết vẫn đủ điểm nếu số là thật.

- Ngày giờ viết: 27/11/2026 18:25 — sau 2 lượt kiểm thử trên Snoop (`evidence/snoop-observation.md`), **trước** khi phỏng vấn học viên và **trước** khi đếm `data/preclass/chat.csv`. Giả thuyết dưới đây dùng cho hai nguồn đó; không sửa sau khi có kết quả.
- Người dùng chính (một vai cụ thể): học viên AI20K lớp L3 đang tự học bài pre-class, hỏi trợ giảng ngay dưới video về một khái niệm mới và chưa hiểu sau lần giải thích đầu.
- **Mình nghĩ:** học viên L3 gặp khó khi **tự học một khái niệm mới trên trang pre-class mà lần giải thích đầu chưa đủ để hiểu**, vì công cụ hỏi đáp hiện có chưa điều chỉnh cách giải thích theo từng người học (trình độ, chỗ đang vướng, cách đã thử), hậu quả là học viên **bỏ qua chỗ chưa hiểu hoặc phải tìm nguồn khác**, và mang lỗ hổng kiến thức vào buổi lab.
- **Có thể còn cách giải thích khác:**
  - Học viên ít khi nhắn "chưa hiểu" với trợ giảng — chưa hiểu thì xem lại video hoặc hỏi ChatGPT ngay, nên lỗi có thật nhưng ít người gặp.
  - Lượt nhắn tiếp liền nhau trong log có thể là hỏi **ý mới**, không phải "chưa hiểu" — log không có câu chữ nên không phân biệt chắc được.
  - Khó khăn nằm ở nội dung bài (bài quá nhanh, thiếu ví dụ) chứ không ở cách trợ giảng trả lời — giải thích lại kiểu gì cũng không giúp nhiều.
- **Mình đúng nếu thấy:**
  - **Phỏng vấn:** ≥2/3 học viên được hỏi kể được ít nhất một lần trong 1 tháng qua đã nhắn kiểu "chưa hiểu / giải thích lại" với trợ giảng, **và** ≥2/3 trong số đó nói lần giải thích sau không giúp họ hiểu hơn hoặc họ bỏ sang cách khác.
  - **Data (`chat.csv`):** ≥10% lượt hỏi trợ giảng dưới video (`channel = video_question`, `addressed_agent_id = teaching_assistant`) là **câu nhắn tiếp ngắn** — cùng học viên, cùng `transcript`, gửi trong vòng 5 phút sau câu trả lời trước, `do_dai_cau_hoi` ≤ 30 ký tự — *(ngưỡng nhóm tự chọn; quy tắc đếm ghi ở `evidence/data-mining.md` trước khi chạy)*.
  - Thấy ít hơn các ngưỡng trên → ghi đúng số, kết luận lỗi có thật nhưng ít phổ biến.
- **Nguồn sẽ dùng** (≥1 nguồn đạt ngưỡng, guide 1.2): [x] đào data · [x] phỏng vấn ≥3 · [ ] khảo sát ≥20 — nguồn chính: **phỏng vấn ≥3 học viên ngoài nhóm** (cho biết có gặp không, vì sao, sau đó làm gì) · nguồn để kiểm lại: **`data/preclass/chat.csv`** (cho biết bao nhiêu lượt có dấu hiệu nhắn tiếp ngắn — số gián tiếp vì log không có câu chữ).

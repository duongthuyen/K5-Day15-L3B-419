# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | Claude Code (28/11 trưa) | Sửa `codebase/agent.py` nhánh giải thích lại (cấu trúc ý chính · ví dụ · đối lập · câu tự kiểm tra, đổi góc theo lần, kiểm trùng phụ đề); viết `codebase/guard.py` (giữ luật giống bản dự phòng, đối chiếu 35 câu vào + 63 phép kiểm câu ra) | Đọc diff trong PR #1 trước khi merge · __ | __ |
| Code bản chạy thử (phần trước 28/11 trưa) | __ | __ | __ | __ |
| Prompt / thiết kế lời gọi mô hình | Claude Code (28/11 trưa) | Viết lại `SYSTEM_REEXPLAIN` + `STRATEGIES` theo yêu cầu của nhóm (không chép phụ đề, cấu trúc 4 phần, 4 góc tiếp cận); thêm luật giọng trung tính cho `SYSTEM` | Nhóm đưa ra yêu cầu sau khi thử web; thử 4 câu trước khi chạy cả bộ | __ |
| Đào data (viết script đếm, gợi ý nhãn) | | | Kiểm tay __ dòng, khớp __ | |
| Rà câu hỏi phỏng vấn / khảo sát | | Chỉ rà câu dẫn dắt | | |
| Viết câu thử (benchmark) | | | Mỗi câu thử có `source`; câu thử AI viết được ghi rõ | |
| Sinh data `synthetic` (nếu có) | | | Seed __ · kiểm tay __ dòng | |
| Chấm cột `pass` bằng LLM (nếu có) | Claude Code | Chấm nháp `run-9`, `run-10` (ghi `[AI nháp]` + lý do từng câu, chấm chặt câu lệch ý; chỉ sửa cột `pass`, `ghi_chu`, đã kiểm không đổi cột khác) | `run-10` chờ người thứ hai duyệt (Nga chấm nháp `run-2` … `run-8`) · kiểm tra thủ công __ câu thử, khớp __/__ | Nga |
| Slide, văn bản | Claude Code | Điền số vào `eval/report.md`, `eval/README.md`, `cost/cost-estimate.md`, `spec.md` §4 §7 §8 §10, README; làm bản slide dự phòng `slides/demo-slides.html` → `demo-slides.pdf` (mọi số trỏ về file nguồn) | Slide chính: Huyền làm · __ | Huyền · __ |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).

# Báo cáo kiểm thử: Trợ giảng Snoop không giải thích lại khi người học nói "chưa hiểu"

## Thông tin chung

| Mục | Nội dung |
|---|---|
| Sản phẩm | Trang pre-class AI20K ([preclass-online.com](https://preclass-online.com)) |
| Tính năng | Trợ giảng AI "Snoop": khung chat "Trao đổi" và "Sổ hiểu bài" |
| Ngày kiểm thử | 27/11/2026 |
| Người kiểm thử | 2 người, kiểm thử độc lập, ẩn danh là **A** và **B** |
| Bài học | A: Kỹ thuật prompt nâng cao · B: Ngày 1 · AI & LLM Foundation, Phần 2 |
| Chủ đề gặp lỗi | few-shot, system prompt (A) · attention, sampling (B) |
| Mức độ | Trung bình – Cao |
| Trạng thái | Đã tái hiện trên 2 người thử, 2 bài, 3 chủ đề |

## 1. Tóm tắt

Khi người học nói "chưa hiểu" ngay sau một câu trả lời, Snoop không giải thích lại chủ đề vừa hỏi. Snoop hỏi ngược "chưa hiểu chỗ nào", có khi liệt kê lại toàn bộ chủ đề đã nói trong phiên. Khi người học chỉ rõ chủ đề, Snoop giảng lại bằng đúng ví dụ và câu chữ của bài giảng, có khi khó hơn lần đầu. Snoop chỉ đổi cách giải thích khi người học tự yêu cầu rất cụ thể.

Lỗi xuất hiện ở **4/4** lượt "chưa hiểu" được quan sát, trên hai người thử độc lập.

## 2. Phương pháp kiểm thử

- **Người thử A:** dùng Snoop trong một phiên hỏi nhiều chủ đề liên tiếp (mốc thời gian, CoT, prompt injection, đáp án quiz, ReAct, few-shot). Sau câu trả lời về few-shot, nhắn "chưa hiểu" hai lần. Lặp lại tình huống tương tự với chủ đề system prompt.
- **Người thử B:** thiết kế sẵn 11 case thuộc 4 nhóm, chạy trong khoảng 30 phút trên một tài khoản học viên: (1) xin giải thích theo cách khác, (2) trả lời đúng nhưng khác cách bài giảng nói, (3) hỏi kiến thức đúng nằm ngoài bài, (4) đối chứng: trả lời sai nhưng dùng đúng từ khoá. Nhật ký đầy đủ ở Phụ lục B.
- Hai người thử không trao đổi kịch bản với nhau trước khi thử.

## 3. Các bước tái hiện

1. Mở một bài trên trang pre-class, vào khung "Trao đổi".
2. Hỏi Snoop về một khái niệm trong bài, ví dụ: "vậy few shot là fine tune model bằng vài ví dụ đúng không ạ".
3. Sau khi Snoop trả lời, nhắn: "mình vẫn chưa hiểu".
4. **Kết quả thực tế:** Snoop hỏi lại người học chưa hiểu chỗ nào, hoặc liệt kê các chủ đề đã nói trong phiên.
5. **Kết quả mong đợi:** Snoop giải thích lại khái niệm vừa hỏi theo một cách khác, rồi hỏi người học đã rõ chưa.

## 4. Kết quả

| ID | Phát hiện | A | B | Dẫn chứng nguyên văn |
|---|---|:-:|:-:|---|
| F1 | Người học nói "chưa hiểu" ngay sau một câu trả lời → Snoop **hỏi ngược** thay vì giảng lại | ✅ few-shot ×2 · system prompt ×1 | ✅ attention ×1 | A: *"'chưa hiểu' thì mình cần biết chưa hiểu chỗ nào mới giảng đúng được"* · B: *"mình chưa rõ bạn đang chưa hiểu chỗ nào — attention hay ý khác?"* |
| F2 | **Liệt kê lại cả loạt chủ đề cũ**, gồm chủ đề không liên quan, thay vì tiếp tục tại chủ đề vừa hỏi | ✅ 6 chủ đề · system prompt | — *(phiên chỉ có 1 chủ đề)* | A: *"giờ giấc trong phần 3, CoT có luôn tốt hơn không, prompt injection, đáp án quiz, ReAct với function calling, và few-shot có phải fine-tune không"* |
| F3 | Khi giải thích lại thì **không đổi cách**: dùng lại định nghĩa, ví dụ, slide của bài; có khi khó hơn | ✅ cả 2 lượt chỉ là định nghĩa | ✅ case 3, 8 | B case 3: hứa *"nói lại bằng cách khác hẳn"* nhưng đưa query/key/value và dùng lại ví dụ "Nam đang đá bóng" của bài |
| F4 | Không theo trình độ, yêu cầu người học đã nêu | — | ✅ case 8 | Xin ví dụ kinh doanh, "2 câu", cho người không biết xác suất → nhận lại ví dụ "nắng/mưa" của slide, 3 gạch đầu dòng, vẫn dùng chữ "xác suất" |
| F5 | Lần giải thích sau **ngắn hơn** lần trước | ✅ 3 ý → 1 dòng | — | A: *"Gần nhất là few-shot khác fine-tune: few-shot chỉ đưa ví dụ ngay trong prompt."* |
| F6 | Giọng thiếu kiên nhẫn | ✅ | — | A: *"Mình vừa trả lời nhiều ý rồi, giờ bạn chưa rõ ý nào hả?"* |
| F7 | **Chỉ đổi cách giảng khi người học yêu cầu rất cụ thể** | — | ✅ case 1 | B xin rõ "ví dụ đời thường, đừng dùng câu chữ bài" → Snoop đưa được ví dụ "nghe giữa phòng đông người" |

**Tần suất:**
- F1: **4/4** lượt "chưa hiểu" quan sát được (A ×3, B ×1).
- F3: **4/4** lần Snoop giải thích lại khi người học không yêu cầu cụ thể cách giải thích (A ×2, B ×2).

## 5. Phân tích nguyên nhân (giả thuyết)

Snoop **có** đọc lịch sử hội thoại: ở phiên của A, Snoop liệt kê đủ 6 chủ đề cũ; ở phiên của B, Snoop nhắc đúng tên "attention". Lỗi không nằm ở việc mất ngữ cảnh mà ở việc Snoop **không neo câu "chưa hiểu" vào câu hỏi gần nhất**. Gặp một câu phản hồi ngắn không nêu chủ đề, Snoop coi như chưa biết người học đang nói về gì, nên hỏi lại hoặc liệt kê cả phiên.

Khi được chỉ rõ chủ đề, Snoop quay về cách nói của bài giảng (F3), vì cách "giải thích khác" chỉ được kích hoạt khi người học tự yêu cầu rõ (F7).

Hệ quả: người học phải tự làm hai việc mà người đang bối rối khó làm nhất, là **tự chỉ ra mình vướng ở đâu** và **tự yêu cầu một cách giải thích khác**.

## 6. Hành vi mong đợi

1. Giữ chủ đề của câu hỏi gần nhất.
2. Người học nói "chưa hiểu" mà không nêu chủ đề khác → mặc định là chủ đề đó, tiếp tục ngay tại phần đó.
3. Giải thích lại **theo cách khác** lần trước (tình huống đời thường → ví dụ cụ thể → so sánh), theo trình độ người học đã nêu, không ngắn hơn lần trước.
4. Kết thúc bằng câu hỏi kiểm tra đã rõ chưa, gợi ý điểm có thể còn vướng.
5. Chỉ hỏi lại khi phiên chưa có câu hỏi nào để neo vào.

Ví dụ phản hồi mong đợi cho phiên few-shot:

> Mình giải thích lại few-shot theo cách khác nhé. Hãy tưởng tượng bạn nhờ một người viết thiệp. Fine-tune giống như cho người đó đi học một khóa viết thiệp: kỹ năng thay đổi vĩnh viễn. Few-shot giống như đưa họ xem 3 tấm thiệp mẫu rồi bảo "viết giống thế này": họ bắt chước mẫu cho lần đó thôi, xong là quên.
> Trong prompt, few-shot trông như sau: Câu: "Tuyệt vời!" → Tích cực / Câu: "Chán quá" → Tiêu cực / Câu: "Cũng được" → ?
> Phần này đã rõ hơn chưa, hay bạn đang vướng ở điểm "model không học lại"?

## 7. Điểm Snoop đang làm tốt

- Câu trả lời đầu tiên thường đúng, gọn, kèm mốc video để nghe lại.
- Khi được yêu cầu rất cụ thể, Snoop đưa được ví dụ mới (B case 1).
- Không chấm thuần theo từ khoá: vẫn bắt được lỗi khái niệm lớn (B case 11).

Vì vậy kết luận chính xác là: Snoop **không tự đổi cách giảng khi người học chưa hiểu**, chứ không phải Snoop không có khả năng giảng theo cách khác.

## 8. Phát hiện khác ngoài phạm vi báo cáo

Người thử B ghi nhận thêm các lỗi sau (chi tiết ở Phụ lục B):

| Dạng | Biểu hiện | Case | Dẫn chứng |
|---|---|---|---|
| Từ chối kiến thức đúng ngoài bài | Không xác nhận điều người học nói đúng nếu bài không dạy | 6, 7, 9 | *"BPE hay subword thì bài không dạy, mình không dám nói thêm"* |
| Trừ điểm câu đúng vì khác cách bài giảng nói | Câu đúng, chính xác hơn bài vẫn bị "Cần củng cố" | 0, 4 *(case 10 thì không)* | *"Bạn dùng 'logits' và 'softmax' là khái niệm ngoài bài giảng"* |
| Chấm không nhất quán | Chat nói "đúng hướng", Sổ hiểu bài nói "không phải do temperature"; lúc phạt lúc không phạt thuật ngữ ngoài bài | 4 vs 5, 4 vs 10, 11 | — |

## 9. Giới hạn và bước tiếp theo

**Giới hạn**
- Mới có 4 lượt "chưa hiểu" trên 2 người thử, 2 bài. Kết quả cho thấy lỗi **lặp lại được**, chưa cho biết bao nhiêu học viên gặp và họ xử lý thế nào.
- Phản hồi của Snoop có tính ngẫu nhiên; mỗi case chưa được chạy lại nhiều lần.
- Ảnh chụp màn hình chưa đính kèm.
- Hội thoại nguyên văn ở chủ đề system prompt chưa được ghi lại.

**Bước tiếp theo**
- Chạy lại mỗi case 3–5 lần để đo tỉ lệ.
- Phỏng vấn và khảo sát học viên: đã từng nói "chưa hiểu" với Snoop chưa, Snoop phản hồi thế nào, sau đó làm gì.
- Đếm trên log chat (`data/preclass/chat.csv`) số lượt học viên nhắn tiếp liền nhau trong cùng một bài.

---

## Phụ lục A. Hội thoại của người thử A

### A.1 Chủ đề few-shot

Phiên có nhiều chủ đề: mốc thời gian, CoT, prompt injection, đáp án quiz, ReAct, few-shot. Câu ngay trước là về few-shot.

**Lượt 0: câu hỏi gốc (Snoop trả lời tốt)**

> **Học viên:** vay few shot la fine tune model bang vai vi du dung ko a
>
> **Snoop:** Bạn ơi, few-shot không phải fine-tune đâu ạ.
> • Fine-tune là huấn luyện lại, đổi trọng số của model.
> • Few-shot chỉ là đưa 2–5 cặp input-output mẫu ngay trong prompt.
> • Model không học lại gì cả, nó chỉ bắt chước khuôn mẫu đó thôi.
> Phần 2 «Kỹ thuật prompt nâng cao» ở 00:49 nói rõ chỗ này, bạn xem lại nhé.

**Lượt 1: "chưa hiểu" lần thứ nhất**

> **Học viên:** mình vẫn chưa hiểu
>
> **Snoop:** Bạn ơi, "chưa hiểu" thì mình cần biết chưa hiểu chỗ nào mới giảng đúng được. Trong mấy lượt vừa rồi lớp mình nói qua mấy chuyện: giờ giấc trong phần 3, CoT có luôn tốt hơn không, prompt injection, đáp án quiz, ReAct với function calling, và few-shot có phải fine-tune không. Bạn muốn mình nói lại ý nào thì nhắn đúng ý đó nhé.

**Lượt 2: "chưa hiểu" lần thứ hai**

> **Học viên:** vẫn chưa hiểu lắm
>
> **Snoop:** Mình vừa trả lời nhiều ý rồi, giờ bạn chưa rõ ý nào hả?
> • Gần nhất là few-shot khác fine-tune: few-shot chỉ đưa ví dụ ngay trong prompt.
> • Trước đó là ReAct và function calling: một cái là cách agent nghĩ, một cái là cơ chế gọi có cấu trúc.
> • Bạn muốn mình nói lại ý nào thì nhắn đúng ý đó nhé.

### A.2 Chủ đề system prompt

- Hỏi về system prompt, sau đó nói chưa hiểu → Snoop liệt kê lại một loạt chủ đề thay vì giải thích tiếp về system prompt.
- Cùng phiên với few-shot hay phiên mới: __
- Hội thoại nguyên văn: __

## Phụ lục B. Nhật ký kiểm thử của người thử B

### B.1 Cách thử


Snoop xuất hiện ở hai nơi:

| Nơi                     | Chức năng                                                                                                                                                                 |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Trao đổi** (chat lớp) | Trả lời câu hỏi, gắn mốc video "Trong bài giảng ở…"                                                                                                                       |
| **Sổ hiểu bài**         | Sinh viên tự viết 1–3 câu cho mỗi ý chính. Snoop nhận xét theo dạng _Ý đúng / Cần sửa_, gắn nhãn _Hiểu tốt / Cần củng cố / Cần xem lại_. Có thêm "Thử một câu tình huống" |

Mình thiết kế 11 case thuộc 4 nhóm:

1. Xin **giải thích theo cách khác** bài giảng
2. Trả lời **đúng nhưng khác cách bài giảng nói**: thuật ngữ khác, góc nhìn khác
3. Hỏi **kiến thức đúng nằm ngoài bài**
4. Đối chứng: trả lời **sai nhưng nhồi từ khoá của bài giảng**

---

### B.2 Chi tiết 11 case


#### Nhóm 1 – Xin giải thích theo cách khác

##### Case 1 · Xin ví dụ đời thường, yêu cầu rõ ràng

- **Sinh viên:** "Mình vẫn chưa hiểu attention. Giải thích bằng một ví dụ đời thường khác hẳn bài giảng được không, đừng dùng lại câu chữ trong bài?"
- **Snoop:** Đưa ra ví dụ mới: nghe một câu giữa phòng đông người, tập trung vào người đang nói với mình nhưng vẫn liếc sang tiếng khác để hiểu ngữ cảnh. Sau đó lại kéo về ví dụ chữ "đá" của bài và chốt bằng "Bài giảng kỹ ở Phần 2, mốc 04:02 tới 05:23".
- **Nhận định:** ⚠️ Snoop _có thể_ đổi cách giải thích, nhưng **chỉ khi được yêu cầu rất cụ thể**.

##### Case 2 · "Vẫn chưa hiểu lắm"

- **Sinh viên:** "vẫn chưa hiểu lắm"
- **Snoop:** "Bạn ơi, mình chưa rõ bạn đang chưa hiểu chỗ nào — attention hay ý khác?"
- **Nhận định:** ❗ Snoop vừa giải thích attention ngay lượt trước mà **không nhớ**. Có vẻ mỗi lượt chat được xử lý riêng rẽ.

##### Case 3 · Trả lời "attention"

- **Sinh viên:** "attention"
- **Snoop:** Hứa "nói lại bằng cách khác hẳn", nhưng thực tế đưa ra query/key/value, trọng số, value, nhiều head, causal mask. Ví dụ dùng lại "Nam đang đá bóng" của bài, chốt bằng slide "Attention là một phép trộn có trọng số".
- **Nhận định:** ✅ Lỗi tái hiện. Sinh viên càng chưa hiểu thì Snoop càng **quay lại lời giảng, và giải thích khó hơn**.

##### Case 8 · Xin giải thích theo trình độ

- **Sinh viên:** "Mình dân kinh tế, không biết xác suất. Giải thích sampling cho mình bằng một ví dụ trong kinh doanh thôi, 2 câu là đủ."
- **Snoop:** "Sampling giống như bốc thăm trúng thưởng có tỉ lệ… Cửa hàng đặt 50 phiếu 'nắng', 30 phiếu 'mưa' vào hộp rồi rút một phiếu… chỉ là **xác suất** thấp hơn chứ không bị cấm." (3 gạch đầu dòng, kèm mốc video)
- **Nhận định:** ✅ Khớp rõ.
  - Ví dụ "nắng/mưa" chính là ví dụ trong slide của bài. Snoop chỉ thêm chữ "cửa hàng", không phải ví dụ kinh doanh.
  - Vẫn dùng từ "xác suất", dù sinh viên nói mình không biết xác suất.
  - Không làm theo yêu cầu "2 câu".

#### Nhóm 2 – Đúng nhưng khác cách bài giảng nói

##### Case 4 · Sổ hiểu bài – Temperature, dùng thuật ngữ chính xác hơn bài

- **Đề:** "Theo bạn, temperature là gì và nó làm gì?" (1–3 câu)
- **Sinh viên:** "Temperature là số chia vào logits trước softmax. Temperature thấp làm phân phối nhọn lại nên model gần như luôn chọn token có xác suất cao nhất, câu trả lời ổn định; temperature cao làm phân phối phẳng ra nên token ít khả năng dễ được chọn hơn, câu trả lời đa dạng hơn."
- **Snoop:** **Cần củng cố**
  - _Ý đúng:_ nói đúng hướng về nhọn/phẳng.
  - _Cần sửa:_ "**Bạn dùng 'logits' và 'softmax' là khái niệm ngoài bài giảng**, và thiếu ý quan trọng nhất: temperature không thêm token mới… Bạn cũng chưa nói rằng giảm temperature không làm model trả lời đúng hơn."
- **Nhận định:** ✅ **Ca rõ nhất của dạng lỗi này.** Câu trả lời đúng và chính xác hơn bài giảng nhưng bị trừ điểm vì "ngoài bài". Snoop còn trừ điểm vì thiếu những ý mà đề không hỏi.

##### Case 0 (quan sát trước đó) · Sổ hiểu bài – Sampling

- **Đề:** "Vì sao hỏi lại đúng câu cũ, bạn có thể nhận được câu trả lời khác?"
- **Sinh viên:** "vì temperature cao khiến model sinh ra câu trả lời khác"
- **Snoop:** **Cần xem lại**, "…token ít khả năng vẫn có thể được chọn — **không phải do temperature**."
- **Nhận định:** Về kỹ thuật, câu của sinh viên chưa đầy đủ nhưng không sai. Temperature điều chỉnh chính phân phối mà sampling rút thăm từ đó. Nói "không phải do temperature" là gây hiểu nhầm.

##### Case 5 · Chat – hỏi lại cùng ý đó

- **Sinh viên:** "Mình hiểu là hỏi lại cùng câu mà ra câu trả lời khác là vì temperature lớn hơn 0, nếu đặt temperature = 0 thì gần như lần nào cũng ra giống nhau. Mình hiểu vậy đúng không?"
- **Snoop:** "Chỗ bạn hỏi là **đúng hướng**…"
- **Nhận định:** ❗ **Mâu thuẫn.** Cùng một ý, chat bảo "đúng hướng", còn Sổ hiểu bài bảo "không phải do temperature".

##### Case 9 · Câu tình huống – Temperature

- **Snoop hỏi:** "Bạn làm chatbot tra cứu quy định cho công ty và đặt temperature = 0,2. Như vậy đã đủ để câu trả lời luôn chính xác chưa? Vì sao?"
- **Sinh viên:** "Chưa đủ. Temperature thấp chỉ làm câu trả lời ổn định, không làm nó đúng hơn. Muốn chính xác thì nên dùng RAG: truy xuất đúng điều khoản quy định đưa vào prompt, bắt model trích dẫn nguồn và trả lời 'không biết' khi không tìm thấy."
- **Snoop:** **Hiểu tốt**, nhưng thêm: "Bạn nói thêm về RAG và trích dẫn nguồn, **nhưng bài giảng không đề cập**; để hiểu sâu hơn, thử giải thích cơ chế temperature…"
- **Nhận định:** ⚠️ Không trừ điểm, nhưng gạt đi giải pháp đúng trong thực tế để kéo sinh viên về nội dung bài.

##### Case 10 · Sổ hiểu bài – Vòng lặp đoán token, dùng thuật ngữ ngoài bài

- **Sinh viên:** "LLM là mô hình autoregressive: nó không soạn sẵn cả câu mà decode từng token một…"
- **Snoop:** **Hiểu tốt**, không phạt "autoregressive" hay "decode".
- **Nhận định:** ❌ **Case ngược.** Lần này thuật ngữ ngoài bài không bị phạt. Đặt cạnh case 4, điều này cho thấy cách chấm không nhất quán.

#### Nhóm 3 – Kiến thức đúng nằm ngoài bài

##### Case 6 · Greedy và beam search

- **Sinh viên:** "Ngoài sampling thì LLM còn có thể chọn token bằng greedy hoặc beam search đúng không? Khi nào nên dùng cái nào?"
- **Snoop:** "Bài giảng chỉ dạy greedy và sampling, nên **mình chưa có căn cứ để nói về beam search**." Không trả lời phần "khi nào dùng".
- **Nhận định:** ✅ Khớp. Snoop từ chối kiến thức nền tảng và phổ biến.

##### Case 7 · Token là subword

- **Sinh viên:** "Token không phải là một từ đúng không? Mình đọc thấy thường là mảnh từ (subword, kiểu BPE)…"
- **Snoop:** "Bạn hiểu đúng hướng rồi, nhưng bài nói chưa tới mức đó… **Còn tên gọi BPE hay subword thì bài không dạy, mình không dám nói thêm.**"
- **Nhận định:** ✅ Khớp. Sinh viên nói đúng mà không được xác nhận rõ ràng.
  > Đối chiếu: trước đó, với câu hỏi "continual learning là gì", Snoop lại trả lời được, kèm nhãn "Ngoài bài giảng". Ranh giới "dám hay không dám nói ngoài bài" **không nhất quán**.

#### Nhóm 4 – Đối chứng: sai nhưng dùng đúng từ khoá

##### Case 11 · Sổ hiểu bài – Attention

- **Sinh viên (cố ý sai 2 chỗ):** "Attention là một phép trộn có trọng số: model dùng query, key, value để **chọn ra đúng một từ quan trọng nhất rồi bỏ hẳn các từ còn lại**, và nó **nhìn cả các từ phía sau** để hiểu ngữ cảnh rồi mới đoán token tiếp theo."
- **Snoop:** **Cần xem lại**
  - Bắt được lỗi 1: attention không chọn một từ mà trộn nhiều vị trí.
  - **Bỏ sót lỗi 2:** model chỉ được nhìn các token phía trước (causal mask), dù bài có giảng phần này.
  - Lại bắt bẻ cụm "rồi mới đoán token tiếp theo", vốn không sai.
- **Nhận định:** ⚠️ Snoop không chấm thuần theo từ khoá. Nhưng chất lượng chấm **không ổn định**: bỏ sót lỗi thật và bắt lỗi không đáng bắt.

---

### B.3 Quan sát phụ (ngoài trợ giảng)


- **Hiểu sai ý định:** hỏi "continual learning là gì" trong lúc video đang hiện câu quiz thì Snoop trả lời "Mình sẽ không đưa đáp án… bạn đang nghiêng về lựa chọn nào?". Phải gửi lại lần hai mới được trả lời.
- **Tiến độ không đồng bộ:** trang chủ báo 0%, "0/0 checkpoint", "Chưa có hoạt động học tập", trong khi Sổ hiểu bài đã có bài viết.
- **Video không nhớ vị trí:** rời trang khi đang ở 1:23 của Phần 2, quay lại thì về 0:08 màn intro, dù banner ghi "Đã khôi phục phiên học".
- **Lời chào sai giờ:** 17:34 (giờ Việt Nam) nhưng trang chào "Chào buổi sáng".
- **"Bạn học" ảo** (Naveen Thinking, Ducky Hay Hỏi) hiện dòng "đang chờ bạn trả lời", gây áp lực trong lúc xem video.

---

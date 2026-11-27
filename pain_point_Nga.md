# Pain point của Trợ giảng AI "Snoop" trên Preclass Online

> Ghi chép từ phiên dùng thử trực tiếp ngày 27/11/2026, tài khoản học viên, lớp **Ngày 1 · AI & LLM Foundation** (Phần 2 – Cách LLM sinh văn bản và hiểu ngữ cảnh).

---

## 1. Tóm tắt

**Pain point:** Snoop coi bài giảng là ranh giới của sự thật.

- Điều gì bài không dạy thì Snoop **không dám xác nhận**, kể cả khi sinh viên nói đúng.
- Cách nào bài không dùng thì Snoop **không giải thích được**. Khi sinh viên bảo chưa hiểu, Snoop quay lại lời giảng, nhiều khi còn khó hơn.
- Cách chấm **không nhất quán** giữa chat và Sổ hiểu bài, và giữa các lần chấm. Sinh viên không biết nên tin vào đâu.
  **Hậu quả:** sinh viên giỏi bị chấm sai nên mất niềm tin, sinh viên yếu không được giải thích theo cách khác. Cả hai nhóm đều chuyển sang ChatGPT, và lợi thế "lớp học có trợ giảng AI" của sản phẩm mất tác dụng.

---

## 2. Cách thử nghiệm

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

## 3. Chi tiết 11 case

### Nhóm 1 – Xin giải thích theo cách khác

#### Case 1 · Xin ví dụ đời thường, yêu cầu rõ ràng

- **Sinh viên:** "Mình vẫn chưa hiểu attention. Giải thích bằng một ví dụ đời thường khác hẳn bài giảng được không, đừng dùng lại câu chữ trong bài?"
- **Snoop:** Đưa ra ví dụ mới: nghe một câu giữa phòng đông người, tập trung vào người đang nói với mình nhưng vẫn liếc sang tiếng khác để hiểu ngữ cảnh. Sau đó lại kéo về ví dụ chữ "đá" của bài và chốt bằng "Bài giảng kỹ ở Phần 2, mốc 04:02 tới 05:23".
- **Nhận định:** ⚠️ Snoop _có thể_ đổi cách giải thích, nhưng **chỉ khi được yêu cầu rất cụ thể**.

#### Case 2 · "Vẫn chưa hiểu lắm"

- **Sinh viên:** "vẫn chưa hiểu lắm"
- **Snoop:** "Bạn ơi, mình chưa rõ bạn đang chưa hiểu chỗ nào — attention hay ý khác?"
- **Nhận định:** ❗ Snoop vừa giải thích attention ngay lượt trước mà **không nhớ**. Có vẻ mỗi lượt chat được xử lý riêng rẽ.

#### Case 3 · Trả lời "attention"

- **Sinh viên:** "attention"
- **Snoop:** Hứa "nói lại bằng cách khác hẳn", nhưng thực tế đưa ra query/key/value, trọng số, value, nhiều head, causal mask. Ví dụ dùng lại "Nam đang đá bóng" của bài, chốt bằng slide "Attention là một phép trộn có trọng số".
- **Nhận định:** ✅ Khớp pain point. Sinh viên càng chưa hiểu thì Snoop càng **quay lại lời giảng, và giải thích khó hơn**.

#### Case 8 · Xin giải thích theo trình độ

- **Sinh viên:** "Mình dân kinh tế, không biết xác suất. Giải thích sampling cho mình bằng một ví dụ trong kinh doanh thôi, 2 câu là đủ."
- **Snoop:** "Sampling giống như bốc thăm trúng thưởng có tỉ lệ… Cửa hàng đặt 50 phiếu 'nắng', 30 phiếu 'mưa' vào hộp rồi rút một phiếu… chỉ là **xác suất** thấp hơn chứ không bị cấm." (3 gạch đầu dòng, kèm mốc video)
- **Nhận định:** ✅ Khớp rõ.
  - Ví dụ "nắng/mưa" chính là ví dụ trong slide của bài. Snoop chỉ thêm chữ "cửa hàng", không phải ví dụ kinh doanh.
  - Vẫn dùng từ "xác suất", dù sinh viên nói mình không biết xác suất.
  - Không làm theo yêu cầu "2 câu".

### Nhóm 2 – Đúng nhưng khác cách bài giảng nói

#### Case 4 · Sổ hiểu bài – Temperature, dùng thuật ngữ chính xác hơn bài

- **Đề:** "Theo bạn, temperature là gì và nó làm gì?" (1–3 câu)
- **Sinh viên:** "Temperature là số chia vào logits trước softmax. Temperature thấp làm phân phối nhọn lại nên model gần như luôn chọn token có xác suất cao nhất, câu trả lời ổn định; temperature cao làm phân phối phẳng ra nên token ít khả năng dễ được chọn hơn, câu trả lời đa dạng hơn."
- **Snoop:** **Cần củng cố**
  - _Ý đúng:_ nói đúng hướng về nhọn/phẳng.
  - _Cần sửa:_ "**Bạn dùng 'logits' và 'softmax' là khái niệm ngoài bài giảng**, và thiếu ý quan trọng nhất: temperature không thêm token mới… Bạn cũng chưa nói rằng giảm temperature không làm model trả lời đúng hơn."
- **Nhận định:** ✅ **Bằng chứng mạnh nhất.** Câu trả lời đúng và chính xác hơn bài giảng nhưng bị trừ điểm vì "ngoài bài". Snoop còn trừ điểm vì thiếu những ý mà đề không hỏi.

#### Case 0 (quan sát trước đó) · Sổ hiểu bài – Sampling

- **Đề:** "Vì sao hỏi lại đúng câu cũ, bạn có thể nhận được câu trả lời khác?"
- **Sinh viên:** "vì temperature cao khiến model sinh ra câu trả lời khác"
- **Snoop:** **Cần xem lại**, "…token ít khả năng vẫn có thể được chọn — **không phải do temperature**."
- **Nhận định:** Về kỹ thuật, câu của sinh viên chưa đầy đủ nhưng không sai. Temperature điều chỉnh chính phân phối mà sampling rút thăm từ đó. Nói "không phải do temperature" là gây hiểu nhầm.

#### Case 5 · Chat – hỏi lại cùng ý đó

- **Sinh viên:** "Mình hiểu là hỏi lại cùng câu mà ra câu trả lời khác là vì temperature lớn hơn 0, nếu đặt temperature = 0 thì gần như lần nào cũng ra giống nhau. Mình hiểu vậy đúng không?"
- **Snoop:** "Chỗ bạn hỏi là **đúng hướng**…"
- **Nhận định:** ❗ **Mâu thuẫn.** Cùng một ý, chat bảo "đúng hướng", còn Sổ hiểu bài bảo "không phải do temperature".

#### Case 9 · Câu tình huống – Temperature

- **Snoop hỏi:** "Bạn làm chatbot tra cứu quy định cho công ty và đặt temperature = 0,2. Như vậy đã đủ để câu trả lời luôn chính xác chưa? Vì sao?"
- **Sinh viên:** "Chưa đủ. Temperature thấp chỉ làm câu trả lời ổn định, không làm nó đúng hơn. Muốn chính xác thì nên dùng RAG: truy xuất đúng điều khoản quy định đưa vào prompt, bắt model trích dẫn nguồn và trả lời 'không biết' khi không tìm thấy."
- **Snoop:** **Hiểu tốt**, nhưng thêm: "Bạn nói thêm về RAG và trích dẫn nguồn, **nhưng bài giảng không đề cập**; để hiểu sâu hơn, thử giải thích cơ chế temperature…"
- **Nhận định:** ⚠️ Không trừ điểm, nhưng gạt đi giải pháp đúng trong thực tế để kéo sinh viên về nội dung bài.

#### Case 10 · Sổ hiểu bài – Vòng lặp đoán token, dùng thuật ngữ ngoài bài

- **Sinh viên:** "LLM là mô hình autoregressive: nó không soạn sẵn cả câu mà decode từng token một…"
- **Snoop:** **Hiểu tốt**, không phạt "autoregressive" hay "decode".
- **Nhận định:** ❌ **Case ngược.** Lần này thuật ngữ ngoài bài không bị phạt. Đặt cạnh case 4, điều này cho thấy cách chấm không nhất quán.

### Nhóm 3 – Kiến thức đúng nằm ngoài bài

#### Case 6 · Greedy và beam search

- **Sinh viên:** "Ngoài sampling thì LLM còn có thể chọn token bằng greedy hoặc beam search đúng không? Khi nào nên dùng cái nào?"
- **Snoop:** "Bài giảng chỉ dạy greedy và sampling, nên **mình chưa có căn cứ để nói về beam search**." Không trả lời phần "khi nào dùng".
- **Nhận định:** ✅ Khớp. Snoop từ chối kiến thức nền tảng và phổ biến.

#### Case 7 · Token là subword

- **Sinh viên:** "Token không phải là một từ đúng không? Mình đọc thấy thường là mảnh từ (subword, kiểu BPE)…"
- **Snoop:** "Bạn hiểu đúng hướng rồi, nhưng bài nói chưa tới mức đó… **Còn tên gọi BPE hay subword thì bài không dạy, mình không dám nói thêm.**"
- **Nhận định:** ✅ Khớp. Sinh viên nói đúng mà không được xác nhận rõ ràng.
  > Đối chiếu: trước đó, với câu hỏi "continual learning là gì", Snoop lại trả lời được, kèm nhãn "Ngoài bài giảng". Ranh giới "dám hay không dám nói ngoài bài" **không nhất quán**.

### Nhóm 4 – Đối chứng: sai nhưng dùng đúng từ khoá

#### Case 11 · Sổ hiểu bài – Attention

- **Sinh viên (cố ý sai 2 chỗ):** "Attention là một phép trộn có trọng số: model dùng query, key, value để **chọn ra đúng một từ quan trọng nhất rồi bỏ hẳn các từ còn lại**, và nó **nhìn cả các từ phía sau** để hiểu ngữ cảnh rồi mới đoán token tiếp theo."
- **Snoop:** **Cần xem lại**
  - Bắt được lỗi 1: attention không chọn một từ mà trộn nhiều vị trí.
  - **Bỏ sót lỗi 2:** model chỉ được nhìn các token phía trước (causal mask), dù bài có giảng phần này.
  - Lại bắt bẻ cụm "rồi mới đoán token tiếp theo", vốn không sai.
- **Nhận định:** ⚠️ Snoop không chấm thuần theo từ khoá. Nhưng chất lượng chấm **không ổn định**: bỏ sót lỗi thật và bắt lỗi không đáng bắt.

---

## 4. Tổng hợp theo dạng

| Dạng  | Biểu hiện                                                                                           | Case                  | Mức độ                                             |
| ----- | --------------------------------------------------------------------------------------------------- | --------------------- | -------------------------------------------------- |
| **A** | Từ chối hoặc gạt đi kiến thức đúng ngoài bài ("bài không dạy, mình không dám nói")                  | 6, 7, 9               | Rất rõ, lặp lại                                    |
| **B** | Không thoát được ví dụ và cách nói của bài giảng, kể cả khi sinh viên nói rõ trình độ hoặc ngữ cảnh | 3, 8 (1 chỉ một phần) | Rõ                                                 |
| **C** | Trừ điểm câu đúng vì khác bài giảng                                                                 | 0, 4                  | Rõ, nhưng không phải lúc nào cũng xảy ra (case 10) |
| **D** | Chấm không nhất quán giữa chat và Sổ hiểu bài, và giữa các lần                                      | 4 với 5, 4 với 10, 11 | Rõ                                                 |
| **E** | Không nhớ lượt chat vừa xong                                                                        | 2                     | Mới phát hiện, có thể là gốc của B                 |

### Những gì Snoop làm tốt (cần ghi nhận khi pitch)

- Khi được yêu cầu rất cụ thể, Snoop **có** đưa ra được ví dụ mới (case 1).
- Snoop không chấm thuần theo từ khoá: vẫn bắt được lỗi khái niệm lớn (case 11).
- Luôn gắn mốc video để nghe lại, rất tiện.
  → Vì vậy nên nói Snoop **thiếu nhất quán và quá thận trọng với bài giảng**, không nên nói Snoop "không bao giờ" làm được.

---

## 5. Câu pain point đề xuất

> **Snoop coi bài giảng là ranh giới của sự thật. Điều gì bài không dạy thì Snoop không dám xác nhận, dù sinh viên nói đúng. Cách bài không dùng thì Snoop không giải thích được. Và cách chấm thay đổi giữa các lần, nên sinh viên không biết tin vào đâu.**

3 trích dẫn nên đưa vào slide:

1. _"Bạn dùng 'logits' và 'softmax' là khái niệm ngoài bài giảng"_ (case 4)
2. _"BPE hay subword thì bài không dạy, mình không dám nói thêm"_ (case 7)
3. Xin ví dụ kinh doanh, nhận lại đúng ví dụ "nắng/mưa" của slide (case 8)

---

## 6. Hướng giải bằng AI agent (Input → Output)

### Input

1. Câu hỏi hoặc bài viết của sinh viên
2. Ngữ cảnh bài giảng: transcript, slide, mốc video đang xem
3. **Rubric ý cốt lõi** cho từng ý chính: bản chất cần nắm, các cách diễn đạt khác nhưng vẫn đúng, các hiểu lầm thường gặp
4. **Nguồn kiến thức tham chiếu ngoài bài**, để kiểm tra đúng sai mà không chỉ dựa vào lời giảng
5. **Hồ sơ người học và lịch sử hội thoại:** nền tảng, các cách giải thích đã thử, các ý từng sai

### Xử lý

1. Phân loại ý định: hỏi khái niệm, trả lời quiz, xin giảng lại, hay hỏi ngoài bài
2. Chấm theo **ý cốt lõi**, không so câu chữ
3. Câu đúng nhưng khác bài giảng thì **công nhận trước**, rồi nối về cách bài giảng nói
4. Chọn **cách giải thích khác lần trước**, theo trình độ người học
5. **Tự kiểm tra** đúng sai và độ nhất quán với các lần chấm trước rồi mới gửi

### Output

1. Kết luận 3 mức: **Đúng / Đúng nhưng khác góc nhìn bài giảng / Chưa đúng**, kèm lý do
2. Nhận xét ghi nhận phần đúng trước, rồi mới chỉ phần cần bổ sung
3. Một cách giải thích mới, không lặp lại lời giảng
4. Mốc video nên nghe lại
5. Một câu hỏi kiểm tra ngắn
6. Cập nhật Sổ hiểu bài và hồ sơ người học

### Ví dụ: case 4 nếu do agent chấm

- **Hiện tại:** "Cần củng cố – Bạn dùng 'logits' và 'softmax' là khái niệm ngoài bài giảng."
- **Agent:** "**Đúng.** Bạn mô tả chính xác cơ chế: temperature chia logits trước softmax nên phân phối nhọn hơn hoặc phẳng hơn. Bài giảng nói cùng ý đó bằng hình ảnh 'bảng khả năng trước khi rút thăm'. Câu hỏi thêm: nếu bảng đang nghiêng về đáp án sai, giảm temperature có giúp không? → Nghe lại 02:03."

---

## 7. Quan sát phụ (ngoài pain point chính)

- **Hiểu sai ý định:** hỏi "continual learning là gì" trong lúc video đang hiện câu quiz thì Snoop trả lời "Mình sẽ không đưa đáp án… bạn đang nghiêng về lựa chọn nào?". Phải gửi lại lần hai mới được trả lời.
- **Tiến độ không đồng bộ:** trang chủ báo 0%, "0/0 checkpoint", "Chưa có hoạt động học tập", trong khi Sổ hiểu bài đã có bài viết.
- **Video không nhớ vị trí:** rời trang khi đang ở 1:23 của Phần 2, quay lại thì về 0:08 màn intro, dù banner ghi "Đã khôi phục phiên học".
- **Lời chào sai giờ:** 17:34 (giờ Việt Nam) nhưng trang chào "Chào buổi sáng".
- **"Bạn học" ảo** (Naveen Thinking, Ducky Hay Hỏi) hiện dòng "đang chờ bạn trả lời", gây áp lực trong lúc xem video.

---

## 8. Giới hạn của thử nghiệm

- Chỉ 1 tài khoản, 1 bài (Ngày 1, Phần 2), khoảng 11 case trong khoảng 30 phút.
- Câu trả lời của Snoop có tính ngẫu nhiên. Mỗi case nên chạy lại 3–5 lần để đo tỉ lệ.
- Cần kiểm chứng thêm bằng khảo sát người dùng thật và log chat. Gợi ý chỉ số: tỉ lệ sinh viên gửi lại câu hỏi trong vòng 1 phút, tỉ lệ nhãn "Cần sửa" cho câu trả lời mà chuyên gia đánh giá là đúng.

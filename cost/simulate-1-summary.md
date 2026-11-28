# Tóm tắt mô phỏng simulate-1@20261128-120403

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 29 | 3 | 2481 | 403 | 2.8 | 2.6 |
| dung_vua | 17 | 4 | 3455 | 588 | 3.9 | 3.5 |
| dung_nhieu | 4 | 4 | 3546 | 660 | 3.8 | 3.8 |

Tỉ lệ đạt dùng để tính: 18/21 (86%) — lượt run-9@20261128-120235

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-9.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (143 người) | Chi phí / tháng — cơ sở (436 người) | Chi phí / tháng — cao (721 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-5-nano (vào 0.05 · ra 0.4 $/1M) | $0.00034 | $0.00040 | $0.00012 | $0.1754 | $0.5348 | $0.8843 | $0.0012 |
| gpt-6.1-terra (vào 1.0 · ra 5.0 $/1M) | $0.0053 | $0.0062 | $0.0018 | $2.74 | $8.36 | $13.83 | $0.0192 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (3.4) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gpt-5.4-nano. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.

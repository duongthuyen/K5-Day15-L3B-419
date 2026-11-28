"""Giao diện web localhost cho bản chạy thử — mô phỏng trang học pre-class + tutor. Chỉ dùng thư viện chuẩn.

Chạy: python run.py  (app.py gọi web.serve) → mở http://localhost:8000   ·   thêm ?debug=1 để hiện model/token.
- Trái: danh sách đoạn bài (đọc data/lessons.csv — cùng nguồn căn cứ của bot), tìm theo nội dung, có highlight.
- Giữa: trình phát MÔ PHỎNG (không có video thật): timeline có mốc từng đoạn, "phụ đề" là nội dung tóm tắt.
- Phải: tutor — gọi ĐÚNG answer() trong agent.py như bộ chạy eval (bot trên web = bot được chấm).
  · Câu trả lời render markdown an toàn (tự viết, escape trước — không cần thư viện, không cần mạng).
  · "Ghim" đoạn đang hỏi: nút "Mình vẫn chưa hiểu" gửi kèm tiêu đề đoạn → agent tra đúng chủ đề đó
    (agent đã hiểu dạng "chưa hiểu <chủ đề>"), không cần sửa agent.py.
  · Mã đoạn [DNN-VNN-NN] thành chip "▶ 00:57 Tiêu đề" bấm được → trình phát nhảy tới đoạn đó.
Lịch sử hội thoại giữ ở trình duyệt, ghép "[HV] … [Trợ lý] …" giống app.py dòng lệnh.
"""
import json
import os
import re
import sys
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tracing  # noqa: E402
import agent  # noqa: E402
from agent import answer  # noqa: E402

MAX_TURNS = 6      # giữ 6 lượt gần nhất (3 cặp hỏi–đáp) — bớt token đầu vào so với 8
MAX_CHARS = 500    # giới hạn độ dài câu hỏi (chặn sớm ở giao diện, có bộ đếm)
PORT = int(os.environ.get("PORT") or 8000)

PAGE = r"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Học trước buổi học · Tutor AI (bản chạy thử)</title>
<style>
  :root { --bg:#f5f3ee; --card:#fff; --ink:#1d1c1a; --muted:#625d54; --line:#e3ddd1;
          --accent:#1f5596; --accent-soft:#e8eff8; --warn:#9a3f12; --warn-soft:#fbede4;
          --player:#14181f; --mark:#fff2a8; --radius:12px; }
  * { box-sizing:border-box; }
  html,body { height:100%; }
  body { margin:0; font-family:"Segoe UI",-apple-system,Roboto,sans-serif; background:var(--bg); color:var(--ink);
         display:flex; flex-direction:column; font-size:15px; }
  :focus-visible { outline:3px solid #7aa7e0; outline-offset:2px; }
  button { font:inherit; cursor:pointer; }
  .sr { position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0); }
  mark { background:var(--mark); color:inherit; border-radius:2px; padding:0 1px; }

  header { display:flex; align-items:center; justify-content:space-between; gap:12px; padding:10px 20px;
           background:var(--card); border-bottom:1px solid var(--line); }
  header h1 { margin:0; font-size:17px; }
  header .sub { font-size:13px; color:var(--muted); }
  .badge { font-size:12px; background:var(--warn-soft); color:var(--warn); border-radius:999px; padding:3px 10px;
           font-weight:600; white-space:nowrap; }

  .layout { flex:1; min-height:0; display:grid; grid-template-columns:270px minmax(0,1fr) 400px; }
  @media (max-width:1400px) { .layout { grid-template-columns:240px minmax(0,1fr) 360px; } }
  @media (max-width:1100px) { .layout { grid-template-columns:230px minmax(0,1fr); }
                              .chat { grid-column:1 / -1; min-height:560px; } }
  @media (max-width:720px)  { .layout { grid-template-columns:1fr; } }

  /* Trái */
  nav { border-right:1px solid var(--line); background:var(--card); display:flex; flex-direction:column; min-height:0; }
  nav .tools { padding:12px; border-bottom:1px solid var(--line); }
  nav label { font-size:12px; color:var(--muted); display:block; margin-bottom:4px; }
  nav input { width:100%; padding:8px 10px; border:1px solid var(--line); border-radius:8px; font:inherit; }
  nav .found { font-size:12px; color:var(--muted); margin-top:6px; min-height:16px; }
  .lessons { overflow-y:auto; padding:6px 0 16px; }
  .vid { margin:12px 12px 4px; font-size:12.5px; font-weight:700; color:var(--muted); line-height:1.35; }
  .seg { display:flex; gap:10px; width:calc(100% - 16px); margin:1px 8px; text-align:left; padding:7px 10px;
         border:1px solid transparent; border-radius:8px; background:none; color:var(--ink); align-items:baseline; }
  .seg:hover { background:var(--bg); }
  .seg[aria-current="true"] { background:var(--accent-soft); border-color:#c4d6ee; }
  .seg .t { font-family:Consolas,monospace; font-size:12px; color:var(--accent); flex:none; }
  .seg .p { font-size:13.5px; line-height:1.35; }
  .seg .x { display:block; font-size:12px; color:var(--muted); margin-top:2px; }
  .empty-note { padding:16px; color:var(--muted); font-size:13px; }

  /* Giữa */
  main { overflow-y:auto; padding:20px; min-width:0; }
  .player { background:var(--player); color:#f2f2f2; border-radius:var(--radius); aspect-ratio:16/9; max-height:54vh;
            display:flex; flex-direction:column; justify-content:space-between; padding:16px 20px; }
  .ptop { display:flex; justify-content:space-between; align-items:flex-start; gap:12px; }
  .ptop .vt { font-size:14px; color:#c9d1dc; line-height:1.4; }
  .ptop .sim { flex:none; font-size:11.5px; color:#8f99a8; border:1px solid #3a4250; border-radius:999px; padding:2px 9px; white-space:nowrap; }
  .caption { font-size:clamp(15px,1.5vw,19px); line-height:1.5; background:rgba(0,0,0,.55); padding:10px 14px;
             border-radius:8px; align-self:center; max-width:92%; text-align:center; }
  .pbottom { display:flex; justify-content:flex-end; }
  .stuck-overlay { background:#ffffff; color:var(--accent); border:0; border-radius:999px; padding:8px 16px; font-weight:600;
                   box-shadow:0 2px 8px rgba(0,0,0,.3); }
  .controls { display:flex; align-items:center; gap:10px; margin-top:12px; flex-wrap:wrap; }
  .ctl { background:var(--card); border:1px solid var(--line); border-radius:8px; padding:7px 12px; color:var(--ink); white-space:nowrap; }
  .ctl:hover { border-color:var(--accent); color:var(--accent); }
  .clock { font-family:Consolas,monospace; font-size:13px; color:var(--muted); min-width:104px; }
  .timeline { position:relative; flex:1; min-width:160px; height:24px; cursor:pointer; }
  .timeline .rail { position:absolute; left:0; right:0; top:10px; height:4px; background:var(--line); border-radius:2px; }
  .timeline .fill { position:absolute; left:0; top:10px; height:4px; background:var(--accent); border-radius:2px; }
  .timeline .mk { position:absolute; top:4px; width:10px; height:16px; margin-left:-5px; background:none; border:none; padding:0; }
  .timeline .mk::after { content:""; position:absolute; left:3px; top:0; width:4px; height:16px; background:#9fb6d6; border-radius:2px; }
  .timeline .mk[aria-current="true"]::after { background:var(--accent); }
  .timeline .tip { position:absolute; bottom:26px; transform:translateX(-50%); background:var(--ink); color:#fff; font-size:12px;
                   padding:4px 8px; border-radius:6px; white-space:nowrap; pointer-events:none; display:none; }
  .segcard { margin-top:14px; background:var(--card); border:1px solid var(--line); border-radius:var(--radius); padding:14px 16px;
             display:flex; align-items:center; justify-content:space-between; gap:12px; flex-wrap:wrap; }
  .segcard h2 { margin:0; font-size:15px; }
  .segcard .meta { font-size:12.5px; color:var(--muted); margin-top:2px; }
  .primary { background:var(--accent); color:#fff; border:0; border-radius:8px; padding:9px 16px; font-weight:600; white-space:nowrap; }
  .primary:disabled { opacity:.5; cursor:default; }
  .keys { font-size:12px; color:var(--muted); margin-top:10px; }
  kbd { border:1px solid var(--line); border-bottom-width:2px; border-radius:4px; padding:0 5px; font-size:11.5px; background:var(--card); }

  /* Phải */
  .chat { border-left:1px solid var(--line); background:var(--card); display:flex; flex-direction:column; min-height:0; }
  .chat-head { padding:10px 14px; border-bottom:1px solid var(--line); display:flex; justify-content:space-between; align-items:center; gap:8px; }
  .chat-head h2 { margin:0; font-size:15px; }
  .pinbar { font-size:12.5px; color:var(--muted); margin-top:2px; }
  .pinbar b { color:var(--ink); font-weight:600; }
  .log { flex:1; overflow-y:auto; padding:14px; display:flex; flex-direction:column; gap:10px; }
  .msg { max-width:90%; padding:10px 13px; border-radius:12px; line-height:1.55; word-wrap:break-word; }
  .me { align-self:flex-end; background:var(--accent); color:#fff; border-bottom-right-radius:4px; white-space:pre-wrap; }
  .me .att { display:inline-block; font-size:12px; background:rgba(255,255,255,.18); border-radius:6px; padding:1px 7px; margin-bottom:4px; }
  .bot { align-self:flex-start; background:var(--bg); border:1px solid var(--line); border-bottom-left-radius:4px; }
  .bot p { margin:0 0 8px; } .bot p:last-child { margin-bottom:0; }
  .bot ul, .bot ol { margin:4px 0 8px; padding-left:20px; } .bot li { margin:2px 0; }
  .bot .h { display:block; font-weight:700; margin:8px 0 4px; }
  .bot hr { border:0; border-top:1px solid var(--line); margin:8px 0; }
  .bot code { font-family:Consolas,monospace; font-size:.9em; background:#ebe7de; padding:0 4px; border-radius:4px; }
  .bot.err { background:var(--warn-soft); border-color:#efc7ae; color:var(--warn); }
  .bot.typing { color:var(--muted); font-style:italic; }
  .meta2 { font-size:11.5px; color:var(--muted); margin-top:6px; }
  .cite { display:inline-flex; align-items:center; gap:4px; background:var(--accent-soft); color:var(--accent); border:1px solid #c4d6ee;
          font-size:.86em; font-weight:600; padding:0 7px; border-radius:6px; cursor:pointer; vertical-align:baseline; }
  .cite:hover { background:#d6e4f5; }
  .cite .ct { font-family:Consolas,monospace; }
  .follow { display:flex; flex-wrap:wrap; gap:6px; align-self:flex-start; max-width:90%; }
  .chip { border:1px solid var(--line); background:var(--card); border-radius:999px; padding:5px 11px; font-size:13px; color:var(--ink); }
  .chip:hover { border-color:var(--accent); color:var(--accent); }
  .chip.opt { border-color:#c4d6ee; color:var(--accent); }
  .intro { color:var(--muted); font-size:13.5px; line-height:1.5; }
  .toast { margin:0 14px 8px; padding:8px 12px; background:var(--ink); color:#fff; border-radius:8px; font-size:13px;
           display:flex; justify-content:space-between; align-items:center; gap:10px; }
  .toast button { background:none; border:0; color:#9cc4ff; font-weight:600; }
  form { border-top:1px solid var(--line); padding:10px 12px 12px; }
  .stuckbtn { width:100%; margin-bottom:8px; background:var(--accent-soft); color:var(--accent); border:1px solid #c4d6ee; border-radius:8px;
              padding:8px; font-weight:600; }
  .stuckbtn:disabled { opacity:.5; cursor:default; }
  textarea { width:100%; resize:none; border:1px solid var(--line); border-radius:10px; padding:10px 12px; font:inherit;
             min-height:44px; max-height:160px; overflow-y:auto; transition:box-shadow .3s; }
  textarea:focus { border-color:var(--accent); }
  textarea.prefilled { box-shadow:0 0 0 3px var(--mark); }
  .formrow { display:flex; justify-content:space-between; align-items:center; margin-top:6px; gap:8px; }
  .count { font-size:12px; color:var(--muted); }
  .count.over { color:var(--warn); font-weight:600; }
  #send { width:88px; display:inline-flex; justify-content:center; align-items:center; }
  .spin { width:16px; height:16px; border:2px solid rgba(255,255,255,.4); border-top-color:#fff; border-radius:50%; animation:sp .8s linear infinite; }
  @keyframes sp { to { transform:rotate(360deg); } }
  @media (prefers-reduced-motion: reduce) { .spin { animation:none; } }
  .disclaimer { font-size:11.5px; color:var(--muted); padding:0 12px 10px; }
</style>
</head>
<body>
<header>
  <div>
    <h1>Học trước buổi học</h1>
    <div class="sub">Xem đoạn bài → chưa hiểu thì hỏi tutor ngay tại đoạn đó.</div>
  </div>
  <span class="badge" title="Trang mô phỏng phục vụ demo, không phải trang học chính thức">Bản chạy thử · video mô phỏng</span>
</header>

<div class="layout">
  <nav aria-label="Danh sách đoạn bài">
    <div class="tools">
      <label for="filter">Tìm trong nội dung bài</label>
      <input id="filter" type="search" placeholder="vd: temperature, few-shot…" autocomplete="off">
      <div class="found" id="found" aria-live="polite"></div>
    </div>
    <div class="lessons" id="lessons"></div>
  </nav>

  <main>
    <section class="player" aria-label="Trình phát video mô phỏng">
      <div class="ptop">
        <div class="vt" id="vtitle">Chọn một đoạn bài ở cột trái</div>
        <span class="sim">mô phỏng · phụ đề là bản tóm tắt</span>
      </div>
      <div class="caption" id="caption" aria-live="polite">—</div>
      <div class="pbottom"><button class="stuck-overlay" id="stuck2">🤔 Chưa hiểu đoạn này</button></div>
    </section>
    <div class="controls">
      <button class="ctl" id="prev" aria-label="Đoạn trước">◀◀</button>
      <button class="ctl" id="play" aria-label="Phát">▶ Phát</button>
      <button class="ctl" id="next" aria-label="Đoạn sau">▶▶</button>
      <span class="clock" id="clock">00:00 / 00:00</span>
      <div class="timeline" id="timeline" role="group" aria-label="Thanh thời gian — mỗi vạch là đầu một đoạn">
        <div class="rail"></div><div class="fill" id="fill"></div><div class="tip" id="tip"></div>
      </div>
    </div>
    <article class="segcard" id="segcard" hidden>
      <div><h2 id="sctitle"></h2><div class="meta" id="scmeta"></div></div>
      <button class="primary" id="askseg">Hỏi tutor về đoạn này</button>
    </article>
    <div class="keys"><kbd>Space</kbd> phát/dừng · <kbd>←</kbd> <kbd>→</kbd> đoạn trước/sau · <kbd>Enter</kbd> gửi câu hỏi</div>
  </main>

  <section class="chat" aria-label="Tutor">
    <div class="chat-head">
      <div><h2>Tutor</h2><div class="pinbar" id="pinbar">Chưa chọn đoạn</div></div>
      <button class="ctl" id="reset" title="Xoá hội thoại hiện tại (hoàn tác được)">Phiên mới</button>
    </div>
    <div class="log" id="log" aria-live="polite" aria-relevant="additions"></div>
    <div id="toastbox"></div>
    <form id="f">
      <button type="button" class="stuckbtn" id="stuck">🤔 Mình vẫn chưa hiểu — giải thích cách khác</button>
      <label class="sr" for="q">Câu hỏi cho tutor</label>
      <textarea id="q" rows="1" maxlength="__MAX__" placeholder="Gõ câu hỏi… (Enter gửi, Shift+Enter xuống dòng)"></textarea>
      <div class="formrow">
        <span class="count" id="count">0/__MAX__</span>
        <button type="submit" class="primary" id="send">Gửi</button>
      </div>
    </form>
    <div class="disclaimer">Tutor là AI và có thể sai — bấm chip ▶ để đối chiếu với bài. Không làm hộ bài tập.</div>
  </section>
</div>

<script>
const MAX = __MAX__, DEBUG = /[?&]debug=1/.test(location.search);
const $ = id => document.getElementById(id);
let segs = [], byCode = {}, cur = null, pinned = null, history = [], playing = false, tick = null, t = 0, busy = false;

const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const toSec = (s, end) => { const p = String(s||'0').split('-').map(x => x.trim()).filter(Boolean);
  return (end ? p[p.length-1] : p[0] || '0').split(':').map(Number).reduce((a,b) => a*60 + (b||0), 0); };
const mmss = n => { n = Math.max(0, Math.floor(n)); return String(Math.floor(n/60)).padStart(2,'0') + ':' + String(n%60).padStart(2,'0'); };
const vidKey = s => s.ma_doan.slice(0, 7);
const segNo = s => s.ma_doan.slice(8);
const videoLabel = s => 'Ngày ' + Number(s.ma_doan.slice(1,3)) + ' · Video ' + Number(s.ma_doan.slice(5,7)) +
                        ' — ' + (s.video.split(' — ')[1] || s.video.replace(/^V\d+\s*·\s*/, ''));

/* ---------- markdown an toàn: escape TRƯỚC, chỉ chèn thẻ của mình; chịu được markdown viết sai ---------- */
function inline(s) {
  s = s.replace(/`([^`\n]+)`/g, '<code>$1</code>')
       .replace(/\*\*([^*\n]+?)\*\*/g, '<b>$1</b>')
       .replace(/(^|[\s(])\*([^*\n]+?)\*(?=[\s).,;:!?]|$)/g, '$1<i>$2</i>')
       .replace(/(^|[\s(])_([^_\n]+?)_(?=[\s).,;:!?]|$)/g, '$1<i>$2</i>')
       .replace(/\*\*|__/g, '');                                     /* ** lẻ (viết sai) → bỏ */
  return s.replace(/\[((?:D\d{2}-V\d{2}-\d{2})(?:\s*,\s*D\d{2}-V\d{2}-\d{2})*)\]/g, (m, list) =>
    list.split(/\s*,\s*/).map(cite).join(' '));
}
function cite(c) {
  const s = byCode[c];
  if (!s) return '<span class="cite" title="Mã này không có trong danh sách bài">' + c + '</span>';
  return '<button class="cite" data-code="' + c + '" title="' + esc(c + ' · ' + s.tieu_de) + '"><span class="ct">▶ ' + mmss(s.sec) +
         '</span>' + esc(short(s.tieu_de, 28)) + '</button>';
}
const short = (s, n) => s.length > n ? s.slice(0, n - 1).trim() + '…' : s;
function md(src) {
  const lines = esc(String(src).replace(/\r/g, '')).split('\n'); let html = '', list = null, para = [];
  const flushP = () => { if (para.length) { html += '<p>' + inline(para.join(' ')) + '</p>'; para = []; } };
  const flushL = () => { if (list) { html += '<' + list.t + '>' + list.items.map(x => '<li>' + inline(x) + '</li>').join('') + '</' + list.t + '>'; list = null; } };
  for (const raw of lines) {
    const l = raw.trim(); let m;
    if (!l) { flushP(); flushL(); continue; }
    if (/^(-{3,}|\*{3,}|_{3,})$/.test(l)) { flushP(); flushL(); html += '<hr>'; continue; }
    if ((m = l.match(/^#{1,6}\s*(.+)$/))) { flushP(); flushL(); html += '<span class="h">' + inline(m[1].replace(/#+$/, '')) + '</span>'; continue; }
    if ((m = l.match(/^[-*•+]\s+(.+)$/)) || (m = l.match(/^\d+[.)]\s+(.+)$/))) {
      const tp = /^\d/.test(l) ? 'ol' : 'ul'; flushP(); if (!list || list.t !== tp) { flushL(); list = {t: tp, items: []}; }
      list.items.push(m[1]); continue; }
    flushL(); para.push(l);
  }
  flushP(); flushL(); return html;
}

/* ---------- danh sách đoạn ---------- */
async function loadLessons() {
  try { segs = await (await fetch('/api/lessons')).json(); }
  catch (e) { $('lessons').innerHTML = '<div class="empty-note">Không tải được danh sách bài. Kiểm tra máy chủ còn chạy rồi tải lại trang.</div>'; return; }
  segs.forEach(s => { s.sec = toSec(s.moc_thoi_gian); s.endSec = toSec(s.moc_thoi_gian, true); byCode[s.ma_doan] = s; });
  renderList(); if (segs.length) select(segs[0].ma_doan);
}
const fold = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/đ/g, 'd');
function hl(text, q) {                                     /* highlight không phân biệt dấu */
  if (!q) return esc(text);
  const f = fold(text), i = f.indexOf(q); if (i < 0) return esc(text);
  return esc(text.slice(0, i)) + '<mark>' + esc(text.slice(i, i + q.length)) + '</mark>' + hl(text.slice(i + q.length), q);
}
function renderList() {
  const q = fold($('filter').value.trim());
  const shown = segs.filter(s => !q || fold(s.tieu_de + ' ' + s.noi_dung).includes(q));
  $('found').textContent = q ? (shown.length ? shown.length + ' đoạn có “' + $('filter').value.trim() + '”' : '') : '';
  if (!shown.length) { $('lessons').innerHTML = '<div class="empty-note">Không có đoạn nào nói về “' + esc($('filter').value.trim()) + '”. Thử từ ngắn hơn, hoặc hỏi thẳng tutor.</div>'; return; }
  let html = '', last = '';
  shown.forEach(s => {
    if (vidKey(s) !== last) { html += '<div class="vid">' + esc(videoLabel(s)) + '</div>'; last = vidKey(s); }
    let snippet = '';
    if (q) { const f = fold(s.noi_dung), i = f.indexOf(q);
             if (i >= 0) { const a = Math.max(0, i - 30); snippet = (a ? '…' : '') + hl(s.noi_dung.slice(a, i + q.length + 50), q) + '…'; } }
    html += '<button class="seg" data-code="' + s.ma_doan + '"' + (cur === s ? ' aria-current="true"' : '') + '><span class="t">' + mmss(s.sec) +
            '</span><span class="p">' + hl(s.tieu_de, q) + (snippet ? '<span class="x">' + snippet + '</span>' : '') + '</span></button>';
  });
  $('lessons').innerHTML = html;
  $('lessons').querySelectorAll('.seg').forEach(b => b.onclick = () => { setPlaying(false); select(b.dataset.code); });
}
$('filter').addEventListener('input', renderList);

/* ---------- trình phát mô phỏng ---------- */
const sameVideo = () => segs.filter(s => vidKey(s) === vidKey(cur));
const duration = () => Math.max(...sameVideo().map(s => Math.max(s.endSec, s.sec + 30)));
function select(code) {
  const s = byCode[code]; if (!s) return;
  const changed = !cur || vidKey(cur) !== vidKey(s);
  cur = s; t = s.sec; if (changed) buildTimeline(); paint(); renderList();
  const el = $('lessons').querySelector('[aria-current="true"]'); if (el) el.scrollIntoView({block:'nearest'});
}
function buildTimeline() {
  const tl = $('timeline'); tl.querySelectorAll('.mk').forEach(m => m.remove()); const d = duration();
  sameVideo().forEach(s => {
    const m = document.createElement('button'); m.className = 'mk'; m.style.left = (s.sec / d * 100) + '%';
    m.dataset.code = s.ma_doan; m.setAttribute('aria-label', 'Tới ' + mmss(s.sec) + ': ' + s.tieu_de);
    m.onclick = e => { e.stopPropagation(); select(s.ma_doan); };
    m.onmouseenter = m.onfocus = () => { const tp = $('tip'); tp.textContent = mmss(s.sec) + ' · ' + s.tieu_de; tp.style.left = m.style.left; tp.style.display = 'block'; };
    m.onmouseleave = m.onblur = () => { $('tip').style.display = 'none'; };
    tl.appendChild(m);
  });
}
$('timeline').addEventListener('click', e => {
  if (!cur || e.target.closest('.mk')) return;
  const r = e.currentTarget.getBoundingClientRect(); t = (e.clientX - r.left) / r.width * duration(); syncSeg(); paint();
});
function syncSeg() { const v = sameVideo(); let s = v[0]; v.forEach(x => { if (x.sec <= t) s = x; }); if (s !== cur) { cur = s; renderList(); } }
function paint() {
  if (!cur) return; const d = duration();
  $('vtitle').textContent = videoLabel(cur);
  $('caption').textContent = cur.noi_dung;
  $('clock').textContent = mmss(t) + ' / ' + mmss(d);
  $('fill').style.width = Math.min(100, t / d * 100) + '%';
  $('timeline').querySelectorAll('.mk').forEach(m => m.setAttribute('aria-current', m.dataset.code === cur.ma_doan));
  $('segcard').hidden = false; $('sctitle').textContent = cur.tieu_de;
  $('scmeta').textContent = 'Đoạn ' + segNo(cur) + ' · ' + mmss(cur.sec) + (cur.endSec > cur.sec ? '–' + mmss(cur.endSec) : '');
  if (!pinned) pinbar();
}
function setPlaying(on) {
  playing = on; clearInterval(tick);
  $('play').textContent = on ? '❚❚ Dừng' : '▶ Phát'; $('play').setAttribute('aria-label', on ? 'Tạm dừng' : 'Phát');
  if (on) tick = setInterval(() => { t += 1; if (t >= duration()) { t = duration(); setPlaying(false); } syncSeg(); paint(); }, 1000);
}
const step = d => { if (!cur) return; const v = sameVideo(), i = v.indexOf(cur), all = segs.indexOf(cur);
  const nx = v[i + d] || segs[all + d]; if (nx) { setPlaying(false); select(nx.ma_doan); } };
$('play').onclick = () => cur && setPlaying(!playing);
$('prev').onclick = () => step(-1); $('next').onclick = () => step(1);

/* ---------- tutor ---------- */
function pinbar() {
  const p = pinned || cur;
  $('pinbar').innerHTML = p ? (pinned ? 'Đang hỏi về: ' : 'Đang xem: ') + '<b>Đoạn ' + segNo(p) + ' · ' + esc(short(p.tieu_de, 34)) + '</b>' : 'Chưa chọn đoạn';
}
function intro() {
  $('log').innerHTML = '<div class="intro">Mình trả lời <b>chỉ dựa trên nội dung bài</b>, kèm chip ▶ để bạn mở lại đúng đoạn. ' +
    'Chưa hiểu thì bấm <b>🤔 Mình vẫn chưa hiểu</b> để được giải thích theo cách khác.</div>';
  followChips(false);
}
function add(cls, html) {
  const d = document.createElement('div'); d.className = 'msg ' + cls; d.innerHTML = html;
  $('log').appendChild(d); d.scrollIntoView({behavior:'smooth', block:'end'}); return d;
}
function followChips(afterAnswer, options) {
  $('log').querySelectorAll('.follow').forEach(x => x.remove());
  const box = document.createElement('div'); box.className = 'follow';
  const items = [];
  (options || []).forEach(o => items.push(['opt', o, o]));
  if (afterAnswer) {
    items.push(['chip', '🤔 Vẫn chưa hiểu', '__stuck']);
    if (pinned && cur !== pinned) items.push(['chip', '↩ Quay lại đoạn đang hỏi', '__back']);
  } else {
    const p = cur || segs[0];
    if (p) items.push(['chip', 'Đoạn “' + short(p.tieu_de, 30) + '” nói gì?', '__about']);
    items.push(['chip', 'Temperature thấp có làm câu trả lời đúng hơn không?', 'Temperature thấp có làm câu trả lời đúng hơn không?']);
  }
  items.forEach(([c, label, v]) => { const b = document.createElement('button'); b.className = 'chip' + (c === 'opt' ? ' opt' : '');
    b.textContent = label; b.onclick = () => onChip(v); box.appendChild(b); });
  $('log').appendChild(box);
}
function onChip(v) {
  if (v === '__stuck') return stuck();
  if (v === '__back') { setPlaying(false); return select(pinned.ma_doan); }
  if (v === '__about') { const p = cur; pinned = p; pinbar(); return ask('Đoạn “' + p.tieu_de + '” nói gì?', p); }
  ask(v, pinned);
}
/* câu hỏi lại kiểu "…A hay B?" → nút chọn A / B */
function options(out) {
  const last = out.trim().split(/\n/).pop(); if (!/\?\s*$/.test(last) || !/ hay /.test(last)) return [];
  const m = last.replace(/\*\*/g, '').match(/(?:ở|về|là|chỗ|phần)?\s*[“"]?([^?“”"]{3,80}?)[”"]?\s+hay\s+(?:là\s+)?[“"]?([^?“”"]{3,80}?)[”"]?\s*\??\s*$/);
  if (!m) return []; const clean = x => x.replace(/^(bạn\s+)?(đang\s+)?(vướng|rối)\s+(nhất\s+)?(ở\s+)?(chỗ|điểm|phần)?\s*/i, '').trim();
  const a = clean(m[1]).split(/[:,]\s+|\s[—–]\s/).pop(), b = clean(m[2]);
  return a && b && a.length < 70 && b.length < 70 ? ['Mình vướng ở: ' + a, 'Mình vướng ở: ' + b] : [];
}
$('log').addEventListener('click', e => { const b = e.target.closest('button.cite'); if (b) { setPlaying(false); select(b.dataset.code); followChips(true, []); } });

function setBusy(on) {
  busy = on; $('send').disabled = on || !$('q').value.trim() || $('q').value.length > MAX;
  $('send').innerHTML = on ? '<span class="spin" aria-hidden="true"></span><span class="sr">Đang trả lời</span>' : 'Gửi';
  $('stuck').disabled = on || !history.length;
}
async function ask(text, pin, displayText) {
  text = text.trim(); if (!text || busy) return;
  if (text.length > MAX) { add('bot err', 'Câu hỏi dài quá ' + MAX + ' ký tự — bạn rút gọn giúp mình nhé.'); return; }
  $('log').querySelector('.intro')?.remove(); $('log').querySelectorAll('.follow').forEach(x => x.remove());
  add('me', (pin ? '<span class="att">📎 Đoạn ' + segNo(pin) + ' · ' + mmss(pin.sec) + '</span>\n' : '') + esc(displayText || text));
  $('q').value = ''; $('q').classList.remove('prefilled'); grow(); updateCount(); setBusy(true);
  const wait = add('bot typing', 'Đang tra bài và soạn câu trả lời…');
  try {
    const r = await fetch('/api/answer', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({text, history})});
    const data = await r.json(); wait.remove();
    if (data.error) add('bot err', esc(data.error) + '<div class="meta2">Bạn thử gửi lại, hoặc bấm “Phiên mới” nếu lỗi lặp lại.</div>');
    else {
      history = data.history; const m = data.meta || {};
      add('bot', md(data.output) + (DEBUG ? '<div class="meta2">' + (m.model ? esc(m.model) + ' · ' + m.tokens_in + ' token vào · ' + m.tokens_out + ' ra · ' : 'không gọi model · ') + m.seconds + 's</div>' : ''));
      followChips(true, options(data.output));
    }
  } catch (e) { wait.remove(); add('bot err', 'Mất kết nối tới máy chủ. Kiểm tra cửa sổ terminal còn chạy <code>python run.py</code>, rồi gửi lại.'); }
  setBusy(false); $('q').focus();
}
/* "Mình vẫn chưa hiểu": ghim đoạn đang hỏi bằng cách gửi kèm tiêu đề → agent tra đúng chủ đề, không lạc sang đoạn khác */
function stuck() {
  if (!history.length) return;
  const p = pinned;
  ask(p ? 'Mình vẫn chưa hiểu ' + p.tieu_de : 'Mình vẫn chưa hiểu', p, 'Mình vẫn chưa hiểu, giải thích cách khác giúp mình');
}
$('stuck').onclick = stuck;
function askAboutSeg() {
  if (!cur) return; pinned = cur; pinbar();
  if (history.length) { ask('Mình chưa hiểu ' + cur.tieu_de, cur, 'Mình chưa hiểu đoạn này'); return; }
  $('q').value = 'Mình chưa hiểu đoạn “' + cur.tieu_de + '”, giải thích dễ hiểu hơn giúp mình?';
  $('q').classList.add('prefilled'); grow(); updateCount(); $('q').focus();
}
$('askseg').onclick = askAboutSeg; $('stuck2').onclick = () => { setPlaying(false); askAboutSeg(); };
function grow() { const q = $('q'); q.style.height = 'auto'; q.style.height = Math.min(160, q.scrollHeight + 2) + 'px'; }
function updateCount() { const n = $('q').value.length; $('count').textContent = n + '/' + MAX; $('count').classList.toggle('over', n >= MAX); setBusy(busy); }
$('q').addEventListener('input', () => { grow(); updateCount(); });
$('q').addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); } });
$('f').onsubmit = e => { e.preventDefault(); send(); };
function send() { const v = $('q').value; const pin = $('q').classList.contains('prefilled') ? pinned : null; if (!pin) pinned = cur; pinbar(); ask(v, pin || null); }

/* Phiên mới: xoá ngay + "Hoàn tác" trong 8 giây (không dùng confirm() chặn trang) */
let undo = null;
$('reset').onclick = () => {
  if (!history.length) { intro(); return; }
  const saved = {html: $('log').innerHTML, history, pinned};
  history = []; pinned = null; pinbar(); intro(); setBusy(false);
  clearTimeout(undo?.timer);
  $('toastbox').innerHTML = '<div class="toast" role="status">Đã bắt đầu phiên mới.<button id="undo">Hoàn tác</button></div>';
  undo = {timer: setTimeout(() => $('toastbox').innerHTML = '', 8000)};
  $('undo').onclick = () => { $('log').innerHTML = saved.html; history = saved.history; pinned = saved.pinned; pinbar();
                              $('toastbox').innerHTML = ''; setBusy(false); };
};
document.addEventListener('keydown', e => {
  if (/TEXTAREA|INPUT/.test(document.activeElement.tagName) || e.ctrlKey || e.metaKey || e.altKey) return;
  if (e.key === ' ' || e.key === 'k') { e.preventDefault(); $('play').click(); }
  else if (e.key === 'ArrowLeft') { e.preventDefault(); step(-1); }
  else if (e.key === 'ArrowRight') { e.preventDefault(); step(1); }
});

intro(); updateCount(); setBusy(false); loadLessons().then(() => intro());
</script>
</body>
</html>""".replace("__MAX__", str(MAX_CHARS))


def _one_line(s):
    return " ".join(str(s).split())


def _title(noi_dung, video=""):
    """Tiêu đề ngắn cho một đoạn — lấy cụm đầu câu (trước ':' / '.' / ';' / ' — '), tối đa ~7 từ."""
    s = re.sub(r"^\s*(Tóm tắt[^:]*:|Bài [^:]*:|Ví dụ[^:]*:)\s*", "", noi_dung.strip()) or noi_dung.strip()
    head = re.split(r"[:.;]|\s—\s|\s–\s|\(", s, maxsplit=1)[0].strip()
    words = head.split()
    if len(words) > 7:
        head = " ".join(words[:7]) + "…"
    return head[:1].upper() + head[1:] if head else video


def lessons():
    """Các đoạn bài dùng làm căn cứ (cùng nguồn với search_lesson) — để hiển thị, không gọi model."""
    out = []
    for r in agent._lesson_rows():
        row = {k: r.get(k, "") for k in ("ma_doan", "video", "moc_thoi_gian", "noi_dung")}
        row["tieu_de"] = (r.get("tieu_de") or "").strip() or _title(row["noi_dung"], row["video"])
        out.append(row)
    return out


def handle(text, history):
    """Ghép hội thoại giống app.py dòng lệnh rồi gọi answer(). Trả dict cho trình duyệt."""
    history = [h for h in history if isinstance(h, str)][-MAX_TURNS:]
    if "[HV]" in text or "[Trợ lý]" in text:
        dialog, turns = text, None
    else:
        turns = (history + ["[HV] " + _one_line(text)])[-MAX_TURNS:]
        dialog = " ".join(turns)
    t0 = time.time()
    tracing.begin("app")
    try:
        result = answer(dialog)
    except Exception as e:
        tracing.end()
        return {"error": "Lỗi khi trả lời (%s): %s" % (type(e).__name__, e)}
    summary, _ = tracing.end()
    output = result.get("output", "") if isinstance(result, dict) else str(result)
    new_hist = (turns + ["[Trợ lý] " + _one_line(output)])[-MAX_TURNS:] if turns is not None else history
    meta = {"model": ", ".join(summary.get("models") or []),
            "tokens_in": summary.get("tokens_in", 0), "tokens_out": summary.get("tokens_out", 0),
            "seconds": round(time.time() - t0, 1)}
    return {"output": output, "history": new_hist, "meta": meta}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            self._send(200, PAGE, "text/html")
        elif path == "/api/lessons":
            self._send(200, json.dumps(lessons(), ensure_ascii=False), "application/json")
        else:
            self._send(404, "not found", "text/plain")

    def do_POST(self):
        if self.path != "/api/answer":
            return self._send(404, "not found", "text/plain")
        try:
            n = int(self.headers.get("Content-Length") or 0)
            body = json.loads(self.rfile.read(n).decode("utf-8") or "{}")
            text = str(body.get("text") or "").strip()[:MAX_CHARS]
            history = body.get("history") or []
        except Exception:
            return self._send(400, json.dumps({"error": "yêu cầu không hợp lệ"}), "application/json")
        res = handle(text, history if isinstance(history, list) else []) if text else {"error": "Câu hỏi trống."}
        self._send(200, json.dumps(res, ensure_ascii=False), "application/json")

    def log_message(self, fmt, *args):  # gọn terminal: chỉ in yêu cầu hỏi đáp
        if "/api/answer" in (args[0] if args else ""):
            sys.stderr.write("  %s\n" % (fmt % args))


def serve(port=PORT, open_browser=True):
    # Chỉ nghe trên máy này (127.0.0.1): không lộ bot + key ra mạng phòng thi.
    httpd = HTTPServer(("127.0.0.1", port), Handler)
    url = "http://localhost:%d" % port
    print("Bản chạy thử (web) đang chạy: %s  — dừng: Ctrl+C  (thêm ?debug=1 để xem model/token)" % url)
    print("Bản dòng lệnh: python codebase/app.py --cli")
    if open_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
    finally:
        httpd.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(serve())

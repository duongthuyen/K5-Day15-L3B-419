"""Giao diện web localhost cho bản chạy thử — mô phỏng trang học pre-class + tutor. Chỉ dùng thư viện chuẩn.

Chạy: python run.py  (app.py gọi web.serve) → mở http://localhost:8000
- Trái: danh sách bài / đoạn video (đọc từ data/lessons.csv — cùng nguồn căn cứ của bot).
- Giữa: trình phát MÔ PHỎNG (không có video thật): timeline có mốc từng đoạn, "phụ đề" là nội dung tóm tắt.
- Phải: tutor — gọi ĐÚNG answer() trong agent.py như bộ chạy eval (bot trên web = bot được chấm).
  Mã đoạn [DNN-VNN-NN] trong câu trả lời bấm được → trình phát nhảy tới đúng đoạn.
Lịch sử hội thoại giữ ở trình duyệt, ghép "[HV] … [Trợ lý] …" giống app.py dòng lệnh.
"""
import json
import os
import sys
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tracing  # noqa: E402
import agent  # noqa: E402
from agent import answer  # noqa: E402

MAX_TURNS = 8      # giống app.py: giữ tối đa 8 lượt gần nhất
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
          --accent:#1f5596; --accent-soft:#e8eff8; --ok:#2c6e49; --warn:#9a3f12; --warn-soft:#fbede4;
          --player:#14181f; --radius:12px; }
  * { box-sizing:border-box; }
  html,body { height:100%; }
  body { margin:0; font-family:"Segoe UI",-apple-system,Roboto,sans-serif; background:var(--bg); color:var(--ink);
         display:flex; flex-direction:column; font-size:15px; }
  :focus-visible { outline:3px solid #7aa7e0; outline-offset:2px; }
  button { font:inherit; cursor:pointer; }
  .sr { position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0); }

  header { display:flex; align-items:center; justify-content:space-between; gap:12px; padding:10px 20px;
           background:var(--card); border-bottom:1px solid var(--line); }
  header h1 { margin:0; font-size:17px; }
  header .sub { font-size:13px; color:var(--muted); }
  .badge { font-size:12px; background:var(--warn-soft); color:var(--warn); border-radius:999px; padding:3px 10px;
           font-weight:600; white-space:nowrap; }

  .layout { flex:1; min-height:0; display:grid; grid-template-columns:280px minmax(0,1fr) 400px; }
  @media (max-width:1100px) { .layout { grid-template-columns:240px minmax(0,1fr); }
                              .chat { grid-column:1 / -1; min-height:520px; } }
  @media (max-width:720px)  { .layout { grid-template-columns:1fr; } }

  /* Trái: danh sách bài */
  nav { border-right:1px solid var(--line); background:var(--card); display:flex; flex-direction:column; min-height:0; }
  nav .tools { padding:12px; border-bottom:1px solid var(--line); }
  nav label { font-size:12px; color:var(--muted); display:block; margin-bottom:4px; }
  nav input { width:100%; padding:8px 10px; border:1px solid var(--line); border-radius:8px; font:inherit; }
  .lessons { overflow-y:auto; padding:6px 0 16px; }
  .vid { margin:10px 12px 4px; font-size:12.5px; font-weight:700; color:var(--muted); }
  .seg { display:grid; grid-template-columns:auto 1fr; gap:2px 8px; width:calc(100% - 16px); margin:2px 8px;
         text-align:left; padding:8px 10px; border:1px solid transparent; border-radius:8px; background:none; color:var(--ink); }
  .seg:hover { background:var(--bg); }
  .seg[aria-current="true"] { background:var(--accent-soft); border-color:#c4d6ee; }
  .seg .t { font-family:Consolas,monospace; font-size:12px; color:var(--accent); grid-row:span 2; padding-top:1px; }
  .seg .c { font-size:11.5px; color:var(--muted); font-family:Consolas,monospace; }
  .seg .p { font-size:13px; line-height:1.35; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }
  .empty-note { padding:16px; color:var(--muted); font-size:13px; }

  /* Giữa: trình phát mô phỏng */
  main { overflow-y:auto; padding:20px; min-width:0; }
  .player { background:var(--player); color:#f2f2f2; border-radius:var(--radius); aspect-ratio:16/9; max-height:56vh;
            display:flex; flex-direction:column; justify-content:space-between; padding:18px 22px; position:relative; }
  .player .vt { font-size:14px; color:#b9c2cf; }
  .player .sim { position:absolute; top:16px; right:18px; font-size:11.5px; color:#8f99a8; border:1px solid #3a4250;
                 border-radius:999px; padding:2px 9px; }
  .caption { font-size:clamp(15px,1.6vw,19px); line-height:1.5; background:rgba(0,0,0,.55); padding:10px 14px;
             border-radius:8px; align-self:center; max-width:92%; text-align:center; }
  .controls { display:flex; align-items:center; gap:12px; margin-top:12px; }
  .ctl { background:var(--card); border:1px solid var(--line); border-radius:8px; padding:7px 14px; color:var(--ink); }
  .ctl:hover { border-color:var(--accent); color:var(--accent); }
  .clock { font-family:Consolas,monospace; font-size:13px; color:var(--muted); min-width:110px; }
  .timeline { position:relative; flex:1; height:22px; cursor:pointer; }
  .timeline .rail { position:absolute; left:0; right:0; top:9px; height:4px; background:var(--line); border-radius:2px; }
  .timeline .fill { position:absolute; left:0; top:9px; height:4px; background:var(--accent); border-radius:2px; }
  .timeline .mk { position:absolute; top:4px; width:4px; height:14px; margin-left:-2px; background:#9fb6d6; border-radius:2px;
                  border:none; padding:0; }
  .timeline .mk[aria-current="true"] { background:var(--accent); height:16px; top:3px; }
  .segcard { margin-top:16px; background:var(--card); border:1px solid var(--line); border-radius:var(--radius); padding:16px 18px; }
  .segcard h2 { margin:0 0 6px; font-size:15px; }
  .segcard .meta { font-size:12.5px; color:var(--muted); margin-bottom:8px; font-family:Consolas,monospace; }
  .segcard p { margin:0 0 12px; line-height:1.55; }
  .primary { background:var(--accent); color:#fff; border:0; border-radius:8px; padding:9px 16px; font-weight:600; }
  .primary:disabled { opacity:.5; cursor:default; }
  .hint { font-size:12.5px; color:var(--muted); margin-top:10px; }

  /* Phải: tutor */
  .chat { border-left:1px solid var(--line); background:var(--card); display:flex; flex-direction:column; min-height:0; }
  .chat-head { padding:12px 16px; border-bottom:1px solid var(--line); display:flex; justify-content:space-between; align-items:center; gap:8px; }
  .chat-head h2 { margin:0; font-size:15px; }
  .chat-head p { margin:2px 0 0; font-size:12px; color:var(--muted); }
  .log { flex:1; overflow-y:auto; padding:14px; display:flex; flex-direction:column; gap:10px; }
  .msg { max-width:88%; padding:10px 13px; border-radius:12px; line-height:1.5; white-space:pre-wrap; word-wrap:break-word; }
  .me { align-self:flex-end; background:var(--accent); color:#fff; border-bottom-right-radius:4px; }
  .bot { align-self:flex-start; background:var(--bg); border:1px solid var(--line); border-bottom-left-radius:4px; }
  .bot.err { background:var(--warn-soft); border-color:#efc7ae; color:var(--warn); }
  .bot.typing { color:var(--muted); font-style:italic; }
  .meta2 { font-size:11.5px; color:var(--muted); margin-top:6px; }
  .code { display:inline-block; background:var(--accent-soft); color:var(--accent); border:1px solid #c4d6ee; font-weight:600;
          font-family:Consolas,monospace; font-size:.85em; padding:0 6px; border-radius:5px; cursor:pointer; }
  .code:hover { background:#d6e4f5; }
  .intro { color:var(--muted); font-size:13.5px; line-height:1.5; }
  .chips { display:flex; flex-wrap:wrap; gap:6px; margin-top:8px; }
  .chip { border:1px solid var(--line); background:var(--card); border-radius:999px; padding:6px 12px; font-size:13px; color:var(--ink); }
  .chip:hover { border-color:var(--accent); color:var(--accent); }
  form { border-top:1px solid var(--line); padding:10px 12px 12px; }
  textarea { width:100%; resize:none; border:1px solid var(--line); border-radius:10px; padding:10px 12px; font:inherit; height:64px; }
  textarea:focus { border-color:var(--accent); }
  .formrow { display:flex; justify-content:space-between; align-items:center; margin-top:6px; gap:8px; }
  .count { font-size:12px; color:var(--muted); }
  .count.over { color:var(--warn); font-weight:600; }
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
  <nav aria-label="Danh sách bài học">
    <div class="tools">
      <label for="filter">Tìm đoạn bài</label>
      <input id="filter" type="search" placeholder="vd: temperature, few-shot…" autocomplete="off">
    </div>
    <div class="lessons" id="lessons" role="list"></div>
  </nav>

  <main>
    <section class="player" aria-label="Trình phát video mô phỏng">
      <div class="vt" id="vtitle">Chọn một đoạn bài ở cột trái</div>
      <span class="sim">mô phỏng — phụ đề là bản tóm tắt</span>
      <div class="caption" id="caption" aria-live="polite">—</div>
      <div></div>
    </section>
    <div class="controls">
      <button class="ctl" id="play" aria-label="Phát">▶ Phát</button>
      <span class="clock" id="clock">00:00 / 00:00</span>
      <div class="timeline" id="timeline" role="group" aria-label="Thanh thời gian, các vạch là đầu mỗi đoạn">
        <div class="rail"></div><div class="fill" id="fill"></div>
      </div>
    </div>
    <article class="segcard" id="segcard" hidden>
      <h2 id="sctitle"></h2>
      <div class="meta" id="scmeta"></div>
      <p id="sctext"></p>
      <button class="primary" id="askseg">Mình chưa hiểu đoạn này</button>
      <div class="hint">Câu hỏi được điền sẵn vào ô chat để bạn sửa trước khi gửi.</div>
    </article>
  </main>

  <section class="chat" aria-label="Tutor">
    <div class="chat-head">
      <div><h2>Tutor</h2><p>Chỉ trả lời theo nội dung bài · có mã đoạn để bạn kiểm lại</p></div>
      <button class="ctl" id="reset" title="Xoá hội thoại hiện tại">Phiên mới</button>
    </div>
    <div class="log" id="log" aria-live="polite" aria-relevant="additions"></div>
    <form id="f">
      <label class="sr" for="q">Câu hỏi cho tutor</label>
      <textarea id="q" maxlength="__MAX__" placeholder="Gõ câu hỏi… (Enter để gửi, Shift+Enter xuống dòng)"></textarea>
      <div class="formrow">
        <span class="count" id="count">0/__MAX__</span>
        <button type="submit" class="primary" id="send">Gửi</button>
      </div>
    </form>
    <div class="disclaimer">Tutor là AI và có thể sai — bấm mã đoạn để đối chiếu với bài. Không làm hộ bài tập.</div>
  </section>
</div>

<script>
const MAX = __MAX__;
const $ = id => document.getElementById(id);
let segs = [], byCode = {}, cur = null, history = [], playing = false, tick = null, t = 0, busy = false;

const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const toSec = s => (s||'0').split(':').map(Number).reduce((a,b) => a*60 + (b||0), 0);
const mmss = n => { n = Math.max(0, Math.floor(n)); const m = Math.floor(n/60), s = n % 60;
                    return String(m).padStart(2,'0') + ':' + String(s).padStart(2,'0'); };
const videoOf = s => s.video.split(' — ')[0];
const topicOf = s => (s.video.split(' — ')[1] || s.video);

/* ---------- danh sách bài ---------- */
async function loadLessons() {
  try {
    const r = await fetch('/api/lessons'); segs = await r.json();
  } catch (e) { $('lessons').innerHTML = '<div class="empty-note">Không tải được danh sách bài. Kiểm tra máy chủ đang chạy rồi tải lại trang.</div>'; return; }
  segs.forEach(s => { s.sec = toSec(s.moc_thoi_gian); byCode[s.ma_doan] = s; });
  renderList('');
  if (segs.length) select(segs[0].ma_doan, false);
}
function renderList(f) {
  f = f.trim().toLowerCase();
  const shown = segs.filter(s => !f || (s.noi_dung + ' ' + s.video + ' ' + s.ma_doan).toLowerCase().includes(f));
  if (!shown.length) { $('lessons').innerHTML = '<div class="empty-note">Không có đoạn nào khớp “' + esc(f) + '”. Thử từ khoá ngắn hơn.</div>'; return; }
  let html = '', last = '';
  shown.forEach(s => {
    if (s.video !== last) { html += '<div class="vid">' + esc(s.video) + '</div>'; last = s.video; }
    html += '<button class="seg" role="listitem" data-code="' + esc(s.ma_doan) + '"' + (cur && cur.ma_doan === s.ma_doan ? ' aria-current="true"' : '') +
            '><span class="t">' + mmss(s.sec) + '</span><span class="c">' + esc(s.ma_doan) + '</span><span class="p">' + esc(s.noi_dung) + '</span></button>';
  });
  $('lessons').innerHTML = html;
  $('lessons').querySelectorAll('.seg').forEach(b => b.onclick = () => select(b.dataset.code, true));
}
$('filter').addEventListener('input', e => renderList(e.target.value));

/* ---------- trình phát mô phỏng ---------- */
const sameVideo = () => segs.filter(s => s.video === cur.video);
const duration = () => { const v = sameVideo(); return Math.max(...v.map(s => s.sec)) + 60; };
function select(code, focusCard) {
  const s = byCode[code]; if (!s) return;
  const changedVideo = !cur || cur.video !== s.video;
  cur = s; t = s.sec;
  if (changedVideo) buildTimeline();
  paint();
  renderList($('filter').value);
  if (focusCard) $('segcard').scrollIntoView({behavior:'smooth', block:'nearest'});
}
function buildTimeline() {
  const tl = $('timeline'); tl.querySelectorAll('.mk').forEach(m => m.remove());
  const d = duration();
  sameVideo().forEach(s => {
    const m = document.createElement('button');
    m.className = 'mk'; m.style.left = (s.sec / d * 100) + '%';
    m.title = mmss(s.sec) + ' · ' + s.ma_doan; m.setAttribute('aria-label', 'Tới đoạn ' + s.ma_doan + ' lúc ' + mmss(s.sec));
    m.dataset.code = s.ma_doan;
    m.onclick = e => { e.stopPropagation(); select(s.ma_doan, false); };
    tl.appendChild(m);
  });
}
$('timeline').addEventListener('click', e => {           /* bấm vào thanh → tua tới thời điểm đó */
  if (!cur) return;
  const r = e.currentTarget.getBoundingClientRect();
  t = (e.clientX - r.left) / r.width * duration(); syncSegToTime(); paint();
});
function syncSegToTime() {                               /* đoạn hiện tại = đoạn cuối có mốc ≤ t */
  const v = sameVideo(); let s = v[0];
  v.forEach(x => { if (x.sec <= t) s = x; }); if (s !== cur) { cur = s; renderList($('filter').value); }
}
function paint() {
  if (!cur) return;
  const d = duration();
  $('vtitle').textContent = videoOf(cur) + ' · ' + topicOf(cur);
  $('caption').textContent = cur.noi_dung;
  $('clock').textContent = mmss(t) + ' / ' + mmss(d);
  $('fill').style.width = Math.min(100, t / d * 100) + '%';
  $('timeline').querySelectorAll('.mk').forEach(m => m.setAttribute('aria-current', m.dataset.code === cur.ma_doan));
  $('segcard').hidden = false;
  $('sctitle').textContent = topicOf(cur);
  $('scmeta').textContent = cur.ma_doan + ' · từ ' + mmss(cur.sec);
  $('sctext').textContent = cur.noi_dung;
}
function setPlaying(on) {
  playing = on; clearInterval(tick);
  $('play').textContent = on ? '❚❚ Tạm dừng' : '▶ Phát'; $('play').setAttribute('aria-label', on ? 'Tạm dừng' : 'Phát');
  if (on) tick = setInterval(() => { t += 1; if (t >= duration()) { t = duration(); setPlaying(false); }
                                     syncSegToTime(); paint(); }, 1000);
}
$('play').onclick = () => cur && setPlaying(!playing);

/* ---------- tutor ---------- */
function fmt(s) {
  return esc(s).replace(/\[(D\d{2}-V\d{2}-\d{2})\]/g, (m, c) => byCode[c]
    ? '<button class="code" data-code="' + c + '" title="Mở đoạn ' + c + ' (' + mmss(byCode[c].sec) + ')">' + c + ' · ' + mmss(byCode[c].sec) + '</button>'
    : '<span class="code" title="Mã này không có trong danh sách bài">' + c + '</span>');
}
function intro() {
  $('log').innerHTML = '<div class="intro">Mình trả lời <b>chỉ dựa trên nội dung bài</b>, kèm mã đoạn để bạn bấm xem lại. ' +
    'Nói “mình vẫn chưa hiểu” để được giải thích theo cách khác.<div class="chips">' +
    ['Sampling là gì?', 'Temperature thấp có làm câu trả lời đúng hơn không?', 'mình vẫn chưa hiểu']
      .map(s => '<button class="chip">' + esc(s) + '</button>').join('') + '</div></div>';
  $('log').querySelectorAll('.chip').forEach(b => b.onclick = () => ask(b.textContent));
}
function add(cls, html) {
  const intro = $('log').querySelector('.intro'); if (intro) intro.remove();
  const d = document.createElement('div'); d.className = 'msg ' + cls; d.innerHTML = html;
  $('log').appendChild(d); d.scrollIntoView({behavior:'smooth', block:'end'}); return d;
}
$('log').addEventListener('click', e => { const b = e.target.closest('button.code'); if (b) { setPlaying(false); select(b.dataset.code, true); } });

function setBusy(on) { busy = on; $('send').disabled = on || !$('q').value.trim() || $('q').value.length > MAX;
                       $('send').textContent = on ? 'Đang trả lời…' : 'Gửi'; }
async function ask(text) {
  text = text.trim(); if (!text || busy) return;
  if (text.length > MAX) { add('bot err', 'Câu hỏi dài quá ' + MAX + ' ký tự — bạn rút gọn giúp mình nhé.'); return; }
  add('me', esc(text)); $('q').value = ''; updateCount(); setBusy(true);
  const wait = add('bot typing', 'Đang tra bài và soạn câu trả lời…');
  try {
    const r = await fetch('/api/answer', {method:'POST', headers:{'Content-Type':'application/json'},
                                          body: JSON.stringify({text, history})});
    const data = await r.json(); wait.remove();
    if (data.error) add('bot err', esc(data.error) + '<div class="meta2">Bạn thử gửi lại, hoặc bấm “Phiên mới” nếu lỗi lặp lại.</div>');
    else {
      history = data.history; const m = data.meta || {};
      add('bot', fmt(data.output) + (m.model
        ? '<div class="meta2">' + esc(m.model) + ' · ' + (m.tokens_in||0) + ' token vào · ' + (m.tokens_out||0) + ' ra · ' + (m.seconds||0) + 's</div>'
        : '<div class="meta2">trả lời theo luật, không gọi model</div>'));
    }
  } catch (e) { wait.remove(); add('bot err', 'Mất kết nối tới máy chủ. Kiểm tra cửa sổ terminal còn chạy <code>python run.py</code> không, rồi gửi lại.'); }
  setBusy(false); $('q').focus();
}
function updateCount() { const n = $('q').value.length; $('count').textContent = n + '/' + MAX;
                         $('count').classList.toggle('over', n >= MAX); setBusy(busy); }
$('q').addEventListener('input', updateCount);
$('q').addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); ask($('q').value); } });
$('f').onsubmit = e => { e.preventDefault(); ask($('q').value); };
$('askseg').onclick = () => { if (!cur) return;
  $('q').value = 'Mình chưa hiểu đoạn này: ' + topicOf(cur) + ' — ' + cur.noi_dung.split('.')[0] + '. Giải thích dễ hiểu hơn giúp mình?';
  updateCount(); $('q').focus(); };
$('reset').onclick = () => { if (history.length && !confirm('Xoá hội thoại hiện tại và bắt đầu phiên mới?')) return;
                             history = []; intro(); $('q').focus(); };
document.addEventListener('keydown', e => {             /* phím tắt: k = phát/dừng (khi không gõ chữ) */
  if (e.key === 'k' && !/TEXTAREA|INPUT/.test(document.activeElement.tagName)) { e.preventDefault(); $('play').click(); } });

intro(); updateCount(); loadLessons();
</script>
</body>
</html>""".replace("__MAX__", str(MAX_CHARS))


def _one_line(s):
    return " ".join(str(s).split())


def lessons():
    """Các đoạn bài dùng làm căn cứ (cùng nguồn với search_lesson) — để hiển thị, không gọi model."""
    return [{k: r.get(k, "") for k in ("ma_doan", "video", "moc_thoi_gian", "noi_dung")} for r in agent._lesson_rows()]


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
        if self.path in ("/", "/index.html"):
            self._send(200, PAGE, "text/html")
        elif self.path == "/api/lessons":
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
    print("Bản chạy thử (web) đang chạy: %s  — dừng: Ctrl+C" % url)
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

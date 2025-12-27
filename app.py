from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

DB_PATH = "bookings.db"

# Admin key: đặt trên Render Environment -> ADMIN_KEY
# Nếu chưa đặt thì tạm dùng 1234
ADMIN_KEY = os.environ.get("ADMIN_KEY", "1234")

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,
            name TEXT,
            phone TEXT,
            date TEXT,
            time TEXT,
            service TEXT,
            combo TEXT,
            note TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

HOME_HTML = r"""
<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Bin Hair Studio</title>
  <style>
    :root{
      --bg1:#0ea5e9;
      --bg2:#22c55e;
      --card:#ffffff;
      --muted:#6b7280;
      --text:#111827;
      --shadow: 0 18px 45px rgba(0,0,0,.12);
      --radius: 18px;
    }
    *{box-sizing:border-box}
    body{
      margin:0;
      font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      color:var(--text);
      background:
        radial-gradient(1000px 700px at 10% 10%, rgba(34,197,94,.25), transparent 60%),
        radial-gradient(900px 650px at 90% 20%, rgba(14,165,233,.25), transparent 55%),
        linear-gradient(135deg, #f8fafc, #eef2ff);
      padding: 22px 12px 40px;
    }
    .wrap{max-width: 960px; margin:0 auto;}
    .card{
      background: var(--card);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      overflow:hidden;
      border: 1px solid rgba(17,24,39,.06);
    }
    .hero{
      padding: 20px 18px 10px;
      display:flex;
      gap:16px;
      align-items:flex-start;
      justify-content:space-between;
      flex-wrap:wrap;
    }
    h1{
      margin:0;
      font-size: 30px;
      letter-spacing: .2px;
    }
    .sub{
      margin:6px 0 0;
      color: var(--muted);
      font-size: 14px;
    }
    .pill{
      display:inline-flex;
      gap:10px;
      align-items:center;
      padding:10px 12px;
      border-radius: 999px;
      background: rgba(17,24,39,.04);
      color: #111827;
      font-weight: 600;
      font-size: 13px;
      border: 1px solid rgba(17,24,39,.06);
    }

    /* Buttons row */
    .btns{
      padding: 0 18px 16px;
      display:flex;
      gap:10px;
      flex-wrap:wrap;
    }
    .btn{
      flex: 1 1 220px;
      display:flex;
      align-items:center;
      justify-content:center;
      gap:10px;
      padding: 14px 12px;
      border-radius: 16px;
      text-decoration:none;
      color:#fff;
      font-weight:800;
      letter-spacing:.2px;
      box-shadow: 0 10px 25px rgba(0,0,0,.10);
      transform: translateY(0);
      transition: .15s ease;
      user-select:none;
    }
    .btn:hover{ transform: translateY(-1px); }
    .btn span{
      display:block;
      font-weight:700;
      font-size: 13px;
      opacity:.9;
    }
    .b1{ background: linear-gradient(135deg, #16a34a, #22c55e); }
    .b2{ background: linear-gradient(135deg, #f97316, #fb7185); }
    .b3{ background: linear-gradient(135deg, #0ea5e9, #2563eb); }

    /* Section */
    .section{
      padding: 14px 18px 18px;
      border-top: 1px solid rgba(17,24,39,.06);
    }
    .section h3{
      margin: 0 0 12px;
      font-size: 18px;
      display:flex;
      align-items:center;
      gap:10px;
    }
    .hint{
      color: var(--muted);
      font-size: 13px;
      margin-top: 6px;
      line-height:1.4;
    }

    /* Gallery */
    .gallery-grid{
      display:grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
    }
    @media (max-width: 860px){
      .gallery-grid{ grid-template-columns: 1fr; }
      .btn{ flex:1 1 100%; }
    }
    .gallery-item{
      border-radius: 16px;
      overflow:hidden;
      border: 1px solid rgba(17,24,39,.08);
      background: #fff;
      box-shadow: 0 10px 22px rgba(0,0,0,.07);
    }
    .gallery-item img{
      width:100%;
      height: 220px;
      object-fit: cover;
      display:block;
      background: #f3f4f6;
    }
    .cap{
      padding: 12px 12px 13px;
      display:flex;
      align-items:flex-start;
      justify-content:space-between;
      gap: 10px;
    }
    .cap b{font-size:14px}
    .cap .price{
      font-weight:900;
      color:#b45309;
      white-space:nowrap;
      font-size: 13px;
    }
    .cap .desc{
      margin-top:6px;
      color: var(--muted);
      font-size:12.5px;
      line-height:1.35;
    }

    /* Booking */
    form{
      display:grid;
      gap:10px;
      margin-top: 12px;
    }
    .row{
      display:grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }
    @media (max-width: 520px){
      .row{ grid-template-columns: 1fr; }
    }
    input, textarea{
      width:100%;
      padding: 12px 12px;
      border-radius: 14px;
      border: 1px solid rgba(17,24,39,.14);
      outline:none;
      font-size: 14px;
      background: #fff;
    }
    textarea{ min-height: 90px; resize: vertical; }
    .submit{
      padding: 14px 14px;
      border:0;
      border-radius: 16px;
      background: #111827;
      color:#fff;
      font-weight:900;
      cursor:pointer;
      box-shadow: 0 10px 25px rgba(17,24,39,.22);
    }
    .submit:hover{ filter: brightness(1.05); }

    .msg{
      margin: 0 18px 10px;
      padding: 12px 12px;
      border-radius: 14px;
      background: rgba(34,197,94,.12);
      border: 1px solid rgba(34,197,94,.25);
      color: #166534;
      font-weight: 700;
    }
    .footer{
      padding: 10px 18px 18px;
      color: var(--muted);
      font-size: 12.5px;
      border-top: 1px solid rgba(17,24,39,.06);
    }
 /* ===== PILL ROW (Inbox + Fanpage) ===== */
.pill-row{
  display:flex;
  gap:10px;
  flex-wrap:wrap;              /* mobile tự xuống dòng */
  align-items:center;
  margin-top:12px;
}

/* ===== PILL BASE ===== */
.pill{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  gap:8px;

  padding:10px 14px;
  border-radius:999px;
  font-weight:800;
  font-size:13px;
  line-height:1;

  text-decoration:none;
  user-select:none;
  cursor:pointer;

  color:#0f172a;
  background:rgba(255,255,255,.9);
  border:1px solid rgba(17,24,39,.12);
  box-shadow:0 10px 22px rgba(17,24,39,.10);

  transition:transform .18s ease, box-shadow .18s ease, filter .18s ease;
}

.pill:hover{
  transform:translateY(-2px);
  box-shadow:0 16px 30px rgba(17,24,39,.16);
  filter:saturate(1.05);
}

.pill:active{
  transform:translateY(0px) scale(.99);
}

/* focus cho bàn phím */
.pill:focus-visible{
  outline:3px solid rgba(59,130,246,.35);
  outline-offset:2px;
}

/* ===== VARIANTS ===== */
.pill-fb{
  color:#fff;
  border:none;
  background:linear-gradient(135deg,#1877f2,#0ea5e9);
}

.pill-fanpage{
  color:#fff;
  border:none;
  background:linear-gradient(135deg,#8b5cf6,#ec4899);
}

/* icon nhỏ xinh */
.pill .ico{
  font-size:14px;
  line-height:1;
}

/* ===== MOBILE ===== */
@media (max-width:520px){
  .pill-row{ gap:8px; }
  .pill{
    width:100%;               /* mobile mỗi pill 1 dòng cho đẹp */
    justify-content:center;
    padding:12px 14px;
    font-size:14px;
  }
}
 .pill:active{
  transform: scale(.97);
}
  </style>
</head>

<body>
  <div class="wrap">
    <div class="card">
      <div class="hero">
        <div>
          <h1>Bin Hair Studio</h1>
          <p class="sub">Uốn · Nhuộm · Phục hồi · Chăm sóc tóc nữ</p>
          <div style="margin-top:10px">
  <div class="pill-row">
  <a class="pill pill-fb"
     href="https://m.me/61566317721912"
     target="_blank" rel="noopener">
     💬 Inbox Facebook • Tư vấn & đặt lịch nhanh
  </a>

  <a class="pill pill-fanpage"
     href="https://www.facebook.com/profile.php?id=61566317721912"
     target="_blank" rel="noopener">
     📌 Fanpage Bin Hair Studio
  </a>
</div>
</div>
          </div>
        </div>
        <div style="text-align:right">
          <div class="pill">⏰ Giờ vàng: 07:30 & 09:30 (-10%)</div>
        </div>
      </div>

      {% if msg %}
        <div class="msg">{{ msg }}</div>
      {% endif %}

      <div class="btns">
        <a class="btn b1" href="tel:0931668146">📞 Gọi ngay <span>0931 668 146</span></a>
        <a class="btn b2" href="tel:0799978985">📞 Gọi ngay <span>0799 978 985</span></a>
        <a class="btn b3" href="#booking-form" onclick="document.getElementById('booking-form').scrollIntoView({behavior:'smooth'});return false;">🗓️ Đặt lịch <span>nhanh trong 30s</span></a>
      </div>

      <div class="section">
        <h3>💰 Bảng giá dịch vụ</h3>

        <!-- 1 ảnh / 1 dịch vụ để khỏi thừa -->
        <div class="gallery-grid">
          <div class="gallery-item">
            <img src="{{ url_for('static', filename='images/balayage.jpg') }}" alt="Balayage">
            <div class="cap">
              <div>
                <b>BALAYAGE</b>
                <div class="desc">Sáng tự nhiên · sang · không lộ chân tóc</div>
              </div>
              <div class="price">1.500k – 2.500k</div>
            </div>
          </div>

          <div class="gallery-item">
            <img src="{{ url_for('static', filename='images/ombre.jpg') }}" alt="Ombre">
            <div class="cap">
              <div>
                <b>OMBRE</b>
                <div class="desc">Chuyển màu đậm → nhạt rõ · cá tính</div>
              </div>
              <div class="price">1.000k – 2.000k</div>
            </div>
          </div>

          <div class="gallery-item">
            <img src="{{ url_for('static', filename='images/highlight.jpg') }}" alt="Highlight">
            <div class="cap">
              <div>
                <b>HIGHLIGHT</b>
                <div class="desc">Tạo điểm nhấn · che sâu mái · tăng độ dày</div>
              </div>
              <div class="price">400k – 800k</div>
            </div>
          </div>
        </div>

        <div class="hint">
          <b>UỐN / ÉP</b>
<div class="price">400.000đ – 1.000.000đ</div>
<div class="desc">
Tạo form chuẩn, giữ nếp bền đẹp, tóc mềm mại tự nhiên – phù hợp mọi dáng tóc.
</div>

<br>

<b>NHUỘM</b>
<div class="price">300.000đ – 900.000đ</div>
<div class="desc">
Lên màu thời trang, tôn da – chuẩn tone, hạn chế khô xơ, phai màu.
</div>

<br>

<b>✨ COMBO NHUỘM + UỐN / ÉP ✨</b>
<div class="desc">
Sự kết hợp hoàn hảo cho mái tóc <b>vừa vào nếp đẹp – vừa lên màu chuẩn salon</b>.
</div>
<div class="desc">
🎁 <b>Tặng kèm 01 lần hấp máy phục hồi chuyên sâu</b> giúp tóc chắc khỏe,
bóng mượt, giảm hư tổn và giữ nếp – giữ màu bền lâu hơn.
</div>
<div class="desc">
Lựa chọn lý tưởng cho khách muốn làm đẹp trọn gói, tiết kiệm thời gian
mà vẫn đảm bảo tóc khỏe đẹp từ trong ra ngoài.
</div>
        </div>
      </div>

      <div class="section" id="booking-form">
        <h3>📝 Đặt lịch nhanh</h3>
        <form method="post" action="/">
          <input name="name" placeholder="Tên" required>
          <input name="phone" placeholder="SĐT" type="tel" required>

          <div class="row">
            <input type="date" name="date" required>
            <input type="time" name="time" required>
          </div>

          <input name="service" placeholder="Dịch vụ (uốn/nhuộm/ép/phục hồi...)">
          <input name="combo" placeholder="Combo (nếu có)">
          <textarea name="note" placeholder="Ghi chú (tóc yếu/đã tẩy/khung giờ...)"></textarea>

          <button class="submit" type="submit">✅ Xác nhận đặt lịch</button>
        </form>

        <div class="hint">
          Sau khi gửi, salon sẽ inbox/ gọi xác nhận lịch sớm nhất.
        </div>
      </div>

      <div class="footer">
        © Bin Hair Studio · Made with ❤️
      </div>
    </div>
  </div>
</body>
</html>
"""

ADMIN_HTML = r"""
<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Admin - Bin Hair Studio</title>
  <style>
    body{font-family:system-ui,Segoe UI,Arial; background:#f6f7fb; margin:0; padding:18px;}
    .wrap{max-width:1000px; margin:0 auto;}
    .card{background:#fff; border:1px solid #e6e7ee; border-radius:16px; padding:16px; box-shadow:0 12px 30px rgba(0,0,0,.06);}
    h2{margin:0 0 10px}
    .muted{color:#6b7280}
    table{width:100%; border-collapse:collapse; font-size:14px; margin-top:10px;}
    th,td{border-bottom:1px solid #eee; padding:10px 8px; text-align:left; vertical-align:top;}
    th{background:#fafafa}
    code{background:#f3f4f6; padding:2px 6px; border-radius:8px}
    .bad{background:#fee2e2; border:1px solid #fecaca; color:#7f1d1d; padding:12px; border-radius:12px; font-weight:700;}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <h2>Admin</h2>

      {% if not ok %}
        <div class="bad">
          Sai key. Vào đúng dạng:
          <code>/admin?key=YOUR_KEY</code>
        </div>
      {% else %}
        <div class="muted">Tổng lịch: <b>{{ rows|length }}</b></div>
        <table>
          <tr>
            <th>ID</th>
            <th>Thời gian tạo</th>
            <th>Tên</th>
            <th>SĐT</th>
            <th>Ngày</th>
            <th>Giờ</th>
            <th>Dịch vụ</th>
            <th>Combo</th>
            <th>Ghi chú</th>
          </tr>
          {% for r in rows %}
          <tr>
            <td>{{ r["id"] }}</td>
            <td>{{ r["created_at"] }}</td>
            <td>{{ r["name"] }}</td>
            <td>{{ r["phone"] }}</td>
            <td>{{ r["date"] }}</td>
            <td>{{ r["time"] }}</td>
            <td>{{ r["service"] }}</td>
            <td>{{ r["combo"] }}</td>
            <td>{{ r["note"] }}</td>
          </tr>
          {% endfor %}
        </table>
      {% endif %}
    </div>
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        phone = (request.form.get("phone") or "").strip()
        date = (request.form.get("date") or "").strip()
        time = (request.form.get("time") or "").strip()
        service = (request.form.get("service") or "").strip()
        combo = (request.form.get("combo") or "").strip()
        note = (request.form.get("note") or "").strip()

        if not name or not phone or not date or not time:
            return render_template_string(HOME_HTML, msg="❌ Thiếu thông tin bắt buộc (Tên/SĐT/Ngày/Giờ).")

        conn = db()
        conn.execute(
            "INSERT INTO bookings(created_at,name,phone,date,time,service,combo,note) VALUES (?,?,?,?,?,?,?,?)",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name, phone, date, time, service, combo, note)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("home", ok=1))

    msg = None
    if request.args.get("ok") == "1":
        msg = "✅ Đặt lịch thành công! Salon sẽ liên hệ xác nhận sớm nhất."
    return render_template_string(HOME_HTML, msg=msg)

@app.route("/admin")
def admin():
    key = request.args.get("key", "")
    ok = (key == ADMIN_KEY)

    rows = []
    if ok:
        conn = db()
        rows = conn.execute("SELECT * FROM bookings ORDER BY id DESC").fetchall()
        conn.close()

    return render_template_string(ADMIN_HTML, ok=ok, rows=rows)

if __name__ == "__main__":
    # chạy local: python app.py
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))





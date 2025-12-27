from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# ========== CONFIG ==========
DB = os.environ.get("DB_PATH", "bookings.db")
# Deploy (Render) nhớ set biến môi trường ADMIN_KEY (Settings -> Environment)
ADMIN_KEY = os.environ.get("ADMIN_KEY", "1234")


# ========== DB HELPERS ==========
def get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as con:
        con.execute(
            """
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
            """
        )
        con.commit()


init_db()


# ========== HTML ==========
HOME = r"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Bin Hair Studio</title>
  <style>
    body{font-family:Arial; margin:0; padding:0; background:#f6f7fb;}
    .wrap{max-width:900px; margin:24px auto; padding:0 12px;}
    .card{background:#fff; border:1px solid #e6e6e6; border-radius:16px; padding:18px; box-shadow:0 6px 18px rgba(0,0,0,.06);}
    h1{margin:0 0 8px;}
    .sub{color:#555; margin:0 0 14px;}
    .btns{display:flex; gap:10px; flex-wrap:wrap; margin:14px 0 6px;}
    .btn{
      display:flex; align-items:center; justify-content:center;
      gap:8px; min-width:180px;
      padding:14px 10px; border-radius:16px; text-decoration:none;
      color:#fff; font-weight:700; box-shadow:0 8px 20px rgba(0,0,0,.18);
    }
    .b1{background:linear-gradient(135deg,#00c853,#00a843);}
    .b2{background:linear-gradient(135deg,#ff6f00,#ff8f00);}
    .btn span{display:block; font-size:13px; font-weight:600; opacity:.95;}
    .section{margin-top:14px;}
    .service{white-space:pre-line; background:#fafafa; border:1px dashed #ddd; padding:12px; border-radius:12px; line-height:1.45;}
    form{margin-top:12px;}
    input, textarea{
      width:100%; box-sizing:border-box; padding:12px;
      border:1px solid #ddd; border-radius:12px; margin:8px 0; font-size:15px;
      outline:none;
    }
    .row{display:flex; gap:10px;}
    .row > div{flex:1;}
    button{
      width:100%; padding:14px 12px; border:0; border-radius:14px;
      background:#111; color:#fff; font-weight:800; cursor:pointer;
    }
    .msg{margin:10px 0; padding:10px 12px; border-radius:12px; background:#eef7ff; border:1px solid #cfe8ff; color:#0b4a7a;}
    .hint{color:#666; font-size:13px; margin-top:6px;}
    .price-box {
  background: #f9f9f9;
  border-radius: 14px;
  padding: 16px;
  margin-bottom: 16px;
}

.price-box h4 {
  margin: 0 0 6px;
  font-size: 18px;
}

.price {
  font-weight: 700;
  color: #d35400;
  margin: 4px 0;
}

.desc {
  font-size: 14px;
  color: #555;
  line-height: 1.5;
}

.note {
  font-size: 13px;
  color: #777;
  margin-top: 12px;
}
  
</style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <h1>Bin Hair Studio</h1>
      <p class="sub">Uốn - Nhuộm - Phục hồi - Chăm sóc tóc nữ</p>

      {% if msg %}
        <div class="msg">{{ msg }}</div>
      {% endif %}

      <div class="btns">
        <!-- Hotline 1 -->
        <a class="btn b1" href="tel:0931668146">
          📞 Gọi ngay<br>
          <span>0931 668 146</span>
        </a>

        <!-- Hotline 2 -->
        <a class="btn b2" href="tel:0799978985">
          📞 Gọi ngay<br>
          <span>0799 978 985</span>
        </a>

        <!-- Đặt lịch -->
        <a class="btn b1" href="#booking-form"
           onclick="document.getElementById('booking-form').scrollIntoView({behavior:'smooth'}); return false;">
          🗓️ Đặt lịch
        </a>
      </div>

      <div class="section">
        <h3 style="margin:10px 0 8px;">💰 Bảng giá dịch vụ</h3>
        <div class="service">
BALAYAGE
- Balayage
Phù hợp khách thích tóc Tây,không lộ chân tóc
  Hiệu ứng sáng tự nhiên, sang trọng.
  1.500k - 2.500k
OMBRE
1.000k-2.000k
Chuyển màu đậm --> nhạt rõ ràng 
Cá tính - nổi bật - thời thượng 
HIGHLIGHT
400k-800k
Tăng độ dày,chiều sâu cho mái tóc 
  Tạo điểm nhấn, che sâu mái tóc.

COMBO uốn/ép/…  400.000 - 1.000.000đ (tuỳ chiều dài tóc)
 Nhuộm màu thời trang ( tuỳ chiều dài tóc)
 300.000 - 900.000đ
ComBo nhuộm-uốn được nằm máy hấp phục hồi chuyên sâu cho tóc hư tổn vừa qua hoá chất 
🎁 ƯU ĐÃI KHUNG GIỜ VÀNG
- Đặt lịch 07:30 - 09:30 sáng giảm 10% tổng hóa đơn
- Đi 2 người sẽ được giảm 10% tổng hoá đơn 
        </div>
      </div>

      <div class="section" id="booking-form">
        <h3 style="margin:10px 0 8px;">📝 Inbox Facebook để tư vấn & đặt lịch nhanh</h3>

        <form method="post" action="{{ url_for('book') }}">
          <input name="name" placeholder="Tên" required />
          <input name="phone" placeholder="SĐT" required />

          <div class="row">
            <div><input type="date" name="date" required /></div>
            <div><input type="time" name="time" required /></div>
          </div>

          <input name="service" placeholder="Dịch vụ (uốn/nhuộm/phục hồi…)" />
          <input name="combo" placeholder="Combo (nếu có)" />
          <textarea name="note" placeholder="Ghi chú"></textarea>

          <button type="submit">Đặt lịch</button>
          <div class="hint">* Sau khi đặt lịch, salon sẽ liên hệ xác nhận.</div>
        </form>
      </div>

    </div>
  </div>
</body>
</html>
"""

ADMIN = r"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Admin - Web Salon</title>
  <style>
    body{font-family:Arial; background:#f6f7fb; margin:0;}
    .wrap{max-width:1100px; margin:24px auto; padding:0 12px;}
    .card{background:#fff; border:1px solid #e6e6e6; border-radius:16px; padding:16px; box-shadow:0 6px 18px rgba(0,0,0,.06);}
    table{width:100%; border-collapse:collapse;}
    th,td{border-bottom:1px solid #eee; padding:10px; text-align:left; vertical-align:top;}
    th{background:#fafafa;}
    .ok{display:inline-block; padding:6px 10px; border-radius:999px; background:#e8fff1; color:#067d3c; border:1px solid #bff0d0; font-weight:700;}
    .bad{display:inline-block; padding:6px 10px; border-radius:999px; background:#ffecec; color:#a30000; border:1px solid #ffc5c5; font-weight:700;}
    .top{display:flex; gap:10px; align-items:center; flex-wrap:wrap;}
    .keybox{padding:10px 12px; border:1px solid #ddd; border-radius:12px; min-width:240px;}
    .btn{padding:10px 12px; background:#111; color:#fff; border-radius:12px; text-decoration:none; font-weight:700;}
    .muted{color:#666;}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <div class="top">
        <h2 style="margin:0;">Admin</h2>
        {% if ok %}
          <span class="ok">Đúng key ✅</span>
        {% else %}
          <span class="bad">Sai key ❌</span>
        {% endif %}
        <span class="muted">Mở: /admin?key=YOUR_KEY</span>
      </div>

      <div style="margin:12px 0;">
        <form method="get" action="{{ url_for('admin') }}">
          <input class="keybox" name="key" placeholder="Nhập key admin..." value="{{ key|e }}" />
          <button class="btn" type="submit">Xem</button>
          <a class="btn" href="{{ url_for('home') }}" style="background:#4b5563;">Về trang chủ</a>
        </form>
      </div>

      {% if ok %}
        <table>
          <tr>
            <th>ID</th>
            <th>Created</th>
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
      {% else %}
        <p class="muted">Nhập đúng key để xem danh sách đặt lịch.</p>
      {% endif %}
    </div>
  </div>
</body>
</html>
"""


# ========== ROUTES ==========
@app.get("/")
def home():
    msg = request.args.get("msg", "")
    return render_template_string(HOME, msg=msg)


@app.post("/book")
def book():
    name = (request.form.get("name") or "").strip()
    phone = (request.form.get("phone") or "").strip()
    date = (request.form.get("date") or "").strip()
    time_ = (request.form.get("time") or "").strip()
    service = (request.form.get("service") or "").strip()
    combo = (request.form.get("combo") or "").strip()
    note = (request.form.get("note") or "").strip()

    # Bắt buộc tối thiểu
    if not (name and phone and date and time_):
        return redirect(url_for("home", msg="Thiếu thông tin, nhập lại nhé!"))

    created_at = datetime.now().isoformat(timespec="seconds")

    with get_conn() as con:
        con.execute(
            """
            INSERT INTO bookings(created_at, name, phone, date, time, service, combo, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (created_at, name, phone, date, time_, service, combo, note),
        )
        con.commit()

    return redirect(url_for("home", msg="Đặt lịch thành công! Salon sẽ liên hệ xác nhận."))


@app.get("/admin")
def admin():
    key = request.args.get("key", "")
    ok = (key == ADMIN_KEY)

    rows = []
    if ok:
        with get_conn() as con:
            rows = con.execute(
                """
                SELECT id, created_at, name, phone, date, time, service, combo, note
                FROM bookings
                ORDER BY id DESC
                """
            ).fetchall()

    return render_template_string(ADMIN, ok=ok, rows=rows, key=key)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)






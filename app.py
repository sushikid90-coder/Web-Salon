from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB = "bookings.db"

PAGE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Bin Hair Studio / Đặt lịch làm tóc Nam Nữ </title>
  <style>
    body{font-family:Arial; max-width:720px; margin:24px auto; padding:0 12px;}
    input, select, textarea, button{width:100%; padding:10px; margin:8px 0; box-sizing:border-box;}
    .row{display:flex; gap:10px;}
    .row > div{flex:1;}
    .msg{background:#f8fff0; padding:10px; border:1px solid #cde7b0; margin:10px 0;}
    .err{background:#fff0f0; padding:10px; border:1px solid #f0b0b0; margin:10px 0;}
    a{color:#0a66c2;}
    table{width:100%; border-collapse:collapse; margin-top:12px;}
    th, td{border:1px solid #ddd; padding:8px; text-align:left;}
  </style>
</head>
<body>
  <h2>Bin Hair Studio</h2><p
  style="Color : #888 : margin-top: -6px:">
  Uốn - Nhuộm - Phục hồi - Chăm sóc tóc nữ <?p>
  <div style="
  background:#fff;
  border:1px solid #eee;
  border-radius:14px;
  padding:14px;
  margin:14px 0;
">
  <b style="font-size:16px;">💰 Bảng giá dịch vụ</b>

  <table style="margin-top:10px;">
   <!-- các <tr> bảng giá của bạn -->
</table>
  <div class="card">
  <span class="badge">✨ Dịch vụ nổi bật</span>

  <div class="hair-grid">

    <div class="hair-card">
  <div class="hair-head">
    <div class="hair-title">BALAYAGE</div>
    <div class="hair-price">1.500k – 2.500k</div>
  </div>

  <div class="hair-photos">
    <img src="/static/images/balayage1.jpg" alt="Balayage 1">
    <img src="/static/images/balayage2.jpg" alt="Balayage 2">
</div>
  </div>
  <div class="hair-note">
    Hiệu ứng sáng tự nhiên, sang trọng.
  </div>
</div>
    <div class="hair-card">
  <div class="hair-head">
    <div class="hair-title">OMBRE</div>
    <div class="hair-price">1.000k – 2.000k</div>
  </div>
  <div class="hair-photos">
    <img src="/static/images/ombre1.jpg" alt="Ombre 1">
    <img src="/static/images/ombre2.jpg" alt="Ombre 2">
</div>
  </div>
  <div class="hair-note">
    Chuyển màu mềm mại, nữ tính.
  </div>
</div>
    </div>
    <div class="hair-card">
  <div class="hair-head">
    <div class="hair-title">HIGHLIGHT</div>
    <div class="hair-price">400k – 800k</div>
  </div>
  <div class="hair-photos">
    <img src="/static/images/highlight1.jpg" alt="Highlight 1">
    <img src="/static/images/highlight2.jpg" alt="Highlight 2">
</div>
  </div>

  <div class="hair-note">
    Tạo điểm nhấn, chiều sâu mái tóc.
  </div>
</div>
    </div>

  </div>
</div>
</div>
    <tr>
      <td>✂️ Cắt + gội + sấy</td>
      <td><b>100.000đ</b></td>
    </tr>
    <tr>
  <td>🌊 Uốn tóc</td>
  <td><b>400.000 - 1.000.000đ</b></td>
</tr>

<tr>
  <td>🎨 Nhuộm tóc</td>
  <td><b>300.000 - 900.000đ</b></td>
</tr>

<tr>
  <td colspan="2" style="
    background: linear-gradient(135deg,#f7e7dc,#fdf6f1);
    border-radius:14px;
    padding:14px;
    font-size:14px;
    color:#555;
    line-height:1.5;
  ">
    💖 <b style="font-size:15px;">Combo Uốn & Nhuộm cao cấp</b><br>
    <style>
    .wrap{max-width:1050px;margin:28px auto;padding:0 14px;}
.header{
  text-align:center;
  margin-bottom:14px;
  padding:16px 12px;
  border:1px solid #e9d8e6;
  border-radius:16px;
  background:linear-gradient(135deg,#fff7fb,#f7fbff);
}
.brand{font-size:28px;letter-spacing:1px;margin:0;font-weight:800;}
.sub{margin:6px 0 0;color:#777;font-size:13px}

.grid{
  display:flex;
  gap:16px;
  align-items:flex-start;
}
.col{flex:1;}
.card{
  border:1px solid #eed9e7;
  border-radius:16px;
  background:#fff;
  padding:14px;
  box-shadow:0 6px 18px rgba(0,0,0,.05);
}

.badge{
  display:inline-block;
  padding:6px 10px;
  border-radius:999px;
  font-size:12px;
  background:#fff1f6;
  border:1px dashed #d98ab0;
  color:#a24c73;
  font-weight:700;
}

.price-table{width:100%;border-collapse:collapse;margin-top:10px;}
.price-table td{border-bottom:1px solid #f0e1ea;padding:10px 6px;}
.price-table td:last-child{text-align:right;font-weight:800;color:#333;}

.gallery{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:10px;
  margin-top:12px;
}
.gitem{
  border:1px solid #f0dbe7;
  border-radius:14px;
  overflow:hidden;
  background:#fff;
}
.gitem img{width:100%;height:150px;object-fit:cover;display:block;}
.gcap{padding:8px 10px;font-size:12px;color:#666;}
.gtitle{font-weight:800;color:#333}
@media(max-width:900px){
  .grid{flex-direction:column;}
  .gallery{grid-template-columns:1fr;}
  .gitem img{height:190px;}
}
</style>
    Tặng kèm <b>hấp phục hồi bằng máy</b> giúp tóc mềm mượt,
    giảm hư tổn, giữ màu bền đẹp và vào nếp tự nhiên.<br>
    <span style="font-size:12px;color:#888;">
      * Áp dụng khi làm combo trong cùng buổi
      </span>
  </td>
      <tr>
  <td colspan="2" style="
    background:#fff3f6;
    border:1px dashed #f3b6c8;
    border-radius:14px;
    padding:14px;
    margin-top:8px;
    font-size:14px;
    color:#555;
    line-height:1.6;
  ">
    🎀 <b style="font-size:15px;color:#b84b6a;">
      ƯU ĐÃI KHUNG GIỜ VÀNG
    </b><br>

    ⏰ <b>07:30 – 09:30 sáng</b> giảm ngay <b>10%</b> tổng hóa đơn<br>
    📅 <b>Đặt lịch online</b> được ưu đãi <b>10%</b><br>

    <span style="font-size:12px;color:#888;">
      * Áp dụng mỗi khách 1 lần / Không cộng dồn ưu đãi
    </span>
  </td>

    </tr>
    <tr>
      <td>✨ Phục hồi tóc</td>
      <td><b>200.000 – 600.000đ</b></td>
    </tr>
  </table>

  <div style="font-size:12px;color:#777;margin-top:6px;">
    * Giá có thể thay đổi theo độ dài và tình trạng tóc
  </div>
</div>
  {% if msg %}<div class="msg">{{msg}}</div>{% endif %}
  {% if err %}<div class="err">{{err}}</div>{% endif %}

  <form method="post" action="/book">
    <input name="name" placeholder="Tên"/>
    <input name="phone" placeholder="SĐT"/>
    <div class="row">
      <div><input type="date" name="date"/></div>
      <div><input type="time" name="time"/></div>
    </div>
    <input name="service" placeholder="Dịch vụ (uốn/nhuộm/duỗi...)"/>
    <input name="combo" placeholder="Combo (nếu có)"/>
    <textarea name="note" placeholder="Ghi chú"></textarea>
    <button type="submit">Đặt lịch</button>
  </form>

  <p>Admin: <code>/admin?key=1234</code></p>
</body>
</html>
"""

ADMIN = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Admin - Web Salon</title>
</head>
<body style="font-family:Arial; max-width:900px; margin:24px auto; padding:0 12px;">
  <h2>Admin</h2>
  {% if not ok %}
    <p>Sai key. Vào đúng dạng: <code>/admin?key=1234</code></p>
  {% else %}
    <p>Đúng key ✅</p>
    <table>
      <tr>
        <th>ID</th><th>Created</th><th>Name</th><th>Phone</th><th>Date</th><th>Time</th><th>Service</th><th>Combo</th><th>Note</th>
      </tr>
      {% for r in rows %}
      <tr>
        <td>{{r[0]}}</td><td>{{r[1]}}</td><td>{{r[2]}}</td><td>{{r[3]}}</td><td>{{r[4]}}</td><td>{{r[5]}}</td><td>{{r[6]}}</td><td>{{r[7]}}</td><td>{{r[8]}}</td>
      </tr>
      {% endfor %}
    </table>
  {% endif %}
</body>
</html>
"""

def init_db():
    with sqlite3.connect(DB) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS bookings(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              created_at TEXT NOT NULL,
              name TEXT NOT NULL,
              phone TEXT NOT NULL,
              date TEXT NOT NULL,
              time TEXT NOT NULL,
              service TEXT NOT NULL,
              combo TEXT,
              note TEXT
            )
        """)
        con.commit()

init_db()

@app.get("/")
def home():
    msg = request.args.get("msg", "")
    err = request.args.get("err", "")
    return render_template_string(PAGE, msg=msg, err=err)

@app.post("/book")
def book():
    name = (request.form.get("name") or "").strip()
    phone = (request.form.get("phone") or "").strip()
    date = (request.form.get("date") or "").strip()
    time = (request.form.get("time") or "").strip()
    service = (request.form.get("service") or "").strip()
    combo = (request.form.get("combo") or "").strip()
    note = (request.form.get("note") or "").strip()

    if not (name and phone and date and time and service):
        return redirect(url_for("home", err="Thiếu thông tin, nhập lại nhé."))

    with sqlite3.connect(DB) as con:
        con.execute(
            "INSERT INTO bookings(created_at,name,phone,date,time,service,combo,note) VALUES (?,?,?,?,?,?,?,?)",
            (datetime.now().isoformat(timespec="seconds"), name, phone, date, time, service, combo, note)
        )
        con.commit()

    return redirect(url_for("home", msg="Đặt lịch thành công! Salon sẽ liên hệ xác nhận."))

@app.get("/admin")
def admin():
    key = request.args.get("key", "")
    admin_key = "1234"   # đổi key tại đây
    ok = (key == admin_key)
    rows = []
    if ok:
        with sqlite3.connect(DB) as con:
            rows = con.execute("SELECT id, created_at, name, phone, date, time, service, combo, note FROM bookings ORDER BY id DESC").fetchall()
    return render_template_string(ADMIN, ok=ok, rows=rows)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)












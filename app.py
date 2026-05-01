import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mailman import Mail, EmailMessage

app = Flask(__name__)
app.secret_key = "forest_secret_key"  # フラッシュメッセージに必要

# --- Gmail送信設定 ---
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "atoz.arita@gmail.com"
app.config["MAIL_PASSWORD"] = "fjgn kkht uoyv muaf"  # 16桁のアプリパスワード
app.config["MAIL_DEFAULT_SENDER"] = "atoz.arita@gmail.com"

mail = Mail()
mail.init_app(app)

# データベースの保存先
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "forest_contact.db")


# データベースの準備
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS inquiries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                furigana TEXT,
                email TEXT,
                tel TEXT,
                method TEXT,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)


# トップページ
@app.route("/")
def index():
    return render_template("index.html")


# 例：別ページ（あとで増やせる）
@app.route("/price")
def price():
    return render_template("price.html")


@app.route("/rental")
def rental():
    return render_template("rental.html")


@app.route("/faq")
def faq():
    return render_template("faq.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = {
            "username": request.form.get("username", "").strip(),
            "furigana": request.form.get("furigana", "").strip(),
            "email": request.form.get("email", "").strip(),
            "tel": request.form.get("tel", "").strip(),
            "method": request.form.get("contact_method"),
            "message": request.form.get("message", "").strip(),
        }

        # バリデーション
        if (
            not data["username"]
            or not data["furigana"]
            or not data["email"]
            or not data["method"]
        ):
            flash("必須項目を入力してください。")
            return redirect(url_for("contact"))

        try:
            # データベースに保存
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute(
                    """
                    INSERT INTO inquiries (username, furigana, email, tel, method, message)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        data["username"],
                        data["furigana"],
                        data["email"],
                        data["tel"],
                        data["method"],
                        data["message"],
                    ),
                )

            # Gmail送信
            msg = EmailMessage(
                subject=f"【キャンプ場】お問い合わせ通知：{data['username']} 様",
                to=["atoz.arita@gmail.com"],
                body=f"""
キャンプ場のお問い合わせフォームから新しい投稿がありました。

【お客様情報】
お名前: {data['username']}
ふりがな: {data['furigana']}
メールアドレス: {data['email']}
電話番号: {data['tel']}
希望連絡方法: {data['method']}

【お問い合わせ内容】
{data['message']}
                """,
            )
            msg.send()

            flash("お問い合わせを受け付けました。ありがとうございました！")

        except Exception as e:
            flash("システムエラーが発生しました。お電話にてご連絡ください。")
            print(f"Error: {e}")

        return redirect(url_for("contact"))

    return render_template("contact.html")


# デバッグ用データ確認関数
def check_db():
    if os.path.exists(DB_PATH):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute("SELECT * FROM inquiries ORDER BY created_at DESC")
            rows = cursor.fetchall()
            print("\n--- 登録データ一覧 ---")
            for row in rows:
                print(row)
            print("--------------------\n")


if __name__ == "__main__":
    init_db()  # 起動時にDBテーブルを作成
    app.run(debug=True)

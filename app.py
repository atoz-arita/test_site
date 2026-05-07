from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # フラッシュメッセージ用に必要

# --- メール送信設定 (例: Gmailを使用する場合) ---
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "atoz.arita@gmail.com"
app.config["MAIL_PASSWORD"] = "fjgn kkht uoyv muaf"
app.config["MAIL_DEFAULT_SENDER"] = "atoz.arita@gmail.com"

mail = Mail(app)

# --- ルーティング設定 ---


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/price")
def price():
    return render_template("price.html")


@app.route("/rental")
def rental():
    return "レンタル品一覧ページ"


@app.route("/faq")
def faq():
    return render_template("faq.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # フォームデータの取得
        username = request.form.get("username")
        furigana = request.form.get("furigana")
        email = request.form.get("email")
        tel = request.form.get("tel")
        method = request.form.get("contact_method")
        body = request.form.get("message")

        msg = Message(
            subject=f"【フォレスト】{username}様よりお問い合わせ",
            recipients=["atoz.arita@gmail.com"],  # 管理者の受信希望アドレス
        )
        msg.body = f"""
        お問い合わせがありました。

        【お名前】: {username} ({furigana})
        【メール】: {email}
        【電話番号】: {tel}
        【希望連絡方法】: {method}
        【内容】:
        {body}
        """

        try:
            mail.send(msg)
            flash("お問い合わせを受け付けました。自動返信メールをご確認ください。")
        except Exception as e:
            flash("エラーが発生しました。時間をおいて再度お試しください。")
            print(f"Mail Error: {e}")

        return redirect(url_for("contact"))

    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)

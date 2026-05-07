from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
import os

app = Flask(__name__)
# flashメッセージを表示するために必要なシークレットキー
app.secret_key = "your_secret_key_here"

# --- メール送信設定 (Gmailを使用する場合の例) ---
# セキュリティのため、本来は環境変数などでの管理が推奨されます
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "atoz.arita@gmail.com"
app.config["MAIL_PASSWORD"] = "fjgn kkht uoyv muaf"
app.config["MAIL_DEFAULT_SENDER"] = "atoz.arita@gmail.com"

mail = Mail(app)

# --- ルーティング ---


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/price")
def price():
    return render_template("price.html")


@app.route("/faq")
def faq():
    return render_template("faq.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # フォームから送られてきたデータを取得
        # contact.htmlの各inputタグの 'name' 属性と一致させる必要があります
        username = request.form.get("username")
        furigana = request.form.get("furigana")
        email = request.form.get("email")
        tel = request.form.get("tel")
        contact_method = request.form.get("contact_method")
        message_body = request.form.get("message")

        # 管理者へ届くメールの内容を作成
        msg = Message(
            subject=f"【お問い合わせ】{username}様より",
            recipients=["atoz.arita@gmail.com"],  # 通知を受け取りたいメールアドレス
        )
        msg.body = f"""
        Webサイトからお問い合わせがありました。

        【お名前】: {username} ({furigana})
        【メール】: {email}
        【電話番号】: {tel}
        【希望連絡方法】: {contact_method}
        【内容】:
        {message_body}
        """

        try:
            # メールの送信実行
            mail.send(msg)
            flash("お問い合わせを受け付けました。ありがとうございます。")
            # 送信成功後、お問い合わせページにリダイレクト（再読み込み対策）
            return redirect(url_for("contact"))
        except Exception as e:
            print(f"Mail Error: {e}")
            flash("メール送信中にエラーが発生しました。設定を確認してください。")
            return redirect(url_for("contact"))

    # GETリクエスト（ページ表示時）
    return render_template("contact.html")


if __name__ == "__main__":
    # debug=True にするとコードを変更した際に自動でサーバーが再起動します
    app.run(debug=True)

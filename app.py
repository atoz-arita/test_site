import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mailman import Mail, EmailMessage

app = Flask(__name__)
app.secret_key = "forest_secret_key"

# --- Gmail送信設定 ---
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True

app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME", "atoz.arita@gmail.com")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_USERNAME")

mail = Mail()
mail.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


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
            msg = EmailMessage(
                subject=f"【キャンプ場】お問い合わせ：{data['username']} 様",
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
            # fail_silently=False にすることで、エラー時に except ブロックへ飛ばします
            msg.send(fail_silently=False)
            flash("お問い合わせを受け付けました。ありがとうございました！")

        except Exception as e:
            print(f"Mail sending failed: {e}")
            flash(
                "メール送信中にエラーが発生しました。お手数ですが、お電話にてご連絡ください。"
            )

        return redirect(url_for("contact"))

    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)

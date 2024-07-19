from flask import Flask, render_template

app = Flask(__name__)

# Danh sách các sản phẩm đồng hồ
products = [
    {"name": "Đồng hồ nam A", "price": 100, "image": "watch1.jpg"},
    {"name": "Đồng hồ nữ B", "price": 150, "image": "watch2.jpg"},
    {"name": "Đồng hồ thể thao C", "price": 120, "image": "watch3.jpg"},
]

# Cấu hình tên miền mới, không bao gồm cổng
app.config['SERVER_NAME'] = 'webdongho.com'

@app.route("/")
def index():
    return render_template("index.html", products=products)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True, host='webdongho.com', port=80)

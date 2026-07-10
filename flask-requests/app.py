from flask import Flask, render_template, request
from converter import convert_currency

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        try:
            amount = float(request.form["amount"])
            from_curr = request.form["from_currency"].upper()
            to_curr = request.form["to_currency"].upper()
            result = convert_currency(amount, from_curr, to_curr)
        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)

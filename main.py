from flask import Flask, render_template

app = Flask(__name__)

@app.route("/home")
def home():
    return render_template('landing.html', subtitle='Home Page', text='This is the home page')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

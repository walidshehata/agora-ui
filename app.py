from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', html_title='Nutanix Dashboard', message="Hello world")


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', html_title='Nutanix Dashboard')


@app.route('/login')
def login():
    return render_template('auth/login.html', html_title='Login')


@app.route('/register')
def register():
    return render_template('auth/register.html', html_title='Register')


if __name__ == '__main__':
    app.run()

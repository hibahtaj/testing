from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def reg():
    return render_template('reg.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    if not name or not password:
        return render_template('reg.html', error='Name and password are required'), 400
    return render_template('succ.html', name=name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

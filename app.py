from flask import Flask

from rouets.phone_bp import phone_blueprint

app = Flask(__name__)

app.register_blueprint(phone_blueprint)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=5000,
            debug=True)

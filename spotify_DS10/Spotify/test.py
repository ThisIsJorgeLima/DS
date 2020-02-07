from flask import Flask

app = Flask(__name__)

db = SQLAlchemy()

app = Flask(__name__, instance_relative_config=False)
app.config.from_object('config.Config')

db.init_app(app)
login_manager.init_app(app)


def create_app():
    """create and configures an instance of a flask app"""
    app = Flask(__name__)


@app.route('/')
def home():
    return "<h1>Hello, World!</h1>"


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'{username}'


if __name__ == "__main__":
    app.run(debug=True, port=8080)
return app

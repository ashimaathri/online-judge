from flask import Flask
from online_judge.blueprints.home import home_page
from online_judge.blueprints.auth import auth
from online_judge.db.session_interface import MongoSessionInterface

def main():
    app = Flask(__name__)
    app.session_interface = MongoSessionInterface()
    app.register_blueprint(home_page)
    app.register_blueprint(auth)
    app.run(debug=True)

if __name__ == '__main__':
    main()

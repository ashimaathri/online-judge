from flask import Flask
from blueprints.home import home_page
from blueprints.auth import auth
from db.session_interface import MongoSessionInterface

app = Flask(__name__)
app.session_interface = MongoSessionInterface()
app.register_blueprint(home_page)
app.register_blueprint(auth)
app.run(debug=True)

if __name__ == '__main__':
    main()

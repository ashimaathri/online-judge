from flask import Flask
from blueprints.home import home_page

app = Flask(__name__)
app.register_blueprint(home_page)
app.run(debug=True)

if __name__ == '__main__':
    main()

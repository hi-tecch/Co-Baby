from flask_app import app
from flask_app.controllers import login_controllers
from flask_app.controllers import report_controllers
# from flask_app.controllers import messages_controller
from flask_app.controllers import imgs


if __name__ == "__main__":
    app.run(debug=True)


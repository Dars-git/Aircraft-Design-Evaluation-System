from flask import Flask, render_template, session, flash, redirect
from flask_session import Session
from login_handler import login_blueprint
from register_handler import register_blueprint
from route_handlers import route_handlers_blueprint
from flying_wing_design_calculator import fwdc_blueprint
from Stabilizer_shape_design_calculator import ssdc_blueprint
from standard_fuselage_design_calculator import sfdc_blueprint
from standard_wing_design_calculator import swdc_blueprint

app = Flask(__name__,template_folder="views" , static_folder="static")


app.register_blueprint(login_blueprint)
app.register_blueprint(register_blueprint)
app.register_blueprint(route_handlers_blueprint)
app.register_blueprint(fwdc_blueprint)
app.register_blueprint(ssdc_blueprint)
app.register_blueprint(sfdc_blueprint)
app.register_blueprint(swdc_blueprint)

keyFile = open("secret_key", "r")
app.config['SECRET_KEY']=keyFile.read()
app.config['SESSION_TYPE'] = 'filesystem'


def default_session():
    if 'username' not in session:
        session['name'] = None
        session['username'] = None
        session.permanent = True
@app.route('/')
def home_page():
    default_session()
    return Sensitivity_Study()
@app.route('/home')
def Sensitivity_Study():
    return render_template("home.html")

@app.route('/test_missions')
def test_missions():
    return render_template("test_missions.html")

@app.route('/documentation')
def documentation():
    return render_template("docs.html")

@app.route('/calculator')
def calculator():
    return render_template("calculator.html")

@app.route('/flying_wing_design_calculator')
def flying_wing_design_calculator():
    default_session()
    return render_template("flying_wing_design_calculator.html")

@app.route('/Stabilizer_shape_design_calculator')
def Stabilizer_shape_design_calculator():
    default_session()
    return render_template("Stabilizer_shape_design_calculator.html")

@app.route('/standard_fuselage_design_calculator')
def standard_fuselage_design_calculator():
    default_session()
    return render_template("standard_fuselage_design_calculator.html")

@app.route('/standard_wing_design_calculator')
def standard_wing_design_calculator():
    default_session()
    return render_template("standard_wing_design_calculator.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")
def init_app():
    app.run()


@app.route('/logout')
def logout():
    if 'name' in session:
        session.pop('name', None)  # Remove the user_id from the session
    return redirect('/')

Session(app)
if __name__ == '__main__':
    init_app()
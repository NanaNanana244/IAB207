from flask import Flask, session, Blueprint, request, render_template

app = Flask(__name__)
app.secret_key = "fhuroudnefiodnjfijsdlkdansalnfd"


@app.route('/')
@app.route('/home')
@app.route('/Index.html')
def login():
    return render_template("Index.html")



@app.route("/bookinghistory")
@app.route('/BookingHistory.html')
def history():
    return render_template('BookingHistory.html')

@app.route("/create")
@app.route('/EventCreation.html')
def create():
    return render_template('EventCreation.html')

@app.route('/detail')
@app.route('/EventDetail.html')
def detail():
    return render_template('EventDetail.html')

#from .login import login_bp
#app.register_blueprint(login_bp)

if __name__ == "__main__":
    app.run(
        debug=True,
        port=8023,
        host='0.0.0.0'
    )



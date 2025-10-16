# import flask - from 'package' import 'Class'
from flask import Flask, render_template 
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.secret_key = 'somesecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.sqlite'
    db.init_app(app)

    Bootstrap5(app)

    UPLOAD_FOLDER = '/static/Image/uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
  
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.scalar(db.select(User).where(User.userid==user_id))

    # Register blueprints - ONLY these four
    from .views import main_bp
    app.register_blueprint(main_bp)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .create import createbp
    app.register_blueprint(createbp)

    from .edit import editbp
    app.register_blueprint(editbp)
    
    
    # Error Handling
    @app.errorhandler(404)   #Invalid URL
    def not_found(e):
        return render_template('404.html', error=e, title = 'Page Not Found'), 404
    
    @app.errorhandler(500)  #Internal server error
    def server_error(e):
        return render_template('500.html', error=e, title='Internal Server Error'), 500
        
  
    return app
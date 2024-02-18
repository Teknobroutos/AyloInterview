#_init_.py
from flask import Flask

#function to create and configure Flask application instance.
def create_app():
    # Create instance.
    app = Flask(__name__)

    # Register blueprints with the application.
    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)


    # @app.errorhandler(404)
    # def not_found(error):
    #     return render_template('404.html'), 404
    #commented beacause of lack of 404 page
    # Return the configured Flask application instance.
    return app

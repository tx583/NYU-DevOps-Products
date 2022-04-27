"""
Package: service
Package for the application models and service routes
This module creates and configures the Flask app and sets up the logging
and SQL database
"""
import sys
import logging
from flask import Flask

# Create Flask application
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object("config")

# Import the routes After the Flask app is created
from service import routes, models
# from .utils import error_handlers

# Set up logging for production
print("Setting up logging for {}...".format(__name__))
app.logger.propagate = False

# to run this program, use command "flask run"
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    # Make all log formats consistent
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s", "%Y-%m-%d %H:%M:%S %z"
    )
    for handler in app.logger.handlers:
        handler.setFormatter(formatter)
    app.logger.info("Logging handler established")

app.logger.info(70 * "*")
app.logger.info("  P R O D U C T   S T O R E   S E R V I C E  ".center(70, "*"))
app.logger.info(70 * "*")

try:
    models.init_db(app)  # make our sqlalchemy tables
except Exception as error:
    app.logger.critical("%s: Cannot continue", error)
    # gunicorn requires exit code 4 to stop spawning workers when they die
    sys.exit(4)

app.logger.info("Service initialized!")

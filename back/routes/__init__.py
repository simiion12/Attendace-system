from flask import Blueprint

# Create a Blueprint for the routes in this directory
main_routes = Blueprint("main_routes", __name__)

# Import the routes from the department_route.py file
from back.routes.department_route import department_routes
main_routes.register_blueprint(department_routes)

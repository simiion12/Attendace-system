# routes/__init__.py
from flask import Blueprint

# Create a Blueprint for the routes in this directory
main_routes = Blueprint("main_routes", __name__)

# Import the routes from the department_route.py file
from .department_route import department_routes
main_routes.register_blueprint(department_routes)

from .admin_route import admin_routes
main_routes.register_blueprint(admin_routes)

from .user_route import user_routes
main_routes.register_blueprint(user_routes)

from .user_attendance_route import user_attendance_routes
main_routes.register_blueprint(user_attendance_routes)

from .admin_attendance_route import admin_attendance_routes
main_routes.register_blueprint(admin_attendance_routes)

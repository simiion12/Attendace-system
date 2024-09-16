from flask import Blueprint, jsonify, request

# Create a Blueprint for the routes in this directory
user_attendance_routes = Blueprint("user_attendance_routes", __name__)
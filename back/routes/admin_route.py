from flask import Blueprint, jsonify, request

# Create a Blueprint for the routes in this directory
admin_routes = Blueprint("admin_routes", __name__)
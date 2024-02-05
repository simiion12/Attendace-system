from back import app
from back.routes import main_routes

# Register the main_routes Blueprint
app.register_blueprint(main_routes)

if __name__ == '__main__':
    app.run(debug=True)

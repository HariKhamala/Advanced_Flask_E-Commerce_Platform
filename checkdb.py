from ecommerceflask import create_app
from ecommerceflask.db import init_db

# Create the Flask app instance
app = create_app()

# Use the app context to initialize the database
with app.app_context():
    init_db()
    print("Database initialized successfully.")

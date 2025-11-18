from flask_sqlalchemy import SQLAlchemy

import os

db = SQLAlchemy()

class Database:
    """Database management class."""

    def __init__(self, app):
        self.app = app
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
            "DATABASE_URL", "postgresql://flaskuser:flaskpass@localhost:5432/flaskdb"
        )
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(app)

    def create_tables(self):
        with self.app.app_context():
            try:
                db.create_all()
                print("Database tables created successfully")
            except Exception as e:
                print(f"Error creating tables: {e}")

    def upload_to_database(self, filename, description):
        upload = Upload(filename=filename, description=description)
        db.session.add(upload)
        db.session.commit()

class Upload(db.Model):
    __tablename__ = 'upload'

    filename = db.Column(db.String(50), primary_key=True)
    description = db.Column(db.Text, nullable=False)
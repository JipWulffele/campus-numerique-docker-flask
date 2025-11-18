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

    def upload_to_database(self, filename, raw_description, parsed=None):
        upload = Upload(
            filename=filename,
            raw_description=raw_description,
            background_color=(parsed.background_color if parsed else None),
            genre=(parsed.genre if parsed else None),
            animal=(parsed.animal if parsed else None),
            num_animals=(parsed.num_animals if parsed else None),
            story=(parsed.story if parsed else None)
        )
        
        db.session.add(upload)
        db.session.commit()

class Upload(db.Model):
    __tablename__ = 'upload'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50), unique=True)
    raw_description = db.Column(db.Text, nullable=False)

    # Parsed fields
    background_color = db.Column(db.String(30))
    genre = db.Column(db.String(30))
    animal = db.Column(db.String(30))
    num_animals = db.Column(db.Integer)
    story = db.Column(db.Text)
        
from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Enum('admin', 'editor', 'data_operator', 'viewer'), nullable=False)
    
    logs = db.relationship('Log', backref='user', lazy=True)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(50), nullable=False)
    culture = db.Column(db.String(50), nullable=False)
    damage = db.Column(db.String(50), nullable=False)
    disease = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    ir_spectrum = db.Column(db.String(200))
    visible_spectrum = db.Column(db.String(200))
    uv_spectrum = db.Column(db.String(200))
    ir_image_url = db.Column(db.String(200))
    visible_image_url = db.Column(db.String(200))
    uv_image_url = db.Column(db.String(200))
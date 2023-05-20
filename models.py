from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 

"""Create Tables in Database"""

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    phoneNumber = db.Column(db.String(20), unique=True, nullable=False)
    firstName = db.Column(db.String(80), nullable=False)
    lastName = db.Column(db.String(80), nullable=False)
    cashBalance = db.Column(db.Integer, default=0)
    bookings = db.relationship('Booking', backref='user', lazy=True)
    waiting_list = db.relationship('WaitingList', backref='user', lazy=True)

    def __repr__(self):
        return f'<User: {self.username}>'

class Field(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fieldName = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    pricing = db.Column(db.Float, nullable=False)
    slots = db.relationship('Slot', backref='field', lazy=True)

    def __repr__(self):
        return f'<Field: {self.fieldName}>'
    

class Slot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fieldId = db.Column(db.Integer, db.ForeignKey('field.id'), nullable=False)
    startTime = db.Column(db.Time, nullable=False)
    endTime = db.Column(db.Time, nullable=False)
    date = db.Column(db.Date, nullable=False)
    maxCapacity = db.Column(db.Integer, nullable=False)
    currentCapacity = db.Column(db.Integer, nullable=False, default=0)
    fieldId = db.Column(db.Integer, db.ForeignKey('field.id'), nullable=False)
    bookings = db.relationship('Booking', backref='slot', lazy=True)
    waiting_list = db.relationship('WaitingList', backref='slot', lazy=True)

    def __repr__(self):
        return f'<Slot: {self.id}>'

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    slotId = db.Column(db.Integer, db.ForeignKey('slot.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Booking: {self.id}>'

class WaitingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    slotId = db.Column(db.Integer, db.ForeignKey('slot.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<WaitingList: {self.id}>'
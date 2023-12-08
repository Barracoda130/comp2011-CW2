from app import db
import app.db_functions as db_functions
from app.calculate_stock import *

# Relationship tables - prevent many-many relationships
# Not sure how to ensure these are deleted if necessary
itemInKit = db.Table('item_in_kit', db.Model.metadata,
                     db.Column('item_id', db.Integer, db.ForeignKey('stock_item.id')),
                     db.Column('kit_id', db.Integer, db.ForeignKey('kit.id')))

class StockItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    stock = db.Column(db.Integer)
    supplier = db.Column(db.String)
    price = db.Column(db.Double)
    
    kits = db.relationship('Kit', secondary=itemInKit)
    
    def data(self):
        required = calculate_required(self)
        return [self.name, self.stock, required, calculate_diff(self, required), self.supplier, self.price]
    
    def form_details(self):
        return [self.name, self.stock, self.supplier, self.price]
    
    def headers(self):
        return ["name", "stock", "required", "diff", "supplier", "price"]
    
    

class Kit(db.Model):
    """
    Model to represent a kit list for either a venue or a course.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    course = db.Column(db.Integer, db.ForeignKey('course.id'))
    items = db.relationship('StockItem', secondary=itemInKit, overlaps="kits")
    
    def data(self):
        if self.course:
            return [self.name, db_functions.get_course_with_id(self.course).name]
        return [self.name, None]
    
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    events = db.relationship('Event', backref='course_events', lazy='dynamic')
    kits = db.relationship('Kit', backref='course_kits', lazy='dynamic')
    
    def data(self):
        return [self.name]
    

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    course = db.Column(db.Integer, db.ForeignKey('course.id'))
    numberOfKids = db.Column(db.Integer)
    
    def data(self):
        if self.course:
            return [self.start.date(), self.end.date(), db_functions.get_course_with_id(self.course).name,  self.numberOfKids]
        return [self.start, self.end, None, self.numberOfKids]
    
    
class User(db.Model):
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)
    
    def is_authenticated(self):
        return self.authenticated
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.username)





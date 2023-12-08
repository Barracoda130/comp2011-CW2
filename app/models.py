from app import db
import app.db_functions as db_functions
from app.calculate_stock import *

# Relationship tables - prevent many-many relationships
itemInKit = db.Table('item_in_kit', db.Model.metadata,
                     db.Column('item_id', db.Integer, db.ForeignKey('stock_item.id')),
                     db.Column('kit_id', db.Integer, db.ForeignKey('kit.id')))


class StockItem(db.Model):
    """
    Model to represent a single item of stock.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    stock = db.Column(db.Integer)
    supplier = db.Column(db.String)
    price = db.Column(db.Double)
    
    kits = db.relationship('Kit', secondary=itemInKit)
    
    def data(self):
        """
        Returns a list of all the variables needed to display the item.
        """
        required = calculate_required(self)
        return [self.name, self.stock, required, calculate_diff(self, required), self.supplier, self.price]
    
    def form_details(self):
        """
        Returns a list of all the variables needed to be set for a new stock item to be made.
        """
        return [self.name, self.stock, self.supplier, self.price]
    
    def headers(self):
        return ["name", "stock", "required", "diff", "supplier", "price"]
    
    

class Kit(db.Model):
    """
    Model to represent a kit list for a course.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    course = db.Column(db.Integer, db.ForeignKey('course.id'))
    items = db.relationship('StockItem', secondary=itemInKit, overlaps="kits")
    
    def data(self):
        """
        Returns a list of all the variables needed to display the item.
        """
        if self.course:
            return [self.name, db_functions.get_course_with_id(self.course).name]
        return [self.name, None]
    
class Course(db.Model):
    """
    Model to represent a course.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    events = db.relationship('Event', backref='course_events', lazy='dynamic')
    kits = db.relationship('Kit', backref='course_kits', lazy='dynamic')
    
    def data(self):
        """
        Returns a list of all the variables needed to display the item.
        """
        return [self.name]
    

class Event(db.Model):
    """
    Model to represent an event.
    """
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    course = db.Column(db.Integer, db.ForeignKey('course.id'))
    numberOfKids = db.Column(db.Integer)
    
    def data(self):
        """
        Returns a list of all the variables needed to display the item.
        """
        if self.course:
            return [self.start.date(), self.end.date(), db_functions.get_course_with_id(self.course).name,  self.numberOfKids]
        return [self.start, self.end, None, self.numberOfKids]
    
    
class User(db.Model):
    """
    Model to represent a user.
    """
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





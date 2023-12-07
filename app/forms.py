from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, BooleanField, SubmitField, IntegerField, FloatField, DateField, PasswordField
from wtforms.validators import DataRequired, Regexp
import app.models as model
import datetime
from app import app, db
from .db_functions import *
import bcrypt

class AddStockItemForm(FlaskForm):
    """
    Superclass form for a generic transaction input.
    Is used by Income() and Expense() sublcasses.
    """
    name = StringField('Name')
    stock = IntegerField('Stock')
    supplier = StringField('Supplier')
    price = FloatField('Price')
    
    def __iter__(self):
        return iter([self.name, self.stock, self.supplier, self.price])
    
    def fields(self):
        return [self.name, self.stock, self.supplier, self.price]
    
    def add_to_database(self):
        """
        Creates and adds the new model to the database.
        Args:
            type (model.Transaction): What type of model is added to the database.
            category (SelectField): What category the model should be.
        """
        # Create model
        si = model.StockItem()
        si.name = self.name.data
        si.stock = self.stock.data
        si.supplier = self.supplier.data
        si.price = self.price.data
        
        # Commit model to database
        with app.app_context():
            db.session.add(si)
            db.session.commit()
            
class AddCourseForm(FlaskForm):
    """
    Superclass form for a generic transaction input.
    Is used by Income() and Expense() sublcasses.
    """
    name = StringField('Name')
    
    def __iter__(self):
        return iter([self.name])
    
    def fields(self):
        return [self.name]
    
    def add_to_database(self):
        """
        Creates and adds the new model to the database.
        Args:
            type (model.Transaction): What type of model is added to the database.
            category (SelectField): What category the model should be.
        """
        # Create model
        c = model.Course()
        c.name = self.name.data
        
        # Commit model to database
        with app.app_context():
            db.session.add(c)
            db.session.commit()
            
class AddEventForm(FlaskForm):
    """
    Superclass form for a generic transaction input.
    Is used by Income() and Expense() sublcasses.
    """
    start = DateField('Start Date', validators=[DataRequired()])
    end = DateField('End Date', validators=[DataRequired()])
    course = SubmitField('Select Course')
    numberOfKids = IntegerField('Number of Kids', validators=[DataRequired()])
    
    
    def __iter__(self):
        return iter([self.start, self.end, self.numberOfKids, self.course])
    
    def fields(self):
        return [self.start, self.end, self.numberOfKids, self.course]
    
    def add_to_database(self, course_id):
        """
        Creates and adds the new model to the database.
        Args:
            type (model.Transaction): What type of model is added to the database.
            category (SelectField): What category the model should be.
        """
        # Create model
        e = model.Event()
        e.start = self.start.data
        e.end = self.end.data
        e.numberOfKids = self.numberOfKids.data
        
        c = get_course_with_id(course_id)
        c.events.append(e)
        
        # Commit model to database
        db.session.add(e)
        db.session.add(c)
        db.session.commit()

class AddKitForm(FlaskForm):
    """
    Superclass form for a generic transaction input.
    Is used by Income() and Expense() sublcasses.
    """
    name = StringField('Name')
    course = SubmitField('Select Course')
    items = SubmitField('Select Items')
    
    
    def __iter__(self):
        return iter([self.name, self.course, self.items])
    
    def fields(self):
        return [self.name, self.course, self.items]
    
    def add_to_database(self, item_ids, course_id):
        """
        Creates and adds the new model to the database.
        Args:
            type (model.Transaction): What type of model is added to the database.
            category (SelectField): What category the model should be.
        """
        # Create model
        k = model.Kit()
        k.name = self.name.data
        items = []
        for id in item_ids:
            items.append(get_stock_item_with_id(id))
            
        k.items = items
        c = get_course_with_id(course_id)
        c.kits.append(k)
        
        print("adding to db:", items)
        
        # Commit model to database
        #with app.app_context():
        db.session.add(k)
        db.session.add(c)
        db.session.commit()
        
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    
    def __iter__(self):
        return iter([self.username, self.password])
    
class AddUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    
    def __iter__(self):
        return iter([self.username, self.password])
    
    def add_to_database(self):
        u = model.User()
        u.username = self.username.data
        encode = self.password.data.encode('utf-8')
        salt = bcrypt.gensalt()
        u.password = bcrypt.hashpw(encode, salt)
        
        with app.app_context():
            db.session.add(u)
            db.session.commit()
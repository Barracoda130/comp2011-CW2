from flask_wtf import FlaskForm
from wtforms import SubmitField
from app import app, db
import app.db_functions as db_functions

class SortStockItemForm(FlaskForm):
    """
    Form for sorting the finances page.
    """
    name = SubmitField('Name')
    stock = SubmitField('Stock')
    required = SubmitField('Required')
    diff = SubmitField('Diff')
    supplier = SubmitField('Supplier')
    price = SubmitField('Price')
    
    def __iter__(self):
        return iter([self.name, self.stock, self.required, self.diff, self.supplier, self.price])
    
    def sort(self, stockItems, sort_by, reverse):
        """
        Sorts the provided list of transactions by what is defined in sort_by
        Args:
            transactions (list: Transaction): List to be sorted
            sort_by (str): What to sort the list by
            reverse (bool): Whether the sort should be reversed

        Returns:
            list: Transaction: The sorted list
        """
        try:
            if sort_by == 'name':
                stockItems.sort(key=lambda x: x.name.lower(), reverse=reverse)
            elif sort_by == 'stock':
                stockItems.sort(key=lambda x: x.stock, reverse=reverse)
            elif sort_by == 'required':
                stockItems.sort(key=lambda x: x.required, reverse=reverse)
            elif sort_by == 'diff':
                stockItems.sort(key=lambda x: x.diff, reverse=reverse)
            elif sort_by == 'supplier':
                stockItems.sort(key=lambda x: x.supplier.lower(), reverse=reverse)
            elif sort_by == 'price':
                stockItems.sort(key=lambda x: x.price, reverse=reverse)
        except:
            print("could not sort")
        return stockItems
    
class SortKitsForm(FlaskForm):
    """
    Form for sorting the finances page.
    """
    name = SubmitField('Name')
    course = SubmitField('Course')
    
    def __iter__(self):
        return iter([self.name, self.course])
    
    def sort(self, kit, sort_by, reverse):
        """
        Sorts the provided list of transactions by what is defined in sort_by
        Args:
            transactions (list: Transaction): List to be sorted
            sort_by (str): What to sort the list by
            reverse (bool): Whether the sort should be reversed

        Returns:
            list: Transaction: The sorted list
        """
        try:
            if sort_by == 'name':
                kit.sort(key=lambda x: x.name.lower(), reverse=reverse)
            elif sort_by == 'course':
                kit.sort(key=lambda x: db_functions.get_course_with_id(x.course).name.lower(), reverse=reverse)
        except:
            print("could not sort")
        return kit   
 
class SortCoursesForm(FlaskForm):
    """
    Form for sorting the finances page.
    """
    name = SubmitField('Name')
    
    def __iter__(self):
        return iter([self.name])
    
    def sort(self, courses, sort_by, reverse):
        """
        Sorts the provided list of transactions by what is defined in sort_by
        Args:
            transactions (list: Transaction): List to be sorted
            sort_by (str): What to sort the list by
            reverse (bool): Whether the sort should be reversed

        Returns:
            list: Transaction: The sorted list
        """
        try:
            if sort_by == 'name':
                courses.sort(key=lambda x: x.name.lower(), reverse=reverse)
        except:
            print("could not sort")
        return courses
    
class SortEventsForm(FlaskForm):
    """
    Form for sorting the finances page.
    """
    start = SubmitField('Start')
    end = SubmitField('End')
    course = SubmitField('Course')
    number_of_kids = SubmitField('No. Kids')
    
    def __iter__(self):
        return iter([self.start, self.end, self.course, self.number_of_kids])
    
    def sort(self, event, sort_by, reverse):
        """
        Sorts the provided list of transactions by what is defined in sort_by
        Args:
            transactions (list: Transaction): List to be sorted
            sort_by (str): What to sort the list by
            reverse (bool): Whether the sort should be reversed

        Returns:
            list: Transaction: The sorted list
        """
        try:
            if sort_by == 'start':
                event.sort(key=lambda x: x.start, reverse=reverse)
            elif sort_by == 'end':
                event.sort(key=lambda x: x.end, reverse=reverse)
            elif sort_by == 'course':
                event.sort(key=lambda x: db_functions.get_course_with_id(x.course).name.lower(), reverse=reverse)
            elif sort_by == 'numberOfKids':
                event.sort(key=lambda x: x.numberOfKids, reverse=reverse)
        except:
            print("could not sort")
        return event
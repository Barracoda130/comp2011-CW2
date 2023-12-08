from app import models
import app.db_functions as db_functions

def calculate_required(item):
    """
    Calculates required stock for the given stock item
    Args:
        item (StockItem): The stock item to calculate stock for

    Returns:
        int: The required amount of stock
    """
    required = 0
    for kit in item.kits:
        print(kit)
        if kit.course:
            course = db_functions.get_course_with_id(kit.course)
            for event in course.events:
                required += event.numberOfKids
    return required

def calculate_diff(item, required):
    """
    Calculate the difference between the required amount and the current amount of stock 
    for a given item.
    Args:
        item (StockItem): The stock item
        required (int): The required amount

    Returns:
        int: The difference
    """
    return required - item.stock
    
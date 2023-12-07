from app import models
import app.db_functions as db_functions

def calculate_required(item):
    required = 0
    for kit in item.kits:
        print(kit)
        if kit.course:
            course = db_functions.get_course_with_id(kit.course)
            for event in course.events:
                required += event.numberOfKids
    return required

def caluclate_diff(item, required):
    return required - item.stock
    
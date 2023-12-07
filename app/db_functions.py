from app import models, app, db

def get_stock_items():
    return models.StockItem.query.all()

def get_stock_item_with_id(id):
    return models.StockItem.query.get(id)

def get_course_with_id(id):
    return models.Course.query.get(id)

def get_kit_with_id(id):
    return models.Kit.query.get(id)

def get_event_with_id(id):
    return models.Event.query.get(id)

def delete_stock_item(id):
    with app.app_context():
        db.session.delete(get_stock_item_with_id(id))
        db.session.commit()

def get_courses():
    return models.Course.query.all()

def get_kits():
    return models.Kit.query.all()

def get_events():
    return models.Event.query.all()

def get_course_with_id(course_id):
    return models.Course.query.get(course_id)

def get_events_from_course(course):
    models.Event.query.filter()
    
def delete_from_db(model_type, id):
    with app.app_context():
        if model_type == 'stock':
            db.session.delete(get_stock_item_with_id(id))
        elif model_type == 'kit':
            db.session.delete(get_kit_with_id(id))
        elif model_type == 'course':
            db.session.delete(get_course_with_id(id))
        elif model_type == 'event':
            db.session.delete(get_event_with_id(id))
        db.session.commit()
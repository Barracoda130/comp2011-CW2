from app import db, models, app
from app.db_functions import *
import bcrypt
from app.calculate_stock import *

with app.app_context():
    for item in get_stock_items():
        required = calculate_required(item)
        print(caluclate_diff(item, required))
        
        
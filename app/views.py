from app import app
from flask import render_template, request, redirect, url_for, session, flash
from .db_functions import *
from .forms import *
from .models import *
from .sort_forms import *
from flask_login import login_user, login_required
import bcrypt
import datetime

# ----------------------------------------------------------------
# Login/signup
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.username.data)
        print(form.username.data)
        print(form.password.data)
        print(user)
        if user:
            encode = form.password.data.encode('utf-8')
            if bcrypt.checkpw(encode, user.password):
                user.authenticated = True
                print("authenticated")
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect('/view/stock')
            else:
                flash("Username or password is incorrect")
        else:
            flash("Username or password is incorrect")
            
    
    return render_template('login.html',
                           form=form,
                           title="Login")

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    form = AddUserForm()
    
    if form.validate_on_submit():
        print("submit")
        try:
            form.add_to_database()
            return redirect(url_for('login')) 
        except:
            flash("Username already in use - please pick another")
            return render_template('add_model.html',
                           form=form,
                           title="Add user",
                           active_page='add_user')
        
    else:
        print(form.errors)
    
    return render_template('add_model.html',
                           form=form,
                           active_page='add_user')
# ----------------------------------------------------------------
# View models
@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('login'))

@app.route('/view/<model_type>', methods=['GET', 'POST'])
@login_required
def courses(model_type):
    # Define if not already defined
    # Used to store sort for when page is refreshed
    try:
        reverse = session['reverse']
    except:
        reverse = False
    try:
        sort_by = session['sort_by']
    except:
        sort_by = None
    
    if model_type == 'stock':
        sort = SortStockItemForm()
        items = get_stock_items()
    elif model_type == 'kit':
        sort = SortKitsForm()
        items = get_kits()
    elif model_type == 'course':
        sort = SortCoursesForm()
        items = get_courses()
    elif model_type == 'event':
        sort = SortEventsForm()
        items = get_events()
    
    # Sort columns 
    print(sort_by)
    for a in sort:
        if a.data:
            if a.name == sort_by:
                reverse = not reverse
            session['sort_by'] = a.name
            session['reverse'] = reverse
            return redirect(f'/view/{model_type}')
    else:
        print(sort.errors)
            

    # Handle deleting of transactions
    if request.method == 'POST':
        for i in items:
            if request.form.get(f'delete_{i.id}') == 'Delete':
                delete_from_db(model_type, i.id)
                return redirect(f'/view/{model_type}')
            
            if request.form.get(f'edit_{i.id}') == 'Edit':
                return redirect(f'/edit/{model_type}/{i.id}')

    items = sort.sort(items, sort_by, reverse)

    
    return render_template('view_model.html',
                           allItems = items,
                           headers=sort,
                           title=model_type,
                           active_page='view')

# ----------------------------------------------------------------
# Add models    
@app.route('/add_stock', methods=['GET', 'POST'])
@login_required
def add_stock():
    form = AddStockItemForm()
    
    if form.validate_on_submit():
        print("submit")
        form.add_to_database()
        return redirect(url_for('index')) 
    else:
        print(form.errors)
    
    return render_template('add_model.html',
                           form=form,
                           active_page='add',
                           title='Stock')
    
@app.route('/add_kit', methods=['GET', 'POST'])
@login_required
def add_kit():
    form = AddKitForm()
    
    
    if form.validate_on_submit():
        print("submit")
        # Save form data
        for field in form:
            session['kit'+field.name] = field.data
            
        if form.items.data:
            return redirect(url_for('add_selected_stock_items'))
        elif form.course.data:
            return redirect('/add_selected_course/add_kit')
        else:
            form.add_to_database(session['selected_item_ids'], session['selected_course_id'])
            session['selected_item_ids'] = []
            session['selected_course_id'] = None
            
            for field in form:
                session['kit'+field.name] = None
            return redirect('/view/kit') 
    else:
        print(form.errors)
        
    for field in form:
        try:
            field.data = session['kit'+field.name]
        except:
            pass
    
    return render_template('add_model.html',
                           form=form,
                           active_page='add',
                           title='Kit')
    
@app.route('/add_course', methods=['GET', 'POST'])
@login_required
def add_course():
    form = AddCourseForm()
    
    print("reload page")
    
    if form.validate_on_submit():
        print("submit")
        form.add_to_database()
        return redirect('/view/course') 
    else:
        print(form.errors)
    
    return render_template('add_model.html',
                           form=form,
                           active_page='add',
                           title='Course')
    
@app.route('/add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    form = AddEventForm()
    
    print("reload page")
    
    if form.validate_on_submit():
        print("submit")
        # Save form data
        for field in form:
            print(type(field.data))
            session['event'+field.name] = field.data

        if form.course.data:
            return redirect('/add_selected_course/add_event')
        else:
            form.add_to_database(session['selected_course_id'])
            session['selected_course_id'] = None
            for field in form:
                session['event'+field.name] = None
            return redirect('/view/event') 
    else:
        print(form.errors)

    for field in form:
        try:
            if field.name == 'start' or field.name == 'end':
                if field.data:
                    field.data = datetime.datetime.strptime(session['event'+field.name], '%a, %d %b %Y %H:%M:%S %Z').date()
            else:
                field.data = session['event'+field.name]
        except:
            pass
        

    return render_template('add_model.html',
                           form=form,
                           active_page='add',
                           title='Event')

# ----------------------------------------------------------------
# Add selected    
@app.route('/add_selected_stock_items', methods=['GET', 'POST'])
@login_required
def add_selected_stock_items():
    # Define if not already defined
    # Used to store sort for when page is refreshed
    form_type = "checkbox"
    
    try:
        reverse = session['reverse']
    except:
        reverse = False
    try:
        sort_by = session['sort_by']
    except:
        sort_by = None
        
        
    stock = get_stock_items()
    sort = SortStockItemForm()
    
    # Sort columns 
    print(sort_by)
    for a in sort:
        if a.data:
            if a.name == sort_by:
                reverse = not reverse
            session['sort_by'] = a.name
            session['reverse'] = reverse
            return redirect(url_for('add_selected_stock_items'))
    else:
        print(sort.errors)

    # Selecting items
    if request.method == 'POST':
        session['selected_item_ids'] = []
        if form_type == "radio":
            session['selected_item_ids'] = [request.form['radio_input']]
        else:
            for id in request.form:
                # Link all items with ID
                session['selected_item_ids'].append(int(id))
            
        return redirect(url_for('add_kit'))
        
    stock = sort.sort(stock, sort_by, reverse)       
    print("selected", session['selected_item_ids'])
    return render_template('add_selected_items.html',
                           allItems = stock,
                           headers=sort,
                           form_type = form_type,
                           already_selected = session['selected_item_ids'],
                           active_page='add')

@app.route('/add_selected_course/<redirect_to>', methods=['GET', 'POST'])
@login_required
def add_selected_course(redirect_to):
    # Define if not already defined
    # Used to store sort for when page is refreshed
    form_type = "radio"
    
    try:
        reverse = session['reverse']
    except:
        reverse = False
    try:
        sort_by = session['sort_by']
    except:
        sort_by = None
        
    courses = get_courses()
    sort = SortCoursesForm()
    
    # Sort columns 
    print(sort_by)
    for a in sort:
        if a.data:
            if a.name == sort_by:
                reverse = not reverse
            session['sort_by'] = a.name
            session['reverse'] = reverse
            return redirect(url_for('add_selected_course'))
    else:
        print(sort.errors)

    # Selecting items
    if request.method == 'POST':
        if form_type == "radio":
            session['selected_course_id'] = int(request.form['radio_input'])
        else:
            for id in request.form:
                # Link all items with ID
                session['selected_course_id'].append(int(id))
        return redirect(url_for(redirect_to))
        
    courses = sort.sort(courses, sort_by, reverse)
    print("selected", session['selected_course_id'])
    return render_template('add_selected_items.html',
                           allItems = courses,
                           headers=sort,
                           form_type = form_type,
                           already_selected = session['selected_course_id'],
                           active_page='add')

# ----------------------------------------------------------------
# Edit models
@app.route('/edit/<model_type>/<id>', methods=['GET', 'POST'])
@login_required
def edit_stock(model_type, id):
    if model_type == 'stock':
        form = AddStockItemForm()
        stock_item = get_stock_item_with_id(id)
    elif model_type == 'kit':
        form = AddKitForm()
        stock_item = get_stock_item_with_id(id)
    elif model_type == 'course':
        form = AddCourseForm()
        stock_item = get_stock_item_with_id(id)
    elif model_type == 'event':
        form = AddEventForm()
        stock_item = get_stock_item_with_id(id)
    
    
    if form.validate_on_submit():
        print("submit")
        delete_from_db(model_type, id)
        form.add_to_database()
        return redirect(url_for('index')) 
    else:
        print(form.errors)
        
    if form.validate_on_submit():
        print("submit")
        # Save form data
        for field in form:
            session[field.name] = field.data
            
        if form.items.data:
            return redirect(url_for('add_selected_stock_items'))
        elif form.course.data:
            return redirect('/add_selected_course/add_kit')
        else:
            form.add_to_database(session['selected_item_ids'], session['selected_course_id'])
            session['selected_item_ids'] = []
            session['selected_course_id'] = None
            return redirect('/view/kit') 
    else:
        print(form.errors)
        
    for field in form:
        try:
            field.data = session[field.name]
        except:
            pass
    
    
    for i in range(len(form.fields())):
        form.fields()[i].data = stock_item.data()[i]
    
    return render_template('add_model.html',
                           form=form,
                           active_page='view')
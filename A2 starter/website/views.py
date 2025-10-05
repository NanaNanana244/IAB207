from flask import Blueprint, render_template, request
from . import db
from .models import Event

main_bp = Blueprint('main', __name__)

@main_bp.route('/debug-db')
def debug_db():
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    
    # Check Event table columns
    columns = inspector.get_columns('event')
    result = "ACTUAL DATABASE COLUMNS:\n"
    for column in columns:
        result += f"- {column['name']} ({column['type']})\n"
    
    # Check if there are any events
    try:
        events = db.session.execute(db.select(Event)).scalars().all()
        result += f"\nEVENTS IN DATABASE: {len(events)}\n"
        for event in events:
            result += f"- {event.title} (Country: {getattr(event, 'country', 'NO COUNTRY ATTRIBUTE')})\n"
    except Exception as e:
        result += f"\nERROR READING EVENTS: {e}"
    
    return f"<pre>{result}</pre>"


@main_bp.route('/')
def index():
    # Get filters from URL parameters
    country_filter = request.args.get('country', '')
    status_filter = request.args.get('status', '')
    
    # TEMPORARY: Get all events without country filtering
    try:
        events = Event.query.all()
    except Exception as e:
        print("Database error, returning empty events:", e)
        events = []
    
    # TEMPORARY: Manual filtering in Python instead of SQL
    if country_filter:
        events = [event for event in events if hasattr(event, 'country') and event.country == country_filter]
    
    if status_filter:
        events = [event for event in events if event.status == status_filter]
    
    return render_template('home.html', 
                         events=events, 
                         title='Home Page',
                         selected_country=country_filter,
                         selected_status=status_filter)

# Search route remains the same
@main_bp.route('/search')
def search():
    query = request.args.get('q', '')
    events = [] 
    results_count = 0
    return render_template('search.html', 
                         events=events, 
                         query=query, 
                         results_count=results_count,
                         title=f"Search: {query}")
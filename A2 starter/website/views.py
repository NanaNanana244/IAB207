from flask import Blueprint, render_template, request
from . import db
from .models import Event

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Get filters from URL parameters
    country_filter = request.args.get('country', '')
    status_filter = request.args.get('status', '')
    
    # Start with all events
    query = Event.query
    
    # Apply country filter if specified - FIXED TO HANDLE CASE INSENSITIVE
    if country_filter:
        # Use ilike for case-insensitive filtering
        query = query.filter(Event.country.ilike(country_filter))
    
    # Apply status filter if specified  
    if status_filter:
        query = query.filter(Event.status == status_filter)
    
    events = query.all()
    
    return render_template('home.html', 
                         events=events, 
                         title='Home Page',
                         selected_country=country_filter,
                         selected_status=status_filter)

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

@main_bp.route('/event/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_detail.html', event=event, title=event.title)

@main_bp.route('/demo-event')
def demo_event():
    return render_template('event_details/DemoEvent.html', title='Demo Event')

@main_bp.route('/booking-history')
def booking_history():
    # Show all events for now since we're not using authentication yet
    user_events = Event.query.all()
    
    return render_template('history.html', 
                         user_events=user_events,
                         title='Booking History')

@main_bp.route('/register')
def register():
    return "Register page coming soon"
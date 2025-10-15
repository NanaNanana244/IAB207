from flask import Blueprint, render_template, request, redirect, url_for, flash 
from flask_login import login_required, current_user
from datetime import datetime
from . import db
from .models import Event, Comment, Order 
from .forms import CreateEvent, SearchForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    # Get filters from URL parameters
    country_filter = request.args.get('country', '')
    status_filter = request.args.get('status', '')
    price_sort = request.args.get('price_sort', '')

    # Start with all events
    query = Event.query

    # Update status for all events before filtering
    all_events = Event.query.all()
    for event in all_events:
        event.update_status()
    db.session.commit() 

    # Apply country filter if specified
    if country_filter:
        if country_filter == 'other':
            # Case-insensitive exclusion for "other" category
            excluded_countries = ['america', 'australia', 'canada', 'china', 'japan', 'korea']
            for country in excluded_countries:
                query = query.filter(~Event.country.ilike(country))
        else:
            # Case-insensitive inclusion for specific countries
            query = query.filter(Event.country.ilike(country_filter))
    # Apply status filter if specified  
    if status_filter:
        query = query.filter(Event.status == status_filter)
    # Apply price sorting if specified
    if price_sort:
        # When sorting by price, only show available events
        query = query.filter(Event.status == 'Available')
        if price_sort == 'normal_low_to_high':
            query = query.order_by(Event.normalPrice.asc())
        elif price_sort == 'normal_high_to_low':
            query = query.order_by(Event.normalPrice.desc())
        elif price_sort == 'vip_low_to_high':
            query = query.order_by(Event.vipPrice.asc())
        elif price_sort == 'vip_high_to_low':
            query = query.order_by(Event.vipPrice.desc())
            
    events = query.all()

    return render_template('home.html', 
                         events=events, 
                         title='Home Page',
                         selected_country=country_filter,
                         selected_status=status_filter,
                         selected_price_sort=price_sort)


# Search functionality
@main_bp.route('/search', methods =['GET'])
def search():
    query = request.args.get('q')  #Get query from search bar
    if query:
        results= Event.query.filter(Event.title.ilike(f'%{query}%') |
                                    Event.artist.ilike(f'%{query}%') |
                                    Event.location.ilike(f'%{query}%') |
                                    Event.country.ilike(f'%{query}%') |
                                    Event.description.ilike(f'%{query}%') |
                                    Event.tags.ilike(f'%{query}%')
                                    ).all()   #Match with attributes title, artist, location, country, description and tags
        results_count = len(results)  #Count results
    else:
        results = []
        results_count = 0
    
    return render_template('search.html', events=results, query=query, results_count=results_count)

# Event detail page
@main_bp.route('/event/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    event.update_status()
    return render_template('event_details/details.html', event=event, title=event.title)

# Event details - Select amount of tickets and process order
@main_bp.route('/event/<int:event_id>/purchase', methods=['POST'])
@login_required
def purchase_tickets(event_id):
    event = Event.query.get_or_404(event_id)
    normal_qty = int(request.form.get('normal_qty', 0))
    vip_qty = int(request.form.get('vip_qty', 0))
    # Validate quantities
    if normal_qty < 0 or vip_qty < 0:
        flash('Ticket quantities cannot be negative.', 'error')
        return redirect(url_for('main.event_detail', event_id=event_id))
    if normal_qty > event.normalAvail:
        flash(f'Cannot purchase {normal_qty} normal tickets. Only {event.normalAvail} available.', 'error')
        return redirect(url_for('main.event_detail', event_id=event_id))
    if vip_qty > event.vipAvail:
        flash(f'Cannot purchase {vip_qty} VIP tickets. Only {event.vipAvail} available.', 'error')
        return redirect(url_for('main.event_detail', event_id=event_id))
    if normal_qty == 0 and vip_qty == 0:
        flash('Please select at least one ticket.', 'error')
        return redirect(url_for('main.event_detail', event_id=event_id))
    # Calculate total
    total = (normal_qty * event.normalPrice) + (vip_qty * event.vipPrice)
    # Create order
    new_order = Order(
        userid=current_user.userid,
        eventid=event_id,
        normalQty=normal_qty,
        vipQty=vip_qty,
        totalPrice=total,
        timeBooked=datetime.now()
    )
    # Update event availability
    event.normalAvail -= normal_qty
    event.vipAvail -= vip_qty
    db.session.add(new_order)
    db.session.commit()
    
    # Update event status after ticket purchase (checks for sold out)
    event.update_status()
    db.session.commit()

    # Redirect back with confirm parameter instead of flash message
    return redirect(url_for('main.event_detail', event_id=event_id, confirm='true'))

# Event details - Commenting 
@main_bp.route('/event/<int:event_id>/comment', methods=['POST'])
@login_required
def add_comment(event_id):
    comment_text = request.form.get('comment_text')
    new_comment = Comment(
        eventid=event_id,
        userid=current_user.userid,
        comment=comment_text
    )
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('main.event_detail', event_id=event_id))

# Booking History page 
@main_bp.route('/booking-history')
@login_required
def booking_history():
    # Get user's orders with event details
    user_orders = Order.query.filter_by(userid=current_user.userid)\
                            .join(Event)\
                            .order_by(Order.timeBooked.desc())\
                            .all()
    # Get user's created events
    user_events = Event.query.filter_by(userid=current_user.userid).all()
    
    # Update status for user's events
    for event in user_events:
        event.update_status()
    return render_template('history.html', 
                         user_orders=user_orders,
                         user_events=user_events,
                         title='Booking History')
    
# Error pages
@main_bp.route('/404')
def not_found():
    return render_template('404.html', title='404 Not Found')
@main_bp.route('/500')
def server_error():
    return render_template('500.html', title='500 Internal Server Error')

# Order details page
@main_bp.route('/order/<int:order_id>') 
@login_required
def order_details(order_id): 
    # Get the specific order
    order = Order.query.filter_by(orderid=order_id, userid=current_user.userid).first_or_404()
    return render_template('order_details.html', 
                         order=order,
                         title=f'Order #{order.orderid}')


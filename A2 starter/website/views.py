from flask import Blueprint, render_template, request, redirect, url_for, flash 
from flask_login import login_required, current_user
from datetime import datetime
from . import db
from .models import Event, Comment, Order 

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Get filters from URL parameters
    country_filter = request.args.get('country', '')
    status_filter = request.args.get('status', '')
    
    # Start with all events
    query = Event.query
    
    # Apply country filter if specified
    if country_filter:
        if country_filter == 'other':
            # Filter out the specific countries, show everything else
            query = query.filter(~Event.country.in_(['america', 'australia', 'canada', 'china', 'japan', 'korea']))
        else:
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
    query = request.args.get('q')
    results= Event.query.filter(Event.title.ilike(f'%{query}')).all()
    return render_template('search.html', results=results)

@main_bp.route('/event/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_details/details.html', event=event, title=event.title)

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
    
    # Calculate prices
    normal_total = normal_qty * event.normalPrice
    vip_total = vip_qty * event.vipPrice
    total_price = normal_total + vip_total
    
    # Create order
    new_order = Order(
        userid=current_user.userid,
        eventid=event_id,
        normalQty=normal_qty,
        vipQty=vip_qty,
        totalPrice=total_price,
        timeBooked=datetime.now()
    )
    
    # Update event availability
    event.normalAvail -= normal_qty
    event.vipAvail -= vip_qty
    
    db.session.add(new_order)
    db.session.commit()
    
    flash(f'Purchase confirmed! {normal_qty} normal + {vip_qty} VIP tickets. Total: ${total_price}', 'success')
    return redirect(url_for('main.event_detail', event_id=event_id))

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
    

@main_bp.route('/404')
def not_found():
    return render_template('404.html', title='404 Not Found')

@main_bp.route('/500')
def server_error():
    return render_template('500.html', title='500 Internal Server Error')

@main_bp.route('/order-details')
def order_details():
    return render_template('order_details.html', title='Order Details')
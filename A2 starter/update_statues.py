from main import create_app
from website import db
from website.models import Event
from datetime import date

# Create app context
app = create_app()

with app.app_context():
    events = Event.query.all()
    print(f"Found {len(events)} events")
    
    for event in events:
        old_status = event.status
        event.update_status()
        if old_status != event.status:
            print(f"Updated {event.title}: {old_status} → {event.status}")
    
    db.session.commit()
    print("All event statuses updated!")
    
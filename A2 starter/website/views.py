from flask import Blueprint, render_template, request

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('home.html', title='Home Page')

# Search route
@main_bp.route('/search')
def search():
    query = request.args.get('q', '')  # Get search query from URL
    # For now, return empty results. Add the database search later
    events = [] 
    results_count = 0
    return render_template('search.html', 
                         events=events, 
                         query=query, 
                         results_count=results_count,
                         title=f"Search: {query}")
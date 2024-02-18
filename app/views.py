#views.py
from flask import Blueprint, render_template, request
from .downloader import fetch_json_feed
from math import ceil
from random import sample

# Initialize Flask Blueprint
main = Blueprint('main', __name__)

# Define constants for the pagination
PER_PAGE = 40
JSON_FEED_URL = "https://www.pornhub.com/files/json_feed_pornstars.json"

@main.route('/')
def index():
    # Get the current page number from query parameters, default to 1 if not specified.
    page = request.args.get('page', 1, type=int)
    
    # Fetch JSON data from the defined URL function.
    json_data = fetch_json_feed(JSON_FEED_URL)
    if json_data is not None:
        items = json_data.get('items', [])
        # Filter out items with a 'rank' of 0 and sort the remaining items by 'rank' (because of many bad data rank=0).
        filtered_and_sorted_items = sorted(
            [item for item in items if item['attributes']['stats']['rank'] > 0],
            key=lambda x: x['attributes']['stats']['rank']
        )
    else:
        filtered_and_sorted_items = []

    # Calculate start and end indices for pagination.
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    total_pages = len(filtered_and_sorted_items) // PER_PAGE + (1 if len(filtered_and_sorted_items) % PER_PAGE > 0 else 0)

    # Slice the sorted list to obtain items for the current page.
    items_for_page = filtered_and_sorted_items[start:end]

    # Render the index page, passing the items for the current page and pagination details.
    return render_template('index.html', items=items_for_page, page=page, total_pages=total_pages, per_page=PER_PAGE)

@main.route('/item/<int:item_id>')
def item_detail(item_id):
    # Fetch JSON data again for details of a specific item.
    json_data = fetch_json_feed(JSON_FEED_URL)
    recommendations = []
    if json_data is not None:
        items = json_data.get('items', [])
        # Find the specific item by its ID.
        item = next((item for item in items if item['id'] == item_id), None)
        if item:
            # Find similar items based on the gender attribute.
            similar_items = [i for i in items if i['id'] != item_id and i['attributes']['gender'] == item['attributes']['gender']]
            # Randomly select 10 similar items for recommendations.
            recommendations = sample(similar_items, min(len(similar_items), 10))
    else:
        item = None

    # If the item was not found, return a 404 error page.
    if item is None:
        return render_template('404.html'), 404

    # Render the detail page for the item, including recommendations.
    return render_template('detail.html', item=item, recommendations=recommendations)

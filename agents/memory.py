from database.mongodb import plans_collection, sessions_collection

# store user learning state
def save_event(event_type, data):

    plans_collection.insert_one({
        "type": event_type,
        "data": data
    })


def get_context():
    """Fetch recent memory for AI context"""

    plans = list(plans_collection.find({}, {"_id": 0}).limit(5))
    sessions = list(sessions_collection.find({}, {"_id": 0}).limit(5))

    return {
        "plans": plans,
        "sessions": sessions
    }
from flask import Blueprint, jsonify, request
from src.models.github_event import GitHubEvent
from datetime import datetime

api_bp = Blueprint('api', __name__)

def format_timestamp(timestamp_str):
    """Format timestamp for display"""
    try:
        # Parse ISO timestamp
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        
        # Format for display
        return dt.strftime('%d %B %Y - %I:%M %p UTC')
    except Exception as e:
        print(f"Error formatting timestamp: {e}")
        return timestamp_str

def format_event_message(event):
    """Format event message according to specifications"""
    author = event.get('author', 'Unknown')
    action = event.get('action', '')
    to_branch = event.get('to_branch', '')
    from_branch = event.get('from_branch', '')
    timestamp = format_timestamp(event.get('timestamp', ''))
    
    if action == 'PUSH':
        return f'"{author}" pushed to "{to_branch}" on {timestamp}'
    elif action == 'PULL_REQUEST':
        return f'"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp}'
    elif action == 'MERGE':
        return f'"{author}" merged branch "{from_branch}" to "{to_branch}" on {timestamp}'
    else:
        return f'"{author}" performed {action} on {timestamp}'

@api_bp.route('/events', methods=['GET'])
def get_events():
    """Get latest GitHub events"""
    try:
        limit = request.args.get('limit', 50, type=int)
        limit = min(limit, 100)  # Cap at 100 events
        
        events = GitHubEvent.get_latest_events(limit)
        
        # Format events for frontend display
        formatted_events = []
        for event in events:
            formatted_event = {
                'id': event.get('_id'),
                'request_id': event.get('request_id'),
                'author': event.get('author'),
                'action': event.get('action'),
                'from_branch': event.get('from_branch'),
                'to_branch': event.get('to_branch'),
                'timestamp': event.get('timestamp'),
                'formatted_timestamp': format_timestamp(event.get('timestamp', '')),
                'message': format_event_message(event)
            }
            formatted_events.append(formatted_event)
        
        return jsonify({
            'status': 'success',
            'count': len(formatted_events),
            'events': formatted_events
        }), 200
        
    except Exception as e:
        print(f"Error fetching events: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/events/<event_id>', methods=['GET'])
def get_event(event_id):
    """Get a specific event by ID"""
    try:
        event = GitHubEvent.get_event_by_id(event_id)
        
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        formatted_event = {
            'id': event.get('_id'),
            'request_id': event.get('request_id'),
            'author': event.get('author'),
            'action': event.get('action'),
            'from_branch': event.get('from_branch'),
            'to_branch': event.get('to_branch'),
            'timestamp': event.get('timestamp'),
            'formatted_timestamp': format_timestamp(event.get('timestamp', '')),
            'message': format_event_message(event)
        }
        
        return jsonify({
            'status': 'success',
            'event': formatted_event
        }), 200
        
    except Exception as e:
        print(f"Error fetching event: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/events/sample', methods=['POST'])
def create_sample_events():
    """Create sample events for testing"""
    try:
        # Clear existing events first
        deleted_count = GitHubEvent.delete_all_events()
        print(f"Deleted {deleted_count} existing events")
        
        # Create sample events
        event_ids = GitHubEvent.create_sample_events()
        
        return jsonify({
            'status': 'success',
            'message': f'Created {len(event_ids)} sample events',
            'event_ids': event_ids
        }), 200
        
    except Exception as e:
        print(f"Error creating sample events: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Git Ping API',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


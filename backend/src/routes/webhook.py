from flask import Blueprint, request, jsonify
from src.models.github_event import GitHubEvent
import json

webhook_bp = Blueprint('webhook', __name__)

def parse_push_event(payload):
    """Parse GitHub push event payload"""
    try:
        commits = payload.get('commits', [])
        if not commits:
            return None
            
        # Get the latest commit
        latest_commit = commits[-1]
        
        return GitHubEvent(
            request_id=latest_commit.get('id', ''),
            author=payload.get('pusher', {}).get('name', 'Unknown'),
            action="PUSH",
            to_branch=payload.get('ref', '').replace('refs/heads/', ''),
            from_branch=None
        )
    except Exception as e:
        print(f"Error parsing push event: {e}")
        return None

def parse_pull_request_event(payload):
    """Parse GitHub pull request event payload"""
    try:
        pull_request = payload.get('pull_request', {})
        
        return GitHubEvent(
            request_id=str(pull_request.get('id', '')),
            author=pull_request.get('user', {}).get('login', 'Unknown'),
            action="PULL_REQUEST",
            to_branch=pull_request.get('base', {}).get('ref', ''),
            from_branch=pull_request.get('head', {}).get('ref', '')
        )
    except Exception as e:
        print(f"Error parsing pull request event: {e}")
        return None

def parse_merge_event(payload):
    """Parse GitHub merge event payload (pull request merged)"""
    try:
        pull_request = payload.get('pull_request', {})
        
        # Check if it's actually a merge
        if not pull_request.get('merged', False):
            return None
            
        return GitHubEvent(
            request_id=str(pull_request.get('id', '')),
            author=pull_request.get('merged_by', {}).get('login', 'Unknown'),
            action="MERGE",
            to_branch=pull_request.get('base', {}).get('ref', ''),
            from_branch=pull_request.get('head', {}).get('ref', '')
        )
    except Exception as e:
        print(f"Error parsing merge event: {e}")
        return None

@webhook_bp.route('/webhook', methods=['POST'])
def github_webhook():
    """Handle GitHub webhook events"""
    try:
        # Get the event type from headers
        event_type = request.headers.get('X-GitHub-Event')
        payload = request.get_json()
        
        if not payload:
            return jsonify({'error': 'No payload received'}), 400
        
        print(f"Received GitHub event: {event_type}")
        
        github_event = None
        
        if event_type == 'push':
            github_event = parse_push_event(payload)
        elif event_type == 'pull_request':
            action = payload.get('action')
            if action == 'opened':
                github_event = parse_pull_request_event(payload)
            elif action == 'closed' and payload.get('pull_request', {}).get('merged', False):
                github_event = parse_merge_event(payload)
        
        if github_event:
            event_id = github_event.save()
            if event_id:
                print(f"Saved event with ID: {event_id}")
                return jsonify({
                    'status': 'success',
                    'message': 'Event processed successfully',
                    'event_id': event_id
                }), 200
            else:
                return jsonify({'error': 'Failed to save event'}), 500
        else:
            return jsonify({
                'status': 'ignored',
                'message': f'Event type {event_type} not processed'
            }), 200
            
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@webhook_bp.route('/webhook/test', methods=['POST'])
def test_webhook():
    """Test endpoint for webhook functionality"""
    try:
        data = request.get_json()
        
        # Create a test event
        test_event = GitHubEvent(
            request_id=data.get('request_id', 'test-123'),
            author=data.get('author', 'test-user'),
            action=data.get('action', 'PUSH'),
            to_branch=data.get('to_branch', 'main'),
            from_branch=data.get('from_branch')
        )
        
        event_id = test_event.save()
        if event_id:
            return jsonify({
                'status': 'success',
                'message': 'Test event created successfully',
                'event_id': event_id
            }), 200
        else:
            return jsonify({'error': 'Failed to save test event'}), 500
            
    except Exception as e:
        print(f"Error creating test event: {e}")
        return jsonify({'error': 'Internal server error'}), 500


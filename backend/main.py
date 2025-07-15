import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.webhook import webhook_bp
from routes.api import api_bp

# Initialize Flask app
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'git-ping-secret-key-2024')

# Enable CORS for all routes
CORS(app, origins="*")

# Register blueprints
app.register_blueprint(webhook_bp, url_prefix='/api')
app.register_blueprint(api_bp, url_prefix='/api')

# Serve frontend static files (if placed under /static folder in backend)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    full_path = os.path.join(static_folder_path, path)
    if path != "" and os.path.exists(full_path):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "Git Ping - Frontend not built yet", 200

# API metadata route
@app.route('/api')
def api_info():
    return {
        'service': 'Git Ping API',
        'version': '1.0.0',
        'endpoints': {
            'webhook': '/api/webhook',
            'events': '/api/events',
            'health': '/api/health'
        }
    }

# Entry point
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

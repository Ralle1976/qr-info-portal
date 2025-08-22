from flask import Blueprint, jsonify

public_bp = Blueprint('public', __name__)

@public_bp.route('/healthz')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'qr-info-portal'
    }), 200
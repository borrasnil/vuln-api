import requests
from flask import Blueprint, jsonify, request

v5_bp = Blueprint('v5', __name__, url_prefix='/api/v5')


@v5_bp.route('/fetch', methods=['POST'])
def v5_fetch():
    data = request.get_json() or {}
    url = data.get('url', '')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        resp = requests.get(url, timeout=5)
        return jsonify({
            'success': True, 
            'fetched_url': url, 
            'status_code': resp.status_code,
            'content_length': len(resp.content),
            'message': f'Fetched from {url}'
        })
    except requests.exceptions.RequestException as e:
        return jsonify({'success': True, 'fetched_url': url, 'error': str(e), 'message': 'URL fetched but failed'})


@v5_bp.route('/proxy', methods=['GET'])
def v5_proxy():
    url = request.args.get('url', '')
    if not url:
        return jsonify({'error': 'url parameter required'}), 400
    
    try:
        resp = requests.get(url, timeout=5)
        return jsonify({'proxy_to': url, 'status': resp.status_code, 'content': resp.text[:500]})
    except requests.exceptions.RequestException as e:
        return jsonify({'proxy_to': url, 'error': str(e)})


@v5_bp.route('/webhook', methods=['POST'])
def v5_webhook():
    data = request.get_json() or {}
    webhook_url = data.get('webhook_url', '')
    return jsonify({'success': True, 'webhook_set': webhook_url, 'message': 'Webhook configured (no validation)'})
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://api_user:api_pass@postgres:5432/api_lab')

CHALLENGES = {
    1: {
        'name': 'Broken Object Level Authorization',
        'short': 'BOLA / IDOR',
        'description': 'Access other users\' resources by manipulating object IDs',
        'severity': 'Critical',
        'explanation': 'APIs expose endpoints that handle object identifiers without verifying ownership. Any user can access anyone else\'s data by changing the ID in the URL.',
        'why_vulnerable': 'No ownership check on resource access\nTrusting user-provided IDs\nLack of authorization at object level',
        'endpoints': [
            {'method': 'GET', 'path': '/api/v1/users', 'desc': 'List all users'},
            {'method': 'GET', 'path': '/api/v1/users/{id}', 'desc': 'Get user by ID'},
            {'method': 'GET', 'path': '/api/v1/items', 'desc': 'List all items'},
            {'method': 'GET', 'path': '/api/v1/items/{id}', 'desc': 'Get item by ID'},
            {'method': 'GET', 'path': '/api/v1/secrets', 'desc': 'List all secrets'},
        ]
    },
    2: {
        'name': 'Broken Authentication',
        'short': 'Broken Auth',
        'description': 'Flawed login allowing account takeover and brute force attacks',
        'severity': 'Critical',
        'explanation': 'Flawed login mechanisms allowing account takeover, brute force attacks, token manipulation, and session hijacking.',
        'why_vulnerable': 'No rate limiting\nNo account lockout\nWeak password policies\nNo verification on password reset',
        'endpoints': [
            {'method': 'POST', 'path': '/api/v2/login', 'desc': 'Login'},
            {'method': 'POST', 'path': '/api/v2/register', 'desc': 'Register new user'},
            {'method': 'POST', 'path': '/api/v2/reset-password', 'desc': 'Reset password'},
        ]
    },
    3: {
        'name': 'Broken Object Property Level Auth',
        'short': 'Property Auth',
        'description': 'Excessive data exposure and mass assignment vulnerabilities',
        'severity': 'High',
        'explanation': 'API returns all fields including sensitive data (passwords, secrets) and allows users to modify privileged fields like role and admin status.',
        'why_vulnerable': 'No field-level filtering\nDirect parameter binding\nNo allowlist for sensitive fields',
        'endpoints': [
            {'method': 'GET', 'path': '/api/v3/users', 'desc': 'List users (exposes password)'},
            {'method': 'GET', 'path': '/api/v3/users/{id}', 'desc': 'Get user details'},
            {'method': 'PUT', 'path': '/api/v3/users/{id}', 'desc': 'Update user (mass assignment)'},
            {'method': 'PATCH', 'path': '/api/v3/items/{id}', 'desc': 'Update item price'},
        ]
    },
    4: {
        'name': 'Unrestricted Resource Consumption',
        'short': 'Resource',
        'description': 'No rate limiting allowing DoS and cost escalation',
        'severity': 'High',
        'explanation': 'No rate limiting allowing DoS attacks via excessive API calls or cost escalation through expensive operations.',
        'why_vulnerable': 'No request limits\nNo pagination\nNo timeout on expensive operations',
        'endpoints': [
            {'method': 'GET', 'path': '/api/v4/search?q=query', 'desc': 'Search (no limit)'},
            {'method': 'GET', 'path': '/api/v4/export', 'desc': 'Export all data'},
            {'method': 'POST', 'path': '/api/v4/bulk-action', 'desc': 'Bulk operations'},
        ]
    },
    5: {
        'name': 'Server-Side Request Forgery',
        'short': 'SSRF',
        'description': 'API fetches user URLs enabling internal network attacks',
        'severity': 'High',
        'explanation': 'API fetches user-controlled URLs enabling internal network attacks, cloud metadata access, and port scanning.',
        'why_vulnerable': 'No URL validation\nBlind trust of user input\nFollowing redirects',
        'endpoints': [
            {'method': 'POST', 'path': '/api/v5/fetch', 'desc': 'Fetch URL'},
            {'method': 'GET', 'path': '/api/v5/proxy', 'desc': 'Proxy request'},
            {'method': 'POST', 'path': '/api/v5/webhook', 'desc': 'Set webhook'},
        ]
    },
    6: {
        'name': 'SQL Injection',
        'short': 'SQLi',
        'description': 'Direct SQL concatenation allowing data extraction',
        'severity': 'Critical',
        'explanation': 'Classic SQL injection allowing data extraction, authentication bypass, and potential database takeover.',
        'why_vulnerable': 'String concatenation in queries\nNo input sanitization\nNo parameterized queries',
        'endpoints': [
            {'method': 'GET', 'path': '/api/v6/search?q=query', 'desc': 'Search'},
            {'method': 'GET', 'path': '/api/v6/customers', 'desc': 'List customers'},
            {'method': 'POST', 'path': '/api/v6/login', 'desc': 'Login (SQLi bypass)'},
        ]
    }
}
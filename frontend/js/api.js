const API_BASE = 'http://localhost:5000';

async function callAPI(method, path) {
  const url = API_BASE + path;
  try {
    const res = await fetch(url, { method });
    const data = await res.json();
    document.getElementById('response').textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    document.getElementById('response').textContent = 'Error: ' + e.message;
  }
}

async function postJSON(path, body) {
  const res = await fetch(API_BASE + path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  const data = await res.json();
  document.getElementById('response').textContent = JSON.stringify(data, null, 2);
}

async function putJSON(path, body) {
  const res = await fetch(API_BASE + path, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  const data = await res.json();
  document.getElementById('response').textContent = JSON.stringify(data, null, 2);
}

async function patchJSON(path, body) {
  const res = await fetch(API_BASE + path, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  const data = await res.json();
  document.getElementById('response').textContent = JSON.stringify(data, null, 2);
}
// BASE_URL vazio = usa URLs relativas (nginx faz o proxy em Docker)
// Em dev, o vite.config.js tem proxy para http://localhost:8000
const BASE_URL = import.meta.env.VITE_API_URL || '';

function getHeaders() {
  const token = localStorage.getItem('token');
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Token ${token}`;
  return headers;
}

async function req(method, path, body) {
  const opts = { method, headers: getHeaders() };
  if (body !== undefined) opts.body = JSON.stringify(body);

  const res = await fetch(`${BASE_URL}${path}`, opts);

  if (res.status === 401) {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    window.location.href = '/login';
    return;
  }

  if (res.status === 204) return null;

  const data = await res.json();
  if (!res.ok) {
    const err = new Error('API Error');
    err.status = res.status;
    err.data = data;
    throw err;
  }
  return data;
}

export const api = {
  login: (username, password) =>
    req('POST', '/api/login/', { username, password }),

  logout: () => req('POST', '/api/logout/'),

  getDashboard: () => req('GET', '/api/dashboard/'),

  getTarefas: (params = {}) => {
    const entries = Object.entries(params).filter(
      ([, v]) => v !== null && v !== undefined && v !== ''
    );
    const qs = new URLSearchParams(entries).toString();
    return req('GET', `/api/tarefas/${qs ? '?' + qs : ''}`);
  },

  concluirTarefa: (id) => req('PATCH', `/api/tarefas/${id}/concluir/`),
  reabrirTarefa: (id) => req('PATCH', `/api/tarefas/${id}/reabrir/`),
  dispensarTarefa: (id) => req('PATCH', `/api/tarefas/${id}/dispensar/`),

  getEmpresas: () => req('GET', '/api/empresas/'),
  criarEmpresa: (data) => req('POST', '/api/empresas/', data),

  getObrigacoes: () => req('GET', '/api/obrigacoes/'),
  criarObrigacao: (data) => req('POST', '/api/obrigacoes/', data),

  getCompetencias: () => req('GET', '/api/competencias/'),
};

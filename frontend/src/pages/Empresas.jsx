import { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import { api } from '../api/client';

const TIPO_OPTIONS = [
  { value: 'SN_COM_FOLHA',    label: 'Simples Nacional c/ Folha' },
  { value: 'SN_SEM_FOLHA',    label: 'Simples Nacional s/ Folha' },
  { value: 'MEI',             label: 'MEI' },
  { value: 'LUCRO_PRESUMIDO', label: 'Lucro Presumido' },
];

const EMPTY_FORM = { nome: '', codigo: '', tipo: 'SN_COM_FOLHA' };

export default function Empresas() {
  const [empresas, setEmpresas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState(EMPTY_FORM);
  const [submitting, setSubmitting] = useState(false);
  const [feedback, setFeedback] = useState({ msg: '', type: '' });

  useEffect(() => {
    fetchEmpresas();
  }, []);

  async function fetchEmpresas() {
    setLoading(true);
    try {
      const data = await api.getEmpresas();
      setEmpresas(Array.isArray(data) ? data : data.results || []);
    } catch {
      setError('Erro ao carregar empresas.');
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setSubmitting(true);
    try {
      await api.criarEmpresa(form);
      showFeedback('Empresa criada! As tarefas da competência atual foram geradas automaticamente.', 'success');
      setForm(EMPTY_FORM);
      setShowForm(false);
      fetchEmpresas();
    } catch (err) {
      const detail =
        err?.data?.codigo?.[0] ||
        err?.data?.nome?.[0] ||
        err?.data?.non_field_errors?.[0] ||
        'Erro ao criar empresa.';
      showFeedback(detail, 'error');
    } finally {
      setSubmitting(false);
    }
  }

  function showFeedback(msg, type) {
    setFeedback({ msg, type });
    setTimeout(() => setFeedback({ msg: '', type: '' }), 5000);
  }

  function tipoLabel(tipo) {
    return TIPO_OPTIONS.find((o) => o.value === tipo)?.label || tipo;
  }

  return (
    <div className="page">
      <Navbar />
      <main className="main-content">
        <div className="page-header">
          <h2 className="page-title">Empresas</h2>
          <button
            className={`btn btn-sm ${showForm ? 'btn-ghost' : 'btn-primary'}`}
            onClick={() => {
              setShowForm(!showForm);
              setForm(EMPTY_FORM);
            }}
          >
            {showForm ? '✕ Cancelar' : '+ Nova Empresa'}
          </button>
        </div>

        {feedback.msg && (
          <div
            className={`feedback-message ${
              feedback.type === 'error' ? 'feedback-error' : 'feedback-success'
            }`}
          >
            {feedback.msg}
          </div>
        )}

        {showForm && (
          <div className="card form-card">
            <h3 className="form-title">Nova Empresa</h3>
            <p className="form-hint">
              Ao criar uma empresa, as tarefas da competência atual serão
              geradas automaticamente com base no tipo selecionado.
            </p>
            <form onSubmit={handleSubmit} className="form-grid">
              <div className="form-group">
                <label>Nome *</label>
                <input
                  type="text"
                  value={form.nome}
                  onChange={(e) => setForm((f) => ({ ...f, nome: e.target.value }))}
                  placeholder="Nome da empresa"
                  required
                />
              </div>
              <div className="form-group">
                <label>Código *</label>
                <input
                  type="text"
                  value={form.codigo}
                  onChange={(e) => setForm((f) => ({ ...f, codigo: e.target.value }))}
                  placeholder="Código único (ex: CNPJ)"
                  required
                />
              </div>
              <div className="form-group">
                <label>Tipo *</label>
                <select
                  value={form.tipo}
                  onChange={(e) => setForm((f) => ({ ...f, tipo: e.target.value }))}
                >
                  {TIPO_OPTIONS.map((o) => (
                    <option key={o.value} value={o.value}>
                      {o.label}
                    </option>
                  ))}
                </select>
              </div>
              <div className="form-actions">
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={submitting}
                >
                  {submitting ? 'Criando...' : 'Criar Empresa'}
                </button>
              </div>
            </form>
          </div>
        )}

        {loading ? (
          <div className="loading">Carregando empresas...</div>
        ) : error ? (
          <div className="error-message">{error}</div>
        ) : empresas.length === 0 ? (
          <div className="empty-state">
            <p>Nenhuma empresa cadastrada.</p>
            <button
              className="btn btn-primary"
              onClick={() => setShowForm(true)}
            >
              Criar primeira empresa
            </button>
          </div>
        ) : (
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Nome</th>
                  <th>Código</th>
                  <th>Tipo</th>
                  <th>Criada em</th>
                </tr>
              </thead>
              <tbody>
                {empresas.map((emp, i) => (
                  <tr key={emp.id}>
                    <td className="text-muted">{i + 1}</td>
                    <td className="font-medium">{emp.nome}</td>
                    <td className="text-mono">{emp.codigo}</td>
                    <td>
                      <span className="tipo-badge">{tipoLabel(emp.tipo)}</span>
                    </td>
                    <td className="text-muted">
                      {emp.criada_em
                        ? new Date(emp.criada_em).toLocaleDateString('pt-BR')
                        : '—'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  );
}

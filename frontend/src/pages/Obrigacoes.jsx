import { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import { api } from '../api/client';

const EMPTY_FORM = { nome: '', dia_vencimento: '' };

export default function Obrigacoes() {
  const [obrigacoes, setObrigacoes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState(EMPTY_FORM);
  const [submitting, setSubmitting] = useState(false);
  const [feedback, setFeedback] = useState({ msg: '', type: '' });

  useEffect(() => {
    fetchObrigacoes();
  }, []);

  async function fetchObrigacoes() {
    setLoading(true);
    try {
      const data = await api.getObrigacoes();
      setObrigacoes(Array.isArray(data) ? data : data.results || []);
    } catch {
      setError('Erro ao carregar obrigações.');
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setSubmitting(true);
    try {
      const payload = {
        nome: form.nome,
        ...(form.dia_vencimento
          ? { dia_vencimento: parseInt(form.dia_vencimento, 10) }
          : { dia_vencimento: null }),
      };
      await api.criarObrigacao(payload);
      showFeedback('Obrigação criada com sucesso!', 'success');
      setForm(EMPTY_FORM);
      setShowForm(false);
      fetchObrigacoes();
    } catch (err) {
      const detail =
        err?.data?.nome?.[0] ||
        err?.data?.non_field_errors?.[0] ||
        'Erro ao criar obrigação.';
      showFeedback(detail, 'error');
    } finally {
      setSubmitting(false);
    }
  }

  function showFeedback(msg, type) {
    setFeedback({ msg, type });
    setTimeout(() => setFeedback({ msg: '', type: '' }), 4000);
  }

  return (
    <div className="page">
      <Navbar />
      <main className="main-content">
        <div className="page-header">
          <h2 className="page-title">Obrigações</h2>
          <button
            className={`btn btn-sm ${showForm ? 'btn-ghost' : 'btn-primary'}`}
            onClick={() => {
              setShowForm(!showForm);
              setForm(EMPTY_FORM);
            }}
          >
            {showForm ? '✕ Cancelar' : '+ Nova Obrigação'}
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
            <h3 className="form-title">Nova Obrigação</h3>
            <p className="form-hint">
              O dia de vencimento é usado para calcular o prazo das tarefas
              automaticamente. Deixe em branco se não houver vencimento fixo.
            </p>
            <form onSubmit={handleSubmit} className="form-grid">
              <div className="form-group">
                <label>Nome *</label>
                <input
                  type="text"
                  value={form.nome}
                  onChange={(e) =>
                    setForm((f) => ({ ...f, nome: e.target.value }))
                  }
                  placeholder="Ex: INSS, FGTS, DAS..."
                  required
                />
              </div>
              <div className="form-group">
                <label>
                  Dia de Vencimento{' '}
                  <span className="text-muted">(opcional, 1–31)</span>
                </label>
                <input
                  type="number"
                  min="1"
                  max="31"
                  value={form.dia_vencimento}
                  onChange={(e) =>
                    setForm((f) => ({ ...f, dia_vencimento: e.target.value }))
                  }
                  placeholder="Ex: 20"
                />
              </div>
              <div className="form-actions">
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={submitting}
                >
                  {submitting ? 'Criando...' : 'Criar Obrigação'}
                </button>
              </div>
            </form>
          </div>
        )}

        {loading ? (
          <div className="loading">Carregando obrigações...</div>
        ) : error ? (
          <div className="error-message">{error}</div>
        ) : obrigacoes.length === 0 ? (
          <div className="empty-state">
            <p>Nenhuma obrigação cadastrada.</p>
            <button
              className="btn btn-primary"
              onClick={() => setShowForm(true)}
            >
              Criar primeira obrigação
            </button>
          </div>
        ) : (
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Nome</th>
                  <th>Dia de Vencimento</th>
                  <th>Criada em</th>
                </tr>
              </thead>
              <tbody>
                {obrigacoes.map((ob) => (
                  <tr key={ob.id}>
                    <td className="font-medium">{ob.nome}</td>
                    <td>
                      {ob.dia_vencimento ? (
                        <span className="tipo-badge">Dia {ob.dia_vencimento}</span>
                      ) : (
                        <span className="text-muted">Sem vencimento fixo</span>
                      )}
                    </td>
                    <td className="text-muted">
                      {ob.criada_em
                        ? new Date(ob.criada_em).toLocaleDateString('pt-BR')
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

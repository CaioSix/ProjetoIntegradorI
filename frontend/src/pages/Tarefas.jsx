import { useState, useEffect, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import Navbar from '../components/Navbar';
import StatusBadge from '../components/StatusBadge';
import PrazoTag from '../components/PrazoTag';
import Modal from '../components/Modal';
import { api } from '../api/client';

const ACTION_TITLES = {
  concluir: 'Concluir Tarefa',
  dispensar: 'Dispensar Tarefa',
  reabrir: 'Reabrir Tarefa',
};

const ACTION_CONFIRM_LABELS = {
  concluir: 'Concluir',
  dispensar: 'Dispensar',
  reabrir: 'Reabrir',
};

export default function Tarefas() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [tarefas, setTarefas] = useState([]);
  const [empresas, setEmpresas] = useState([]);
  const [competencias, setCompetencias] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [count, setCount] = useState(0);
  const [page, setPage] = useState(1);

  const [modal, setModal] = useState({ open: false, tarefa: null, action: null });
  const [actionLoading, setActionLoading] = useState(false);
  const [feedback, setFeedback] = useState({ msg: '', type: '' });

  const statusFilter = searchParams.get('status') || '';
  const empresaFilter = searchParams.get('empresa') || '';
  const competenciaFilter = searchParams.get('competencia') || '';

  // Carrega dados auxiliares uma vez
  useEffect(() => {
    Promise.all([api.getEmpresas(), api.getCompetencias()])
      .then(([e, c]) => {
        setEmpresas(Array.isArray(e) ? e : e.results || []);
        setCompetencias(Array.isArray(c) ? c : c.results || []);
      })
      .catch(() => {});
  }, []);

  const fetchTarefas = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const data = await api.getTarefas({
        status: statusFilter || undefined,
        empresa: empresaFilter || undefined,
        competencia: competenciaFilter || undefined,
        page: page > 1 ? page : undefined,
      });
      setTarefas(data.results || []);
      setCount(data.count || 0);
    } catch {
      setError('Erro ao carregar tarefas. Verifique sua conexão.');
    } finally {
      setLoading(false);
    }
  }, [statusFilter, empresaFilter, competenciaFilter, page]);

  useEffect(() => {
    fetchTarefas();
  }, [fetchTarefas]);

  function setFilter(key, value) {
    const p = new URLSearchParams(searchParams);
    if (value) p.set(key, value);
    else p.delete(key);
    setSearchParams(p);
    setPage(1);
  }

  function clearFilters() {
    setSearchParams({});
    setPage(1);
  }

  function openModal(tarefa, action) {
    setModal({ open: true, tarefa, action });
  }

  async function executeAction() {
    const { tarefa, action } = modal;
    setActionLoading(true);
    try {
      if (action === 'concluir') await api.concluirTarefa(tarefa.id);
      else if (action === 'dispensar') await api.dispensarTarefa(tarefa.id);
      else if (action === 'reabrir') await api.reabrirTarefa(tarefa.id);

      setFeedback({ msg: `Tarefa ${action === 'concluir' ? 'concluída' : action === 'dispensar' ? 'dispensada' : 'reaberta'} com sucesso!`, type: 'success' });
      setModal({ open: false, tarefa: null, action: null });
      fetchTarefas();
    } catch (err) {
      const msg = err?.data?.message || 'Operação não permitida.';
      setFeedback({ msg: `Erro: ${msg}`, type: 'error' });
      setModal({ open: false, tarefa: null, action: null });
    } finally {
      setActionLoading(false);
      setTimeout(() => setFeedback({ msg: '', type: '' }), 4000);
    }
  }

  const totalPages = Math.ceil(count / 20);
  const hasFilters = statusFilter || empresaFilter || competenciaFilter;

  return (
    <div className="page">
      <Navbar />
      <main className="main-content">
        <h2 className="page-title">Tarefas</h2>

        {/* Filtros */}
        <div className="filters-bar">
          <select
            className="filter-select"
            value={statusFilter}
            onChange={(e) => setFilter('status', e.target.value)}
          >
            <option value="">Todos os status</option>
            <option value="PENDENTE">Pendente</option>
            <option value="CONCLUIDA">Concluída</option>
            <option value="DISPENSADA">Dispensada</option>
          </select>

          <select
            className="filter-select"
            value={empresaFilter}
            onChange={(e) => setFilter('empresa', e.target.value)}
          >
            <option value="">Todas as empresas</option>
            {empresas.map((emp) => (
              <option key={emp.id} value={emp.id}>
                {emp.nome}
              </option>
            ))}
          </select>

          <select
            className="filter-select"
            value={competenciaFilter}
            onChange={(e) => setFilter('competencia', e.target.value)}
          >
            <option value="">Todas as competências</option>
            {competencias.map((c) => (
              <option key={c.id} value={c.id}>
                {String(c.mes).padStart(2, '0')}/{c.ano}
              </option>
            ))}
          </select>

          {hasFilters && (
            <button className="btn btn-ghost btn-sm" onClick={clearFilters}>
              ✕ Limpar filtros
            </button>
          )}
        </div>

        {/* Feedback de ações */}
        {feedback.msg && (
          <div
            className={`feedback-message ${
              feedback.type === 'error' ? 'feedback-error' : 'feedback-success'
            }`}
          >
            {feedback.msg}
          </div>
        )}

        {/* Contagem */}
        {!loading && (
          <div className="results-info">
            {count} tarefa{count !== 1 ? 's' : ''} encontrada
            {count !== 1 ? 's' : ''}
          </div>
        )}

        {/* Tabela */}
        {loading ? (
          <div className="loading">Carregando tarefas...</div>
        ) : error ? (
          <div className="error-message">{error}</div>
        ) : tarefas.length === 0 ? (
          <div className="empty-state">
            {hasFilters
              ? 'Nenhuma tarefa encontrada com os filtros selecionados.'
              : 'Nenhuma tarefa cadastrada.'}
          </div>
        ) : (
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Empresa</th>
                  <th>Obrigação</th>
                  <th>Status</th>
                  <th>Prazo</th>
                  <th>Situação</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {tarefas.map((tarefa) => (
                  <tr key={tarefa.id}>
                    <td className="empresa-cell">{tarefa.empresa_nome}</td>
                    <td>{tarefa.obrigacao_nome}</td>
                    <td>
                      <StatusBadge status={tarefa.status} />
                    </td>
                    <td className="text-mono">
                      {tarefa.prazo_formatado || '—'}
                    </td>
                    <td>
                      <PrazoTag
                        diasPrazo={tarefa.dias_prazo}
                        statusPrazo={
                          tarefa.status !== 'PENDENTE'
                            ? tarefa.status === 'CONCLUIDA'
                              ? 'Concluída'
                              : 'Dispensada'
                            : tarefa.status_prazo
                        }
                      />
                    </td>
                    <td>
                      <TarefaActions
                        tarefa={tarefa}
                        onAction={openModal}
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Paginação */}
        {totalPages > 1 && (
          <div className="pagination">
            <button
              className="btn btn-ghost btn-sm"
              disabled={page === 1}
              onClick={() => setPage((p) => p - 1)}
            >
              ← Anterior
            </button>
            <span className="pagination-info">
              Página {page} de {totalPages}
            </span>
            <button
              className="btn btn-ghost btn-sm"
              disabled={page >= totalPages}
              onClick={() => setPage((p) => p + 1)}
            >
              Próxima →
            </button>
          </div>
        )}
      </main>

      <Modal
        isOpen={modal.open}
        title={modal.action ? ACTION_TITLES[modal.action] : ''}
        message={
          modal.tarefa
            ? `Confirma ${modal.action} a tarefa "${modal.tarefa.obrigacao_nome}" da empresa "${modal.tarefa.empresa_nome}"?`
            : ''
        }
        onConfirm={executeAction}
        onCancel={() => setModal({ open: false, tarefa: null, action: null })}
        loading={actionLoading}
        confirmLabel={modal.action ? ACTION_CONFIRM_LABELS[modal.action] : 'Confirmar'}
      />
    </div>
  );
}

function TarefaActions({ tarefa, onAction }) {
  if (tarefa.status === 'PENDENTE') {
    return (
      <div className="action-buttons">
        <button
          className="btn btn-success btn-xs"
          onClick={() => onAction(tarefa, 'concluir')}
        >
          Concluir
        </button>
        <button
          className="btn btn-muted btn-xs"
          onClick={() => onAction(tarefa, 'dispensar')}
        >
          Dispensar
        </button>
      </div>
    );
  }

  if (tarefa.status === 'CONCLUIDA') {
    return (
      <div className="action-buttons">
        <button
          className="btn btn-warning btn-xs"
          onClick={() => onAction(tarefa, 'reabrir')}
        >
          Reabrir
        </button>
      </div>
    );
  }

  // DISPENSADA — não pode reabrir
  return <span className="text-muted text-xs">—</span>;
}

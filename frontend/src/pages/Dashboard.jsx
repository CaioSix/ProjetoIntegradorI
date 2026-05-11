import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import StatusBadge from '../components/StatusBadge';
import { api } from '../api/client';

const TIPO_LABELS = {
  SN_COM_FOLHA: 'Simples Nacional c/ Folha',
  SN_SEM_FOLHA: 'Simples Nacional s/ Folha',
  MEI: 'MEI',
  LUCRO_PRESUMIDO: 'Lucro Presumido',
};

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    api
      .getDashboard()
      .then(setData)
      .catch(() => setError('Erro ao carregar dashboard.'))
      .finally(() => setLoading(false));
  }, []);

  if (loading)
    return (
      <div className="page">
        <Navbar />
        <div className="loading">Carregando...</div>
      </div>
    );

  if (error)
    return (
      <div className="page">
        <Navbar />
        <main className="main-content">
          <div className="error-message">{error}</div>
        </main>
      </div>
    );

  const empresas = data?.results || [];
  const totalPendentes = empresas.reduce((s, e) => s + e.pendentes, 0);
  const totalConcluidas = empresas.reduce((s, e) => s + e.concluidas, 0);
  const totalDispensadas = empresas.reduce(
    (s, e) => s + e.tarefas.filter((t) => t.status === 'DISPENSADA').length,
    0
  );

  return (
    <div className="page">
      <Navbar />
      <main className="main-content">
        <h2 className="page-title">Dashboard</h2>

        {/* Resumo geral */}
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-value">{empresas.length}</div>
            <div className="stat-label">Empresas</div>
          </div>
          <div className="stat-card">
            <div className="stat-value stat-warning">{totalPendentes}</div>
            <div className="stat-label">Pendentes</div>
          </div>
          <div className="stat-card">
            <div className="stat-value stat-success">{totalConcluidas}</div>
            <div className="stat-label">Concluídas</div>
          </div>
          <div className="stat-card">
            <div className="stat-value stat-muted">{totalDispensadas}</div>
            <div className="stat-label">Dispensadas</div>
          </div>
        </div>

        {/* Cards de empresa */}
        {empresas.length === 0 ? (
          <div className="empty-state">
            <p>Nenhuma empresa cadastrada.</p>
            <button
              className="btn btn-primary"
              onClick={() => navigate('/empresas')}
            >
              Cadastrar primeira empresa
            </button>
          </div>
        ) : (
          <div className="empresa-grid">
            {empresas.map((emp) => (
              <EmpresaCard
                key={emp.empresa_id}
                empresa={emp}
                onViewTasks={() =>
                  navigate(`/tarefas?empresa=${emp.empresa_id}`)
                }
              />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

function EmpresaCard({ empresa, onViewTasks }) {
  const dispensadas = empresa.tarefas.filter(
    (t) => t.status === 'DISPENSADA'
  ).length;

  const progresso =
    empresa.tarefas.length > 0
      ? Math.round((empresa.concluidas / empresa.tarefas.length) * 100)
      : 0;

  return (
    <div className="card empresa-card">
      <div className="empresa-card-header">
        <div className="empresa-card-info">
          <h3 className="empresa-nome">{empresa.empresa_nome}</h3>
          <span className="tipo-badge">
            {TIPO_LABELS[empresa.tipo] || empresa.tipo}
          </span>
        </div>
        <div className="empresa-counts">
          {empresa.pendentes > 0 && (
            <span className="count-badge count-pendente">
              {empresa.pendentes} pend.
            </span>
          )}
          {empresa.concluidas > 0 && (
            <span className="count-badge count-concluida">
              {empresa.concluidas} concl.
            </span>
          )}
          {dispensadas > 0 && (
            <span className="count-badge count-dispensada">
              {dispensadas} disp.
            </span>
          )}
        </div>
      </div>

      {/* Barra de progresso */}
      {empresa.tarefas.length > 0 && (
        <div className="progress-bar-container">
          <div
            className="progress-bar"
            style={{ width: `${progresso}%` }}
          />
          <span className="progress-label">{progresso}% concluído</span>
        </div>
      )}

      {/* Mini-lista de tarefas */}
      {empresa.tarefas.length > 0 && (
        <div className="tarefas-mini-list">
          {empresa.tarefas.slice(0, 4).map((t) => (
            <div key={t.id} className="tarefa-mini-item">
              <span className="tarefa-obrigacao">{t.obrigacao_nome}</span>
              <StatusBadge status={t.status} />
              {t.prazo && (
                <span className="tarefa-prazo-mini">{t.prazo}</span>
              )}
            </div>
          ))}
          {empresa.tarefas.length > 4 && (
            <div className="tarefa-mini-more">
              +{empresa.tarefas.length - 4} mais tarefas
            </div>
          )}
        </div>
      )}

      <button
        className="btn btn-ghost btn-sm btn-full"
        style={{ marginTop: 12 }}
        onClick={onViewTasks}
      >
        Ver todas as tarefas →
      </button>
    </div>
  );
}

const STATUS_MAP = {
  PENDENTE:   { label: 'Pendente',   cls: 'badge-warning' },
  CONCLUIDA:  { label: 'Concluída',  cls: 'badge-success' },
  DISPENSADA: { label: 'Dispensada', cls: 'badge-muted' },
};

export default function StatusBadge({ status }) {
  const { label, cls } = STATUS_MAP[status] || { label: status, cls: 'badge-muted' };
  return <span className={`badge ${cls}`}>{label}</span>;
}

export default function PrazoTag({ diasPrazo, statusPrazo }) {
  if (!statusPrazo || statusPrazo === 'Sem prazo') {
    return <span className="prazo-tag prazo-none">Sem prazo</span>;
  }

  let cls = 'prazo-future';
  if (diasPrazo < 0)       cls = 'prazo-overdue';
  else if (diasPrazo === 0) cls = 'prazo-today';
  else if (diasPrazo <= 7)  cls = 'prazo-soon';

  return <span className={`prazo-tag ${cls}`}>{statusPrazo}</span>;
}

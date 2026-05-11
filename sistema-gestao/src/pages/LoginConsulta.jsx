import PageContainer from "../components/PageContainer";

const S3_URL = "https://univespprojetor1.s3.us-east-1.amazonaws.com/backend_contabil.zip";
const S3_URL_DOC = "https://univespprojetor1.s3.us-east-1.amazonaws.com/manual_sistema.pdf";
const S3_URL_COMPOSE = "https://univespprojetor1.s3.us-east-1.amazonaws.com/docker-compose.yml";

const steps = [
  "Instale o Python (python.org) marcando \"Add Python to PATH\"",
  "Extraia o arquivo ZIP baixado",
  "Abra o terminal na pasta extraída e execute:",
];

const commands = `pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata core/fixtures/dados_iniciais.json
python manage.py createsuperuser
python manage.py runserver`;

export default function LoginConsulta() {
  return (
    <PageContainer title="Sistema de Controle de Tarefas Contábeis">

      {/* ── Opção 1: Docker (recomendado) ── */}
      <div style={styles.sectionHeader}>
        {/* <span style={styles.sectionBadge}>Recomendado</span> */}
        {/* <p style={styles.sectionTitle}>Rodar com Docker</p> */}
      </div>
      {/* <p style={styles.description}>
        Não precisa instalar nada além do Docker.
      </p> */}

      <a href={S3_URL_COMPOSE} download="docker-compose.yml" style={styles.downloadBtn}>
        Baixar docker-compose.yml
      </a>

      <div style={styles.instructions}>
        <p style={styles.instructionsTitle}>Como usar:</p>
        <p style={styles.step}>
          <span style={styles.stepNumber}>1.</span> Instale o{" "}
          <span style={styles.highlight}>Docker Desktop</span> em{" "}
          <span style={styles.highlight}>docker.com/get-started</span>
        </p>
        <p style={styles.step}>
          <span style={styles.stepNumber}>2.</span> Abra o terminal na pasta onde salvou o arquivo e execute:
        </p>
        <pre style={styles.code}>docker compose up</pre>
        <p style={styles.step}>
          <span style={styles.stepNumber}>3.</span> Acesse{" "}
          <span style={styles.highlight}>http://localhost:3000</span> no navegador
        </p>
      </div>

      {/* ── Divisor ── */}
      {/* <div style={styles.divider}>
        <span style={styles.dividerText}>ou</span>
      </div> */}

      {/* ── Opção 2: Manual ── */}
      {/* <p style={styles.sectionTitle}>Rodar manualmente (Python)</p>
      <p style={styles.description}>
        Baixe o sistema abaixo e rode localmente na sua máquina.
      </p> */}

      {/* <a href={S3_URL} download style={styles.downloadBtn}>
        Baixar Sistema (.zip)
      </a>

      <a href={S3_URL_DOC} download style={styles.downloadBtn}>
        Baixar Documentação
      </a>

      <div style={styles.instructions}>
        <p style={styles.instructionsTitle}>Como instalar:</p>
        {steps.map((step, i) => (
          <p key={i} style={styles.step}>
            <span style={styles.stepNumber}>{i + 1}.</span> {step}
          </p>
        ))}
        <pre style={styles.code}>{commands}</pre>
        <p style={styles.step}>
          <span style={styles.stepNumber}>4.</span> Acesse{" "}
          <span style={styles.highlight}>http://localhost:8000/api/docs/</span> no navegador
        </p>
      </div> */}
    </PageContainer>
  );
}

const styles = {
  sectionHeader: {
    width: "100%",
    display: "flex",
    alignItems: "center",
    gap: 8,
    marginBottom: 4,
  },
  sectionBadge: {
    background: "#166534",
    color: "#86efac",
    fontSize: 10,
    fontWeight: 700,
    padding: "2px 7px",
    borderRadius: 4,
    textTransform: "uppercase",
    letterSpacing: "0.05em",
  },
  sectionTitle: {
    color: "#f9fafb",
    fontWeight: 700,
    fontSize: 13,
    margin: 0,
  },
  divider: {
    width: "100%",
    display: "flex",
    alignItems: "center",
    gap: 10,
    margin: "8px 0",
  },
  dividerText: {
    color: "#4b5563",
    fontSize: 12,
    whiteSpace: "nowrap",
    padding: "0 8px",
    background: "#111827",
    position: "relative",
    zIndex: 1,
    alignSelf: "center",
    margin: "0 auto",
    border: "1px solid #1f2937",
    borderRadius: 20,
  },
  description: {
    color: "#9ca3af",
    textAlign: "center",
    margin: "0 0 20px",
    fontSize: 14,
    width: "100%",
  },
  downloadBtn: {
    display: "block",
    width: "100%",
    padding: "12px",
    borderRadius: 10,
    background: "#2563eb",
    color: "white",
    fontWeight: 700,
    fontSize: 15,
    textAlign: "center",
    textDecoration: "none",
    boxSizing: "border-box",
  },
  instructions: {
    width: "100%",
    marginTop: 20,
    padding: "16px",
    borderRadius: 8,
    background: "#1f2937",
    boxSizing: "border-box",
  },
  instructionsTitle: {
    color: "#f9fafb",
    fontWeight: 700,
    margin: "0 0 12px",
    fontSize: 13,
  },
  step: {
    color: "#d1d5db",
    fontSize: 12,
    margin: "6px 0",
    lineHeight: 1.5,
    wordBreak: "break-word",
  },
  stepNumber: {
    color: "#2563eb",
    fontWeight: 700,
  },
  code: {
    background: "#111827",
    color: "#86efac",
    fontSize: 11,
    padding: "10px 12px",
    borderRadius: 6,
    overflowX: "auto",
    margin: "8px 0",
    fontFamily: "monospace",
    lineHeight: 1.6,
    whiteSpace: "pre",
    maxWidth: "100%",
    display: "block",
  },
  highlight: {
    color: "#60a5fa",
    fontFamily: "monospace",
    wordBreak: "break-all",
  },
};

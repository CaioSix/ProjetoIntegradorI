export default function Modal({ open, title, message, onClose }) {
  if (!open) return null;

  return (
    <div style={styles.backdrop} onClick={onClose}>
      <div style={styles.modal} onClick={(e) => e.stopPropagation()}>
        <h2 style={styles.title}>{title}</h2>
        <p style={styles.message}>{message}</p>
        <button style={styles.closeBtn} onClick={onClose}>
          Fechar
        </button>
      </div>
    </div>
  );
}

const styles = {
  backdrop: {
    position: "fixed",
    inset: 0,
    background: "rgba(0,0,0,0.6)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: 16,
    zIndex: 999,
  },
  modal: {
    width: "100%",
    maxWidth: 460,
    background: "#111827",
    border: "1px solid #1f2937",
    borderRadius: 12,
    padding: 18,
    color: "#e5e7eb",
  },
  title: {
    margin: 0,
    marginBottom: 8,
    fontSize: 18,
    fontWeight: 800,
  },
  message: {
    marginTop: 0,
    marginBottom: 14,
    color: "#cbd5e1",
    lineHeight: 1.5,
  },
  closeBtn: {
    width: "100%",
    padding: "10px 12px",
    borderRadius: 10,
    border: "none",
    cursor: "pointer",
    background: "#334155",
    color: "white",
    fontWeight: 700,
  },
};
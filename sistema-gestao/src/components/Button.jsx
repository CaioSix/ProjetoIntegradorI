export default function Button({ children, onClick, type = "button" }) {
  return (
    <button type={type} onClick={onClick} style={styles.btn}>
      {children}
    </button>
  );
}

const styles = {
  btn: {
    width: "100%",
    padding: "10px 12px",
    borderRadius: 10,
    border: "none",
    cursor: "pointer",
    background: "#2563eb",
    color: "white",
    fontWeight: 700,
    fontSize: 14,
    marginTop: 8,
  },
};
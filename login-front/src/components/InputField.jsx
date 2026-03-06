export default function InputField({
  label,
  type = "text",
  value,
  onChange,
  placeholder,
}) {
  return (
    <div style={styles.group}>
      <label style={styles.label}>{label}</label>
      <input
        style={styles.input}
        type={type}
        value={value}
        placeholder={placeholder}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}

const styles = {
  group: {
    display: "flex",
    flexDirection: "column",
    gap: 8,
    marginBottom: 12,
  },
  label: {
    fontSize: 14,
    color: "#cbd5e1",
  },
  input: {
    padding: "10px 12px",
    borderRadius: 10,
    border: "1px solid #402e53",
    background: "#0b1220",
    color: "#e5e7eb",
    outline: "none",
  },
};
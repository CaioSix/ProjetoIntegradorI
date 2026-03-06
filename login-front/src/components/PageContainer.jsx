import univesp from "../assets/univesp.png"

export default function PageContainer({ title, children }) {
  return (
    <div style={styles.wrapper}>
      <div style={styles.card}>
        <h1 style={styles.title}>{title}</h1>

        <div style={styles.form}>
          {children}
        </div>
      </div>

      <img
        src={univesp}
        alt="decoracao"
        style={styles.image}
      />
    </div>
  );
}

const styles = {
  wrapper: {
    width: "100vw",
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "#8d2a2a",
    position: "relative"
  },

  card: {
    width: "420px",
    padding: "30px",
    borderRadius: "12px",
    background: "#111827",
    boxShadow: "0 10px 40px rgba(0,0,0,0.2)",
  },

  title: {
    textAlign: "center",
    color: "white",
    marginBottom: "25px"
  },

  form: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: "12px",
  },

  image: {
    position: "absolute",
    bottom: "20px",
    right: "20px",
    width: "250px",
    opacity: 0.9
  }
};
import "../index.css";
import univesp from "../assets/univesp.png";

export default function PageContainer({ title, children }) {
  return (
    <div className="page-wrapper">
      <div className="page-card">
        <h1 className="page-title">{title}</h1>
        <div className="page-form">
          {children}
        </div>
      </div>

      <img
        src={univesp}
        alt="logo univesp"
        className="page-logo"
      />
    </div>
  );
}

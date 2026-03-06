import { useState } from "react";
import PageContainer from "../components/PageContainer";
import InputField from "../components/InputField";
import Button from "../components/Button";
import Modal from "../components/Modal";


export default function LoginConsulta() {
  const [cpf, setCpf] = useState("");
  const [senha, setSenha] = useState("");
  const [dataInicio, setDataInicio] = useState("");
  const [dataFim, setDataFim] = useState("");

  const [modalOpen, setModalOpen] = useState(false);

  function handleSubmit() {
    const payload = {
      cpf,
      senha,
      dataInicio,
      dataFim,
    };

    console.log("Payload preparado:", payload);

    setModalOpen(true);
  }

  return (
    <PageContainer title="Consulta / Login">
      <InputField
        label="CPF"
        value={cpf}
        onChange={setCpf}
        placeholder="Digite seu CPF (somente números)"
      />

      <InputField
        label="Senha"
        type="password"
        value={senha}
        onChange={setSenha}
        placeholder="Digite sua senha"
      />

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
        <InputField
          label="Data início"
          type="date"
          value={dataInicio}
          onChange={setDataInicio}
        />
        <InputField
          label="Data fim"
          type="date"
          value={dataFim}
          onChange={setDataFim}
        />
      </div>

      <Button onClick={handleSubmit}>Enviar</Button>

      <Modal
        open={modalOpen}
        title="Em processamento aguarde..."        
        onClose={() => setModalOpen(false)}
      />
    </PageContainer>
  );
}
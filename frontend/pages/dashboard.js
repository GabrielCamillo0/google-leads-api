import { useEffect, useState } from "react";
import axios from "axios";

export default function Dashboard() {
  const [apiKey, setApiKey] = useState("");

  useEffect(() => {
    setApiKey(localStorage.getItem("api_key") || "Nenhuma chave disponível");
  }, []);

  return (
    <div className="p-10">
      <h1 className="text-2xl">Painel do Usuário</h1>
      <p className="mt-4">Sua chave de API: <b>{apiKey}</b></p>
    </div>
  );
}

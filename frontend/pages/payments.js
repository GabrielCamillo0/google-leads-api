import { useState } from "react";
import axios from "axios";

export default function Payments() {
  const [loading, setLoading] = useState(false);

  async function handleCheckout() {
    setLoading(true);
    const username = localStorage.getItem("username");

    try {
      const response = await axios.post("http://localhost:8000/create-checkout-session", {
        plan: "premium",
        username
      });

      window.location.href = response.data.url; // Redireciona para Stripe
    } catch (error) {
      alert("Erro ao iniciar pagamento");
    }
  }

  return (
    <div className="p-10">
      <h1 className="text-2xl">Plano Premium</h1>
      <p>Acesso ilimitado por apenas R$19,90</p>
      <button onClick={handleCheckout} disabled={loading} className="bg-blue-500 text-white px-4 py-2 mt-4">
        {loading ? "Processando..." : "Assinar Plano Premium"}
      </button>
    </div>
  );
}

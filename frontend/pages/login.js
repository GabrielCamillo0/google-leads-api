import { useState } from "react";
import axios from "axios";
import { useRouter } from "next/router";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  async function handleLogin() {
    try {
      const response = await axios.post("http://localhost:8000/login", { username, password });
      localStorage.setItem("api_key", response.data.api_key);
      router.push("/dashboard");
    } catch (error) {
      alert("Erro ao fazer login!");
    }
  }

  return (
    <div className="p-10 text-center">
      <h1 className="text-2xl">Login</h1>
      <input className="border p-2 mt-2" placeholder="Usuário" value={username} onChange={(e) => setUsername(e.target.value)} />
      <input className="border p-2 mt-2" type="password" placeholder="Senha" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button className="bg-blue-500 text-white p-2 mt-4" onClick={handleLogin}>Entrar</button>
    </div>
  );
}

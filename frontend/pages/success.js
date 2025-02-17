import { useEffect } from "react";
import { useRouter } from "next/router";

export default function Success() {
  const router = useRouter();

  useEffect(() => {
    setTimeout(() => {
      router.push("/dashboard");
    }, 3000);
  }, []);

  return (
    <div className="p-10 text-center">
      <h1 className="text-2xl text-green-500">Pagamento Confirmado! ✅</h1>
      <p>Redirecionando para o painel...</p>
    </div>
  );
}

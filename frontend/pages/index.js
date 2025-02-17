import Link from "next/link";

export default function Home() {
  return (
    <div className="p-10 text-center">
      <h1 className="text-3xl font-bold">Google Leads Scraper</h1>
      <p className="mt-4">Encontre leads qualificados para seu negócio</p>
      <Link href="/login" className="mt-6 bg-blue-500 text-white px-4 py-2 rounded">Acessar</Link>
    </div>
  );
}

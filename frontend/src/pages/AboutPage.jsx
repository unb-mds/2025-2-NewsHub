import React from 'react';
import { Link } from 'react-router-dom'; // Importa o componente de Link

function AboutPage() {
  return (
    <div className="bg-gray-900 text-white min-h-screen flex flex-col items-center justify-center text-center p-4">
      <h1 className="text-5xl font-bold text-cyan-400">Sobre o Projeto NewsHub</h1>
      <p className="mt-4 max-w-2xl text-gray-300">
        Este é um agregador de notícias criado para a disciplina de Métodos de Desenvolvimento de Software.
        A aplicação utiliza React no frontend e Flask no backend, tudo orquestrado com Docker.
      </p>
      <Link to="/" className="mt-8">
        <button className="px-6 py-3 bg-purple-600 text-white font-semibold rounded-lg shadow-md hover:bg-purple-700 transition-colors">
          Voltar para a Home
        </button>
      </Link>
    </div>
  );
}

export default AboutPage;
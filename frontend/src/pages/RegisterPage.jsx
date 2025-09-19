import React, { useState } from 'react';
import { Link } from 'react-router-dom';

function RegisterPage() {
  // 1. Estados para armazenar os dados do formulário
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [birthdate, setBirthdate] = useState(''); // <-- NOVO ESTADO ADICIONADO

  // Estados para feedback da API
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  // 2. Função que lida com o envio do formulário
  const handleSubmit = async (event) => {
    event.preventDefault();

    setMessage('');
    setError('');

    // 3. Monta o corpo da requisição com os dados do estado
    const userData = {
      full_name: fullName,
      email: email,
      password: password,
      birthdate: birthdate, // <-- NOVO CAMPO ADICIONADO
    };

    try {
      // Pega a URL base da variável de ambiente
      const apiUrl = import.meta.env.VITE_API_BASE_URL;

      // 4. Faz a chamada da API
      const response = await fetch(`${apiUrl}/users/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      const data = await response.json();

      // 5. Lida com a resposta
      if (response.ok) {
        setMessage(`Usuário ${data.full_name} registrado com sucesso!`);
      } else {
        setError(data.error || 'Ocorreu um erro desconhecido.');
      }
    } catch (err) {
      setError('Não foi possível conectar ao servidor. Tente novamente mais tarde.');
    }
  };

  return (
    <div className="bg-gray-900 text-white min-h-screen flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-md bg-gray-800 rounded-lg shadow-xl p-8">
        <h1 className="text-3xl font-bold text-center text-cyan-400 mb-6">Criar Conta</h1>

        <form onSubmit={handleSubmit}>
          {/* Campo Nome Completo */}
          <div className="mb-4">
            <label className="block text-gray-300 mb-2" htmlFor="fullName">Nome Completo</label>
            <input
              id="fullName"
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              className="w-full px-4 py-2 bg-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              required
            />
          </div>

          {/* Campo Email */}
          <div className="mb-4">
            <label className="block text-gray-300 mb-2" htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2 bg-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              required
            />
          </div>

          {/* NOVO CAMPO DE DATA DE NASCIMENTO */}
          <div className="mb-4">
            <label className="block text-gray-300 mb-2" htmlFor="birthdate">Data de Nascimento</label>
            <input
              id="birthdate"
              type="date" // O tipo "date" abre um seletor de data no navegador
              value={birthdate}
              onChange={(e) => setBirthdate(e.target.value)}
              className="w-full px-4 py-2 bg-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
          </div>

          {/* Campo Senha */}
          <div className="mb-6">
            <label className="block text-gray-300 mb-2" htmlFor="password">Senha</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 bg-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              required
            />
          </div>
          <button type="submit" className="w-full py-2 bg-purple-600 rounded-md font-semibold hover:bg-purple-700 transition-colors">
            Registrar
          </button>
        </form>

        {message && <p className="mt-4 text-center text-green-400">{message}</p>}
        {error && <p className="mt-4 text-center text-red-400">{error}</p>}

        <p className="text-center text-gray-400 mt-6">
          <Link to="/" className="hover:text-cyan-400">Voltar para a Home</Link>
        </p>
      </div>
    </div>
  );
}

export default RegisterPage;
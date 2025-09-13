import React, { useState } from "react";
import { Link } from "react-router-dom";

function RegisterPage() {
  // 1. Estados para armazenar os dados do formulário
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState(""); // Estado adicionado para confirmação de senha
  const [birthdate, setBirthdate] = useState("");

  // Estados para feedback da API e validação
  const [message, setMessage] = useState("");
  const [errors, setErrors] = useState({}); // Mudança de "error" para "errors" para lidar com múltiplos campos

  // 2. Função de validação do formulário
  const validateForm = () => {
    const newErrors = {};

    if (!fullName.trim()) {
      newErrors.fullName = "O nome é obrigatório.";
    }

    if (!email.trim() || !/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = "O email é inválido.";
    }

    if (password.length < 6) {
      newErrors.password = "A senha deve ter no mínimo 6 caracteres.";
    }

    if (password !== confirmPassword) {
      newErrors.confirmPassword = "As senhas não coincidem.";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // 3. Função que lida com o envio do formulário
  const handleSubmit = async (event) => {
    event.preventDefault();

    // Limpa mensagens anteriores
    setMessage("");
    setErrors({});

    // Chama a função de validação
    if (!validateForm()) {
      return; // Se a validação falhar, para o processo de envio
    }

    // Monta o corpo da requisição com os dados do estado
    const userData = {
      full_name: fullName,
      email: email,
      password: password,
      birthdate: birthdate,
    };

    try {
      // Pega a URL base da variável de ambiente
      const apiUrl = import.meta.env.VITE_API_BASE_URL;

      // Faz a chamada da API
      const response = await fetch(`${apiUrl}/users/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });

      const data = await response.json();

      // Lida com a resposta
      if (response.ok) {
        // A API deve retornar um objeto com a propriedade `full_name`
        // Exemplo de resposta da API: { "full_name": "Nome Completo do Usuário", "email": "..." }
        setMessage(`Usuário ${data.full_name} cadastrado com sucesso!`);
      } else {
        setMessage(data.error || "Ocorreu um erro desconhecido.");
      }
    } catch (err) {
      setMessage(
        "Não foi possível conectar ao servidor. Tente novamente mais tarde."
      );
    }
  };

  return (
    <div className="flex min-h-screen">
      {/* Lado esquerdo (formulário) */}
      <div className="flex w-1/2 flex-col items-center justify-start bg-white p-8">
        {/* Container para o "Synapse" - alinhado à esquerda */}
        <div className="w-full max-w-sm text-left">
          <h1 className="mb-10 text-64xl font-bold text-black font-rajdhani">
            Synapse
          </h1>
        </div>
        <div className="w-full max-w-sm">
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Campo Email */}
            <div>
              <label
                className="block text-sm font-medium text-gray-900 font-montserrat"
                htmlFor="email"
              >
                Email
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Digite seu e-mail..."
                className="mt-1 block w-full border border-gray-300 p-2 shadow-sm transition-colors duration-300 ease-in-out
                focus:border-black focus:ring-black
                hover:border-black"
                required
              />
              {errors.email && (
                <p className="mt-1 text-sm text-red-600">{errors.email}</p>
              )}
            </div>
            {/* Campo Nome Completo */}
            <div>
              <label
                className="mt-6 block text-sm font-medium text-gray-900 font-montserrat"
                htmlFor="fullName"
              >
                Nome Completo
              </label>
              <input
                id="fullName"
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Digite seu nome..."
                className="mt-1 block w-full border border-gray-300 p-2 shadow-sm transition-colors duration-300 ease-in-out
                focus:border-black focus:ring-black
                hover:border-black"
                required
              />
              {errors.fullName && (
                <p className="mt-1 text-sm text-red-600">{errors.fullName}</p>
              )}
            </div>
            {/* NOVO CAMPO DE DATA DE NASCIMENTO */}
            <div>
              <label
                className="mt-6 block text-sm font-medium text-gray-900 font-montserrat"
                htmlFor="birthdate"
              >
                Data de Nascimento
              </label>
              <input
                id="birthdate"
                type="date"
                value={birthdate}
                onChange={(e) => setBirthdate(e.target.value)}
                className="mt-1 block w-full border border-gray-300 p-2 shadow-sm transition-colors duration-300 ease-in-out
                focus:border-black focus:ring-black
                hover:border-black"
              />
            </div>
            {/* Campo de Senha */}
            <div>
              <label
                className="mt-6 block text-sm font-medium text-gray-900 font-montserrat"
                htmlFor="password"
              >
                Senha
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Sua senha..."
                className="mt-1 block w-full border border-gray-300 p-2 shadow-sm transition-colors duration-300 ease-in-out
                focus:border-black focus:ring-black
                hover:border-black"
                required
              />
              {errors.password && (
                <p className="mt-1 text-sm text-red-600">{errors.password}</p>
              )}
            </div>

            {/* Campo Confirmação de Senha */}
            <div>
              <label
                className="mt-6 block text-sm font-medium text-gray-900 font-montserrat"
                htmlFor="confirmPassword"
              >
                Confirme a Senha
              </label>
              <input
                id="confirmPassword"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Confirme sua senha..."
                className="mt-1 block w-full border border-gray-300 p-2 shadow-sm transition-colors duration-300 ease-in-out
                focus:border-black focus:ring-black
                hover:border-black"
                required
              />
              {errors.confirmPassword && (
                <p className="mt-1 text-sm text-red-600">
                  {errors.confirmPassword}
                </p>
              )}
            </div>
            <button
              type="submit"
              className="mt-8 w-full rounded-md bg-black py-3 px-5 text-white hover:bg-gray-900"
            >
              Cadastrar
            </button>
          </form>

          {message && (
            <p className="mt-4 text-center text-green-600">{message}</p>
          )}
          {Object.keys(errors).length > 0 && !message && (
            <p className="mt-4 text-center text-red-600">
              Por favor, corrija os erros no formulário.
            </p>
          )}

          <p className="mt-4 text-center text-sm text-black">
            Já tem uma conta?{" "}
            <Link to="/" className="font-medium text-blue-600 hover:underline">
              Login aqui
            </Link>
          </p>
        </div>
      </div>

      {/* Lado direito (design system) */}
      <div className="flex w-1/2 flex-col items-left justify-center bg-black p-8 text-white">
        <h2 className="ml-8 text-160xl font-light leading-none font-rajdhani">
          Know
        </h2>
        <h2 className="ml-8 text-160xl font-light leading-none font-rajdhani">
          Your
        </h2>
        <h2 className="ml-8 text-160xl font-light leading-none font-rajdhani">
          World,
        </h2>
        <h2 className="ml-8 text-160xl font-bold leading-none font-rajdhani">
          Faster.
        </h2>
      </div>
    </div>
  );
}

export default RegisterPage;

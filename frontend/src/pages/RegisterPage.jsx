import React, { useState } from "react";
import { Link } from "react-router-dom";

function RegisterPage() {
  // 1. Estados para armazenar os dados do formulário
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [birthdate, setBirthdate] = useState("");

  // Estados para feedback da API e validação
  const [message, setMessage] = useState("");
  // Estado para controlar a cor da mensagem
  const [isError, setIsError] = useState(false);
  const [errors, setErrors] = useState({});

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

    // Limpa mensagens e estados anteriores
    setMessage("");
    setIsError(false); // Reinicia o estado de erro
    setErrors({});

    if (!validateForm()) {
      return;
    }

    const userData = {
      full_name: fullName,
      email: email,
      password: password,
      birthdate: birthdate,
    };

    try {
      const apiUrl = import.meta.env.VITE_API_BASE_URL;

      const response = await fetch(`${apiUrl}/users/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });

      const data = await response.json();

      if (response.ok) {
        // Se a resposta for OK, define a mensagem e isError como false
        setMessage(`Usuário cadastrado com sucesso!`);
        setIsError(false);
      } else {
        // Se houver um erro, define a mensagem e isError como true
        setMessage(data.error || "Ocorreu um erro desconhecido.");
        setIsError(true);
      }
    } catch (err) {
      // Em caso de falha de conexão, define isError como true
      setMessage(
        "Não foi possível conectar ao servidor. Tente novamente mais tarde."
      );
      setIsError(true);
    }
  };

  return (
    <div className="min-h-screen lg:flex bg-[#f5f5f5]">
      {/* Lado esquerdo (formulário) */}
      <div
        className="flex w-full lg:w-1/2 flex-col
      items-center justify-center lg:justify-start
      bg-[#f5f5f5] p-8"
      >
        {/* Container para o "Synapse" - alinhado à esquerda */}
        <div className="w-full max-w-lg text-left">
          <h1 className="mb-10 text-64xl font-bold text-black font-rajdhani">
            Synapse
          </h1>
        </div>
        <div className="w-full max-w-lg">
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Campo Email */}
            <div className="relative">
              <div className="absolute inset-y-0 left-2 top-6 flex items-center pointer-events-none">
                <img
                  src="./src/icons/envelope-regular-full.svg"
                  alt="ícone email"
                  class="h-5 w-5"
                />
              </div>
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
                className="mt-1 block w-full text-[#989898] valid:text-[#111] border border-gray-300 py-2
                 px-8 shadow-sm transition-colors duration-200 ease-in-out
                focus:border-black focus:ring-black
                hover:border-black"
                required
              />
              {errors.email && (
                <p className="mt-1 text-sm text-red-600">{errors.email}</p>
              )}
            </div>
            {/* Campo Nome Completo */}
            <div className="relative">
              <div className="absolute inset-y-0 left-2 top-6 flex items-center pointer-events-none">
                <img
                  src="./src/icons/user-regular-full.svg"
                  alt="ícone user"
                  class="h-5 w-5"
                />
              </div>
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
                className="mt-1 block text-[#989898] valid:text-[#111] w-full border border-gray-300 py-2
                 px-8 shadow-sm transition-colors duration-200 ease-in-out
                focus:border-black focus:ring-black
                hover:border-black"
                required
              />
              {errors.fullName && (
                <p className="mt-1 text-sm text-red-600">{errors.fullName}</p>
              )}
            </div>
            {/* Campo data de nascimento*/}
            <div className="relative">
              <div className="absolute inset-y-0 left-2 top-6 flex items-center pointer-events-none">
                <img
                  src="./src/icons/calendar-regular-full.svg"
                  alt="ícone calendario"
                  class="h-5 w-5"
                />
              </div>
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
                required
                className="mt-1 text-[#989898] valid:text-[#111] block w-full border border-gray-300 py-2
                 px-8 shadow-sm transition-colors duration-200 ease-in-out
                focus:border-black focus:ring-black
                hover:border-black  [&::-webkit-calendar-picker-indicator]:hidden"
              />
            </div>
            {/* Campo de Senha */}
            <div className="relative">
              <div className="absolute inset-y-0 left-2 top-6 flex items-center pointer-events-none">
                <img
                  src="./src/icons/lock-regular-full.svg"
                  alt="ícone user"
                  class="h-5 w-5"
                />
              </div>
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
                className="mt-1 block w-full border border-gray-300 py-2
                 px-8 shadow-sm transition-colors duration-200 ease-in-out
                focus:border-black focus:ring-black
                hover:border-black"
                required
              />
              {errors.password && (
                <p className="mt-1 text-sm text-red-600">{errors.password}</p>
              )}
            </div>

            {/* Campo Confirmação de Senha */}
            <div className="relative">
              <div className="absolute inset-y-0 left-2 top-6 flex items-center pointer-events-none">
                <img
                  src="./src/icons/lock-regular-full.svg"
                  alt="ícone user"
                  class="h-5 w-5"
                />
              </div>
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
                className="mt-1 block w-full border border-gray-300 py-2
                 px-8 shadow-sm transition-colors duration-200 ease-in-out
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
            // Classe da cor depende se é erro ou sucesso
            <p
              className={`mt-4 text-center text-sm ${
                isError ? "text-red-600" : "text-green-600"
              }`}
            >
              {message}
            </p>
          )}
          {Object.keys(errors).length > 0 && !message && (
            <p className="mt-4 text-center text-red-600">
              Por favor, corrija os erros no formulário.
            </p>
          )}

          <p className="mt-4 text-center text-sm text-black border-t border-[#111] pt-3">
            Já tem uma conta?{" "}
            <Link
              to="/"
              className="font-medium text-[#111] no-underline hover:underline hover:bg-[#1c1c1c] hover:text-[#fff] pt-0.2 px-0.5"
            >
              Login aqui
            </Link>
          </p>
        </div>
      </div>

      {/* Lado direito da tela*/}
      <div className="hidden lg:flex w-full lg:w-1/2 flex-col items-left justify-center bg-black p-4 sm:p-8 text-white">
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

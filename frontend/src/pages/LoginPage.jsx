import React, { useState } from "react";
import { Link } from "react-router-dom";

function LoginPage() {
  // 1. Estados para armazenar os dados do formulário
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // Estados para feedback da API e validação
  const [message, setMessage] = useState("");
  const [isError, setIsError] = useState(false);
  const [errors, setErrors] = useState({});

  // 2. Função de validação do formulário
  const validateForm = () => {
    const newErrors = {};

    if (!email.trim() || !/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = "O email é inválido.";
    }
    if (!password.trim()) {
      newErrors.password = "Por favor, insira sua senha.";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // 3. Função que lida com o envio do formulário
  const handleSubmit = async (event) => {
    event.preventDefault();

    // Limpa mensagens anteriores
    setMessage("");
    setIsError(false); // Reinicia o estado de erro
    setErrors({});

    // Chama a função de validação
    if (!validateForm()) {
      return; // Se a validação falhar, para o processo de envio
    }

    // Monta o corpo da requisição com os dados do estado
    const userData = {
      email: email,
      password: password,
    };

    try {
      // Pega a URL base da variável de ambiente
      const apiUrl = import.meta.env.VITE_API_BASE_URL;

      // Faz a chamada da API
      const response = await fetch(`${apiUrl}/users/login`, {
        // Alteração para a rota de login
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });

      const data = await response.json();

      // Lida com a resposta
      if (response.ok) {
        // Exemplo de resposta da API: { "token": "...", "user": { "full_name": "...", "email": "..." } }
        setMessage(`Login bem-sucedido! Bem-vindo, ${data.user.full_name}.`);
        setIsError(false);
        // Aqui você pode redirecionar o usuário ou salvar o token
      } else {
        setMessage(data.error || "Ocorreu um erro desconhecido.");
        setIsError(true);
      }
    } catch (err) {
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
        className="
      flex w-full lg:w-1/2 flex-col
      items-center justify-center lg:justify-start
      bg-[#f5f5f5] p-8"
      >
        {/* Container para o "Synapse" - alinhado à esquerda */}
        <div className="mt-12 w-full max-w-lg text-left">
          <h1 className="mb-10 text-64xl font-bold text-black font-rajdhani">
            Synapse.
          </h1>
        </div>
        <div className="w-full max-w-lg">
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Campo Email */}
            <div className="relative">
              <label
                className="block text-sm font-medium text-gray-900 font-montserrat"
                htmlFor="email"
              >
                Email
                <div className="relative mt-1">
                  <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    <img
                      src="./src/icons/envelope-regular-full.svg"
                      alt="ícone email"
                      className="h-5 w-5"
                    />
                  </div>
                  <input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder=" Digite seu e-mail..."
                    className="mt-1 block w-full text-[#989898] valid:text-[#111] border border-gray-300 py-2
                 px-8 shadow-sm transition-colors duration-200 ease-in-out
                focus:border-black focus:ring-black
                hover:border-black"
                    required
                  />
                </div>
              </label>
              {errors.email && (
                <p className="mt-1 text-sm text-red-600">{errors.email}</p>
              )}
            </div>
            {/* Campo de Senha */}
            <div className="relative">
              <label
                className="mt-6 block text-sm font-medium text-gray-900 font-montserrat"
                htmlFor="password"
              >
                Senha
                <div className="relative mt-1">
                  <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    <img
                      src="./src/icons/lock-regular-full.svg"
                      alt="ícone user"
                      class="h-5 w-5"
                    />
                  </div>
                  <input
                    id="password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder=" Sua senha..."
                    className="mt-1 block w-full border border-gray-300 py-2
                  px-8 shadow-sm transition-colors duration-200 ease-in-out
                  focus:border-black focus:ring-black
                  hover:border-black"
                    required
                  />
                </div>
              </label>
              {errors.password && (
                <p className="mt-1 text-sm text-red-600">{errors.password}</p>
              )}
            </div>

            {/* Links Adicionais */}
            <div className="flex justify-between items-center text-sm font-montserrat">
              <div className="flex items-center">
                <input
                  id="remember-me"
                  type="checkbox"
                  className="h-4 w-4 text-black border-gray-300 rounded py-2
                 px-7"
                />
                <label
                  htmlFor="remember-me"
                  className="ml-2 block text-gray-900 pt-0.2"
                >
                  Lembre de mim
                </label>
              </div>
              <a
                href="#"
                className="font-medium text-[#111] no-underline hover:underline hover:bg-[#1c1c1c] hover:text-[#fff] pt-0.2 px-0.5"
              >
                Esqueci minha senha
              </a>
            </div>

            <button
              type="submit"
              className="mt-8 w-full rounded-md bg-black py-3 px-5 text-white hover:bg-gray-900"
            >
              Entrar
            </button>
          </form>

          {message && (
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
            Não tem uma conta?{" "}
            <Link
              to="/registrar"
              className="font-medium text-[#111] no-underline hover:underline hover:bg-[#1c1c1c] hover:text-[#fff] pt-0.2 px-0.5"
            >
              Cadastre-se aqui
            </Link>
          </p>
        </div>
      </div>

      {/* Lado direito (design system) */}
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

export default LoginPage;

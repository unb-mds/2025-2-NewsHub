import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

function LoginPage() {
  // 1. Estados para armazenar os dados do formulário
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  // Estados para feedback da API e validação
  const [errors, setErrors] = useState({});

  // 2. Função de validação do formulário
  const validateForm = () => {
    const newErrors = {};

    if (!email.trim() || !/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = "The email is invalid.";
    }
    if (!password.trim()) {
      newErrors.password = "Please enter your password.";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // 3. Função que lida com o envio do formulário
  const handleSubmit = async (event) => {
    event.preventDefault();

    setErrors({});

    // Chama a função de validação
    if (!validateForm()) {
      toast.error("Please correct the errors in the form.");
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
        credentials: "include", // Permite que o navegador envie e receba cookies
      });

      const data = await response.json();

      // Lida com a resposta
      if (response.ok) {
        // O backend retorna os dados do usuário no campo 'data'
        toast.success(`Login successful! Welcome, ${data.data.full_name}.`);
        navigate("/account");
      } else {
        toast.error(data.error || "An unknown error occurred.");
      }
    } catch (err) {
      toast.error("Could not connect to the server. Please try again later.");
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
            
              <label
                className="block text-sm font-medium text-gray-900 font-montserrat"
                htmlFor="email"
              >
                Email Address
                <div className="relative mt-1">
                  <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    <img
                      src="./src/icons/envelope-regular-full.svg"
                      alt="email icon"
                      className="h-5 w-5"
                    />
                  </div>
                  <input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Enter your e-mail..."
                    className={`w-full border rounded py-2 px-9 focus:outline-none focus:ring-1 font-montserrat ${errors.email ? "border-red-500 focus:ring-red-500" : "border-gray-800 focus:ring-black"}`}
                    required
                  />
                </div>
              {errors.email && (
                <p className="mt-1 text-sm text-red-600">{errors.email}</p>
              )}
            </label> 
            {/* Campo de Senha */}
            <label
                className="mt-6 block text-sm font-medium text-gray-900 font-montserrat"
                htmlFor="password"
              >
                Password
                <div className="relative mt-1">
                  <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    <img
                      src="./src/icons/lock-regular-full.svg"
                      alt="lock icon"
                      className="h-5 w-5"
                    />
                  </div>
                  <input
                    id="password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Your password..."
                    className={`w-full border rounded py-2 px-9 focus:outline-none focus:ring-1 font-montserrat ${errors.password ? "border-red-500 focus:ring-red-500" : "border-gray-800 focus:ring-black"}`}
                    required
                  />
                </div>
              {errors.password && (
                <p className="mt-1 text-sm text-red-600">{errors.password}</p>
              )}
            </label>

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
                  Remember me
                </label>
              </div>
              <a
                href="#"
                className="font-medium text-[#111] no-underline hover:underline hover:bg-[#1c1c1c] hover:text-[#fff] pt-0.2 px-0.5"
              >
                Forgot my password
              </a>
            </div>

            <button
              type="submit"
              className="mt-8 w-full rounded-md bg-black py-3 px-5 text-white hover:bg-gray-900"
            >
              Sign In
            </button>
          </form>

          <p className="mt-4 text-center text-sm text-black border-t border-[#111] pt-3">
            Don't have an account?{" "}
            <Link
              to="/registrar"
              className="font-medium text-[#111] no-underline hover:underline hover:bg-[#1c1c1c] hover:text-[#fff] pt-0.2 px-0.5"
            >
              Sign up here
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
};

export default LoginPage;

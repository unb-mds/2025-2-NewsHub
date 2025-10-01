import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

function RegisterPage() {
  // 1. Estados para armazenar os dados do formulário
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [birthdate, setBirthdate] = useState("");
  const navigate = useNavigate();

  // Estados para feedback da API e validação
  const [errors, setErrors] = useState({});

  // Regex para validação de senha
  const uppercaseRegex = /[A-Z]/;
  const lowercaseRegex = /[a-z]/;
  const numberRegex = /[0-9]/;

  // 2. Função de validação do formulário
  const validateForm = () => {
    const newErrors = {};

    if (!fullName.trim()) {
      newErrors.fullName = "Full name is required.";
    }

    if (!email.trim() || !/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = "The email is invalid.";
    }

    if (
      password.length < 8 ||
      !uppercaseRegex.test(password) ||
      !lowercaseRegex.test(password) ||
      !numberRegex.test(password)
    ) {
      newErrors.password =
        "Password must be at least 8 characters long, with one uppercase letter, one lowercase letter, and one number.";
    }

    if (password !== confirmPassword) {
      newErrors.confirmPassword = "Passwords do not match.";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // 3. Função que lida com o envio do formulário
  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!validateForm()) {
      toast.error("Please correct the errors in the form.");
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
        toast.success(`User registered successfully! Redirecting to login...`);
        setTimeout(() => {
          navigate("/");
        }, 2000);
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
                    onChange={(e) => {
                      setEmail(e.target.value);
                      if (errors.email) {
                        setErrors({ ...errors, email: null });
                      }
                    }}
                    placeholder="Enter your e-mail..."
                    className={`w-full border rounded py-2 px-9 focus:outline-none focus:ring-1 font-montserrat ${errors.email ? "border-red-500 focus:ring-red-500" : "border-gray-800 focus:ring-black"}`}
                    required
                  />
                </div>
              {errors.email && (
                <p className="mt-1 text-sm text-red-600">{errors.email}</p>
              )}
            </label>
            {/* Campo Nome Completo */}
            <label
                className="mt-6 block text-sm font-medium text-gray-900 font-montserrat"
                htmlFor="fullName"
              >
                Full Name
                <div className="relative mt-1">
                  <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    <img
                      src="./src/icons/user-regular-full.svg"
                      alt="user icon"
                      className="h-5 w-5"
                    />
                  </div>
                  <input
                    id="fullName"
                    type="text"
                    value={fullName}
                    onChange={(e) => {
                      setFullName(e.target.value);
                      if (errors.fullName) {
                        setErrors({ ...errors, fullName: null });
                      }
                    }}
                    placeholder="Enter your name..."
                    className={`w-full border rounded py-2 px-9 focus:outline-none focus:ring-1 font-montserrat ${errors.fullName ? "border-red-500 focus:ring-red-500" : "border-gray-800 focus:ring-black"}`}
                    required
                  />
                </div>
              {errors.fullName && (
                <p className="mt-1 text-sm text-red-600">{errors.fullName}</p>
              )}
            </label>
            {/* Campo data de nascimento*/}
            <label
                className="mt-6 block text-sm font-medium text-gray-900 font-montserrat"
                htmlFor="birthdate"
              >
                Birthdate
                <div className="relative mt-1">
                  <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    <img
                      src="./src/icons/calendar-regular-full.svg"
                      alt="calendar icon"
                      className="h-5 w-5"
                    />
                  </div>
                  <input
                    id="birthdate"
                    type="date"
                    value={birthdate}
                    onChange={(e) => setBirthdate(e.target.value)}
                    required
                    className="w-full border rounded py-2 px-9 focus:outline-none focus:ring-1 font-montserrat border-gray-800 focus:ring-black [&::-webkit-calendar-picker-indicator]:hidden"
                  />
                </div>
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
                    onChange={(e) => {
                      setPassword(e.target.value);
                      if (errors.password) {
                        setErrors({ ...errors, password: null });
                      }
                    }}
                    placeholder="Your password..."
                    className={`w-full border rounded py-2 px-9 focus:outline-none focus:ring-1 font-montserrat ${errors.password ? "border-red-500 focus:ring-red-500" : "border-gray-800 focus:ring-black"}`}
                    required
                  />
                </div>
              {errors.password && (
                <p className="mt-1 text-sm text-red-600">{errors.password}</p>
              )}
            </label>

            {/* Campo Confirmação de Senha */}
            <label
                className="mt-6 block text-sm font-medium text-gray-900 font-montserrat"
                htmlFor="ConfirmPassword"
              >
                Confirm Password
                <div className="relative mt-1">
                  <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    <img
                      src="./src/icons/lock-regular-full.svg"
                      alt="lock icon"
                      className="h-5 w-5"
                    />
                  </div>
                  <input
                    id="ConfirmPassword"
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => {
                      setConfirmPassword(e.target.value);
                      if (errors.confirmPassword) {
                        setErrors({ ...errors, confirmPassword: null });
                      }
                    }}
                    placeholder="Confirm your password..."
                    className={`w-full border rounded py-2 px-9 focus:outline-none focus:ring-1 font-montserrat ${errors.confirmPassword ? "border-red-500 focus:ring-red-500" : "border-gray-800 focus:ring-black"}`}
                    required
                  />
                </div>
              {errors.confirmPassword && (
                <p className="mt-1 text-sm text-red-600">
                  {errors.confirmPassword}
                </p>
              )}
            </label>
            <button
              type="submit"
              className="mt-8 w-full rounded-md bg-black py-3 px-5 text-white hover:bg-gray-900"
            >
              Sign Up
            </button>
          </form>

          <p className="mt-4 text-center text-sm text-black border-t border-[#111] pt-3">
            Already have an account?{" "}
            <Link
              to="/"
              className="font-medium text-[#111] no-underline hover:underline hover:bg-[#1c1c1c] hover:text-[#fff] pt-0.2 px-0.5"
            >
              Login here
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

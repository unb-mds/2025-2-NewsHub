import React, { useState } from "react";
import { Link } from "react-router-dom";
import Header from "../components/HeaderEditAccount";

// Importe os ícones que você está usando no formulário
import UserIcon from "../icons/user-regular-full.svg";
import EnvelopeIcon from "../icons/envelope-regular-full.svg";
import CalendarIcon from "../icons/calendar-regular-full.svg";

function EditAccount() {
  // Estado para os dados do formulário
  const [formData, setFormData] = useState({
    fullName: "Gustavo da Costa Cintra",
    email: "gustavo.cintra@email.com",
    birthdate: "05-04-2004",
  });

  // Estado para os erros de validação
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false); // Estado de carregamento
  const [message, setMessage] = useState(""); // Mensagem de feedback
  const [isError, setIsError] = useState(false); // Tipo da mensagem (erro ou sucesso)

  const validateForm = () => {
    const newErrors = {};

    if (!formData.fullName.trim()) {
      newErrors.fullName = "O nome é obrigatório.";
    }

    if (!formData.email.trim() || !/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = "O email é inválido.";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (validateForm()) {
      alert("Formulário válido! Pronto para ser enviado.");
      // Aqui você faria a chamada à API para atualizar os dados do usuário.
    }
  };

  return (
    <>
      <Header userEmail={formData.email} />
      {/* Container principal da página de edição */}
      <div className="min-h-screen flex flex-col justify-start items-center bg-[#f5f5f5] pt-16">
        <div className="w-full max-w-lg">
          <div className="w-full text-center">
            <h2 className=" mb-2 text-3xl font-bold text-black font-montserrat">
              Edit Your Account Information
            </h2>
            <p className="mt-5 mb-8 text-sm text-gray-600 font-montserrat">
              Edit your account information and confirm.
            </p>
          </div>

          {/* Formulário com os campos */}
          <form onSubmit={handleSubmit} className="mt-8 space-y-4">
            {/* Campo Nome Completo */}
            <div className="relative">
              <label
                className="mt-6 block text-sm font-medium text-gray-900 font-montserrat"
                htmlFor="fullName"
              >
                Nome Completo
                <div className="relative mt-1">
                  <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    {/* Usa o ícone do padrão de cadastro */}
                    <img src={UserIcon} alt="ícone user" className="h-5 w-5" />
                  </div>
                  <input
                    id="fullName"
                    name="fullName"
                    type="text"
                    value={formData.fullName}
                    onChange={handleChange}
                    placeholder=" Digite seu nome..."
                    className="mt-1 block text-[#989898] valid:text-[#111] w-full border border-gray-300 py-2
                     px-8 shadow-sm transition-colors duration-200 ease-in-out
                     focus:border-black focus:ring-black
                     hover:border-black"
                  />
                </div>
                {errors.fullName && (
                  <p className="mt-1 text-sm text-red-600 font-montserrat">
                    {errors.fullName}
                  </p>
                )}
              </label>
            </div>

            {/* Campo Email */}
            <div className="relative">
              <label
                className="mt-6 block text-sm font-medium text-gray-900 font-montserrat"
                htmlFor="email"
              >
                Email
                <div className="relative mt-1">
                  <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    {/* Usa o ícone do padrão de cadastro */}
                    <img
                      src={EnvelopeIcon}
                      alt="ícone email"
                      className="h-5 w-5"
                    />
                  </div>
                  <input
                    id="email"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder=" Digite seu e-mail..."
                    className="mt-1 block w-full text-[#989898] valid:text-[#111] border border-gray-300 py-2
                   px-8 shadow-sm transition-colors duration-200 ease-in-out
                   focus:border-black focus:ring-black
                   hover:border-black"
                  />
                </div>
                {errors.email && (
                  <p className="mt-1 text-sm text-red-600 font-montserrat">
                    {errors.email}
                  </p>
                )}
              </label>
            </div>

            {/* Campo Data de Nascimento */}
            <div className="relative">
              <label
                className="mt-6 block text-sm font-medium text-gray-900 font-montserrat"
                htmlFor="birthdate"
              >
                Data de Nascimento
                <div className="relative mt-1">
                  <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    {/* Usa o ícone do padrão de cadastro */}
                    <img
                      src={CalendarIcon}
                      alt="ícone calendario"
                      className="h-5 w-5"
                    />
                  </div>
                  <input
                    id="birthdate"
                    name="birthdate"
                    type="date"
                    value={formData.birthdate}
                    onChange={handleChange}
                    className="mt-1 text-[#989898] valid:text-[#111] block w-full border border-gray-300 py-2
                     px-8 shadow-sm transition-colors duration-200 ease-in-out
                     focus:border-black focus:ring-black
                     hover:border-black [&::-webkit-calendar-picker-indicator]:hidden"
                  />
                </div>
              </label>
            </div>

            {/* Botão de Confirmação com o mesmo estilo de 'Cadastrar' */}
            <button
              type="submit"
              className="mt-6 w-full rounded-md bg-black py-3 px-5 text-white hover:bg-gray-900"
            >
              Confirmar
            </button>
          </form>
        </div>
      </div>
    </>
  );
}

export default EditAccount;

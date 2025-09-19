import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Header from "../components/HeaderEditAccount";

// Importe os ícones que você está usando no formulário
import UserIcon from "../icons/user-regular-full.svg";
import EnvelopeIcon from "../icons/envelope-regular-full.svg";
import CalendarIcon from "../icons/calendar-regular-full.svg";

function EditAccount() {
  // Estado para os dados do formulário
  const [formData, setFormData] = useState({
    fullName: "",
    email: "",
    birthdate: "",
  });

  // Estado para os erros de validação
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false); // Estado de carregamento
  const [message, setMessage] = useState(""); // Mensagem de feedback
  const [isError, setIsError] = useState(false); // Tipo da mensagem (erro ou sucesso)

  // useEffect para buscar os dados do usuário ao carregar o componente
  useEffect(() => {
    const fetchUserData = async () => {
      // Definindo estado de carregamento
      setLoading(true);

      try {
        const apiUrl = import.meta.env.VITE_API_BASE_URL;
        // Faz a requisição GET para a API
        const response = await fetch(`${apiUrl}/users/profile`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            // "Authorization": `Bearer ${token}`
          },
          credentials: "include", // Adicionado para enviar cookies de autenticação
        });

        const data = await response.json();

        if (response.ok) {
          // Atualizando o estado 'formData' com os dados da API
          setFormData({
            fullName: data.data.full_name,
            email: data.data.email,
            birthdate: data.data.birthdate,
          });
        } else {
          // Tratamento de erros de resposta da API
          setMessage(data.error || "Não foi possível carregar os dados.");
          setIsError(true);
        }
      } catch (err) {
        // Tratamento de erros de conexão
        setMessage("Erro de conexão. Tente novamente mais tarde.");
        setIsError(true);
      } finally {
        // Finaliza o carregamento
        setLoading(false);
      }
    };

    fetchUserData(); // Chama a função para buscar os dados do usuário ao montar o componente
  }, []);
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

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Limpa estados e mensagens anteriores
    setMessage("");
    setIsError(false);
    setLoading(true);

    // Valida o formulário
    if (!validateForm()) {
      setLoading(false);
      return;
    }

    // Obtém a URL da API da variável de ambiente
    const apiUrl = import.meta.env.VITE_API_BASE_URL;

    // Prepara os dados para a API
    const userData = {
      full_name: formData.fullName,
      email: formData.email,
      birthdate: formData.birthdate,
    };

    try {
      // Faz a chamada à API de atualização com o método PATCH
      const response = await fetch(`${apiUrl}/users/profile`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          // Adicione seu token de autenticação aqui se a API exigir
          // "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(userData),
        credentials: "include",
      });

      const data = await response.json();

      // Gerenciando a resposta da API
      if (response.ok) {
        setMessage(`Dados atualizados com sucesso!`);
        setIsError(false);
      } else {
        setMessage(data.error || "Ocorreu um erro desconhecido.");
        setIsError(true);
      }
    } catch (err) {
      // Tratamento de erros de conexão
      setMessage(
        "Não foi possível conectar ao servidor. Tente novamente mais tarde."
      );
      setIsError(true);
    } finally {
      // Finalizando o estado de carregamento
      setLoading(false);
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

          {/* Mensagem de feedback para o usuário */}
          {message && (
            <p
              className={`mt-4 text-center text-sm font-montserrat ${
                isError ? "text-red-600" : "text-green-600"
              }`}
            >
              {message}
            </p>
          )}
        </div>
      </div>
    </>
  );
}

export default EditAccount;

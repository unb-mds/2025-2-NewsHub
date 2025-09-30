import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import Header from "../components/HeaderEditAccount";

// Importe os ícones que você está usando no formulário
import UserIcon from "../icons/user-regular-full.svg";
import EnvelopeIcon from "../icons/envelope-regular-full.svg";
import CalendarIcon from "../icons/calendar-regular-full.svg";

// Função auxiliar para ler um cookie pelo nome
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

function EditAccount() {
  // Hook para navegação programática
  const navigate = useNavigate();

  // Estado para os dados do formulário
  const [formData, setFormData] = useState({
    fullName: "",
    email: "",
    birthdate: "",
  });

  // Estado para os erros de validação
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(true); // Estado de carregamento

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
          // Corrige o problema de fuso horário da data de nascimento
          const birthdateFromAPI = data.data.birthdate;
          const date = new Date(birthdateFromAPI);
          const userTimezoneOffset = date.getTimezoneOffset() * 60000;
          const adjustedDate = new Date(date.getTime() + userTimezoneOffset);
          // Formata para YYYY-MM-DD para o input type="date"
          const formattedDate = adjustedDate.toISOString().split("T")[0];

          // Atualizando o estado 'formData' com os dados da API
          setFormData({
            fullName: data.data.full_name,
            email: data.data.email,
            birthdate: formattedDate,
          });
        } else {
          // Tratamento de erros de resposta da API
          toast.error(data.error || "Could not load data.");
        }
      } catch (err) {
        // Tratamento de erros de conexão
        toast.error("Connection error. Please try again later.");
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
      newErrors.fullName = "Full name is required.";
    }

    if (!formData.email.trim() || !/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = "The email is invalid.";
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

    setLoading(true);

    // Valida o formulário
    if (!validateForm()) {
      toast.error("Please correct the errors in the form.");
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
      const csrfToken = getCookie("csrf_access_token"); // Pega o token CSRF do cookie

      // Faz a chamada à API de atualização com o método PUT
      const response = await fetch(`${apiUrl}/users/profile/update`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-CSRF-TOKEN": csrfToken, // Adiciona o header CSRF
        },
        body: JSON.stringify(userData),
        credentials: "include",
      });

      const data = await response.json();

      // Gerenciando a resposta da API
      if (response.ok) {
        toast.success(`Data updated successfully!`);
        // Pequeno delay para o usuário ver a mensagem e depois redireciona
        setTimeout(() => {
          navigate("/account"); // Redireciona para a página da conta
        }, 2000); // Atraso de 2 segundos
      } else {
        toast.error(data.error || "An unknown error occurred.");
      }
    } catch (err) {
      // Tratamento de erros de conexão
      toast.error("Could not connect to the server. Please try again later.");
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
                Full Name
                <div className="relative mt-1">
                  <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    {/* Usa o ícone do padrão de cadastro */}
                    <img src={UserIcon} alt="user icon" className="h-5 w-5" />
                  </div>
                  <input
                    id="fullName"
                    name="fullName"
                    type="text"
                    value={formData.fullName}
                    onChange={handleChange}
                    placeholder="Enter your name..."
                    className={`w-full border rounded py-2 px-9 focus:outline-none focus:ring-1 font-montserrat ${errors.fullName ? "border-red-500 focus:ring-red-500" : "border-gray-800 focus:ring-black"}`}
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
                Email Address
                <div className="relative mt-1">
                  <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    {/* Usa o ícone do padrão de cadastro */}
                    <img
                      src={EnvelopeIcon}
                      alt="email icon"
                      className="h-5 w-5"
                    />
                  </div>
                  <input
                    id="email"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="Enter your e-mail..."
                    className={`w-full border rounded py-2 px-9 focus:outline-none focus:ring-1 font-montserrat ${errors.email ? "border-red-500 focus:ring-red-500" : "border-gray-800 focus:ring-black"}`}
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
                Birthdate
                <div className="relative mt-1">
                  <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    {/* Usa o ícone do padrão de cadastro */}
                    <img
                      src={CalendarIcon}
                      alt="calendar icon"
                      className="h-5 w-5"
                    />
                  </div>
                  <input
                    id="birthdate"
                    name="birthdate"
                    type="date"
                    value={formData.birthdate}
                    onChange={handleChange}
                    className="w-full border rounded py-2 px-9 focus:outline-none focus:ring-1 font-montserrat border-gray-800 focus:ring-black [&::-webkit-calendar-picker-indicator]:hidden"
                  />
                </div>
              </label>
            </div>

            {/* Botão de Confirmação com o mesmo estilo de 'Cadastrar' */}
            <button
              type="submit"
              className="mt-6 w-full rounded-md bg-black py-3 px-5 text-white hover:bg-gray-900"
              disabled={loading}
            >
              {loading ? "Confirming..." : "Confirm"}
            </button>
          </form>
        </div>
      </div>
    </>
  );
}

export default EditAccount;

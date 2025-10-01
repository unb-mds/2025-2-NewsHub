import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import BackIcon from "../icons/back-svgrepo-com.svg";
import ArrowDownIcon from "../icons/arrow-down.svg";

// Função auxiliar para ler um cookie pelo nome
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

const Header = ({ userEmail }) => {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const navigate = useNavigate();

  // Função de logout
  const handleLogout = async () => {
    try {
      const apiUrl = import.meta.env.VITE_API_BASE_URL;
      const csrfToken = getCookie("csrf_access_token");

      await fetch(`${apiUrl}/users/logout`, {
        method: "POST",
        headers: { "X-CSRF-TOKEN": csrfToken },
        credentials: "include",
      });
    } finally {
      navigate("/"); // redireciona para login, mesmo se a chamada falhar
    }
  };

  return (
    <>
      <header className="flex justify-between items-center p-6 bg-white border-b border-gray-300 relative">
        {/* Lado esquerdo: Botão "Back" */}
        <Link
          to="/account"
          className="flex items-center text-gray-800 hover:text-gray-600"
        >
          <img src={BackIcon} alt="Ícone de Voltar" className="w-5 h-5 mr-2" />
          <span className="font-medium font-montserrat">Back</span>
        </Link>

        {/* Lado direito: E-mail do usuário + seta + dropdown */}
        <div className="relative">
          <button
            className="flex items-center rounded-md text-gray-800 hover:text-gray-600 focus:outline-none text-sm font-montserrat"
            onClick={() => setDropdownOpen((open) => !open)}
          >
            <span className="font-medium font-montserrat">{userEmail}</span>
            <img
              src={ArrowDownIcon}
              alt="Ícone de Seta para Baixo"
              className="ml-2 w-4 h-4"
            />
          </button>
          {dropdownOpen && (
            <div className="absolute right-0 mt-2 w-32 bg-white border border-gray-200 rounded-xl shadow-lg z-10 text-xs font-montserrat">
              <button
                onClick={handleLogout}
                className="block w-full text-left px-4 py-2 text-gray-800 hover:bg-gray-100 font-montserrat"
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </header>
      <div className="w-full h-px bg-gray-200"></div>
    </>
  );
};

export default Header;

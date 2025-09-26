import React from "react";
import { Link } from "react-router-dom";
// O caminho de importação DEVE ser relativo à localização deste arquivo.
// Supondo que você está em src/pages/HeaderEditAccount.jsx e seus ícones estão em src/icons.
import BackIcon from "../icons/back-svgrepo-com.svg";
import ArrowDownIcon from "../icons/arrow-down.svg";

const Header = ({ userEmail }) => {
  return (
    <>
      <header className="flex justify-between items-center p-6 bg-white border-b border-gray-300">
        {/* Lado esquerdo: Botão "Back" */}
        <Link
          to="/"
          className="flex items-center text-gray-800 hover:text-gray-600"
        >
          {/* Usa o ícone importado na propriedade src */}
          <img src={BackIcon} alt="Ícone de Voltar" className="w-5 h-5 mr-2" />
          <span className="font-medium font-montserrat">Back</span>
        </Link>

        {/* Lado direito: E-mail do usuário */}
        <Link
          to="#"
          className="flex items-center text-gray-800 hover:text-gray-600"
        >
          <span className="font-medium font-montserrat">{userEmail}</span>
          {/* Exemplo de como usar um ícone para a seta para baixo */}
          <img
            src={ArrowDownIcon}
            alt="Ícone de Seta para Baixo"
            className="ml-2 w-4 h-4"
          />
        </Link>
      </header>
      {/* Esta div cria a linha separadora horizontal */}
      <div className="w-full h-px bg-gray-200"></div>
    </>
  );
};

export default Header;

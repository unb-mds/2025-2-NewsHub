import React from 'react';

// O nome do componente segue o padrão PascalCase
function ProfileCard() {
  return (
    // Container principal para centralizar o card na tela
    <div className="bg-gray-900 min-h-screen flex items-center justify-center p-4">

      {/* O Card */}
      <div className="
        bg-gray-800 text-white rounded-2xl shadow-2xl
        max-w-sm overflow-hidden
        transform hover:scale-105 transition-transform duration-300 ease-in-out
        border-4 border-transparent hover:border-purple-500
      ">
        {/* Imagem de Banner */}
        <div className="h-32 bg-cover" style={{ backgroundImage: 'url(https://images.unsplash.com/photo-1579546929518-9e396f3cc809?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80)' }}></div>

        {/* Avatar */}
        <div className="relative -mt-16 flex justify-center">
          <img
            className="h-24 w-24 rounded-full border-4 border-gray-800"
            src="https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y"
            alt="Avatar"
          />
        </div>

        {/* Conteúdo do Card */}
        <div className="p-6 text-center">
          <h1 className="text-2xl font-bold text-cyan-400">Olá, Desenvolvedor!</h1>
          <p className="mt-2 text-gray-400">
            Componente importado com sucesso!
          </p>

          {/* Botão com transição */}
          <button className="
            mt-6 px-6 py-2 bg-purple-600 rounded-full
            font-semibold text-white
            hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-opacity-50
            transition-all duration-300 ease-in-out
            transform hover:-translate-y-1
          ">
            Começar a Criar
          </button>
        </div>
      </div>

    </div>
  );
}

// "Exporta" o componente para que outros arquivos possam importá-lo
export default ProfileCard;
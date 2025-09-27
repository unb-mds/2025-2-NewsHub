import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Header from "../components/HeaderEditAccount";
import BackIcon from "../icons/back-svgrepo-com.svg";

// Sub-componente que representa cada card de fonte
const SourceSelectCard = ({ source, isSelected, onToggle }) => {
  const baseClasses =
    "w-full flex items-center justify-between p-4 rounded-lg cursor-pointer transition-all duration-200 border"; // Ajuste na duração para smooth
  const selectedClasses =
    "bg-black border-black text-white transform scale-[1.01] shadow-md"; // Aumentar um pouco a escala
  const unselectedClasses =
    "bg-white border-gray-300 hover:border-black text-gray-800 hover:shadow-sm"; // Adicionado hover shadow

  return (
    <div
      className={`${baseClasses} ${
        isSelected ? selectedClasses : unselectedClasses
      }`}
      onClick={() => onToggle(source)}
    >
      <div>
        <h3 className="font-semibold text-base font-montserrat">
          {source.name}
        </h3>
        <p
          className={`text-sm ${
            isSelected ? "text-gray-200" : "text-gray-500"
          }`}
        >
          {source.url}
        </p>
      </div>
      {/* Ícone de check para a animação de seleção */}
      {isSelected && (
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-6 w-6 text-white animate-pulse" // Animação
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fillRule="evenodd"
            d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
            clipRule="evenodd"
          />
        </svg>
      )}
    </div>
  );
};

const AddSource = ({ onSave, onBack }) => {
  // Estado para a pesquisa e para as fontes selecionadas
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedSources, setSelectedSources] = useState({});

  useEffect(() => {
    const fetchUnattachedSources = async () => {
      setLoading(true);
      setError(null);
      try {
        const apiUrl = import.meta.env.VITE_API_BASE_URL;
        const response = await fetch(
          `${apiUrl}/news_sources/list_all_unattached_sources`,
          {
            method: "GET",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
          }
        );
        const data = await response.json();
        if (response.ok) {
          setSources(data.data || []);
        } else {
          setError(data.error || "Failed to load sources.");
        }
      } catch (err) {
        setError("Connection error. Please try again.");
      } finally {
        setLoading(false);
      }
    };
    fetchUnattachedSources();
  }, []);

  // Filtra as fontes sugeridas com base no termo de pesquisa
  const filteredSources = sources.filter(
    (source) =>
      source.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      source.url.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Função para adicionar ou remover uma fonte
  const handleToggleSource = (source) => {
    setSelectedSources((prevSelected) => {
      const newSelected = { ...prevSelected };
      if (newSelected[source.id]) {
        delete newSelected[source.id]; // Remove
      } else {
        newSelected[source.id] = source; // Adiciona
      }
      return newSelected;
    });
  };

  // Transforma o objeto de fontes selecionadas em um array e chama a função de salvar
  const handleSave = () => {
    const sourcesArray = Object.values(selectedSources);
    onSave(sourcesArray); // Esta função será passada da AccountPage
  };

  const selectedCount = Object.keys(selectedSources).length;

  return (
    <div className="bg-white min-h-screen">
      <header className="flex justify-between items-center p-6 border-b border-gray-300">
        <button
          onClick={onBack}
          className="text-black hover:text-gray-700 font-semibold flex items-center"
        >
          <img src={BackIcon} alt="Ícone de Voltar" className="w-5 h-5 mr-2" />
          <span className="font-medium font-montserrat">Back</span>
        </button>
      </header>

      <main className="max-w-xl mx-auto py-12 px-4 w-full text-center">
        <h2 className=" mb-2 text-3xl font-bold text-black font-montserrat">
          Add Preferred News Sources
        </h2>
        <p className="mt-5 mb-8 text-sm text-gray-600 font-montserrat">
          Select sources you trust to personalize your feed.
        </p>

        {/* Campo de Pesquisa */}
        <div className="mb-8">
          <input
            type="text"
            placeholder="search sources (e.g., The Guardian)"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="mx-auto w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:border-black focus:ring-1 focus:ring-black text-xs font-montserrat"
          />
        </div>

        {/* Div para conter a lista de fontes com rolagem */}
        {/* Adicionei `mb-24` (ou um valor maior) para garantir que o scroll não fique sob o footer */}
        <div className="h-96 overflow-y-auto space-y-4 pl-4 pr-4 mb-24 relative">
          {loading ? (
            <div className="flex justify-center items-center h-full">
              <svg
                className="animate-spin h-8 w-8 text-black"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
                />
              </svg>
            </div>
          ) : error ? (
            <div className="text-center text-red-500 mt-12">{error}</div>
          ) : filteredSources.length > 0 ? (
            filteredSources.map((source) => (
              <SourceSelectCard
                key={source.id}
                source={source}
                isSelected={!!selectedSources[source.id]}
                onToggle={handleToggleSource}
              />
            ))
          ) : searchTerm ? (
            <p className="text-center text-gray-500 mt-12">
              No sources found matching "{searchTerm}".
            </p>
          ) : (
            <p className="text-center text-gray-500 mt-12">
              All available sources have been added.
            </p>
          )}
        </div>
      </main>

      {/* Footer Fixo para o Botão Salvar */}
      <footer className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-4 shadow-lg">
        <div className="max-w-xl mx-auto flex justify-between items-center">
          <p className="text-lg font-montserrat">
            **{selectedCount}** source(s) selected
          </p>
          <button
            onClick={handleSave}
            disabled={selectedCount === 0}
            className={`px-6 py-3 rounded-lg text-white font-bold font-montserrat transition-colors ${
              selectedCount > 0
                ? "bg-black hover:bg-gray-800"
                : "bg-gray-400 cursor-not-allowed"
            }`}
          >
            Save Sources
          </button>
        </div>
      </footer>
    </div>
  );
};

export default AddSource;

// src/pages/AccountPage.jsx
import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Header from "../components/HeaderEditAccount";
// Objeto de dados mockados (Simula a resposta da sua API)
const mockUserData = {
  id: 1,
  full_name: "Arthur Sismene Carvalho",
  email: "arthursismene@gmail.com",
  birthdate: "2004-10-05",
  preferred_topics: [
    { id: 1, name: "Technology" },
    { id: 2, name: "artificial intelligence" },
    { id: 3, name: "Cristiano Ronaldo" },
    { id: 4, name: "Python" },
  ],
  preferred_sources: [
    { id: 101, name: "G1", url: "g1.globo.com" },
    { id: 102, name: "BBC", url: "bbc.com" },
  ],
};

// --- Componentes movidos para dentro da AccountPage ---

// Sub-componente para evitar repetição de código em AccountInformation
const InfoRow = ({ label, value, action, actionLink }) => (
  <div className="flex justify-between items-center py-3">
    <div>
      <p className="text-base text-gray-500 font-montserrat">{label}</p>
      <p className="mt-1 text-base text-gray-900 font-montserrat">{value}</p>
    </div>
    {action && (
      <Link
        to={actionLink}
        className="font-medium text-base text-black hover:underline font-montserrat"
      >
        {action}
      </Link>
    )}
  </div>
);

const AccountInformation = ({ user }) => {
  // Converte a data de nascimento para o formato brasileiro
  const formattedBirthdate = user.birthdate
    ? new Date(user.birthdate).toLocaleDateString("pt-BR")
    : "Não informado";

  return (
    <div className="rounded-lg">
      {/* Container do cabeçalho da seção */}
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-medium text-gray-900 font-montserrat">
          Account information
        </h2>
        <Link
          to="/edit-account"
          className="font-medium text-base text-black hover:underline font-montserrat"
        >
          Edit
        </Link>
      </div>
      {/* Linha horizontal para separar o cabeçalho do conteúdo */}
      <hr className="my-4 border-t-2 border-black" />

      <div>
        <InfoRow label="Name" value={user.full_name} />
        <InfoRow label="Email" value={user.email} />
        <InfoRow label="Birthdate" value={formattedBirthdate} />
        <InfoRow
          label="Password"
          value="***************"
          action="Change"
          actionLink="/change-password"
        />
      </div>
    </div>
  );
};

// SourceCard component for PreferredSources
const SourceCard = ({ source }) => (
  <div className="flex items-center justify-between border border-black rounded shadow-lg p-4">
    <div>
      <h3 className="font-semibold text-gray-800">{source.name}</h3>
      {source.url && <p className="text-sm text-gray-500">{source.url}</p>}
    </div>
    <button className="text-red-500 hover:text-red-700">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        className="h-5 w-5"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M6 18L18 6M6 6l12 12"
        />
      </svg>
    </button>
  </div>
);

const AccountPage = () => {
  // Seus estados continuam perfeitos. Apenas o valor inicial de loading muda.
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true); // Começa como true
  const [error, setError] = useState(null);
  // Estado para o campo de adicionar tópico
  const [newTopic, setNewTopic] = useState("");

  // Usamos useEffect para simular a busca de dados quando o componente carregar
  useEffect(() => {
    // Usamos setTimeout para simular o tempo de espera de uma requisição de rede (ex: 1 segundo)
    const timer = setTimeout(() => {
      try {
        // Se a "requisição" for um sucesso:
        setUserData(mockUserData); // Colocamos os dados mockados no estado
        setLoading(false); // Finalizamos o carregamento
      } catch (err) {
        // Se houvesse um erro:
        setError("Ocorreu um erro ao buscar os dados.");
        setLoading(false);
      }
    }, 1000); // 1000ms = 1 segundo

    // Função de limpeza para evitar problemas de memória
    return () => clearTimeout(timer);
  }, []); // O array vazio [] garante que este efeito rode apenas uma vez

  // Sua renderização condicional está correta e agora vai funcionar
  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        {/* Spinner de carregamento */}
        <svg
          className="animate-spin h-10 w-10 text-black"
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
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center h-screen text-red-500">
        Erro: {error}
      </div>
    );
  }

  // Se tudo deu certo, userData não será nulo, então renderizamos a página completa
  return (
    <div className="bg-gray-50 min-h-screen">
      {/* Render do component Header */}
      <Header userEmail={userData.email} />

      <main className="max-w-7xl mx-auto px-6">
        <div className="flex">
          <aside className="mt-16 ml-12 w-1/3">
            <nav>
              <ul>
                <li>
                  <a
                    href="#"
                    className="relative block py-2 pl-4 text-base font-semibold text-black font-montserrat before:content-[''] before:absolute before:left-0 before:top-1/2 before:h-1/2 before:w-1.5 before:-translate-y-1/2 before:bg-black"
                  >
                    Account
                  </a>
                </li>
                <li>
                  <a
                    href="#"
                    className="block py-2 text-base text-gray-500 hover:text-black pl-4 font-montserrat"
                  >
                    Newsletter
                  </a>
                </li>
              </ul>
            </nav>
          </aside>

          <section className="mt-16 w-1/2">
            {/* Passamos os dados para os componentes filhos via props */}
            <div className="">
              <AccountInformation user={userData} />

              {/* PreferredTopics in-line */}
              <div className="mt-6 rounded-lg">
                <h2 className=" text-xl font-medium text-gray-900 font-montserrat">
                  Preferred news topics
                </h2>
                <hr className="my-4 border-t-2 border-black mb-6" />
                <div className="flex items-end gap-4">
                  <input
                    type="text"
                    value={newTopic}
                    onChange={(e) => setNewTopic(e.target.value)}
                    placeholder="enter a new topic..."
                    className="h-11 flex-grow border border-gray-800 rounded px-4 focus:outline-none focus:ring-2 focus:ring-black text-xs font-montserrat"
                  />
                  <button className="h-11 flex items-center bg-black text-white text-xs font-bold px-4 rounded hover:bg-gray-800 font-montserrat">
                    Add Topic
                  </button>
                </div>
                <div>
                  <p className="mt-8 mb-3 text-base font-medium text-gray-900 font-montserrat">
                    Your topics
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {userData.preferred_topics.map((topic) => (
                      <div
                        key={topic.id}
                        className="flex items-center gap-2 bg-white text-gray-900 text-xs font-medium border border-black shadow-lg pl-3 pr-2 py-1 rounded-full font-montserrat"
                      >
                        <span>{topic.name}</span>
                        <button className="text-red-500 hover:text-red-700 rounded-full hover:bg-gray-100 p-0.2">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            className="h-4 w-4"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M6 18L18 6M6 6l12 12"
                            />
                          </svg>
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* PreferredSources in-line */}
              <div className="mt-11 rounded-lg ">
                <div className="flex justify-between items-center">
                  <h2 className="text-xl font-medium text-gray-900 font-montserrat">
                    Preferred news sources
                  </h2>
                </div>
                <hr className="my-4 border-t-2 border-black" />
                <div className="mt-6 mb-6">
                  <div className="flex justify-between items-center mb-4">
                    <p className="text-base font-medium text-gray-900 font-montserrat">
                      Your Sources
                    </p>
                    <button className="h-11 flex items-center bg-black text-white text-xs font-bold px-4 rounded hover:bg-gray-800 font-montserrat">
                      Add Source
                    </button>
                  </div>
                  <div className="mt-6 space-y-6">
                    {userData.preferred_sources.map((source) => (
                      <SourceCard key={source.id} source={source} />
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
};

export default AccountPage;

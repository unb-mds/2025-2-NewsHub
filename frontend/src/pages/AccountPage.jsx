// teste
import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { toast } from "react-toastify";
import Header from "../components/HeaderEditAccount";
import PreferredTopics from "../components/PreferredTopics";
import AddSource from "../pages/AddSource";

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
// Componente que agrupa as informações da conta do usuário.
const AccountInformation = ({ user }) => {
  const formattedBirthdate = user.birthdate
    ? new Date(user.birthdate).toLocaleDateString("pt-BR", { timeZone: "UTC" })
    : "Não informado";

  return (
    <div className="rounded-lg">
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
// Componente para exibir um card de uma fonte de notícia.
const SourceCard = ({ source, onDelete }) => (
  <div className="flex items-center justify-between border border-black rounded shadow-lg p-4">
    <div>
      <h3 className="font-semibold text-gray-800">{source.name}</h3>
      {source.url && <p className="text-sm text-gray-500">{source.url}</p>}
    </div>
    <button onClick={() => onDelete(source.id)} className="text-red-500 hover:text-red-700">
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

// Função auxiliar para ler um cookie pelo nome
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

// --- Componente Principal da Página ---
const AccountPage = () => {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newTopic, setNewTopic] = useState("");
  const [topicError, setTopicError] = useState("");
  const [isAddingSource, setIsAddingSource] = useState(false);

  const handleOpenAddSource = () => setIsAddingSource(true);

  const handleSaveSources = async (newSources) => {
    const apiUrl = import.meta.env.VITE_API_BASE_URL;
    const csrfToken = getCookie("csrf_access_token");

    const attachPromises = newSources.map((source) => {
      return fetch(`${apiUrl}/news_sources/attach`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRF-TOKEN": csrfToken,
        },
        body: JSON.stringify({ source_id: source.id }),
        credentials: "include",
      });
    });

    try {
      const responses = await Promise.all(attachPromises);
      const failedResponses = responses.filter((res) => !res.ok);

      if (failedResponses.length > 0) {
        // Opcional: tratar erros individuais
        toast.error("Some sources could not be added.");
      }

      // Atualiza o estado local com as fontes que foram salvas com sucesso
      setUserData((prevData) => ({
        ...prevData,
        preferred_sources: [...prevData.preferred_sources, ...newSources],
      }));
    } catch (err) {
      toast.error("Connection error while saving sources.");
    } finally {
      setIsAddingSource(false); // Fecha a tela de adição
    }
  };
  // Este `useEffect` roda uma vez quando o componente é montado para realizar a busca de dados do usuario.
  useEffect(() => {
    const fetchUserData = async () => {
      setLoading(true);
      setError(null);
      try {
        const apiUrl = import.meta.env.VITE_API_BASE_URL;
        // Busca de dados do perfil, tópicos e fontes em paralelo
        const [profileResponse, topicsResponse, sourcesResponse] = await Promise.all([
          fetch(`${apiUrl}/users/profile`, {
            method: "GET",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
          }),
          fetch(`${apiUrl}/topics/list`, {
            method: "GET",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
          }),
          fetch(`${apiUrl}/news_sources/list_all_attached_sources`, {
            method: "GET",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
          }),
        ]);

        const profileData = await profileResponse.json();
        const topicsData = await topicsResponse.json();
        const sourcesData = await sourcesResponse.json();

        if (profileResponse.ok && topicsResponse.ok && sourcesResponse.ok) {
          setUserData({
            full_name: profileData.data.full_name,
            email: profileData.data.email,
            birthdate: profileData.data.birthdate,
            preferred_topics: topicsData.data || [],
            preferred_sources: sourcesData.data || [],
          });
        } else {
          const errorMsg =
            profileData.error ||
            sourcesData.error ||
            topicsData.error ||
            "Não foi possível carregar os dados.";
          setError(errorMsg);
        }
      } catch (err) {
        setError("Erro de conexão ao buscar dados do usuário.");
      } finally {
        setLoading(false);
      }
    };
    fetchUserData();
  }, []);

  // Função para adicionar um novo tópico à lista.
  const handleAddTopic = async () => {
    if (newTopic.trim() === "") return;
    const limit = 10;
    if (userData.preferred_topics.length >= limit) {
      setTopicError("You can only add a maximum of " + limit + " topics.");
      return;
    }
    setTopicError("");

    try {
      const apiUrl = import.meta.env.VITE_API_BASE_URL;
      const csrfToken = getCookie("csrf_access_token");
      const response = await fetch(`${apiUrl}/topics/create`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRF-TOKEN": csrfToken,
        },
        body: JSON.stringify({ name: newTopic.trim() }),
        credentials: "include",
      });

      const result = await response.json();
      if (response.ok) {
        // Adiciona o novo tópico apenas se ele já não estiver na lista (caso de re-associação)
        if (!userData.preferred_topics.some((t) => t.id === result.data.topic.id)) {
          setUserData((currentUserData) => ({
            ...currentUserData,
            preferred_topics: [...currentUserData.preferred_topics, result.data.topic],
          }));
        }
        setNewTopic("");
      } else {
        setTopicError(result.error || "Error adding topic.");
      }
    } catch (err) {
      setTopicError("Connection error. Try again.");
    }
  };
  // Função para deletar um tópico da lista pelo seu ID.
  const handleDeleteTopic = async (topicId) => {
    try {
      const apiUrl = import.meta.env.VITE_API_BASE_URL;
      const csrfToken = getCookie("csrf_access_token");
      const response = await fetch(`${apiUrl}/topics/delete/${topicId}`, {
        method: "DELETE",
        headers: { "X-CSRF-TOKEN": csrfToken },
        credentials: "include",
      });

      if (response.ok) {
        setUserData((currentUserData) => ({
          ...currentUserData,
          preferred_topics: currentUserData.preferred_topics.filter(
            (topic) => topic.id !== topicId
          ),
        }));
      } else {
        const result = await response.json();
        toast.error(result.error || "Could not remove topic.");
      }
    } catch (err) {
      toast.error("Connection error when removing topic.");
    }
  };

  // Função para deletar uma fonte da lista pelo seu ID.
  const handleDeleteSource = async (sourceId) => {
    try {
      const apiUrl = import.meta.env.VITE_API_BASE_URL;
      const csrfToken = getCookie("csrf_access_token");
      const response = await fetch(`${apiUrl}/news_sources/detach/${sourceId}`, {
        method: "DELETE",
        headers: { "X-CSRF-TOKEN": csrfToken },
        credentials: "include",
      });

      if (response.ok) {
        setUserData((currentUserData) => ({
          ...currentUserData,
          preferred_sources: currentUserData.preferred_sources.filter(
            (source) => source.id !== sourceId
          ),
        }));
      } else {
        const result = await response.json();
        toast.error(result.error || "Could not remove source.");
      }
    } catch (err) {
      toast.error("Connection error when removing source.");
    }
  };
  // --- RENDERIZAÇÃO CONDICIONAL ---
  // Mostra um spinner de carregamento enquanto os dados não chegam.
  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
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

  // Mostra uma mensagem de erro se a busca de dados falhar
  if (error) {
    return (
      <div className="flex justify-center items-center h-screen text-red-500">
        Erro: {error}
      </div>
    );
  }
  if (isAddingSource) {
    return (
      <AddSource
        onSave={handleSaveSources}
        onBack={() => setIsAddingSource(false)}
        userEmail={userData.email}
      />
    );
  }

  // Se não há erro e o carregamento terminou, mostra a página completa.
  return (
    <div className="bg-gray-50 min-h-screen">
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

              <PreferredTopics // Adicione uma chave única aqui, como o email do usuário
                key={userData.email}
                topics={userData.preferred_topics}
                newTopic={newTopic}
                onNewTopicChange={(e) => {
                  setNewTopic(e.target.value);
                  // Limpa o erro assim que o usuário começa a digitar
                  if (topicError) {
                    setTopicError("");
                  }
                }}
                onAddTopic={handleAddTopic}
                onDeleteTopic={handleDeleteTopic}
                topicError={topicError}
              />

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
                    <button
                      onClick={handleOpenAddSource}
                      className="h-11 flex items-center bg-black text-white text-xs font-bold px-4 rounded hover:bg-gray-800 font-montserrat"
                    >
                      Add Source
                    </button>
                  </div>
                  <div className="mt-6 space-y-6">
                    {userData.preferred_sources.map((source) => (
                      <SourceCard
                        key={source.id}
                        source={source}
                        onDelete={handleDeleteSource}
                      />
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

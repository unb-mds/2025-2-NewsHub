// src/pages/AccountPage.jsx
import React, { useState, useEffect } from 'react';

// Importando TODOS os componentes que vamos usar
import AccountHeader from '../components/Account/AccountHeader';
import AccountSidebar from '../components/Account/AccountSidebar';
import AccountInformation from '../components/Account/AccountInformation';
import PreferredTopics from '../components/Account/PreferredTopics';
import PreferredSources from '../components/Account/PreferredSources';

// Objeto de dados mockados (Simula a resposta da sua API)
const mockUserData = {
  id: 1,
  full_name: 'Arthur Sismene Carvalho',
  email: 'arthursismene@gmail.com',
  birthdate: '2004-10-05',
  preferred_topics: [
    { id: 1, name: 'Technology' }, { id: 2, name: 'artificial intelligence' }, { id: 3, name: 'Cristiano Ronaldo' }, { id: 4, name: 'Python'},
  ],
  preferred_sources: [
    { id: 101, name: 'G1', url: 'g1.globo.com' }, { id: 102, name: 'BBC', url: 'bbc.com' },
  ]
};

const AccountPage = () => {
  // 1. Seus estados continuam perfeitos. Apenas o valor inicial de loading muda.
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true); // Começa como true
  const [error, setError] = useState(null);

  // 2. [NOVO] Usamos useEffect para simular a busca de dados quando o componente carregar
  useEffect(() => {
    // Usamos setTimeout para simular o tempo de espera de uma requisição de rede (ex: 1 segundo)
    const timer = setTimeout(() => {
      try {
        // Se a "requisição" for um sucesso:
        setUserData(mockUserData); // Colocamos os dados mockados no estado
        setLoading(false);         // Finalizamos o carregamento
      } catch (err) {
        // Se houvesse um erro:
        setError('Ocorreu um erro ao buscar os dados.');
        setLoading(false);
      }
    }, 1000); // 1000ms = 1 segundo

    // Função de limpeza para evitar problemas de memória
    return () => clearTimeout(timer);
  }, []); // O array vazio [] garante que este efeito rode apenas uma vez

  // 3. Sua renderização condicional está correta e agora vai funcionar
  if (loading) {
    return <div className="flex justify-center items-center h-screen">Carregando informações da conta...</div>;
  }

  if (error) {
    return <div className="flex justify-center items-center h-screen text-red-500">Erro: {error}</div>;
  }

  // Se tudo deu certo, userData não será nulo, então renderizamos a página completa
  return (
    <div className="bg-gray-50 min-h-screen font-sans">
      
      {/* 4. [ATUALIZADO] Usamos os componentes importados */}
      <AccountHeader userEmail={userData.email} />

      <main className="max-w-7xl mx-auto px-6">
        <div className="flex">
          
          <AccountSidebar />

          <section className="w-3/4 py-10">
            {/* 5. Passamos os dados para os componentes filhos via props */}
            <AccountInformation user={userData} />
            <PreferredTopics topics={userData.preferred_topics} />
            <PreferredSources sources={userData.preferred_sources} />
          </section>

        </div>
      </main>
    </div>
  );
};

export default AccountPage;
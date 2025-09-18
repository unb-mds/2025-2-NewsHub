import React, { useState } from "react";
import { Link } from "react-router-dom";

const AccountPage = () => {
    // Estados para guardar os dados, o status de carregamento e possíveis erros
    const [userData, setUserData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    

    // Renderização condicional: mostra mensagens diferentes durante o carregamento ou em caso de erro
    if (loading) {
        return <div>Carregando informações da conta...</div>;
    }

    if (error) {
        return <div>Erro: {error}</div>;
    }

    // Se tudo deu certo, userData não será nulo, então renderizamos os dados
    return (
        <div>
            <h1>Minha Conta</h1>
            
            <section>
                <h2>Informações da Conta</h2>
                <p><strong>Nome:</strong> {userData.name}</p>
                <p><strong>Email:</strong> {userData.email}</p>
                <p><strong>Aniversário:</strong> {userData.birthdate}</p>
            </section>
            
            <section>
                <h2>Meus Tópicos de Interesse</h2>
                <ul>
                
                </ul>
            </section>

            <section>
                <h2>Minhas Fontes de Notícias</h2>
                <ul>

                </ul>
            </section>
        </div>
    );
};

export default AccountPage;
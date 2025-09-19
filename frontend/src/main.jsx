import React from 'react';
import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import './index.css';

import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';
import RegisterPage from './pages/RegisterPage'; // <-- 1. IMPORTE A NOVA PÁGINA


// Cria o objeto de configuração do roteador
const router = createBrowserRouter([
  {
    path: "/", // A URL raiz (ex: http://localhost:5173/)
    element: <HomePage />, // Renderiza o componente HomePage
  },
  {
    path: "/sobre", // A URL da página "sobre"
    element: <AboutPage />, // Renderiza o componente AboutPage
  },
   {
    path: "/registrar", // <-- 2. ADICIONE A NOVA ROTA
    element: <RegisterPage />,
  },
]);

// Renderiza o "Provedor de Rota" em vez do componente diretamente
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./index.css";

import LoginPage from "./pages/LoginPage";
import AboutPage from "./pages/AboutPage";
import RegisterPage from "./pages/RegisterPage";
import EditAccount from "./pages/EditAccount.jsx";

// Cria o objeto de configuração do roteador
const router = createBrowserRouter([
  {
    path: "/", // A URL raiz (ex: http://localhost:5173/)
    element: <LoginPage />, // Renderiza o componente HomePage
  },
  {
    path: "/sobre", // A URL da página "sobre"
    element: <AboutPage />, // Renderiza o componente AboutPage
  },
  {
    path: "/registrar", // A URL da página de registro
    element: <RegisterPage />,
  },
  {
    path: "/edit-account", // A URL da página de edição de conta
    element: <EditAccount />, // Renderiza o componente EditAccount
  },
]);

// Renderiza o "Provedor de Rota" em vez do componente diretamente
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);

import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./index.css";

import LoginPage from "./pages/LoginPage";
import AboutPage from "./pages/AboutPage";
import RegisterPage from "./pages/RegisterPage";
import EditAccount from "./pages/EditAccount.jsx";
import ChangePassword from "./pages/ChangePassword.jsx";
import RegisterPage from "./pages/RegisterPage";
import AccountPage from "./pages/AccountPage";

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
  {
    path: "/change-password", // A URL da página de edição de conta
    element: <ChangePassword />, // Renderiza o componente EditAccount
  },
  {
    path: "/account", // A URL da página da conta
    element: <AccountPage />, // Renderiza o componente AccountPage
  },
]);

// Renderiza o "Provedor de Rota" em vez do componente diretamente
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);

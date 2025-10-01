import { useState, useEffect } from 'react';

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

/**
 * Hook para verificar o status de autenticação do usuário.
 * @returns {{isAuthenticated: boolean}} Objeto contendo o status de autenticação.
 * Hook to check the user's authentication status.
 * @returns {{isAuthenticated: boolean}} An object containing the authentication status.
 */
export const useAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(!!getCookie('csrf_access_token'));


  return { isAuthenticated };
};


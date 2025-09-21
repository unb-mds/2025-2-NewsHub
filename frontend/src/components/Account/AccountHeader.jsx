// src/components/Account/AccountHeader.jsx
import React from 'react';

const AccountHeader = ({ userEmail }) => {
  return (
    <header className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <button className="text-gray-600 hover:text-black">
          &larr; Back
        </button>
        <div className="text-gray-600 font-medium">
          {/* Se o email ainda não carregou, mostra um placeholder */}
          {userEmail ? userEmail : 'Carregando...'}
        </div>
      </div>
    </header>
  );
};

export default AccountHeader;
// src/components/Account/AccountInformation.jsx
import React from 'react';

// Sub-componente para evitar repetição de código
const InfoRow = ({ label, value, action }) => (
  <div className="flex justify-between items-center py-4 border-b border-gray-200">
    <div>
      <p className="text-sm text-gray-500">{label}</p>
      <p className="text-base text-gray-800">{value}</p>
    </div>
    {action && <button className="font-semibold text-sm text-gray-600 hover:text-black">{action}</button>}
  </div>
);

const AccountInformation = ({ user }) => {
  // Formata a data para o padrão brasileiro (DD/MM/AAAA)
  const formattedBirthdate = user.birthdate 
    ? new Date(user.birthdate).toLocaleDateString('pt-BR', { timeZone: 'UTC' }) 
    : 'Não informado';

  return (
    <div className="bg-white p-8 rounded-lg">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold text-gray-900">Account information</h2>
        <button className="font-semibold text-sm text-gray-600 hover:text-black">Edit</button>
      </div>
      <div>
        <InfoRow label="Name" value={user.full_name} />
        <InfoRow label="Email" value={user.email} />
        <InfoRow label="Birthdate" value={formattedBirthdate} />
        <InfoRow label="Password" value="••••••••••••" action="Change" />
      </div>
    </div>
  );
};

export default AccountInformation;
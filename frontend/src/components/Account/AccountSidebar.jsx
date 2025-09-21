// src/components/Account/AccountSidebar.jsx
import React from 'react';

const AccountSidebar = () => {
  return (
    <aside className="w-1/4 py-10 pr-10">
      <nav>
        <ul>
          <li>
            <a href="#" className="block py-2 text-base font-semibold text-black border-l-2 border-black pl-4">
              Account
            </a>
          </li>
          <li>
            <a href="#" className="block py-2 text-base text-gray-500 hover:text-black pl-4">
              Newsletter
            </a>
          </li>
        </ul>
      </nav>
    </aside>
  );
};

export default AccountSidebar;
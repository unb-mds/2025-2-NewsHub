import React from "react"; // <-- ADD THIS LINE
import { Link } from "react-router-dom";
import ProfileCard from "../components/ProfileCard";

function HomePage() {
  return (
    <div>
      <ProfileCard />

      <div className="absolute top-5 right-5 flex space-x-4">
        <Link to="/registrar">
          <button className="px-4 py-2 bg-green-500 text-white font-semibold rounded-lg shadow-md hover:bg-green-700 transition-colors">
            Registre-se
          </button>
        </Link>
        <Link to="/sobre">
          <button className="px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 transition-colors">
            Ir para a Página Sobre
          </button>
        </Link>
      </div>
    </div>
  );
}

export default HomePage;

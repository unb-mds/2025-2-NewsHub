// frontend/src/main.tsx
import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-900 text-white">
      <h1 className="text-4xl font-bold text-blue-400">
        Frontend do NewsHub rodando em um contêiner!
      </h1>
      <button className="mt-6 px-6 py-2 bg-green-500 rounded-lg hover:bg-green-600 transition">
        Botão Tailwind 🎉
      </button>
    </div>
  </React.StrictMode>
);

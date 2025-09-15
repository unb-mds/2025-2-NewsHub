import React, { useState } from "react";
// import { FaEnvelope, FaLock } from "react-icons/fa";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    alert("DADOS PARA O DB => \n email: " + email + "\nsenha: " + password);
  };

  return (
    // #site
    <div className="grid min-h-screen bg-[#f5f5f5] lg:grid-cols-2">
      {/* .container */}
      <div className="flex flex-col justify-center px-8 py-12 sm:px-24">
        <div className="mb-12">
          <form onSubmit={handleSubmit}>
            {/* #logo */}
            <h1 className="mb-10 text-64xl font-bold text-black font-rajdhani">
              Synapse.
            </h1>

            {/* Email Input Field */}
            <div className="relative my-14">
              <label
                htmlFor="email"
                className="text-lg font-bold text-[#1c1c1c]"
              >
                Email
              </label>
              <div className="relative mt-2">
                {/* <FaEnvelope className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400" /> */}
                <input
                  id="email"
                  type="email"
                  className="w-full rounded-[0.3rem] border-2 border-[#d9d9d9] p-4 pl-10 text-lg outline-none transition-colors focus:border-[#1c1c1c] placeholder:text-[#626262]"
                  placeholder="Digite seu @email.com"
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
            </div>

            {/* Password Input Field */}
            <div className="relative my-14">
              <label
                htmlFor="password"
                className="text-lg font-bold text-[#1c1c1c]"
              >
                Senha
              </label>
              <div className="relative mt-2">
                {/* <FaLock className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400" /> */}
                <input
                  id="password"
                  type="password"
                  className="w-full rounded-[0.3rem] border-2 border-[#d9d9d9] p-4 pl-10 text-lg outline-none transition-colors focus:border-[#1c1c1c] placeholder:text-[#626262]"
                  placeholder="Digite sua senha"
                  onChange={(p) => setPassword(p.target.value)}
                  required
                />
              </div>
            </div>

            {/* .recall-forget */}
            <div className="mb-5 flex items-center justify-between text-base">
              <label className="flex items-center font-thin text-[#1c1c1c]">
                <input type="checkbox" className="mr-2" />
                Lembre de mim
              </label>
              <a
                href="#"
                className="rounded-[0.3rem] p-1 text-[#1c1c1c] no-underline transition-colors hover:bg-[#1c1c1c] hover:text-[#f9f9f9] hover:underline"
              >
                Esqueci minha senha
              </a>
            </div>

            <button className="mb-3 h-[50px] w-full cursor-pointer rounded-[0.3rem] bg-[#1c1c1c] text-[1.3rem] font-semibold text-[#f6f6f6] outline-none transition-transform active:scale-95">
              Entrar
            </button>

            {/* .signup-link */}
            <div className="mt-4 border-t-[0.15rem] border-[#d9d9d9] pt-4 text-center text-lg">
              <p>
                Não tem uma conta?{" "}
                <a
                  href="/registrar"
                  className="rounded-[0.3rem] p-1 font-semibold text-[#1c1c1c] no-underline transition-colors hover:bg-[#1c1c1c] hover:text-[#f9f9f9] hover:underline"
                >
                  register here
                </a>
              </p>
            </div>
          </form>
        </div>
      </div>

      {/* #KYWF (Know Your World, Faster) - Painel direito */}
      <div className="hidden bg-[#000000] text-[#f5f5f5] lg:flex lg:flex-col lg:justify-center">
        <div className="mb-20 pl-20">
          {/* A tag <br /> força a quebra de linha */}
          <p className="ml-8 text-160xl font-light leading-none font-rajdhani lg:text-[9rem] xl:text-[10rem] 2xl:text-[12rem]">
            Know
            <br />
            Your
            <br />
            World
            <br />
            <strong className="font-plex-mono font-bold text-[#ffff]">
              Faster.
            </strong>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;

import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import Header from "../components/HeaderEditAccount";
import LockIcon from "../icons/lock-regular-full.svg";
import SeeEye from "../icons/eye-regular-full.svg";
import BlockedEye from "../icons/eye-slash-regular-full.svg";

// Função auxiliar para ler um cookie pelo nome
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

function ChangePassword() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    newPassword: "",
    confirmPassword: "",
  });
  const [userEmail, setUserEmail] = useState("");
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState({
    new: false,
    confirm: false,
  });

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const apiUrl = import.meta.env.VITE_API_BASE_URL;
        const response = await fetch(`${apiUrl}/users/profile`, {
          method: "GET",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
        });
        const data = await response.json();
        if (response.ok) {
          setUserEmail(data.data.email);
        }
      } catch (err) {
        console.error("Error fetching user data:", err);
      }
    };
    fetchUserData();
  }, []);

  const validateForm = () => {
    const newErrors = {};
    const { newPassword, confirmPassword } = formData;

    const uppercaseRegex = /[A-Z]/;
    const lowercaseRegex = /[a-z]/;
    const numberRegex = /\d/;

    if (
      newPassword.length < 8 ||
      !uppercaseRegex.test(newPassword) ||
      !lowercaseRegex.test(newPassword) ||
      !numberRegex.test(newPassword)
    ) {
      newErrors.newPassword =
        "Password must be at least 8 characters long, with one uppercase letter, one lowercase letter, and one number.";
    }

    if (newPassword !== confirmPassword) {
      if (confirmPassword) {
        newErrors.confirmPassword = "Passwords do not match.";
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const togglePasswordVisibility = (field) => {
    setShowPassword((prevState) => ({
      ...prevState,
      [field]: !prevState[field],
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});

    if (!validateForm()) {
      toast.error("Please correct the errors in the form.");
      return;
    }

    setLoading(true);

    const passwordData = { new_password: formData.newPassword };

    try {
      const apiUrl = import.meta.env.VITE_API_BASE_URL;
      const csrfToken = getCookie("csrf_access_token");

      const response = await fetch(`${apiUrl}/users/profile/change_password`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-CSRF-TOKEN": csrfToken,
        },
        body: JSON.stringify(passwordData),
        credentials: "include",
      });

      const data = await response.json();

      if (response.ok) {
        toast.success("Password updated successfully!");
        setTimeout(() => {
          navigate("/account");
        }, 2000);
      } else {
        toast.error(data.error || "An unknown error occurred.");
      }
    } catch (err) {
      toast.error("Could not connect to the server. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Header userEmail={userEmail} />
      <div className="h-[calc(100vh-4.625rem)] flex flex-col justify-start items-center bg-[#f5f5f5] pt-16">
        <div className="w-full max-w-lg">
          <div className="w-full text-center">
            <h2 className=" mb-2 text-3xl font-bold text-black font-montserrat">
              Change your password
            </h2>
            <p className="mt-5 mb-8 text-sm text-gray-600 font-montserrat">
              To change your password, enter a new one below and confirm it.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="mt-8 space-y-4">
            <div className="relative">
              <label
                className="mt-6 block text-sm font-medium text-gray-900 font-montserrat"
                htmlFor="newPassword"
              >
                New Password
                <div className="relative mt-1">
                  <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    <img
                    src={LockIcon}
                    alt="lock icon"
                    className="h-5 w-5"
                    />
                  </div>
                  <input
                    id="newPassword"
                    name="newPassword"
                    type={showPassword.new ? "text" : "password"}
                    value={formData.newPassword}
                    onChange={handleChange}
                    placeholder="enter your password.."
                    className={`w-full border rounded py-2 px-9 focus:outline-none focus:ring-1 font-montserrat ${errors.newPassword ? "border-red-500 focus:ring-red-500" : "border-gray-800 focus:ring-black"}`}
                  />
                  <button
                    type="button"
                    onClick={() => togglePasswordVisibility("new")}
                    className="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400 hover:text-gray-600"
                  >
                    <img
                    src={showPassword.new ? BlockedEye : SeeEye}
                    alt="Show/Hide password"
                    className="h-5 w-5"
                    />
                  </button>
                </div>
                {errors.newPassword && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.newPassword}
                  </p>
                )}
              </label>
            </div>

            <div className="relative">
              <label
                className="mt-6 block text-sm font-medium text-gray-900 font-montserrat"
                htmlFor="confirmPassword"
              >
                Confirm your Password
                <div className="relative mt-1">
                  <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    <img
                    src={LockIcon}
                    alt="lock icon"
                    className="h-5 w-5"
                    />
                  </div>
                  <input
                    id="confirmPassword"
                    name="confirmPassword"
                    type={showPassword.confirm ? "text" : "password"}
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    placeholder="enter your password.."
                    className={`w-full border rounded py-2 px-9 focus:outline-none focus:ring-1 font-montserrat ${errors.confirmPassword ? "border-red-500 focus:ring-red-500" : "border-gray-800 focus:ring-black"}`}
                  />
                  <button
                    type="button"
                    onClick={() => togglePasswordVisibility("confirm")}
                    className="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400 hover:text-gray-600"
                  >
                    <img
                    src={showPassword.confirm ? BlockedEye : SeeEye}
                    alt="Show/Hide password"
                    className="h-5 w-5"
                    />
                  </button>
                </div>
                {errors.confirmPassword && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.confirmPassword}
                  </p>
                )}
              </label>
            </div>

            <button
              type="submit"
              className="mt-6 w-full rounded-md bg-black py-3 px-5 text-white hover:bg-gray-900"
              disabled={loading}
            >
              {loading ? "Confirming..." : "Confirm"}
            </button>
          </form>

        </div>
      </div>
    </>
  );
}

export default ChangePassword;

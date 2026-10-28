
import axios from "axios";

const api = axios.create({
  baseURL: (
    import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1"
  )
    .trim()
    .replace(/\\n$/, ""),
  headers: {
    "Content-Type": "application/json",
  },
});

// Attach the saved JWT token to API requests.
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("eduimpact_token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

export default api;


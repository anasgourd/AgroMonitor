export const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000";

// Add the JWT to requests that require authentication.
export async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem("access_token");

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...options.headers,
            Authorization: `Bearer ${token}`,
        },
    });

    return response;
}
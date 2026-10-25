import { API_BASE_URL, apiFetch } from "./apiFetch";



export async function login(username, password) {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            username,
            password,
        }),
    });

    if (!response.ok) {
        throw new Error("Invalid username or password");
    }

    return response.json();
}

export async function getCurrentUser() {
    const response = await apiFetch("/users/me");

    if (!response.ok) {
        throw new Error("Failed to fetch current user");
    }

    return response.json();
}

export async function getCurrentUserFields() {
    const response = await apiFetch("/users/me/fields");

    if (!response.ok) {
        throw new Error("Failed to fetch current user fields");
    }

    return response.json();
}
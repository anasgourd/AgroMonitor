
import { useState } from "react";

export default function Login({ onLogin }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    async function handleSubmit(event) {
        event.preventDefault();
        setErrorMessage("");

        const success = await onLogin(username, password);

        if (!success) {
            setErrorMessage("Λάθος username ή password. Προσπάθησε ξανά.");
        }
    }

    return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
            <form
                onSubmit={handleSubmit}
                className="w-full max-w-md bg-white p-8 rounded-2xl shadow-sm border border-gray-200"
            >
                <h1 className="text-2xl font-semibold text-gray-900 mb-2">
                    AgroMonitor
                </h1>

                <p className="text-gray-500 mb-6">
                    Sign in to monitor your fields.
                </p>

                <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                        Username
                    </label>

                    <input
                        type="text"
                        value={username}
                        onChange={(event) => setUsername(event.target.value)}
                        className="w-full border border-gray-300 rounded-lg px-3 py-2"
                        placeholder="Username"
                        autoComplete="username"
                        required
                    />
                </div>

                <div className="mb-6">
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                        Password
                    </label>

                    <input
                        type="password"
                        value={password}
                        onChange={(event) => setPassword(event.target.value)}
                        className="w-full border border-gray-300 rounded-lg px-3 py-2"
                        placeholder="Password"
                        autoComplete="current-password"
                        required
                    />
                </div>

                {errorMessage && (
                    <p
                        role="alert"
                        className="mb-4 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700"
                    >
                        {errorMessage}
                    </p>
                )}

                <button
                    type="submit"
                    className="w-full bg-gray-900 text-white rounded-lg py-2.5 hover:bg-gray-800"
                >
                    Sign in
                </button>
            </form>
        </div>
    );
}

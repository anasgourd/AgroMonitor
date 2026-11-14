
import { useState } from "react";

export default function Login({ onLogin, onRegister }) {
    const [isSignUp, setIsSignUp] = useState(false);
    const [fullName, setFullName] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const [successMessage, setSuccessMessage] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    function switchMode() {
        setIsSignUp((current) => !current);
        setErrorMessage("");
        setSuccessMessage("");
        setPassword("");
        setConfirmPassword("");
    }

    async function handleSubmit(event) {
        event.preventDefault();

        if (isLoading) return;

        setErrorMessage("");
        setSuccessMessage("");

        if (isSignUp && password !== confirmPassword) {
            setErrorMessage("Passwords do not match.");
            return;
        }

        setIsLoading(true);

        try {
            if (isSignUp) {
                const success = await onRegister(
                    fullName.trim(),
                    username.trim(),
                    password
                );

                if (success) {
                    setIsSignUp(false);
                    setFullName("");
                    setPassword("");
                    setConfirmPassword("");
                    setSuccessMessage(
                        "Account created successfully. Please sign in."
                    );
                } else {
                    setErrorMessage(
                        "Registration failed. The username may already exist."
                    );
                }
            } else {
                const success = await onLogin(username, password);

                if (!success) {
                    setErrorMessage(
                        "Invalid username or password."
                    );
                }
            }
        } catch {
            setErrorMessage(
                "Something went wrong. Please try again."
            );
        } finally {
            setIsLoading(false);
        }
    }

    const inputClass =
        "w-full border border-gray-300 rounded-lg px-3 py-2";

    return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
            <form
                onSubmit={handleSubmit}
                className="w-full max-w-md bg-white p-8 rounded-2xl shadow-sm border border-gray-200"
            >
                <h1 className="text-2xl font-semibold text-gray-900 mb-2">
                    AgroMonitor
                </h1>

                <p className="text-gray-500 mb-6">
                    {isSignUp
                        ? "Create an account to get started."
                        : "Sign in to monitor your fields."}
                </p>

                {isSignUp && (
                    <div className="mb-4">
                        <label
                            htmlFor="fullName"
                            className="block text-sm font-medium text-gray-700 mb-1"
                        >
                            Full Name
                        </label>
                        <input
                            id="fullName"
                            type="text"
                            value={fullName}
                            onChange={(e) => setFullName(e.target.value)}
                            className={inputClass}
                            placeholder="Full Name"
                            autoComplete="name"
                            required
                        />
                    </div>
                )}

                <div className="mb-4">
                    <label
                        htmlFor="username"
                        className="block text-sm font-medium text-gray-700 mb-1"
                    >
                        Username
                    </label>
                    <input
                        id="username"
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        className={inputClass}
                        placeholder="Username"
                        autoComplete="username"
                        required
                    />
                </div>

                <div className="mb-4">
                    <label
                        htmlFor="password"
                        className="block text-sm font-medium text-gray-700 mb-1"
                    >
                        Password
                    </label>
                    <input
                        id="password"
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className={inputClass}
                        placeholder="Password"
                        autoComplete={
                            isSignUp ? "new-password" : "current-password"
                        }
                        required
                    />
                </div>

                {isSignUp && (
                    <div className="mb-4">
                        <label
                            htmlFor="confirmPassword"
                            className="block text-sm font-medium text-gray-700 mb-1"
                        >
                            Confirm Password
                        </label>
                        <input
                            id="confirmPassword"
                            type="password"
                            value={confirmPassword}
                            onChange={(e) =>
                                setConfirmPassword(e.target.value)
                            }
                            className={inputClass}
                            placeholder="Confirm Password"
                            autoComplete="new-password"
                            required
                        />
                    </div>
                )}

                {errorMessage && (
                    <p
                        role="alert"
                        className="mb-4 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700"
                    >
                        {errorMessage}
                    </p>
                )}

                {successMessage && (
                    <p
                        role="status"
                        className="mb-4 rounded-lg border border-green-200 bg-green-50 px-3 py-2 text-sm text-green-700"
                    >
                        {successMessage}
                    </p>
                )}

                <button
                    type="submit"
                    disabled={isLoading}
                    className="w-full bg-gray-900 text-white rounded-lg py-2.5 hover:bg-gray-800 disabled:opacity-60"
                >
                    {isLoading
                        ? "Please wait..."
                        : isSignUp
                            ? "Create account"
                            : "Sign in"}
                </button>

                <p className="mt-5 text-center text-sm text-gray-500">
                    {isSignUp
                        ? "Already have an account? "
                        : "Don't have an account? "}

                    <button
                        type="button"
                        onClick={switchMode}
                        disabled={isLoading}
                        className="font-semibold text-gray-900 hover:underline"
                    >
                        {isSignUp ? "Sign in" : "Sign up"}
                    </button>
                </p>
            </form>
        </div>
    );
}

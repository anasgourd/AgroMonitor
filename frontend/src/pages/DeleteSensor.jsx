import { useState } from "react";
import { deleteSensor } from "../api/sensor";

export default function DeleteSensor({ sensor, onBack, onDeleted }) {
    const [error, setError] = useState("");
    const [isDeleting, setIsDeleting] = useState(false);

    async function handleDelete() {
        setError("");
        setIsDeleting(true);

        try {
            await deleteSensor(sensor.id);
            onDeleted();
        } catch (error) {
            console.error("Failed to delete sensor:", error);

            if (error.status === 409) {
                setError(
                    "This sensor has recorded measurements or related data and cannot be deleted. Its history must be preserved."
                );
            } else if (error instanceof TypeError) {
                setError(
                    "Could not connect to the server. Please try again."
                );
            } else {
                setError("Failed to delete sensor. Please try again.");
            }
        } finally {
            setIsDeleting(false);
        }
    }

    return (
        <main className="min-h-screen bg-emerald-50 px-6 py-10">
            <div className="mx-auto max-w-2xl">
                <button
                    type="button"
                    onClick={onBack}
                    className="mb-6 text-sm font-medium text-emerald-800 hover:text-emerald-950"
                >
                    ← Back
                </button>

                <section className="rounded-2xl border border-rose-100 bg-white p-8 shadow-sm">
                    <h1 className="text-2xl font-semibold text-gray-900">
                        Delete Sensor
                    </h1>

                    <p className="mt-4 text-gray-600">
                        Are you sure you want to delete{" "}
                        <span className="font-semibold text-gray-900">
                            {sensor.name}
                        </span>
                        ?
                    </p>

                    <p className="mt-2 text-sm text-gray-500">
                        This action cannot be undone.
                    </p>

                    {error && (
                        <p role="alert" className="mt-4 text-sm text-red-600">
                            {error}
                        </p>
                    )}

                    <div className="mt-8 flex justify-end gap-3">
                        <button
                            type="button"
                            onClick={onBack}
                            disabled={isDeleting}
                            className="rounded-lg border border-gray-300 px-5 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-60"
                        >
                            Cancel
                        </button>

                        <button
                            type="button"
                            onClick={handleDelete}
                            disabled={isDeleting}
                            className="rounded-lg bg-rose-700 px-5 py-2.5 text-sm font-medium text-white hover:bg-rose-800 disabled:cursor-not-allowed disabled:opacity-60"
                        >
                            {isDeleting ? "Deleting..." : "Delete Sensor"}
                        </button>
                    </div>
                </section>
            </div>
        </main>
    );
}
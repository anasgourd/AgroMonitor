
import { useState } from "react";

export default function DeleteField({
    field,
    onCancel,
    onDeleted,
}) {
    const [error, setError] = useState("");
    const [isDeleting, setIsDeleting] = useState(false);

    async function handleDelete() {
        setError("");
        setIsDeleting(true);

        try {
            await onDeleted(field.id);
        } catch (error) {
            console.error("Failed to delete field:", error);

            if (error.status === 409) {
                setError(
                    "This field cannot be deleted because it still has sensors. Remove its sensors first."
                );
            } else if (error.status === 404) {
                setError("This field no longer exists.");
            } else if (error instanceof TypeError) {
                setError(
                    "Could not connect to the server. Please try again."
                );
            } else {
                setError("Failed to delete field. Please try again.");
            }
        } finally {
            setIsDeleting(false);
        }
    }

    return (
        <div
            className="fixed inset-0 bg-black/30 flex items-center justify-center z-50 px-4"
            onClick={onCancel}
        >
            <div
                className="bg-white rounded-2xl shadow-xl p-6 w-full max-w-sm"
                onClick={(event) => event.stopPropagation()}
            >
                <h2 className="text-lg font-semibold text-gray-900">
                    Delete field?
                </h2>

                <p className="text-sm text-gray-500 mt-2">
                    Are you sure you want to delete {field.name}?
                </p>

                {error && (
                    <p
                        role="alert"
                        className="mt-4 text-sm text-red-600"
                    >
                        {error}
                    </p>
                )}

                <div className="flex justify-end gap-3 mt-6">
                    <button
                        type="button"
                        onClick={onCancel}
                        disabled={isDeleting}
                        className="px-4 py-2 rounded-lg border border-gray-200
                                   text-gray-700 hover:bg-gray-50
                                   disabled:opacity-50"
                    >
                        Cancel
                    </button>

                    <button
                        type="button"
                        onClick={handleDelete}
                        disabled={isDeleting}
                        className="px-4 py-2 rounded-lg
                                   bg-rose-600 text-white
                                   hover:bg-rose-700
                                   disabled:opacity-50"
                    >
                        {isDeleting ? "Deleting..." : "Delete"}
                    </button>
                </div>
            </div>
        </div>
    );
}
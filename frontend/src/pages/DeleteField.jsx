export default function DeleteField({
    field,
    onCancel,
    onDeleted,
}) {
    async function handleDelete() {
        try {
            await onDeleted(field.id);
        } catch (error) {
            console.error("Failed to delete field:", error);
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

                <div className="flex justify-end gap-3 mt-6">

                    <button
                        type="button"
                        onClick={onCancel}
                        className="px-4 py-2 rounded-lg border border-gray-200
                       text-gray-700 hover:bg-gray-50"
                    >
                        Cancel
                    </button>

                    <button
                        type="button"
                        onClick={handleDelete}
                        className="px-4 py-2 rounded-lg
                       bg-rose-600 text-white
                       hover:bg-rose-700"
                    >
                        Delete
                    </button>

                </div>
            </div>
        </div>
    );
}
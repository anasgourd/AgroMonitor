import { useState } from "react";
import { updateField } from "../api/field";

export default function EditField({ field, onBack, onUpdated }) {
    const [fieldName, setFieldName] = useState(field.name);
    const [type, setType] = useState(field.type);

    // Convert the formatted area value back to a number for the input.
    const [area, setArea] = useState(parseFloat(field.area));

    async function handleSubmit(event) {
        event.preventDefault();

        try {
            const updatedField = await updateField(field.id, {
                field_name: fieldName,
                type,
                area: Number(area),
            });

            console.log("Field updated:", updatedField);
            onUpdated(updatedField);
        } catch (error) {
            console.error("Failed to update field:", error);
        }
    }

    return (
        <main className="min-h-screen bg-emerald-50 px-6 py-8">

            <div className="max-w-2xl mx-auto">

                <button
                    onClick={onBack}
                    className="text-sm font-medium text-emerald-700 hover:text-emerald-900 mb-8"
                >
                    ← Back to fields
                </button>

                <div className="bg-white rounded-2xl shadow-sm border border-emerald-100 p-8">

                    <p className="text-xs font-semibold tracking-[0.2em] text-amber-900 uppercase">
                        FIELD MANAGEMENT
                    </p>

                    <h1 className="text-3xl font-semibold text-emerald-950 mt-2">
                        Edit field
                    </h1>

                    <p className="text-emerald-700 mt-2 mb-8">
                        Update your field information.
                    </p>

                    <form onSubmit={handleSubmit} className="space-y-6">

                        {/* Field name */}
                        <div>
                            <label className="block text-sm font-medium text-emerald-950 mb-2">
                                Field name
                            </label>

                            <input
                                type="text"
                                value={fieldName}
                                onChange={(event) => setFieldName(event.target.value)}
                                className="w-full border border-emerald-200 rounded-xl px-4 py-3
                           bg-emerald-50/40 text-gray-900
                           focus:outline-none focus:ring-2 focus:ring-emerald-500
                           focus:border-transparent"
                            />
                        </div>

                        {/* Type */}
                        <div>
                            <label className="block text-sm font-medium text-emerald-950 mb-2">
                                Field type
                            </label>

                            <input
                                type="text"
                                value={type}
                                onChange={(event) => setType(event.target.value)}
                                className="w-full border border-emerald-200 rounded-xl px-4 py-3
                           bg-emerald-50/40 text-gray-900
                           focus:outline-none focus:ring-2 focus:ring-emerald-500
                           focus:border-transparent"
                            />
                        </div>

                        {/* Area */}
                        <div>
                            <label className="block text-sm font-medium text-emerald-950 mb-2">
                                Area
                            </label>

                            <div className="relative">
                                <input
                                    type="number"
                                    value={area}
                                    onChange={(event) => setArea(event.target.value)}
                                    className="w-full border border-emerald-200 rounded-xl px-4 py-3 pr-16
                             bg-emerald-50/40 text-gray-900
                             focus:outline-none focus:ring-2 focus:ring-emerald-500
                             focus:border-transparent"
                                />

                                <span className="absolute right-4 top-1/2 -translate-y-1/2 text-sm text-gray-500">
                                    acres
                                </span>
                            </div>
                        </div>

                        {/* Actions */}
                        <div className="flex justify-end gap-3 pt-4 border-t border-emerald-100">

                            <button
                                type="button"
                                onClick={onBack}
                                className="px-5 py-2.5 rounded-xl
                           border border-emerald-200
                           text-emerald-800 font-medium
                           hover:bg-emerald-50 transition"
                            >
                                Cancel
                            </button>

                            <button
                                type="submit"
                                className="px-5 py-2.5 rounded-xl
                           bg-emerald-600 hover:bg-emerald-700
                           text-white font-semibold
                           shadow-lg shadow-emerald-100
                           transition"
                            >
                                Save changes
                            </button>

                        </div>

                    </form>

                </div>

            </div>

        </main>
    );
}
import { useState } from "react";
import { createCurrentUserField } from "../api/field";

export default function AddFieldForm({ onCancel, onCreated }) {
    const [fieldName, setFieldName] = useState("");
    const [type, setType] = useState("");
    const [area, setArea] = useState("");

    async function handleSubmit(event) {
        event.preventDefault();

        try {
            const newField = await createCurrentUserField({
                field_name: fieldName,
                type: type,
                area: Number(area),
            });

            console.log("Field created:", newField);
            onCreated(newField);
        } catch (error) {
            console.error("Failed to create field:", error);
        }
    }

    return (
        <form onSubmit={handleSubmit} className="space-y-6">

            {/* Field name */}
            <div>
                <label htmlFor="add-field-name" className="block text-sm font-medium text-emerald-950 mb-2">
                    Field name
                </label>

                <input
                    id="add-field-name"
                    type="text"
                    value={fieldName}
                    onChange={(event) => setFieldName(event.target.value)}
                    placeholder="e.g. North Field"
                    className="w-full border border-emerald-200 rounded-xl px-4 py-3
                     bg-emerald-50/40 text-gray-900
                     focus:outline-none focus:ring-2 focus:ring-emerald-500
                     focus:border-transparent"
                />
            </div>

            {/* Type */}
            <div>
                <label htmlFor="add-field-type" className="block text-sm font-medium text-emerald-950 mb-2">
                    Field type
                </label>

                <input
                    id="add-field-type"
                    type="text"
                    value={type}
                    onChange={(event) => setType(event.target.value)}
                    placeholder="e.g. Olive grove"
                    className="w-full border border-emerald-200 rounded-xl px-4 py-3
                     bg-emerald-50/40 text-gray-900
                     focus:outline-none focus:ring-2 focus:ring-emerald-500
                     focus:border-transparent"
                />
            </div>

            {/* Area */}
            <div>
                <label htmlFor="add-field-area" className="block text-sm font-medium text-emerald-950 mb-2">
                    Area
                </label>

                <div className="relative">
                    <input
                        id="add-field-area"
                        type="number"
                        value={area}
                        onChange={(event) => setArea(event.target.value)}
                        placeholder="e.g. 12.5"
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
                    onClick={onCancel}
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
                    Create Field
                </button>

            </div>

        </form>
    );
}
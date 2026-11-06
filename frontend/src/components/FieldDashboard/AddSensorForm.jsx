import { useState } from "react";
import { createSensor } from "../../api/sensor";

export default function AddSensorForm({
    field,
    onCancel,
    onCreated,
}) {
    const [sensorName, setSensorName] = useState("");
    const [status, setStatus] = useState("active");

    async function handleSubmit(event) {
        event.preventDefault();

        try {
            const newSensor = await createSensor(field.id, {
                sensor_name: sensorName,
                status: status,
            });

            console.log("Sensor created:", newSensor);
            onCreated(newSensor);
        } catch (error) {
            console.error("Failed to create sensor:", error);
        }
    }

    return (
        <form onSubmit={handleSubmit} className="space-y-6">

            {/* Sensor name */}
            <div>
                <label htmlFor="add-sensor-name" className="block text-sm font-medium text-emerald-950 mb-2">
                    Sensor name
                </label>

                <input
                    id="add-sensor-name"
                    type="text"
                    value={sensorName}
                    onChange={(event) => setSensorName(event.target.value)}
                    placeholder="e.g. Temperature Sensor 1"
                    className="w-full border border-emerald-200 rounded-xl px-4 py-3
                     bg-emerald-50/40 text-gray-900
                     focus:outline-none focus:ring-2 focus:ring-emerald-500
                     focus:border-transparent"
                />
            </div>

            {/* Status */}
            <div>
                <label htmlFor="add-sensor-status" className="block text-sm font-medium text-emerald-950 mb-2">
                    Status
                </label>

                <select
                    id="add-sensor-status"
                    value={status}
                    onChange={(event) => setStatus(event.target.value)}
                    className="w-full border border-emerald-200 rounded-xl px-4 py-3
                     bg-emerald-50/40 text-gray-900
                     focus:outline-none focus:ring-2 focus:ring-emerald-500
                     focus:border-transparent"
                >
                    <option value="active">Active</option>
                    <option value="inactive">Inactive</option>
                </select>
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
                    Create Sensor
                </button>

            </div>

        </form>
    );
}
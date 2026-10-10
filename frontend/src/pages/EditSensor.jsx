import { useState } from "react";
import { updateSensor } from "../api/sensor";

export default function EditSensor({ sensor, onBack, onUpdated }) {
  const [sensorName, setSensorName] = useState(sensor.name);
  const [status, setStatus] = useState(sensor.status);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();

    setError("");
    setIsSubmitting(true);

    try {
      const updatedSensor = await updateSensor(sensor.id, {
        sensor_name: sensorName,
        status: status,
      });

      onUpdated(updatedSensor);
    } catch (error) {
      console.error("Failed to update sensor:", error);
      setError("Failed to update sensor. Please try again.");
    } finally {
      setIsSubmitting(false);
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

        <section className="rounded-2xl border border-emerald-100 bg-white p-8 shadow-sm">
          <h1 className="text-2xl font-semibold text-emerald-950">
            Edit Sensor
          </h1>

          <p className="mt-2 text-sm text-gray-500">
            Update the sensor name and status.
          </p>

          <form onSubmit={handleSubmit} className="mt-8 space-y-6">
            <div>
              <label
                htmlFor="sensorName"
                className="mb-2 block text-sm font-medium text-gray-700"
              >
                Sensor Name
              </label>

              <input
                id="sensorName"
                type="text"
                value={sensorName}
                onChange={(event) => setSensorName(event.target.value)}
                required
                className="w-full rounded-lg border border-gray-300 px-4 py-3 outline-none focus:border-emerald-600 focus:ring-2 focus:ring-emerald-100"
              />
            </div>

            <div>
              <label
                htmlFor="sensorStatus"
                className="mb-2 block text-sm font-medium text-gray-700"
              >
                Status
              </label>

              <select
                id="sensorStatus"
                value={status}
                onChange={(event) => setStatus(event.target.value)}
                required
                className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 outline-none focus:border-emerald-600 focus:ring-2 focus:ring-emerald-100"
              >
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
              </select>
            </div>

            {error && (
              <p role="alert" className="text-sm text-red-600">
                {error}
              </p>
            )}

            <div className="flex justify-end gap-3">
              <button
                type="button"
                onClick={onBack}
                className="rounded-lg border border-gray-300 px-5 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                Cancel
              </button>

              <button
                type="submit"
                disabled={isSubmitting}
                className="rounded-lg bg-emerald-800 px-5 py-2.5 text-sm font-medium text-white hover:bg-emerald-900 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {isSubmitting ? "Saving..." : "Save Changes"}
              </button>
            </div>
          </form>
        </section>
      </div>
    </main>
  );
}

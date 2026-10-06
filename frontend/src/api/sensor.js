import { apiFetch } from "./apiFetch";

export async function createSensor(fieldId, sensorData) {
    const response = await apiFetch(`/fields/${fieldId}/sensors`, {
        method: "POST",
        body: JSON.stringify(sensorData),
    });

    if (!response.ok) {
        const errorData = await response.json();
        console.log("Create sensor error:", errorData);
        throw new Error("Failed to create sensor");
    }

    return response.json();
}
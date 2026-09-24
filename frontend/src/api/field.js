const API_BASE_URL = "http://localhost:8000";

export async function getUserFields(userId) {
    const response = await fetch(
        `${API_BASE_URL}/users/${userId}/fields`
    );

    if (!response.ok) {
        throw new Error("Failed to fetch fields");
    }

    return response.json();
}


export async function getField(fieldId) {
  const response = await fetch(
    `${API_BASE_URL}/fields/${fieldId}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch field");
  }

  return response.json();
}


export async function getFieldSensors(fieldId) {
  const response = await fetch(
    `${API_BASE_URL}/fields/${fieldId}/sensors`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch field sensors");
  }

  return response.json();
}


export async function getSensorMeasurements(sensorId) {
  const response = await fetch(
    `${API_BASE_URL}/sensors/${sensorId}/measurements`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch sensor measurements");
  }

  return response.json();
}
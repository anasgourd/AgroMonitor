
import { apiFetch } from "./apiFetch";


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
  const response = await apiFetch(`/fields/${fieldId}`);

  if (!response.ok) {
    throw new Error("Failed to fetch field");
  }

  return response.json();
}


export async function getFieldSensors(fieldId) {
  const response = await apiFetch(`/fields/${fieldId}/sensors`);

  if (!response.ok) {
    throw new Error("Failed to fetch field sensors");
  }

  return response.json();
}

export async function getSensorMeasurements(sensorId) {
  const response = await apiFetch(
    `/sensors/${sensorId}/measurements`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch sensor measurements");
  }

  return response.json();
}

export async function getFieldAlerts(fieldId) {
  const response = await apiFetch(
    `/fields/${fieldId}/alerts`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch field alerts");
  }

  return response.json();
}

export async function createCurrentUserField(fieldData) {
  const response = await apiFetch("/users/me/fields", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(fieldData),
  });

  if (!response.ok) {
    throw new Error("Failed to create field");
  }

  return response.json();
}


export async function updateField(fieldId, fieldData) {
  const response = await apiFetch(`/fields/${fieldId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(fieldData),
  });

  if (!response.ok) {
    throw new Error("Failed to update field");
  }

  return response.json();
}
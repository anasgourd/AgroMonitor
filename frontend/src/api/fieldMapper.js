export function mapFieldFromApi(field) {
  return {
    id: field.field_id,
    name: field.field_name,
    type: field.type,
    area: `${field.area} ha`,
    sensorDetails: [],
    history: {
      temperature: [],
      humidity: [],
    },
    status: "Healthy",
  };
}
export function mapSensorFromApi(sensor, measurements) {
    const latestMeasurement = measurements.at(-1);

    return {
        id: sensor.sensor_id,
        name: sensor.sensor_name,
        type: "Temperature",
        value: latestMeasurement?.value ?? null,
        unit: latestMeasurement?.unit ?? "",
        status: sensor.status,
    };
}
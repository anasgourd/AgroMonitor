
export const statusStyles = {
    Healthy: {
        badge: "bg-emerald-100 text-emerald-800 border-emerald-200",
        dot: "bg-emerald-500",
        message: "Field conditions are stable. No action is required.",
    },
    Attention: {
        badge: "bg-amber-100 text-amber-800 border-amber-200",
        dot: "bg-amber-500",
        message: "Field conditions require attention. Consider performing a checkup.",
    },
    Alert: {
        badge: "bg-rose-100 text-rose-800 border-rose-200",
        dot: "bg-rose-500",
        message: "Critical field conditions detected. Immediate field inspection is recommended."
    },
};

export function calculateAverage(sensors) {
    const activeSensors = sensors.filter(
        (sensor) => sensor.status === "active"
    );

    if (!activeSensors.length) return 0;

    return (
        activeSensors.reduce((sum, sensor) => sum + sensor.value, 0) /
        activeSensors.length
    );
}



export function aggregateFieldTemperature(measurements) {
    const buckets = new Map();

    for (const [sensorId, sensorMeasurements] of Object.entries(measurements)) {
        for (const measurement of sensorMeasurements ?? []) {
            if (measurement.unit !== "C") continue;

            const value = Number(measurement.value);
            const timestamp = new Date(measurement.timestamp).getTime();

            if (!Number.isFinite(value) || !Number.isFinite(timestamp)) {
                continue;
            }

            // Group readings into one-minute UTC buckets.
            const minute = Math.floor(timestamp / 60000) * 60000;

            if (!buckets.has(minute)) {
                buckets.set(minute, new Map());
            }

            const sensorBucket = buckets.get(minute);
            const current = sensorBucket.get(sensorId) ?? {
                sum: 0,
                count: 0,
            };

            current.sum += value;
            current.count += 1;

            sensorBucket.set(sensorId, current);
        }
    }

    return [...buckets.entries()]
        .sort(([timeA], [timeB]) => timeA - timeB)
        .map(([minute, sensors]) => {
            const sensorAverages = [...sensors.values()].map(
                ({ sum, count }) => sum / count
            );

            const average =
                sensorAverages.reduce((sum, value) => sum + value, 0) /
                sensorAverages.length;

            return {
                time: new Date(minute).toISOString(),
                value: average,
            };
        });
}


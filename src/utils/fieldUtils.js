export function createFallbackSensors(field) {
    const temperature = Number(field.temperature ?? 24);
    const humidity = Number(field.moisture ?? 42);

    return [
        {
            id: "T-01",
            type: "Temperature",
            value: temperature,
            unit: "°C",
            status: "Normal",
        },
        {
            id: "T-02",
            type: "Temperature",
            value: Number((temperature + 0.4).toFixed(1)),
            unit: "°C",
            status: "Normal",
        },
        {
            id: "T-03",
            type: "Temperature",
            value: Number((temperature - 0.3).toFixed(1)),
            unit: "°C",
            status: "Normal",
        },
        {
            id: "H-01",
            type: "Humidity",
            value: humidity,
            unit: "%",
            status: "Normal",
        },
        {
            id: "H-02",
            type: "Humidity",
            value: humidity + 2,
            unit: "%",
            status: "Normal",
        },
    ];
}

export function createFallbackHistory(field) {
    const temperature = Number(field.temperature ?? 24);
    const humidity = Number(field.moisture ?? 42);

    return {
        temperature: [
            { time: "08:00", value: Number((temperature - 2.4).toFixed(1)) },
            { time: "10:00", value: Number((temperature - 1.2).toFixed(1)) },
            { time: "12:00", value: Number((temperature - 0.2).toFixed(1)) },
            { time: "14:00", value: Number((temperature + 0.6).toFixed(1)) },
            { time: "16:00", value: Number((temperature + 0.2).toFixed(1)) },
            { time: "18:00", value: Number(temperature.toFixed(1)) },
        ],
        humidity: [
            { time: "08:00", value: humidity + 8 },
            { time: "10:00", value: humidity + 5 },
            { time: "12:00", value: humidity + 2 },
            { time: "14:00", value: humidity - 1 },
            { time: "16:00", value: humidity + 1 },
            { time: "18:00", value: humidity },
        ],
    };
}


export const statusStyles = {
    Healthy: {
        badge: "bg-emerald-100 text-emerald-800 border-emerald-200",
        dot: "bg-emerald-500",
    },
    Attention: {
        badge: "bg-amber-100 text-amber-800 border-amber-200",
        dot: "bg-amber-500",
    },
    Alert: {
        badge: "bg-rose-100 text-rose-800 border-rose-200",
        dot: "bg-rose-500",
    },
};

export function calculateAverage(sensors) {
    if (!sensors.length) return 0;

    return (
        sensors.reduce((sum, sensor) => sum + sensor.value, 0) /
        sensors.length
    );
}

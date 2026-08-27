
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
    if (!sensors.length) return 0;

    return (
        sensors.reduce((sum, sensor) => sum + sensor.value, 0) /
        sensors.length
    );
}

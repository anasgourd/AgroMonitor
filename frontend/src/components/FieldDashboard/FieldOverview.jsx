
import { useEffect, useState } from "react";
import { Activity } from "lucide-react";

export default function FieldOverview({
    fieldId,
    name,
    type,
    status,
    message,
    alerts,
    sensors,
    measurements,
}) {
    const storageKey = `agromonitor_seen_alerts_field_${fieldId}`;

    const [seenAlerts, setSeenAlerts] = useState(() => {
        try {
            return JSON.parse(localStorage.getItem(storageKey) || "[]");
        } catch {
            return [];
        }
    });

    useEffect(() => {
        try {
            localStorage.setItem(storageKey, JSON.stringify(seenAlerts));
        } catch (error) {
            console.error("Failed to save seen alerts:", error);
        }
    }, [storageKey, seenAlerts]);

    function acknowledgeAlert(alertId) {
        setSeenAlerts((previous) =>
            previous.includes(alertId)
                ? previous
                : [...previous, alertId]
        );
    }

    const visibleAlerts = [...alerts].sort(
        (a, b) =>
            new Date(b.timestamp).getTime() -
            new Date(a.timestamp).getTime()
    );
    return (
        <div className="lg:col-span-2 bg-[#bfa58c] rounded-3xl border border-[#aa8d70] shadow-sm p-6 flex flex-col">
            <p className="text-xs font-semibold tracking-[0.2em] text-amber-950/70 uppercase">
                FIELD OVERVIEW
            </p>

            <h2 className="text-2xl font-black text-gray-900 mt-1">
                {name}
            </h2>

            <div className="mt-6 space-y-5">
                <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-800/70">
                        Field Type
                    </span>

                    <span className="font-bold text-gray-900">
                        {type}
                    </span>
                </div>

                <div className="h-px bg-black/10" />

                <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-800/70">
                        Monitoring
                    </span>

                    <span className="inline-flex items-center gap-2 font-bold text-gray-900">
                        <span className="w-2 h-2 rounded-full bg-emerald-600" />
                        {alerts.length > 0 ? "Attention needed" : "Active"}
                    </span>
                </div>
            </div>

            <div className="mt-auto pt-8">
                <div className="rounded-2xl bg-white/25 border border-white/30 p-4">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-emerald-600 flex items-center justify-center">
                            <Activity size={20} className="text-white" />
                        </div>

                        <div>
                            <p className="text-xs uppercase tracking-wider text-gray-800/60 font-semibold">
                                Field Health
                            </p>

                            <p className="font-black text-gray-900">
                                {status}
                            </p>
                        </div>
                    </div>

                    <div className="mt-4 space-y-3 text-sm text-gray-800/80">
                        {visibleAlerts.length === 0 ? (
                            <p>No unseen alerts.</p>
                        ) : (
                            visibleAlerts.map((alert) => {
                                const measurement = Object.values(measurements)
                                    .flat()
                                    .find(
                                        (item) =>
                                            String(item.measurement_id) ===
                                            String(alert.measurement_id)
                                    );

                                const sensor = sensors.find(
                                    (item) =>
                                        String(item.id) ===
                                        String(measurement?.sensor_id)
                                );
                                const isSeen = seenAlerts.some(
                                    (id) => String(id) === String(alert.alert_id)
                                );

                                return (
                                    <div
                                        key={alert.alert_id}
                                        className="flex items-center justify-between gap-3"
                                    >
                                        <div className="min-w-0">
                                            <p>⚠ {alert.message}</p>

                                            <p className="text-xs text-gray-700 mt-1">
                                                Sensor: {sensor?.name ?? "Unknown sensor"}
                                            </p>

                                            <p className="text-xs text-gray-600 mt-1">
                                                {new Date(alert.timestamp).toLocaleString()}
                                            </p>
                                        </div>

                                        <button
                                            type="button"
                                            disabled={isSeen}
                                            onClick={() => acknowledgeAlert(alert.alert_id)}
                                            className={`shrink-0 px-3 py-1.5 rounded-lg text-xs font-semibold ${isSeen
                                                    ? "bg-red-600 text-white cursor-default"
                                                    : "bg-white/70 text-gray-900 hover:bg-white"
                                                }`}
                                        >
                                            {isSeen ? "Seen ✓" : "Seen"}
                                        </button>
                                    </div>
                                );
                            })
                        )}
                    </div>

                    <div className="mt-4">
                        <p className="text-sm text-gray-800/80">
                            {message}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}

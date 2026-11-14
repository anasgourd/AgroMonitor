
import { useState } from "react";
import { Activity, Radio, MapPin } from "lucide-react";

const DAY_MS = 24 * 60 * 60 * 1000;

const COLORS = {
    normal: "#34d399",
    anomaly: "#f87171",
    inactive: "#94a3b8",
    noData: "#fbbf24",
};

export default function FieldMap({
    area,
    fieldName = "Field",
    sensors = [],
    measurements = [],
}) {
    const [selectedId, setSelectedId] = useState(null);

    const now = Date.now();

    // Create one map node for each sensor.
    const sensorNodes = sensors.map((sensor) => {
        const id = String(sensor.sensor_id ?? sensor.id);

        // Find this sensor's measurements.
        const readings = measurements
            .filter(
                (m) => String(m.sensor_id) === id
            )
            .sort(
                (a, b) =>
                    new Date(b.timestamp).getTime() -
                    new Date(a.timestamp).getTime()
            );

        const latest = readings[0] ?? null;

        // Measurements within the last 24 hours.
        const recentReadings = readings.filter((m) => {
            const time = new Date(m.timestamp).getTime();

            return (
                Number.isFinite(time) &&
                time >= now - DAY_MS &&
                time <= now
            );
        });

        const hasAnomaly = recentReadings.some(
            (m) => m.is_anomalous === true
        );

        const isActive =
            String(sensor.status).toLowerCase() === "active";

        // Anomalies take priority over other states.
        const state = hasAnomaly
            ? "anomaly"
            : !isActive
                ? "inactive"
                : recentReadings.length === 0
                    ? "noData"
                    : "normal";

        return {
            ...sensor,
            id,
            latest,
            state,
            hasAnomaly,
        };
    });

    // Distribute the sensors across the field.
    const columns = Math.min(
        5,
        Math.max(1, Math.ceil(Math.sqrt(sensorNodes.length)))
    );

    const selectedSensor = sensorNodes.find(
        (sensor) => sensor.id === selectedId
    );

    const formatDate = (timestamp) => {
        if (!timestamp) return "No readings";

        const date = new Date(timestamp);

        if (Number.isNaN(date.getTime())) {
            return "Unknown";
        }

        return date.toLocaleString([], {
            day: "2-digit",
            month: "2-digit",
            hour: "2-digit",
            minute: "2-digit",
            hour12: false,
        });
    };

    const formatState = (state) => {
        const labels = {
            normal: "Normal",
            anomaly: "Anomaly detected",
            inactive: "Inactive",
            noData: "No recent data",
        };

        return labels[state];
    };

    return (
        <div className="lg:col-span-3 bg-white/75 rounded-3xl border border-emerald-100 shadow-sm overflow-hidden">

            {/* Header */}
            <div className="p-5 flex items-center justify-between gap-3">
                <div>
                    <p className="text-xs font-semibold tracking-[0.2em] text-emerald-700 uppercase">
                        FIELD MONITORING
                    </p>

                    <h2 className="text-xl font-bold text-amber-900 mt-1">
                        Field Sensor Map
                    </h2>
                </div>

                <div className="flex items-center gap-2 text-xs text-emerald-800 font-semibold">
                    <Radio size={16} />
                    Last 24h
                </div>
            </div>

            {/* Map */}
            <div
                className="mx-5 mb-5 rounded-2xl p-5 text-white border border-emerald-900/50"
                style={{
                    backgroundColor: "#14231f",
                    backgroundImage: `
                        linear-gradient(rgba(74, 116, 95, 0.13) 1px, transparent 1px),
                        linear-gradient(90deg, rgba(74, 116, 95, 0.13) 1px, transparent 1px)
                    `,
                    backgroundSize: "24px 24px",
                }}
            >
                {/* Field details */}
                <div className="flex justify-between items-start gap-3">
                    <div>
                        <p className="text-[10px] text-emerald-400 uppercase tracking-widest">
                            Schematic Field Layout
                        </p>

                        <p className="text-sm font-semibold mt-1">
                            {fieldName}
                        </p>
                    </div>

                    <div className="rounded-lg bg-white/10 border border-white/10 px-3 py-2">
                        <p className="text-[10px] text-slate-400 uppercase">
                            Area
                        </p>

                        <p className="text-sm font-semibold">
                            {area ?? "—"}
                        </p>
                    </div>
                </div>

                {/* Sensor layout */}
                <div className="mt-5 rounded-xl border border-dashed border-emerald-500/40 bg-emerald-900/10 p-4">

                    {sensorNodes.length === 0 ? (
                        <div className="min-h-[170px] flex items-center justify-center text-sm text-slate-400">
                            No sensors available
                        </div>
                    ) : (
                        <div
                            className="grid min-h-[170px] gap-3"
                            style={{
                                gridTemplateColumns: `repeat(${columns}, minmax(0, 1fr))`,
                            }}
                        >
                            {sensorNodes.map((sensor, index) => {
                                const color = COLORS[sensor.state];
                                const isSelected = selectedId === sensor.id;

                                return (
                                    <button
                                        key={sensor.id}
                                        type="button"
                                        onMouseEnter={() => setSelectedId(sensor.id)}
                                        onFocus={() => setSelectedId(sensor.id)}
                                        onClick={() => setSelectedId(sensor.id)}
                                        aria-label={`${sensor.sensor_name ?? sensor.name}: ${formatState(sensor.state)}`}
                                        className="flex flex-col items-center justify-center gap-2 py-3 rounded-lg hover:bg-white/5 transition-colors focus-visible:outline-2 focus-visible:outline-emerald-400"
                                    >
                                        <span
                                            className="w-11 h-11 rounded-full flex items-center justify-center border-2 transition-transform hover:scale-110"
                                            style={{
                                                borderColor: color,
                                                backgroundColor: `${color}18`,
                                                boxShadow: isSelected
                                                    ? `0 0 20px ${color}70`
                                                    : "none",
                                            }}
                                        >
                                            <span
                                                className="w-3 h-3 rounded-full"
                                                style={{ backgroundColor: color }}
                                            />
                                        </span>

                                        <span className="text-[10px] text-slate-300 font-semibold">
                                            S{String(index + 1).padStart(2, "0")}
                                        </span>
                                    </button>
                                );
                            })}
                        </div>
                    )}
                </div>

                {/* Selected sensor information */}
                <div className="mt-4 min-h-[110px] rounded-xl border border-white/10 bg-black/25 p-4">

                    {selectedSensor ? (
                        <>
                            <div className="flex items-center justify-between gap-3">
                                <p className="text-sm font-bold">
                                    {selectedSensor.sensor_name ?? selectedSensor.name}
                                </p>

                                <span
                                    className="text-xs font-semibold"
                                    style={{
                                        color: COLORS[selectedSensor.state],
                                    }}
                                >
                                    {formatState(selectedSensor.state)}
                                </span>
                            </div>

                            <div className="grid grid-cols-2 gap-4 mt-3">
                                <div>
                                    <p className="text-[10px] text-slate-400">
                                        Latest Measurement
                                    </p>

                                    <p className="text-sm font-semibold mt-1">
                                        {selectedSensor.latest
                                            ? `${selectedSensor.latest.value} ${selectedSensor.latest.unit ?? ""}`
                                            : "No data"}
                                    </p>
                                </div>

                                <div>
                                    <p className="text-[10px] text-slate-400">
                                        Last Updated
                                    </p>

                                    <p className="text-xs text-slate-200 mt-1">
                                        {formatDate(
                                            selectedSensor.latest?.timestamp
                                        )}
                                    </p>
                                </div>
                            </div>
                        </>
                    ) : (
                        <div className="min-h-[78px] flex items-center justify-center gap-2 text-sm text-slate-400">
                            <MapPin size={16} />
                            Hover or click a sensor to view details
                        </div>
                    )}
                </div>

                {/* Legend */}
                <div className="flex flex-wrap gap-4 mt-4">
                    {[
                        ["Normal", COLORS.normal],
                        ["Anomaly (24h)", COLORS.anomaly],
                        ["Inactive", COLORS.inactive],
                        ["No recent data", COLORS.noData],
                    ].map(([label, color]) => (
                        <div
                            key={label}
                            className="flex items-center gap-2 text-xs text-slate-300"
                        >
                            <span
                                className="w-2 h-2 rounded-full"
                                style={{ backgroundColor: color }}
                            />
                            {label}
                        </div>
                    ))}
                </div>

                <div className="flex items-center gap-2 text-[10px] text-slate-500 mt-4">
                    <Activity size={12} />
                    Schematic positions — not GPS coordinates
                </div>
            </div>
        </div>
    );
}

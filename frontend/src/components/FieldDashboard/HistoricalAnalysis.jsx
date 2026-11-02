
import { useState } from "react";
import { Thermometer } from "lucide-react";
import HistoryCard from "./HistoryCard";

export default function HistoricalAnalysis({ history }) {
    const [period, setPeriod] = useState("all");

    const measurements = history?.temperature ?? [];

    // Find the timestamp of the most recent measurement.
    const latestTimestamp = measurements.reduce((latest, item) => {
        const timestamp = new Date(item.time).getTime();

        return Number.isFinite(timestamp)
            ? Math.max(latest, timestamp)
            : latest;
    }, 0);

    const periods = {
        "24h": 24 * 60 * 60 * 1000,
        "7d": 7 * 24 * 60 * 60 * 1000,
    };

    // Filter measurements by the selected time period.
    const filteredMeasurements =
        period === "all"
            ? measurements
            : measurements.filter((item) => {
                const timestamp = new Date(item.time).getTime();

                return (
                    Number.isFinite(timestamp) &&
                    timestamp >= latestTimestamp - periods[period] &&
                    timestamp <= latestTimestamp
                );
            });

    return (
        <section className="mb-8">

            <div className="mb-5 flex flex-wrap items-end justify-between gap-4">
                <div>
                    <p className="text-xs font-semibold tracking-[0.2em] text-emerald-700 uppercase">
                        HISTORICAL ANALYSIS
                    </p>

                    <h2 className="text-2xl font-black text-amber-900 mt-1">
                        Field condition trends
                    </h2>

                    <p className="text-sm text-gray-600 mt-2">
                        Track how the field conditions evolve over time.
                    </p>
                </div>

                {/* Time range filters */}
                <div className="flex items-center gap-1 rounded-xl bg-gray-100 p-1">
                    {[
                        { value: "24h", label: "24h" },
                        { value: "7d", label: "7d" },
                        { value: "all", label: "All" },
                    ].map((option) => (
                        <button
                            key={option.value}
                            type="button"
                            onClick={() => setPeriod(option.value)}
                            aria-pressed={period === option.value}
                            className={`px-4 py-2 rounded-lg text-sm font-semibold transition-colors ${period === option.value
                                    ? "bg-white text-emerald-700 shadow-sm"
                                    : "text-gray-500 hover:text-gray-800"
                                }`}
                        >
                            {option.label}
                        </button>
                    ))}
                </div>
            </div>

            <div className="grid grid-cols-1 gap-6">
                <HistoryCard
                    title="Temperature history"
                    description="Average across temperature sensors"
                    data={filteredMeasurements}
                    color="#be123c"
                    unit="°C"
                    icon={<Thermometer size={19} className="text-rose-700" />}
                    iconBackground="bg-rose-100"
                />
            </div>

        </section>
    );
}

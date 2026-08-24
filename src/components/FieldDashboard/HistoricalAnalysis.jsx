import { Droplets, Thermometer } from "lucide-react";
import HistoryCard from "./HistoryCard";

export default function HistoricalAnalysis({ history }) {
    return (
        <section className="mb-8">

            <div className="mb-5">
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

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

                <HistoryCard
                    title="Temperature history"
                    description="Average across temperature sensors"
                    data={history.temperature}
                    color="#be123c"
                    unit="°C"
                    icon={<Thermometer size={19} className="text-rose-700" />}
                    iconBackground="bg-rose-100"
                />

                <HistoryCard
                    title="Humidity history"
                    description="Average across humidity sensors"
                    data={history.humidity}
                    color="#047857"
                    unit="%"
                    icon={<Droplets size={19} className="text-emerald-700" />}
                    iconBackground="bg-emerald-100"
                />

            </div>

        </section>
    );
}
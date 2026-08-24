import { Droplets, Radio, Thermometer } from "lucide-react";

export default function SensorSummary({
    averageHumidity,
    averageTemperature,
    sensorCount,
}) {
    return (
        <section className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">

            <div className="bg-[#bfa58c] rounded-2xl border border-[#aa8d70] p-5 shadow-sm">
                <div className="flex items-center justify-between">

                    <div>
                        <p className="text-xs uppercase tracking-widest text-amber-950/70 font-semibold">
                            Soil Humidity
                        </p>

                        <strong className="block text-3xl font-black text-gray-900 mt-2">
                            {averageHumidity.toFixed(0)}%
                        </strong>
                    </div>

                    <div className="w-12 h-12 rounded-xl bg-white/30 flex items-center justify-center">
                        <Droplets size={24} className="text-emerald-800" />
                    </div>

                </div>
            </div>


            <div className="bg-[#bfa58c] rounded-2xl border border-[#aa8d70] p-5 shadow-sm">
                <div className="flex items-center justify-between">

                    <div>
                        <p className="text-xs uppercase tracking-widest text-amber-950/70 font-semibold">
                            Temperature
                        </p>

                        <strong className="block text-3xl font-black text-gray-900 mt-2">
                            {averageTemperature.toFixed(1)}°C
                        </strong>
                    </div>

                    <div className="w-12 h-12 rounded-xl bg-white/30 flex items-center justify-center">
                        <Thermometer size={24} className="text-rose-700" />
                    </div>

                </div>
            </div>


            <div className="bg-[#bfa58c] rounded-2xl border border-[#aa8d70] p-5 shadow-sm">
                <div className="flex items-center justify-between">

                    <div>
                        <p className="text-xs uppercase tracking-widest text-amber-950/70 font-semibold">
                            Active Sensors
                        </p>

                        <strong className="block text-3xl font-black text-gray-900 mt-2">
                            {sensorCount}
                        </strong>
                    </div>

                    <div className="w-12 h-12 rounded-xl bg-white/30 flex items-center justify-center">
                        <Radio size={24} className="text-blue-800" />
                    </div>

                </div>
            </div>

        </section>
    );
}
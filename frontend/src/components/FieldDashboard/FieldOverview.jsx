import { Activity } from "lucide-react";

export default function FieldOverview({
    name,
    type,
    status,
    message,
    alerts,
}) {
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
                    <div className="mt-4 space-y-2 text-sm text-gray-800/80">
                        {alerts.length === 0 ? (
                            <p>No alerts detected.</p>
                        ) : (
                            alerts.map((alert) => (
                                <div
                                    key={alert.alert_id}
                                    className="flex items-center justify-between gap-4"
                                >
                                    <p>⚠ {alert.message}</p>

                                    <span className="text-xs text-gray-600 whitespace-nowrap">
                                        {new Date(alert.timestamp).toLocaleTimeString([], {
                                            hour: "2-digit",
                                            minute: "2-digit",
                                        })}
                                    </span>
                                </div>
                            ))
                        )}
                    </div>
                    <div className="mt-4 flex items-center justify-between text-xs">

                        <p className="text-sm text-gray-800/80">
                            {message}
                        </p>

                    </div>

                </div>

            </div>

        </div>
    );
}
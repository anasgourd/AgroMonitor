import LineChart from "./LineChart";

export default function HistoryCard({
    title,
    description,
    data,
    color,
    unit,
    icon,
    iconBackground,
}) {
    return (
        <div className="bg-white/75 rounded-3xl border border-emerald-100 shadow-sm p-5">

            <div className="flex items-center justify-between">

                <div>
                    <h3 className="text-xl font-bold text-gray-900">
                        {title}
                    </h3>

                    <p className="text-xs text-gray-500 mt-1">
                        {description}
                    </p>
                </div>

                <div
                    className={`w-10 h-10 rounded-xl ${iconBackground} flex items-center justify-center`}
                >
                    {icon}
                </div>

            </div>

            <LineChart
                data={data}
                color={color}
                unit={unit}
            />

        </div>
    );
}
export default function SensorList({
    title,
    sensors,
    icon,
    iconColor,
    iconBackground,
    sensorLetter,
    sensorBackground,
    sensorTextColor,
    sensorDescription,
}) {
    return (
        <div className="bg-white/75 rounded-3xl border border-emerald-100 shadow-sm p-5">

            <div className="flex items-center justify-between mb-5">

                <div>
                    <p className="text-xs uppercase tracking-widest text-gray-500 font-semibold">
                        {title}
                    </p>

                    <h3 className="text-xl font-bold text-gray-900 mt-1">
                        {sensors.length} sensors
                    </h3>
                </div>

                <div
                    className={`w-11 h-11 rounded-xl ${iconBackground} flex items-center justify-center`}
                >
                    {icon}
                </div>

            </div>

            <div className="space-y-3">

                {sensors.map((sensor) => (

                    <div
                        key={sensor.id}
                        className={`flex items-center justify-between rounded-2xl ${sensorBackground} border px-4 py-3`}
                    >

                        <div className="flex items-center gap-3">

                            <div
                                className={`w-9 h-9 rounded-lg bg-white/70 flex items-center justify-center text-xs font-bold ${sensorTextColor}`}
                            >
                                {sensorLetter}
                            </div>

                            <div>
                                <p className="text-sm font-bold text-gray-900">
                                    {sensor.id}
                                </p>

                                <p className="text-xs text-gray-500">
                                    {sensorDescription}
                                </p>
                            </div>

                        </div>

                        <div className="text-right">

                            <p className="text-lg font-black text-gray-900">
                                {Number(sensor.value).toFixed(1)}
                                {sensor.unit}
                            </p>

                            <p className="text-[11px] font-semibold text-emerald-700">
                                {sensor.status}
                            </p>

                        </div>

                    </div>

                ))}

            </div>

        </div>
    );
}
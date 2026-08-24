export default function LineChart({ data, color, unit }) {
    const width = 700;
    const height = 240;
    const padding = 32;

    const values = data.map((item) => item.value);

    const min = Math.min(...values);
    const max = Math.max(...values);

    const range = max - min || 1;

    const points = data
        .map((item, index) => {
            const x =
                padding +
                (index * (width - padding * 2)) / Math.max(data.length - 1, 1);

            const y =
                height -
                padding -
                ((item.value - min) / range) * (height - padding * 2);

            return `${x},${y}`;
        })
        .join(" ");

    return (
        <div className="mt-5">
            <div className="flex items-end justify-between mb-3">
                <div>
                    <p className="text-xs font-semibold uppercase tracking-widest text-gray-500">
                        Historical trend
                    </p>
                </div>

                <span className="text-xs text-gray-500">
                    Last {data.length} readings
                </span>
            </div>

            <div className="rounded-2xl bg-white/70 border border-gray-200 p-3 overflow-hidden">
                <svg
                    viewBox={`0 0 ${width} ${height}`}
                    className="w-full h-56"
                    preserveAspectRatio="none"
                >
                    <line
                        x1={padding}
                        y1={height - padding}
                        x2={width - padding}
                        y2={height - padding}
                        stroke="#d1d5db"
                        strokeWidth="1"
                    />

                    <line
                        x1={padding}
                        y1={padding}
                        x2={padding}
                        y2={height - padding}
                        stroke="#d1d5db"
                        strokeWidth="1"
                    />

                    <polyline
                        points={points}
                        fill="none"
                        stroke={color}
                        strokeWidth="4"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    />

                    {data.map((item, index) => {
                        const x =
                            padding +
                            (index * (width - padding * 2)) /
                            Math.max(data.length - 1, 1);

                        const y =
                            height -
                            padding -
                            ((item.value - min) / range) *
                            (height - padding * 2);

                        return (
                            <circle
                                key={index}
                                cx={x}
                                cy={y}
                                r="5"
                                fill="white"
                                stroke={color}
                                strokeWidth="3"
                            />
                        );
                    })}
                </svg>

                <div className="flex justify-between px-2 text-[10px] text-gray-400">
                    {data.map((item, index) => (
                        <span key={index}>{item.time}</span>
                    ))}
                </div>
            </div>

            <p className="text-xs text-gray-500 mt-2">
                Range: {min}
                {unit} – {max}
                {unit}
            </p>
        </div>
    );
}

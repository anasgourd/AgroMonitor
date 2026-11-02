export default function LineChart({ data, color, unit }) {
    const width = 700;
    const height = 280;

    const paddingLeft = 55;
    const paddingRight = 20;
    const paddingTop = 15;
    const paddingBottom = 45;

    if (!data || data.length === 0) {
        return (
            <div className="mt-5 rounded-2xl bg-white/70 border border-gray-200 p-6 text-sm text-gray-500">
                No measurements available yet.
            </div>
        );
    }

    const values = data.map((item) => Number(item.value));

    const rawMin = Math.min(...values);
    const rawMax = Math.max(...values);

    // Give the Y axis a readable range with some space around the values.
    const interval = (() => {
        const roughStep = (rawMax - rawMin || Math.abs(rawMax) * 0.2 || 1) / 4;
        const magnitude = Math.pow(10, Math.floor(Math.log10(roughStep)));
        const normalized = roughStep / magnitude;

        const niceStep =
            normalized <= 1 ? 1 :
                normalized <= 2 ? 2 :
                    normalized <= 5 ? 5 : 10;

        return niceStep * magnitude;
    })();

    const min = Math.floor(rawMin / interval) * interval;
    const max = Math.ceil(rawMax / interval) * interval + interval;
    const range = max - min || 1;

    const plotWidth = width - paddingLeft - paddingRight;
    const plotHeight = height - paddingTop - paddingBottom;

    const timestamps = data.map((item) => new Date(item.time).getTime());

    const firstTimestamp = Math.min(...timestamps);
    const lastTimestamp = Math.max(...timestamps);
    const timeRange = lastTimestamp - firstTimestamp;

    const getX = (index) =>
        timeRange === 0
            ? paddingLeft + plotWidth / 2
            : paddingLeft +
            ((timestamps[index] - firstTimestamp) / timeRange) * plotWidth;

    const getY = (value) =>
        paddingTop + ((max - value) / range) * plotHeight;

    const points = data
        .map((item, index) => `${getX(index)},${getY(Number(item.value))}`)
        .join(" ");

    // Show at most 6 evenly distributed time labels.
    // Four evenly spaced labels across the actual time range.
    const timeTicks =
        timeRange === 0
            ? [firstTimestamp]
            : Array.from(
                { length: 4 },
                (_, index) =>
                    firstTimestamp + (index * timeRange) / 3
            );

    const formatTime = (time) => {
        const date = new Date(time);

        if (Number.isNaN(date.getTime())) {
            return time;
        }

        return date.toLocaleString([], {
            day: "2-digit",
            month: "2-digit",
            hour: "2-digit",
            minute: "2-digit",
            hour12: false,
        });
    };

    const yTicks = Array.from(
        { length: 5 },
        (_, index) => max - (index * range) / 4
    );

    return (
        <div className="mt-5">
            <div className="flex items-end justify-between mb-3">
                <p className="text-xs font-semibold uppercase tracking-widest text-gray-500">
                    Historical trend
                </p>

                <span className="text-xs text-gray-500">
                    Last {data.length} readings
                </span>
            </div>

            <div className="rounded-2xl bg-white/70 border border-gray-200 p-3 overflow-hidden">
                <svg
                    viewBox={`0 0 ${width} ${height}`}
                    className="w-full h-80"
                    preserveAspectRatio="none"
                    role="img"
                    aria-label={`${unit} historical trend chart`}
                >
                    {/* Y-axis labels and horizontal grid lines */}
                    {yTicks.map((value, index) => {
                        const y = getY(value);

                        return (
                            <g key={index}>
                                <line
                                    x1={paddingLeft}
                                    y1={y}
                                    x2={width - paddingRight}
                                    y2={y}
                                    stroke="#e5e7eb"
                                    strokeWidth="1"
                                />

                                <text
                                    x={paddingLeft - 8}
                                    y={y + 4}
                                    textAnchor="end"
                                    fontSize="12"
                                    fill="#6b7280"
                                >
                                    {Number(value.toFixed(2))}
                                </text>
                            </g>
                        );
                    })}

                    {/* Axes */}
                    <line
                        x1={paddingLeft}
                        y1={paddingTop}
                        x2={paddingLeft}
                        y2={height - paddingBottom}
                        stroke="#9ca3af"
                    />

                    <line
                        x1={paddingLeft}
                        y1={height - paddingBottom}
                        x2={width - paddingRight}
                        y2={height - paddingBottom}
                        stroke="#9ca3af"
                    />

                    {/* Measurement line */}
                    <polyline
                        points={points}
                        fill="none"
                        stroke={color}
                        strokeWidth="3"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    />

                    {/* Measurement points */}
                    {data.map((item, index) => (
                        <circle
                            key={item.measurement_id ?? index}
                            cx={getX(index)}
                            cy={getY(Number(item.value))}
                            r={data.length <= 30 ? 3 : 1.5}
                            fill="white"
                            stroke={color}
                            strokeWidth="1.5"
                        />
                    ))}


                    {/* X-axis date/time labels */}
                    {timeTicks.map((timestamp, index) => {
                        const x =
                            timeRange === 0
                                ? paddingLeft + plotWidth / 2
                                : paddingLeft +
                                ((timestamp - firstTimestamp) / timeRange) * plotWidth;

                        return (
                            <text
                                key={index}
                                x={x}
                                y={height - paddingBottom + 18}
                                textAnchor={
                                    timeRange === 0
                                        ? "middle"
                                        : index === 0
                                            ? "start"
                                            : index === timeTicks.length - 1
                                                ? "end"
                                                : "middle"
                                }
                                fontSize="11"
                                fill="#6b7280"
                            >
                                {formatTime(timestamp)}
                            </text>
                        );
                    })}

                </svg>
            </div>

            <p className="text-xs text-gray-500 mt-2">
                Range: {rawMin.toFixed(2)}{unit} – {rawMax.toFixed(2)}{unit}
            </p>
        </div>
    );
}
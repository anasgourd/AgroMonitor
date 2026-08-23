export default function SummaryCard({
  icon,
  iconBackground,
  value,
  label,
}) {
  return (
    <div
      className="
        group relative overflow-hidden
        rounded-2xl
        border border-white/10
        bg-white/[0.04]
        backdrop-blur-xl
        p-5
        flex items-center gap-4
        transition-all duration-300
        hover:-translate-y-1
        hover:border-emerald-400/30
        hover:bg-white/[0.06]
      "
    >

      {/* subtle glow */}
      <div
        className="
          absolute -top-10 -right-10
          w-24 h-24
          rounded-full
          bg-emerald-400/10
          blur-2xl
          opacity-0
          group-hover:opacity-100
          transition-opacity duration-500
        "
      />

      {/* Icon */}
      <div
        className={`
          relative
          flex items-center justify-center
          w-12 h-12
          rounded-xl
          ${iconBackground}
          bg-opacity-10
          border border-white/10
          text-2xl
        `}
      >
        {icon}
      </div>

      {/* Data */}
      <div className="relative flex flex-col">

        <strong className="text-3xl font-black text-white leading-none tracking-tight">
          {value}
        </strong>

        <span className="text-[10px] text-gray-400 font-semibold mt-2 uppercase tracking-[0.18em]">
          {label}
        </span>

      </div>

    </div>
  );
}
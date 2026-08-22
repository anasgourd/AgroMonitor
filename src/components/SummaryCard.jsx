export default function SummaryCard({
  icon,
  iconBackground,
  value,
  label,
}) {
  return (
    <div className="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm flex items-center gap-4">

      <div className={`text-2xl ${iconBackground} p-3 rounded-xl`}>
        {icon}
      </div>

      <div className="flex flex-col">

        <strong className="text-2xl font-black text-gray-900 leading-none">
          {value}
        </strong>

        <span className="text-xs text-gray-500 font-medium mt-1 uppercase tracking-wider">
          {label}
        </span>

      </div>

    </div>
  );
}
export default function FieldCard({ field, onSelect, onEdit, onDelete, isMonitoring }) {

  const statusStyles = {
    Healthy: "bg-emerald-50 text-emerald-700 border-emerald-100",
    Attention: "bg-amber-50 text-amber-700 border-amber-100",
    Alert: "bg-rose-50 text-rose-700 border-rose-100",
  };

  const dotStyles = {
    Healthy: "bg-emerald-500",
    Attention: "bg-amber-500",
    Alert: "bg-rose-500",
  };

  const fieldImages = {
    "Μπέης": "from-emerald-400 to-teal-500",
    "Βαίτσα": "from-amber-400 to-orange-500",
    "Ευανθία": "from-rose-400 to-pink-500",
  };

  return (

    <article className="bg-amber-50 rounded-2xl border border-[#dfd1c1] shadow-sm overflow-hidden hover:shadow-md transition-shadow flex flex-col">

      {/* FIELD IMAGE */}

      <div
        className={`h-32 bg-gradient-to-br ${fieldImages[field.name]} flex items-center justify-center text-4xl shadow-inner`}
      >
        🌿
      </div>


      {/* CONTENT */}

      <div className="p-5 flex-1 flex flex-col">

        {/* TITLE */}

        <div className="flex items-start justify-between gap-2">

          <div>

            <p className="text-[10px] font-bold tracking-widest text-emerald-600 uppercase">
              {field.type}
            </p>

            <h2 className="text-xl font-bold text-gray-900 mt-0.5">
              {field.name}
            </h2>

          </div>


          {/* STATUS */}

          <span
            className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border ${statusStyles[field.status]}`}
          >

            <span
              className={`w-1.5 h-1.5 rounded-full ${dotStyles[field.status]}`}
            />

            {field.status}

          </span>

        </div>


        {/* FIELD INFO */}

        <div className="flex items-center gap-4 text-xs font-medium text-gray-500 mt-4 border-b border-gray-100 pb-3">

          <span>
            📐 {field.area}
          </span>

          <span>
            📡 {field.sensors} Sensors
          </span>

        </div>


        {/* SENSOR VALUES */}


        <div className="flex items-center gap-3 my-4">

          <div className="bg-emerald-200 p-2.5 rounded-xl border border-gray-100 flex-1">
            <span className="block text-[11px] text-gray-500 font-medium">
              Temperature
            </span>

            <strong className="text-sm font-bold text-emerald-800">
              {isMonitoring ? "Live monitoring" : "Not monitoring"}
            </strong>
          </div>

          <div className="flex items-center gap-1.5">

            <button
              onClick={(event) => {
                event.stopPropagation();
                onEdit(field);
              }}
              className="w-7 h-7 rounded-lg hover:bg-emerald-100 flex items-center justify-center text-sm transition-colors"
              title="Edit field"
            >
              ✏️
            </button>

            <button
              onClick={(event) => {
                event.stopPropagation();
                onDelete(field);
              }}
              className="w-7 h-7 rounded-lg hover:bg-rose-100 flex items-center justify-center text-sm transition-colors"
              title="Delete field"
            >
              ✕
            </button>


          </div>

        </div>

        {/* BUTTON */}

        <button
          onClick={() => onSelect(field)}
          className="mt-auto block w-full text-center bg-emerald-200 hover:bg-gray-100 text-gray-700 font-semibold text-sm py-2.5 rounded-xl border border-gray-200 transition-colors"
        >
          View Field →
        </button>

      </div>

    </article >
  );
}
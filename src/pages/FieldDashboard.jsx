export default function FieldDashboard({
  field,
  onBack,
}) {
  return (

    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

      <button
        onClick={onBack}
        className="text-sm font-semibold text-emerald-600 hover:text-emerald-700 mb-8"
      >
        ← Back to My Fields
      </button>


      <div className="mb-8">

        <p className="text-xs font-bold tracking-widest text-emerald-600 uppercase">
          FIELD DASHBOARD
        </p>

        <h1 className="text-4xl font-black text-gray-900 mt-1">
          {field.name}
        </h1>

        <p className="text-gray-500 mt-2">
          {field.type} · {field.area}
        </p>

      </div>


      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">

        <Metric
          label="Soil Moisture"
          value={`${field.moisture}%`}
        />

        <Metric
          label="Temperature"
          value={`${field.temperature}°C`}
        />

        <Metric
          label="Humidity"
          value={`${field.humidity}%`}
        />

        <Metric
          label="Rainfall"
          value={`${field.rain} mm`}
        />

      </div>


      <div className="mt-8 bg-white rounded-2xl border border-gray-100 shadow-sm p-8 h-80 flex items-center justify-center">

        <div className="text-center">

          <div className="text-5xl mb-4">
            🗺️
          </div>

          <h2 className="text-xl font-bold">
            Field Map
          </h2>

          <p className="text-sm text-gray-500 mt-2">
            Interactive field map will go here.
          </p>

        </div>

      </div>

    </main>
  );
}


function Metric({ label, value }) {
  return (

    <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">

      <span className="text-xs text-gray-500">
        {label}
      </span>

      <strong className="block text-2xl font-black text-gray-900 mt-2">
        {value}
      </strong>

    </div>
  );
}
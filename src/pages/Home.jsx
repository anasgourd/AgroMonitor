import SummaryCard from "../components/SummaryCard";
import FieldCard from "../components/FieldCard";

export default function Home({ fields, onSelectField }) {
  return (

    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

      {/* HERO */}

      <section className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">

        <div>

          <p className="text-xs font-bold tracking-widest text-emerald-600 uppercase">
            OVERVIEW
          </p>

          <h1 className="text-3xl font-black text-gray-900 mt-1 tracking-tight">
            My Fields
          </h1>

          <p className="text-sm text-gray-500 mt-1">
            Monitor the health and conditions of your agricultural fields.
          </p>

        </div>


        <button className="self-start sm:self-auto bg-emerald-600 hover:bg-emerald-700 active:scale-95 text-white font-semibold px-5 py-2.5 rounded-xl shadow-lg shadow-emerald-100 transition-all text-sm">
          + Add Field
        </button>

      </section>


      {/* SUMMARY */}

      <section className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-10">

        <SummaryCard
          icon="🌾"
          iconBackground="bg-amber-50"
          value={fields.length}
          label="Total Fields"
        />

        <SummaryCard
          icon="📡"
          iconBackground="bg-blue-50"
          value={fields.reduce(
            (total, field) => total + field.sensors,
            0
          )}
          label="Active Sensors"
        />

        <SummaryCard
          icon="⚠️"
          iconBackground="bg-rose-50"
          value={
            fields.filter(
              field =>
                field.status === "Alert" ||
                field.status === "Attention"
            ).length
          }
          label="Open Alerts"
        />

      </section>


      {/* FIELDS */}

      <section>

        <div className="flex items-end justify-between mb-5">

          <div>

            <p className="text-xs font-bold tracking-widest text-emerald-600 uppercase">
              YOUR FARMS
            </p>

            <h2 className="text-2xl font-bold text-gray-900">
              Your fields
            </h2>

          </div>

        </div>


        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

          {fields.map(field => (

            <FieldCard
              key={field.id}
              field={field}
              onSelect={onSelectField}
            />

          ))}

        </div>

      </section>

    </main>
  );
}
import SummaryCard from "../components/SummaryCard";
import FieldCard from "../components/FieldCard";

export default function Home({ fields, onSelectField }) {
  return (

    <main className="min-h-screen bg-emerald-50">

      {/* HERO */}

      <section className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-8 mb-12">

        <div>

          <p className="text-8xs font-semibold tracking-[0.2em] text-amber-900 uppercase">
            FIELDS OVERVIEW
          </p>


          <p className="text-lg text-emerald-700 mt-3 max-w-xl leading-relaxed font-light italic tracking-wide">
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

            <p className="text-xl font-red text-amber-900 mt-2 tracking-tight uppercase">
              MY FIELDS
            </p>


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
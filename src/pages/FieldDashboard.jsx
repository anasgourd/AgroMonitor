import {

  calculateAverage,
  statusStyles,
} from "../utils/fieldUtils";

import SensorSummary from "../components/FieldDashboard/SensorSummary";
import SensorInventory from "../components/FieldDashboard/SensorInventory";
import HistoricalAnalysis from "../components/FieldDashboard/HistoricalAnalysis";
import FieldMap from "../components/FieldDashboard/FieldMap";
import FieldOverview from "../components/FieldDashboard/FieldOverview";
import FieldHeader from "../components/FieldDashboard/FieldHeader";


// Handle the case where the requested field does not exist.
// Display a fallback view when no field data is available.
export default function FieldDashboard({ field, onBack }) {
  if (!field) {
    return (
      <main className="min-h-screen bg-emerald-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-black text-amber-900">
            Field not found
          </h2>

          <button
            onClick={onBack}
            className="mt-4 px-4 py-2 rounded-xl bg-emerald-700 text-white font-semibold"
          >
            Back
          </button>
        </div>
      </main>
    );
  }
  // Prepare sensor data, historical data, averages, and field status for the dashboard.
  const sensors = field.sensorDetails

  const temperatureSensors = sensors.filter(
    (sensor) => sensor.type === "Temperature"
  );

  const humiditySensors = sensors.filter(
    (sensor) => sensor.type === "Humidity"
  );

  const history = field.history

  const averageTemperature = calculateAverage(temperatureSensors);
  const averageHumidity = calculateAverage(humiditySensors);

  const currentStatus =
    statusStyles[field.status] || statusStyles.Healthy;


  // Render the field dashboard with the prepared data.
  return (
    <main className="min-h-screen bg-emerald-50 px-4 sm:px-6 lg:px-8 py-6">
      <div className="max-w-7xl mx-auto">

        {/* HEADER */}

        <FieldHeader
          name={field.name}
          status={field.status}
          statusStyle={currentStatus}
          onBack={onBack}
        />

        {/* LIVE SENSOR SUMMARY */}

        <SensorSummary
          averageHumidity={averageHumidity}
          averageTemperature={averageTemperature}
          sensorCount={sensors.length}
        />

        {/* SENSOR INVENTORY */}

        <SensorInventory
          temperatureSensors={temperatureSensors}
          humiditySensors={humiditySensors}
        />

        {/* HISTORICAL ANALYSIS */}
        <HistoricalAnalysis history={history} />

        {/* MAP + FIELD OVERVIEW */}

        <section className="grid grid-cols-1 lg:grid-cols-5 gap-6 mb-8">

          <FieldMap area={field.area} />

          <FieldOverview
            name={field.name}
            type={field.type}
            status={field.status}
            message={currentStatus.message}
          />

        </section>

      </div>
    </main>
  );
}
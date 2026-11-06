import SensorSummary from "../components/FieldDashboard/SensorSummary";
import SensorInventory from "../components/FieldDashboard/SensorInventory";
import HistoricalAnalysis from "../components/FieldDashboard/HistoricalAnalysis";
import FieldMap from "../components/FieldDashboard/FieldMap";
import FieldOverview from "../components/FieldDashboard/FieldOverview";
import FieldHeader from "../components/FieldDashboard/FieldHeader";
import { useEffect, useState } from "react";


import {
  getFieldSensors,
  getSensorMeasurements,
  getFieldAlerts,
} from "../api/field";


import { mapSensorFromApi } from "../api/sensorMapper";

import {
  calculateAverage,
  statusStyles,
  aggregateFieldTemperature,
} from "../utils/fieldUtils";



// Handle the case where the requested field does not exist.
// Display a fallback view when no field data is available.
export default function FieldDashboard({ field, onBack, onAddSensor, onEditSensor, onDeleteSensor, }) {

  // Prepare sensor data, historical data, averages, and field status for the dashboard.
  const [sensors, setSensors] = useState([]);
  const [measurements, setMeasurements] = useState({});
  const [alerts, setAlerts] = useState([]);


  useEffect(() => {
    let isActive = true;
    let isLoading = false;

    async function loadFieldData() {
      if (isLoading) return;

      isLoading = true;

      try {
        const data = await getFieldSensors(field.id);

        const measurementResults = await Promise.all(
          data.map(async (sensor) => {
            const sensorMeasurements = await getSensorMeasurements(
              sensor.sensor_id
            );

            return [sensor.sensor_id, sensorMeasurements];
          })
        );

        const measurementMap = Object.fromEntries(measurementResults);

        const mappedSensors = data.map((sensor) =>
          mapSensorFromApi(
            sensor,
            measurementMap[sensor.sensor_id] ?? []
          )
        );

        const fieldAlerts = await getFieldAlerts(field.id);

        if (!isActive) return;

        setSensors(mappedSensors);
        setMeasurements(measurementMap);
        setAlerts(fieldAlerts);
      } catch (error) {
        console.error("Failed to load field data:", error);
      } finally {
        isLoading = false;
      }
    }

    void loadFieldData();

    const intervalId = setInterval(loadFieldData, 15000);

    return () => {
      isActive = false;
      clearInterval(intervalId);
    };
  }, [field.id]);



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

  const temperatureSensors = sensors.filter(
    (sensor) => sensor.type === "Temperature"
  );

  const temperatureHistory = aggregateFieldTemperature(measurements);

  const history = {
    temperature: temperatureHistory,
    humidity: [],
  };


  const averageTemperature = calculateAverage(temperatureSensors);


  const currentStatus =
    alerts.length > 0
      ? statusStyles.Attention
      : statusStyles.Healthy;


  // Render the field dashboard with the prepared data.
  return (
    <main className="min-h-screen bg-emerald-50 px-4 sm:px-6 lg:px-8 py-6">
      <div className="max-w-7xl mx-auto">

        {/* HEADER */}

        <FieldHeader
          name={field.name}
          status={alerts.length > 0 ? "Attention" : "Healthy"}
          statusStyle={currentStatus}
          onBack={onBack}
        />

        {/* LIVE SENSOR SUMMARY */}

        <SensorSummary
          averageTemperature={averageTemperature}
          sensorCount={sensors.length}
        />

        <button
          onClick={() => onAddSensor(field)}
          className="mb-4 px-4 py-2 rounded-xl bg-emerald-700 text-white font-semibold"
        >
          Add Sensor
        </button>


        {/* SENSOR INVENTORY */}

        <SensorInventory
          temperatureSensors={temperatureSensors}
          onEditSensor={onEditSensor}
          onDeleteSensor={onDeleteSensor}
        />

        {/* HISTORICAL ANALYSIS */}
        <HistoricalAnalysis history={history} />

        {/* MAP + FIELD OVERVIEW */}

        <section className="grid grid-cols-1 lg:grid-cols-5 gap-6 mb-8">

          <FieldMap
            area={field.area}
            fieldName={field.name}
            sensors={sensors}
            measurements={Object.values(measurements).flat()}
          />

          <FieldOverview
            fieldId={field.id}
            name={field.name}
            type={field.type}
            status={field.status}
            message={currentStatus.message}
            alerts={alerts}
            sensors={sensors}
            measurements={measurements}
          />
        </section>

      </div>
    </main>
  );
}



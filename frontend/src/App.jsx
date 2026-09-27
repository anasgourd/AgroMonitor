import { useEffect, useState } from "react";

import Header from "./components/Header";
import Home from "./pages/Home";
import FieldDashboard from "./pages/FieldDashboard";
import { getUserFields, getFieldAlerts, getFieldSensors } from "./api/field";
import { mapFieldFromApi } from "./api/fieldMapper";

export default function App() {

  const [selectedField, setSelectedField] = useState(null);
  const [fields, setFields] = useState([]);
  const [fieldAlerts, setFieldAlerts] = useState({});
  const [fieldSensors, setFieldSensors] = useState({});

  useEffect(() => {
    getUserFields(3)
      .then(async (data) => {
        setFields(data.map(mapFieldFromApi));

        const alertResults = await Promise.all(
          data.map(async (field) => {
            const alerts = await getFieldAlerts(field.field_id);

            return [field.field_id, alerts];
          })
        );

        setFieldAlerts(Object.fromEntries(alertResults));
        console.log("Field alerts:", Object.fromEntries(alertResults));

        const sensorResults = await Promise.all(
          data.map(async (field) => {
            const sensors = await getFieldSensors(field.field_id);

            return [field.field_id, sensors];
          })
        );

        setFieldSensors(Object.fromEntries(sensorResults));
      })
      .catch((error) => {
        console.error("Failed to load fields:", error);
      });
  }, []);
  return (

    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans">

      <Header />


      {selectedField ? (

        <FieldDashboard
          field={selectedField}
          onBack={() => setSelectedField(null)}
        />

      ) : (

        <Home
          fields={fields}
          fieldAlerts={fieldAlerts}
          fieldSensors={fieldSensors}
          onSelectField={setSelectedField}
        />

      )}

    </div>

  );
}


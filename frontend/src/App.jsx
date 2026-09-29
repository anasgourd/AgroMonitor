import { useEffect, useState } from "react";

import Header from "./components/Header";
import Home from "./pages/Home";
import FieldDashboard from "./pages/FieldDashboard";
import { getFieldAlerts, getFieldSensors } from "./api/field";
import { mapFieldFromApi } from "./api/fieldMapper";
import Login from "./pages/Login";
import {
  login,
  getCurrentUser,
  getCurrentUserFields,
} from "./api/auth";
export default function App() {

  const [selectedField, setSelectedField] = useState(null);
  const [fields, setFields] = useState([]);
  const [fieldAlerts, setFieldAlerts] = useState({});
  const [fieldSensors, setFieldSensors] = useState({});

  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // Handle login and update authentication state.

  async function handleLogin(username, password) {
    try {
      const data = await login(username, password);

      console.log("Login successful:", data);
      // Store JWT so it can be used for authenticated API requests.
      localStorage.setItem("access_token", data.access_token);

      const user = await getCurrentUser();
      console.log("Current user:", user)

      setIsLoggedIn(true);
    } catch (error) {
      console.error("Login failed:", error);
    }
  }


  useEffect(() => {
    if (!isLoggedIn) {
      return;
    }
    getCurrentUserFields()
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
  }, [isLoggedIn]);
  // Show login page until the user is authenticated.
  if (!isLoggedIn) {
    return <Login onLogin={handleLogin} />;
  }
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


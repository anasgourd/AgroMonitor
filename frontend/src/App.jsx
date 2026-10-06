import { useEffect, useState } from "react";

import Header from "./components/Header";
import Home from "./pages/Home";
import FieldDashboard from "./pages/FieldDashboard";
import AddField from "./pages/AddField";
import EditField from "./pages/EditField";
import { deleteField } from "./api/field";
import DeleteField from "./pages/DeleteField";
import { getFieldAlerts, getFieldSensors } from "./api/field";
import { mapFieldFromApi } from "./api/fieldMapper";
import Login from "./pages/Login";
import {
  login,
  getCurrentUser,
  getCurrentUserFields,
} from "./api/auth";

import AddSensor from "./pages/AddSensor";

export default function App() {

  const [selectedField, setSelectedField] = useState(null);
  const [showAddField, setShowAddField] = useState(false);
  const [fields, setFields] = useState([]);
  const [fieldAlerts, setFieldAlerts] = useState({});
  const [fieldSensors, setFieldSensors] = useState({});

  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const [fieldToEdit, setFieldToEdit] = useState(null);


  const [fieldToDelete, setFieldToDelete] = useState(null);

  const [fieldToAddSensor, setFieldToAddSensor] = useState(null);

  const [dataVersion, setDataVersion] = useState(0);

  function handleFieldCreated(newField) {
    setFields((currentFields) => [
      ...currentFields,
      mapFieldFromApi(newField),
    ]);

    setShowAddField(false);
  }

  function handleEditField(field) {
    setFieldToEdit(field);
  }

  function handleAddSensor(field) {
    setSelectedField(null);
    setFieldToAddSensor(field);
  }

  function handleFieldUpdated(updatedField) {
    setFields((currentFields) =>
      currentFields.map((field) =>
        field.id === updatedField.field_id
          ? mapFieldFromApi(updatedField)
          : field
      )
    );

    setFieldToEdit(null);
  }

  async function handleFieldDeleted(fieldId) {
    await deleteField(fieldId);

    setFields((currentFields) =>
      currentFields.filter((field) => field.id !== fieldId)
    );

    setFieldToDelete(null);
  }


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
  }, [isLoggedIn, dataVersion]);
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
          onAddSensor={handleAddSensor}
        />
      ) : showAddField ? (
        <AddField
          onBack={() => setShowAddField(false)}
          onCreated={handleFieldCreated}
        />
      ) : fieldToEdit ? (
        <EditField
          field={fieldToEdit}
          onBack={() => setFieldToEdit(null)}
          onUpdated={handleFieldUpdated}
        />
      ) : fieldToAddSensor ? (
        <AddSensor
          field={fieldToAddSensor}
          onBack={() => setFieldToAddSensor(null)}
          onCreated={() => {
            setDataVersion((version) => version + 1);
            setFieldToAddSensor(null);
            setSelectedField(fieldToAddSensor);
          }}
        />
      ) : (
        <Home
          fields={fields}
          fieldAlerts={fieldAlerts}
          fieldSensors={fieldSensors}
          onSelectField={setSelectedField}
          onAddField={() => setShowAddField(true)}
          onEdit={handleEditField}
          onDelete={setFieldToDelete}
        />
      )}

      {fieldToDelete && (
        <DeleteField
          field={fieldToDelete}
          onCancel={() => setFieldToDelete(null)}
          onDeleted={handleFieldDeleted}
        />
      )}

    </div>

  );
}


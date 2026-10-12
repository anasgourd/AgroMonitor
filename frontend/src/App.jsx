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
import EditSensor from "./pages/EditSensor";
import DeleteSensor from "./pages/DeleteSensor";

export default function App() {

  const [selectedField, setSelectedField] = useState(null);
  const [showAddField, setShowAddField] = useState(false);
  const [fields, setFields] = useState([]);
  const [fieldAlerts, setFieldAlerts] = useState({});
  const [fieldSensors, setFieldSensors] = useState({});

  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const [isCheckingAuth, setIsCheckingAuth] = useState(true);

  const [fieldToEdit, setFieldToEdit] = useState(null);


  const [fieldToDelete, setFieldToDelete] = useState(null);

  const [fieldToAddSensor, setFieldToAddSensor] = useState(null);

  //which sensor you edit
  const [sensorToEdit, setSensorToEdit] = useState(null);

  // in witch field you are
  const [fieldForSensorEdit, setFieldForSensorEdit] = useState(null);

  const [sensorToDelete, setSensorToDelete] = useState(null);
  const [fieldForSensorDelete, setFieldForSensorDelete] = useState(null);

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


  function handleDeleteSensor(sensor) {
    setFieldForSensorDelete(selectedField);
    setSelectedField(null);
    setSensorToDelete(sensor);
  }


  function handleLogout() {
    localStorage.removeItem("access_token");

    setIsLoggedIn(false);
    setSelectedField(null);
    setShowAddField(false);

    setFields([]);
    setFieldAlerts({});
    setFieldSensors({});

    setFieldToEdit(null);
    setFieldToDelete(null);
    setFieldToAddSensor(null);

    setSensorToEdit(null);
    setFieldForSensorEdit(null);
    setSensorToDelete(null);
    setFieldForSensorDelete(null);
  }

  function handleGoHome() {
    setSelectedField(null);
    setShowAddField(false);
    setFieldToEdit(null);
    setFieldToDelete(null);
    setFieldToAddSensor(null);
    setSensorToEdit(null);
    setFieldForSensorEdit(null);
    setSensorToDelete(null);
    setFieldForSensorDelete(null);
  }


  // Handle login and update authentication state.


  async function handleLogin(username, password) {
    try {
      const data = await login(username, password);

      localStorage.setItem("access_token", data.access_token);

      await getCurrentUser();
      setIsLoggedIn(true);

      return true;
    } catch (error) {
      console.error("Login failed:", error);

      localStorage.removeItem("access_token");
      setIsLoggedIn(false);

      return false;
    }
  }


  function handleEditSensor(sensor) {
    setFieldForSensorEdit(selectedField);
    setSelectedField(null);
    setSensorToEdit(sensor);
  }


  useEffect(() => {
    async function checkAuthentication() {
      const token = localStorage.getItem("access_token");

      if (!token) {
        setIsLoggedIn(false);
        setIsCheckingAuth(false);
        return;
      }

      try {
        await getCurrentUser();
        setIsLoggedIn(true);
      } catch (error) {
        localStorage.removeItem("access_token");
        setIsLoggedIn(false);
      } finally {
        setIsCheckingAuth(false);
      }
    }

    checkAuthentication();
  }, []);


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
  // Check authentication before rendering the application.
  if (isCheckingAuth) {
    return <div>Checking session...</div>;
  }

  if (!isLoggedIn) {
    return <Login onLogin={handleLogin} />;
  }
  return (

    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans">

      <Header
        onLogout={handleLogout}
        onHome={handleGoHome}
      />


      {selectedField ? (
        <FieldDashboard
          field={selectedField}
          onBack={() => setSelectedField(null)}
          onAddSensor={handleAddSensor}
          onEditSensor={handleEditSensor}
          onDeleteSensor={handleDeleteSensor}
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
      ) : sensorToEdit ? (
        <EditSensor
          sensor={sensorToEdit}
          onBack={() => {
            setSensorToEdit(null);
            setSelectedField(fieldForSensorEdit);
            setFieldForSensorEdit(null);
          }}
          onUpdated={() => {
            //edit sensor page closes
            setSensorToEdit(null);
            //return to the field from where it started
            setSelectedField(fieldForSensorEdit);
            setFieldForSensorEdit(null);
            //dataversion increases so App reloads the data
            setDataVersion((version) => version + 1);
          }}
        />
      ) : sensorToDelete ? (
        <DeleteSensor
          sensor={sensorToDelete}
          onBack={() => {
            setSensorToDelete(null);
            setSelectedField(fieldForSensorDelete);
            setFieldForSensorDelete(null);
          }}
          onDeleted={() => {
            setSensorToDelete(null);
            setSelectedField(fieldForSensorDelete);
            setFieldForSensorDelete(null);
            setDataVersion((version) => version + 1);
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


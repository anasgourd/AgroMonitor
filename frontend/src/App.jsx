import { useEffect, useState } from "react";

import Header from "./components/Header";
import Home from "./pages/Home";
import FieldDashboard from "./pages/FieldDashboard";
import { getUserFields } from "./api/field";
import { mapFieldFromApi } from "./api/fieldMapper";

export default function App() {

  const [selectedField, setSelectedField] = useState(null);
  const [fields, setFields] = useState([]);
  useEffect(() => {
    getUserFields(3)
      .then((data) => {
        setFields(data.map(mapFieldFromApi));
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
          onSelectField={setSelectedField}
        />

      )}

    </div>

  );
}


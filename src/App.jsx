import { useState } from "react";

import Header from "./components/Header";
import Home from "./pages/Home";
import FieldDashboard from "./pages/FieldDashboard";

import { fields } from "./data/fields";


export default function App() {

  const [selectedField, setSelectedField] = useState(null);


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
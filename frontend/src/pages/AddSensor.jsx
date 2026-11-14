import AddSensorForm from "../components/FieldDashboard/AddSensorForm";

export default function AddSensor({
    field,
    onBack,
    onCreated,
}) {
    return (
        <main className="min-h-screen bg-emerald-50 px-4 sm:px-6 lg:px-8 py-6">
            <div className="max-w-3xl mx-auto">

                <button
                    onClick={onBack}
                    className="mb-6 px-4 py-2 rounded-xl bg-white text-amber-900 font-semibold shadow"
                >
                    Back
                </button>

                <div className="bg-white rounded-2xl shadow p-6">
                    <AddSensorForm
                        field={field}
                        onCreated={onCreated}
                        onCancel={onBack}
                    />
                </div>

            </div>
        </main>
    );
}
import AddFieldForm from "../components/AddFieldForm";

export default function AddField({ onBack, onCreated }) {
    return (
        <main className="min-h-screen bg-emerald-50 px-6 py-8">

            <div className="max-w-2xl mx-auto">

                <button
                    onClick={onBack}
                    className="text-sm font-medium text-emerald-700 hover:text-emerald-900 mb-8"
                >
                    ← Back to fields
                </button>

                <div className="bg-white rounded-2xl shadow-sm border border-emerald-100 p-8">

                    <p className="text-xs font-semibold tracking-[0.2em] text-amber-900 uppercase">
                        FIELD MANAGEMENT
                    </p>

                    <h1 className="text-3xl font-semibold text-emerald-950 mt-2">
                        Add a new field
                    </h1>

                    <p className="text-emerald-700 mt-2 mb-8">
                        Add your field information to start monitoring it.
                    </p>

                    <AddFieldForm
                        onCancel={onBack}
                        onCreated={onCreated}
                    />
                </div>

            </div>

        </main>
    );
}
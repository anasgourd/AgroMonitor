import { ArrowLeft } from "lucide-react";

export default function FieldHeader({
    name,
    status,
    statusStyle,
    onBack,
}) {
    return (
        <>
            <button
                onClick={onBack}
                className="inline-flex items-center gap-2 text-sm font-semibold text-amber-900 hover:text-emerald-700 transition-colors mb-6"
            >
                <ArrowLeft size={18} />
                Back to My Fields
            </button>

            <section className="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-5 mb-8">

                <div>
                    <p className="text-xs font-semibold tracking-[0.2em] text-amber-900 uppercase">
                        FIELD DASHBOARD
                    </p>

                    <h1 className="text-4xl font-black text-amber-900 mt-2 tracking-tight">
                        {name}
                    </h1>

                    <p className="text-lg text-emerald-700 mt-2 font-light italic">
                        Live field monitoring & historical analysis
                    </p>
                </div>

                <div
                    className={`inline-flex items-center gap-2 self-start lg:self-auto px-4 py-2 rounded-full border text-sm font-semibold ${statusStyle.badge}`}
                >
                    <span
                        className={`w-2.5 h-2.5 rounded-full ${statusStyle.dot}`}
                    />

                    {status}
                </div>

            </section>
        </>
    );
}
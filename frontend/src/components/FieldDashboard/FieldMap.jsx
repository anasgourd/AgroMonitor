import { MapPin } from "lucide-react";

export default function FieldMap({ area }) {
    return (
        <div className="lg:col-span-3 bg-white/75 rounded-3xl border border-emerald-100 shadow-sm overflow-hidden">

            <div className="p-5 flex items-center justify-between">

                <div>
                    <p className="text-xs font-semibold tracking-[0.2em] text-emerald-700 uppercase">
                        LOCATION
                    </p>

                    <h2 className="text-xl font-bold text-amber-900 mt-1">
                        Field Map
                    </h2>
                </div>

                <div className="flex items-center gap-2 text-xs text-emerald-800 font-semibold">
                    <MapPin size={16} />
                    Live position
                </div>

            </div>

            <div className="mx-5 mb-5 h-[320px] rounded-2xl overflow-hidden relative bg-gradient-to-br from-emerald-200 via-lime-100 to-amber-100">

                {/* όλο το υπόλοιπο map JSX */}

                <div className="absolute bottom-4 left-4 bg-white/80 backdrop-blur-md rounded-xl px-4 py-3 shadow-sm">

                    <p className="text-xs text-gray-500 uppercase tracking-wider font-semibold">
                        Area
                    </p>

                    <p className="text-lg font-bold text-amber-900">
                        {area}
                    </p>

                </div>

            </div>

        </div>
    );
}
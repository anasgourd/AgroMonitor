import { Sprout } from "lucide-react";

export default function Header() {
  return (
    <header className="bg-slate-50 border-b border-gray-200 px-6 py-4 flex items-center justify-between shadow-sm">

      {/* Logo */}
      <div className="flex items-center gap-3">

        <div className="flex items-center justify-center w-11 h-11 rounded-xl bg-emerald-100 text-emerald-700">
          <Sprout size={22} strokeWidth={1.8} />
        </div>

        <div className="flex flex-col">

          <strong className="text-2xl font-black leading-none tracking-tight">
            <span className="text-amber-900">AGRO</span>
            <span className="text-emerald-700">MONITOR</span>
          </strong>

          <span className="text-xs text-emerald-600 font-medium mt-1">
            Smart Agriculture
          </span>

        </div>

      </div>


      {/* User */}
      <div className="flex items-center gap-3">

        <div className="w-10 h-10 bg-emerald-600 text-white rounded-full flex items-center justify-center font-bold shadow-md shadow-emerald-100">
          A
        </div>

        <div className="hidden sm:flex flex-col">

          <strong className="text-sm font-semibold text-gray-800">
            Anastasis
          </strong>

          <span className="text-xs text-gray-500">
            Field Manager
          </span>

        </div>

      </div>

    </header>
  );
}

import { Sprout, LogOut } from "lucide-react";

export default function Header({ onLogout, onHome }) {
  return (
    <header className="bg-slate-50 border-b border-gray-200 px-6 py-4 flex items-center justify-between shadow-sm">
      {/* Logo */}

      {/* Logo */}
      <button
        type="button"
        onClick={onHome}
        className="flex items-center gap-3 text-left cursor-pointer"
        title="Go to Home"
      >
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
      </button>


      {/* User and Logout */}
      <div className="flex items-center gap-4">
        <div className="hidden sm:flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-500" />
          <span className="text-sm font-semibold text-emerald-700">
            System Online
          </span>
        </div>


        <button
          onClick={onLogout}
          className="flex items-center gap-2 px-3 py-2 rounded-lg border border-gray-200 text-gray-600 hover:bg-red-50 hover:text-red-600 hover:border-red-200 transition-colors"
          title="Logout"
        >
          <LogOut size={18} />
          <span className="hidden sm:inline text-sm font-medium">
            Logout
          </span>
        </button>
      </div>
    </header >
  );
}

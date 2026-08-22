export default function Header() {
  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between shadow-sm">

      {/* Logo */}
      <div className="flex items-center gap-3">

        <div className="text-3xl bg-emerald-50 p-2 rounded-xl">
          🌱
        </div>

        <div className="flex flex-col">

          <strong className="text-lg font-bold text-gray-800 leading-none">
            AgroMonitor
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
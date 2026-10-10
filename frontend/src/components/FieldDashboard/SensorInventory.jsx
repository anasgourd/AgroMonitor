import { Droplets, Thermometer } from "lucide-react";
import SensorList from "./SensorList";


export default function SensorInventory({
    temperatureSensors,
    onEditSensor,
}) {
    return (
        <section className="mb-8">

            <div className="mb-5">
                <p className="text-xs font-semibold tracking-[0.2em] text-emerald-700 uppercase">
                    SENSOR NETWORK
                </p>

                <h2 className="text-2xl font-black text-amber-900 mt-1">
                    Connected sensors
                </h2>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">

                <SensorList
                    title="Temperature"
                    sensors={temperatureSensors}
                    icon={<Thermometer size={21} className="text-rose-700" />}
                    iconBackground="bg-rose-100"
                    sensorLetter="T"
                    sensorTextColor="text-rose-700"
                    sensorBackground="bg-rose-50"
                    sensorDescription="Temperature sensor"
                    onEdit={onEditSensor}
                />

            </div>

        </section>
    );
}
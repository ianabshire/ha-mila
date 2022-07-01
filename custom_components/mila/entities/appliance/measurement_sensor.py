from typing import List, Optional
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from milasdk import ApplianceSensorKind

from ...const import DOMAIN
from ...devices import MilaAppliance
from .sensor import MilaApplianceSensor

class MilaApplianceMeasurementSensor(MilaApplianceSensor):
    def __init__(
        self, 
        device: MilaAppliance, 
        name: str,
        sensor_kind: ApplianceSensorKind,
        icon: Optional[str] = None, 
        uom: Optional[str] = None,
        device_class: Optional[SensorDeviceClass] = None
    ):
        super().__init__(device, name, icon, uom, device_class, SensorStateClass.MEASUREMENT)
        self._sensor_kind = sensor_kind

    @property
    def unique_id(self) -> str:
        return f"{DOMAIN}_{self.device.id}_sensor_{self._sensor_kind}".lower()  

    @property
    def native_value(self):
        sensors: List = self.device.get_value("sensors")
        sensor = next((i for i in sensors if i["kind"] == self._sensor_kind), None)
        return sensor["latest"]["value"] if sensor else None

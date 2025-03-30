from __future__ import annotations

from .device import DeviceController
from ....control.controllers import CommunicationController
from ....utils.injector_types import (
    Draw,
    Inject,
    InjectorTable,
    Mode,
    Remote,
    RemoteCommand,
    SourceType,
    Wait,
)
from ....utils.table_types import RegisterFlag, Table
from ....utils.tray_types import Tray


class InjectorController(DeviceController):

    def __init__(self, controller: CommunicationController, table: Table, offline: bool):
        super().__init__(controller, table, offline)

    def get_row(self, row: int) -> None | Remote | Draw | Wait | Inject:
        def return_tray_loc() -> Tray:
            pass

        function = self.get_text(row, RegisterFlag.FUNCTION)
        if function == "Wait":
            return Wait(duration=self.get_num(row, RegisterFlag.TIME))
        elif function == "Inject":
            return Inject()
        elif function == "Draw":
            # TODO: better error handling
            is_source = SourceType(self.get_text(row, RegisterFlag.DRAW_SOURCE))
            is_volume = Mode(self.get_text(row, RegisterFlag.DRAW_VOLUME))
            vol = self.get_num(row, RegisterFlag.DRAW_VOLUME_VALUE) if is_volume == Mode.SET else None
            if is_source is SourceType.SPECIFIC_LOCATION:
                return Draw(amount=vol, source=return_tray_loc())
            elif is_source is SourceType.LOCATION:
                return Draw(amount=vol, location=self.get_text(row, RegisterFlag.DRAW_LOCATION))
        elif function == "Remote":
            return Remote(command=RemoteCommand(self.get_text(row, RegisterFlag.REMOTE)),
                          duration=self.get_num(row, RegisterFlag.REMOTE_DUR))

    def load(self) -> InjectorTable | None:
        rows = self.get_num_rows()
        if rows.is_ok():
            return InjectorTable(functions=[self.get_row(i) for i in range(int(rows.ok_value.num_response))])

   
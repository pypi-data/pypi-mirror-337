import abc
from typing import List, Union, Dict, Optional

from result import Result

from ....analysis.process_report import AgilentReport, ReportType
from ....control.controllers import CommunicationController
from ....control.controllers.tables.table import TableController
from pychemstation.analysis.chromatogram import (
    AgilentChannelChromatogramData,
    AgilentHPLCChromatogram,
)
from ....utils.table_types import T, Table


class DeviceController(TableController, abc.ABC):
    def __init__(
        self, controller: CommunicationController, table: Table, offline: bool
    ):
        super().__init__(
            controller=controller, src=None, data_dirs=[], table=table, offline=offline
        )

    @abc.abstractmethod
    def get_row(self, row: int):
        pass

    def retrieve_recent_data_files(self):
        raise NotImplementedError

    def fuzzy_match_most_recent_folder(self, most_recent_folder: T) -> Result[T, str]:
        raise NotImplementedError

    def get_report(
        self, report_type: ReportType = ReportType.TXT
    ) -> List[AgilentReport]:
        raise NotImplementedError

    def get_data_uv(
        self,
    ) -> Union[
        List[Dict[str, AgilentHPLCChromatogram]], Dict[str, AgilentHPLCChromatogram]
    ]:
        raise NotImplementedError

    def get_data(
        self, custom_path: Optional[str] = None
    ) -> Union[List[AgilentChannelChromatogramData], AgilentChannelChromatogramData]:
        raise NotImplementedError

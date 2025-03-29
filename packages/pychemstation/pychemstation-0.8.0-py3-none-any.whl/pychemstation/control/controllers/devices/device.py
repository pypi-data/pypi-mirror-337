import abc
from typing import Union, List

from result import Result

from ....analysis.process_report import ReportType, AgilentReport
from ....control.controllers import CommunicationController
from ....control.controllers.tables.table import TableController
from ....utils.chromatogram import AgilentChannelChromatogramData
from ....utils.table_types import Table, T


class DeviceController(TableController, abc.ABC):

    def __init__(self, controller: CommunicationController, table: Table, offline: bool):
        super().__init__(controller=controller,
                         src=None,
                         data_dirs=[],
                         table=table,
                         offline=offline)

    @abc.abstractmethod
    def get_row(self, row: int):
        pass

    def retrieve_recent_data_files(self):
        raise NotImplementedError

    def get_data(self) -> Union[List[AgilentChannelChromatogramData], AgilentChannelChromatogramData]:
        raise NotImplementedError

    def fuzzy_match_most_recent_folder(self, most_recent_folder: T) -> Result[T, str]:
        raise NotImplementedError

    def get_report(self, report_type: ReportType = ReportType.TXT) -> List[AgilentReport]:
        raise NotImplementedError

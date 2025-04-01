"""
Abstract module containing shared logic for Method and Sequence tables.

Authors: Lucy Hao
"""

from __future__ import annotations

import abc
import math
import os
import time
import warnings
from typing import Dict, List, Optional, Tuple, Union

import polling
import rainbow as rb
from result import Err, Result, Ok

from ....analysis.process_report import (
    AgilentReport,
    CSVProcessor,
    ReportType,
    TXTProcessor,
)
from ....control.controllers.comm import CommunicationController
from pychemstation.analysis.chromatogram import (
    AgilentChannelChromatogramData,
    AgilentHPLCChromatogram,
)
from ....utils.macro import Command, HPLCRunningStatus, Response
from ....utils.method_types import MethodDetails
from ....utils.sequence_types import SequenceTable
from ....utils.table_types import RegisterFlag, T, Table, TableOperation

TableType = Union[MethodDetails, SequenceTable]


class TableController(abc.ABC):
    def __init__(
        self,
        controller: CommunicationController,
        src: Optional[str],
        data_dirs: Optional[List[str]],
        table: Table,
        offline: bool = False,
    ):
        self.controller = controller
        self.table_locator = table
        self.table_state: Optional[TableType] = None
        self.curr_run_starting_time: Optional[float] = None
        self.timeout: Optional[float] = None

        if not offline:
            if src and not os.path.isdir(src):
                raise FileNotFoundError(f"dir: {src} not found.")

            for d in data_dirs:
                if not os.path.isdir(d):
                    raise FileNotFoundError(f"dir: {d} not found.")
                if r"\\" in d:
                    raise ValueError("Data directories should not be raw strings!")
            self.src: str = src
            self.data_dirs: List[str] = data_dirs

        self.spectra: dict[str, Optional[AgilentHPLCChromatogram]] = {
            "A": AgilentHPLCChromatogram(),
            "B": AgilentHPLCChromatogram(),
            "C": AgilentHPLCChromatogram(),
            "D": AgilentHPLCChromatogram(),
            "E": AgilentHPLCChromatogram(),
            "F": AgilentHPLCChromatogram(),
            "G": AgilentHPLCChromatogram(),
            "H": AgilentHPLCChromatogram(),
        }
        self.report: Optional[AgilentReport] = None
        self.uv: Dict[int, AgilentHPLCChromatogram] = {}
        self.data_files: List = []

    def receive(self) -> Result[Response, str]:
        for _ in range(10):
            try:
                return self.controller.receive()
            except IndexError:
                continue
        return Err("Could not parse response")

    def send(self, cmd: Union[Command, str]):
        if not self.controller:
            raise RuntimeError(
                "Communication controller must be initialized before sending command. It is currently in offline mode."
            )
        self.controller.send(cmd)

    def sleepy_send(self, cmd: Union[Command, str]):
        self.controller.sleepy_send(cmd)

    def sleep(self, seconds: int):
        """
        Tells the HPLC to wait for a specified number of seconds.

        :param seconds: number of seconds to wait
        """
        self.send(Command.SLEEP_CMD.value.format(seconds=seconds))

    def get_num(self, row: int, col_name: RegisterFlag) -> Union[int, float]:
        return self.controller.get_num_val(
            TableOperation.GET_ROW_VAL.value.format(
                register=self.table_locator.register,
                table_name=self.table_locator.name,
                row=row,
                col_name=col_name.value,
            )
        )

    def get_text(self, row: int, col_name: RegisterFlag) -> str:
        return self.controller.get_text_val(
            TableOperation.GET_ROW_TEXT.value.format(
                register=self.table_locator.register,
                table_name=self.table_locator.name,
                row=row,
                col_name=col_name.value,
            )
        )

    def add_new_col_num(self, col_name: RegisterFlag, val: Union[int, float]):
        self.sleepy_send(
            TableOperation.NEW_COL_VAL.value.format(
                register=self.table_locator.register,
                table_name=self.table_locator.name,
                col_name=col_name,
                val=val,
            )
        )

    def add_new_col_text(self, col_name: RegisterFlag, val: str):
        self.sleepy_send(
            TableOperation.NEW_COL_TEXT.value.format(
                register=self.table_locator.register,
                table_name=self.table_locator.name,
                col_name=col_name,
                val=val,
            )
        )

    def _edit_row_num(
        self, col_name: RegisterFlag, val: Union[int, float], row: Optional[int] = None
    ):
        self.sleepy_send(
            TableOperation.EDIT_ROW_VAL.value.format(
                register=self.table_locator.register,
                table_name=self.table_locator.name,
                row=row if row is not None else "Rows",
                col_name=col_name,
                val=val,
            )
        )

    def _edit_row_text(
        self, col_name: RegisterFlag, val: str, row: Optional[int] = None
    ):
        self.sleepy_send(
            TableOperation.EDIT_ROW_TEXT.value.format(
                register=self.table_locator.register,
                table_name=self.table_locator.name,
                row=row if row is not None else "Rows",
                col_name=col_name,
                val=val,
            )
        )

    @abc.abstractmethod
    def get_row(self, row: int):
        pass

    def delete_row(self, row: int):
        self.sleepy_send(
            TableOperation.DELETE_ROW.value.format(
                register=self.table_locator.register,
                table_name=self.table_locator.name,
                row=row,
            )
        )

    def add_row(self):
        """
        Adds a row to the provided table for currently loaded method or sequence.
        """
        self.sleepy_send(
            TableOperation.NEW_ROW.value.format(
                register=self.table_locator.register, table_name=self.table_locator.name
            )
        )

    def delete_table(self):
        """
        Deletes the table for the current loaded method or sequence.
        """
        self.sleepy_send(
            TableOperation.DELETE_TABLE.value.format(
                register=self.table_locator.register, table_name=self.table_locator.name
            )
        )

    def new_table(self):
        """
        Creates the table for the currently loaded method or sequence.
        """
        self.send(
            TableOperation.CREATE_TABLE.value.format(
                register=self.table_locator.register, table_name=self.table_locator.name
            )
        )

    def get_num_rows(self) -> Result[Response, str]:
        self.send(
            TableOperation.GET_NUM_ROWS.value.format(
                register=self.table_locator.register,
                table_name=self.table_locator.name,
                col_name=RegisterFlag.NUM_ROWS,
            )
        )
        self.send(
            Command.GET_ROWS_CMD.value.format(
                register=self.table_locator.register,
                table_name=self.table_locator.name,
                col_name=RegisterFlag.NUM_ROWS,
            )
        )
        res = self.controller.receive()

        if res.is_ok():
            self.send("Sleep 0.1")
            self.send("Print Rows")
            return res
        else:
            return Err("No rows could be read.")

    def check_hplc_is_running(self) -> bool:
        try:
            started_running = polling.poll(
                lambda: isinstance(self.controller.get_status(), HPLCRunningStatus),
                step=1,
                max_tries=20,
            )
        except Exception as e:
            print(e)
            return False
        if started_running:
            self.curr_run_starting_time = time.time()
        return started_running

    def check_hplc_run_finished(self) -> Tuple[float, bool]:
        done_running = self.controller.check_if_not_running()
        if self.curr_run_starting_time and self.timeout:
            time_passed = time.time() - self.curr_run_starting_time
            if time_passed > self.timeout:
                enough_time_passed = time_passed >= self.timeout
                run_finished = enough_time_passed and done_running
                if run_finished:
                    self._reset_time()
                    return 0, run_finished
            else:
                time_left = self.timeout - time_passed
                return time_left, self.controller.check_if_not_running()
        return 0, self.controller.check_if_not_running()

    def check_hplc_done_running(self) -> Ok[T] | Err[str]:
        """
        Checks if ChemStation has finished running and can read data back

        :return: Data file object containing most recent run file information.
        """
        finished_run = False
        minutes = math.ceil(self.timeout / 60)
        try:
            finished_run = not polling.poll(
                lambda: self.check_hplc_run_finished()[1],
                max_tries=minutes - 1,
                step=50,
            )
        except (
            polling.TimeoutException,
            polling.PollingException,
            polling.MaxCallException,
        ):
            try:
                finished_run = polling.poll(
                    lambda: self.check_hplc_run_finished()[1],
                    timeout=self.timeout / 2,
                    step=1,
                )
            except (
                polling.TimeoutException,
                polling.PollingException,
                polling.MaxCallException,
            ):
                pass

        check_folder = self.fuzzy_match_most_recent_folder(self.data_files[-1])
        if check_folder.is_ok() and finished_run:
            return check_folder
        elif check_folder.is_ok():
            try:
                finished_run = polling.poll(
                    lambda: self.check_hplc_run_finished()[1], max_tries=10, step=50
                )
                if finished_run:
                    return check_folder
            except Exception:
                self._reset_time()
                return self.data_files[-1]
        return Err("Run did not complete as expected")

    @abc.abstractmethod
    def fuzzy_match_most_recent_folder(self, most_recent_folder: T) -> Result[T, str]:
        pass

    @abc.abstractmethod
    def get_data(
        self, custom_path: Optional[str] = None
    ) -> Union[List[AgilentChannelChromatogramData], AgilentChannelChromatogramData]:
        pass

    @abc.abstractmethod
    def get_data_uv(
        self,
    ) -> Union[
        List[Dict[str, AgilentHPLCChromatogram]], Dict[str, AgilentHPLCChromatogram]
    ]:
        pass

    @abc.abstractmethod
    def get_report(
        self, report_type: ReportType = ReportType.TXT
    ) -> List[AgilentReport]:
        pass

    def get_uv_spectrum(self, path: str):
        data_uv = rb.agilent.chemstation.parse_file(os.path.join(path, "DAD1.UV"))
        times = data_uv.xlabels
        wavelengths = data_uv.ylabels
        absorbances = data_uv.data.transpose()
        for i, w in enumerate(wavelengths):
            self.uv[w] = AgilentHPLCChromatogram()
            self.uv[w].attach_spectrum(times, absorbances[i])

    def get_report_details(
        self, path: str, report_type: ReportType = ReportType.TXT
    ) -> AgilentReport:
        if report_type is ReportType.TXT:
            txt_report = TXTProcessor(path).process_report()
            if txt_report.is_ok():
                self.report = txt_report.ok_value
        if report_type is ReportType.CSV:
            csv_report = CSVProcessor(path).process_report()
            if csv_report.is_ok():
                self.report = csv_report.ok_value
        return self.report

    def get_spectrum_at_channels(self, data_path: str):
        """
        Load chromatogram for any channel in spectra dictionary.
        """
        for channel, spec in self.spectra.items():
            try:
                spec.load_spectrum(data_path=data_path, channel=channel)
            except FileNotFoundError:
                self.spectra[channel] = AgilentHPLCChromatogram()
                warning = f"No data at channel: {channel}"
                warnings.warn(warning)

    def _reset_time(self):
        self.curr_run_starting_time = None
        self.timeout = None

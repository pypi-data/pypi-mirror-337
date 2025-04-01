import os
import time
import warnings
from typing import Dict, List, Optional

from result import Err, Ok, Result
from typing_extensions import override

from ....analysis.process_report import AgilentReport, ReportType
from ....control.controllers.comm import CommunicationController
from pychemstation.analysis.chromatogram import (
    SEQUENCE_TIME_FORMAT,
    AgilentChannelChromatogramData,
    AgilentHPLCChromatogram,
)
from ....utils.macro import Command
from ....utils.sequence_types import (
    InjectionSource,
    SampleType,
    SequenceDataFiles,
    SequenceEntry,
    SequenceTable,
)
from ....utils.table_types import RegisterFlag, Table
from ....utils.tray_types import FiftyFourVialPlate, TenVialColumn
from .. import MethodController
from .table import TableController


class SequenceController(TableController):
    """
    Class containing sequence related logic
    """

    def __init__(
        self,
        controller: CommunicationController,
        method_controller: MethodController,
        src: str,
        data_dirs: List[str],
        table: Table,
        offline: bool,
    ):
        self.method_controller = method_controller
        self.data_files: List[SequenceDataFiles] = []
        super().__init__(
            controller=controller,
            src=src,
            data_dirs=data_dirs,
            table=table,
            offline=offline,
        )

    def load(self) -> SequenceTable:
        rows = self.get_num_rows()
        self.send(Command.GET_SEQUENCE_CMD)
        seq_name = self.receive()

        if rows.is_ok() and seq_name.is_ok():
            self.table_state = SequenceTable(
                name=seq_name.ok_value.string_response.partition(".S")[0],
                rows=[
                    self.get_row(r + 1) for r in range(int(rows.ok_value.num_response))
                ],
            )
            return self.table_state
        raise RuntimeError(rows.err_value)

    def get_row(self, row: int) -> SequenceEntry:
        sample_name = self.get_text(row, RegisterFlag.NAME)
        vial_location = int(self.get_num(row, RegisterFlag.VIAL_LOCATION))
        method = self.get_text(row, RegisterFlag.METHOD)
        num_inj = int(self.get_num(row, RegisterFlag.NUM_INJ))
        inj_vol = float(self.get_text(row, RegisterFlag.INJ_VOL))
        inj_source = InjectionSource(self.get_text(row, RegisterFlag.INJ_SOR))
        sample_type = SampleType(self.get_num(row, RegisterFlag.SAMPLE_TYPE))
        vial_enum = (
            TenVialColumn(vial_location)
            if vial_location <= 10
            else FiftyFourVialPlate.from_int(num=vial_location)
        )
        return SequenceEntry(
            sample_name=sample_name,
            vial_location=vial_enum,
            method=None if len(method) == 0 else method,
            num_inj=num_inj,
            inj_vol=inj_vol,
            inj_source=inj_source,
            sample_type=sample_type,
        )

    def check(self) -> str:
        time.sleep(2)
        self.send(Command.GET_SEQUENCE_CMD)
        time.sleep(2)
        res = self.receive()
        if res.is_ok():
            return res.ok_value.string_response
        return "ERROR"

    def switch(self, seq_name: str):
        """
        Switch to the specified sequence. The sequence name does not need the '.S' extension.

        :param seq_name: The name of the sequence file
        """
        self.send(f'_SeqFile$ = "{seq_name}.S"')
        self.send(f'_SeqPath$ = "{self.src}"')
        self.send(Command.SWITCH_SEQUENCE_CMD)
        time.sleep(2)
        self.send(Command.GET_SEQUENCE_CMD)
        time.sleep(2)
        parsed_response = self.receive().ok_value.string_response

        assert parsed_response == f"{seq_name}.S", "Switching sequence failed."
        self.table_state = None

    def edit(self, sequence_table: SequenceTable):
        """
        Updates the currently loaded sequence table with the provided table. This method will delete the existing sequence table and remake it.
        If you would only like to edit a single row of a sequence table, use `edit_sequence_table_row` instead.

        :param sequence_table:
        """
        self.table_state = sequence_table
        rows = self.get_num_rows()
        if rows.is_ok():
            existing_row_num = rows.ok_value.num_response
            wanted_row_num = len(sequence_table.rows)
            while existing_row_num != wanted_row_num:
                if wanted_row_num > existing_row_num:
                    self.add_row()
                elif wanted_row_num < existing_row_num:
                    self.delete_row(int(existing_row_num))
                self.send(Command.SAVE_SEQUENCE_CMD)
                existing_row_num = self.get_num_rows().ok_value.num_response
            self.send(Command.SWITCH_SEQUENCE_CMD)

            for i, row in enumerate(sequence_table.rows):
                self._edit_row(row=row, row_num=i + 1)
                self.sleep(1)
            self.send(Command.SAVE_SEQUENCE_CMD)
            self.send(Command.SWITCH_SEQUENCE_CMD)

    def _edit_row(self, row: SequenceEntry, row_num: int):
        """
        Edits a row in the sequence table. If a row does NOT exist, a new one will be created.

        :param row: sequence row entry with updated information
        :param row_num: the row to edit, based on 1-based indexing
        """
        num_rows = self.get_num_rows()
        if num_rows.is_ok():
            while num_rows.ok_value.num_response < row_num:
                self.add_row()
                self.send(Command.SAVE_SEQUENCE_CMD)
                num_rows = self.get_num_rows()
        if row.vial_location:
            loc = row.vial_location
            if isinstance(loc, TenVialColumn):
                loc = row.vial_location.value
            elif isinstance(loc, FiftyFourVialPlate):
                loc = row.vial_location.value()
            self._edit_row_num(
                row=row_num, col_name=RegisterFlag.VIAL_LOCATION, val=loc
            )
        if row.method:
            method_dir = self.method_controller.src
            possible_path = os.path.join(method_dir, row.method) + ".M\\"
            method = row.method
            if os.path.exists(possible_path):
                method = os.path.join(method_dir, row.method)
            self._edit_row_text(row=row_num, col_name=RegisterFlag.METHOD, val=method)
        if row.num_inj:
            self._edit_row_num(
                row=row_num, col_name=RegisterFlag.NUM_INJ, val=row.num_inj
            )
        if row.inj_vol:
            self._edit_row_text(
                row=row_num, col_name=RegisterFlag.INJ_VOL, val=row.inj_vol
            )
        if row.inj_source:
            self._edit_row_text(
                row=row_num, col_name=RegisterFlag.INJ_SOR, val=row.inj_source.value
            )
        if row.sample_name:
            self._edit_row_text(
                row=row_num, col_name=RegisterFlag.NAME, val=row.sample_name
            )
            if row.data_file:
                self._edit_row_text(
                    row=row_num, col_name=RegisterFlag.DATA_FILE, val=row.data_file
                )
            else:
                self._edit_row_text(
                    row=row_num, col_name=RegisterFlag.DATA_FILE, val=row.sample_name
                )
        if row.sample_type:
            self._edit_row_num(
                row=row_num,
                col_name=RegisterFlag.SAMPLE_TYPE,
                val=row.sample_type.value,
            )

        self.send(Command.SAVE_SEQUENCE_CMD)

    def run(self, stall_while_running: bool = True):
        """
        Starts the currently loaded sequence, storing data
        under the <data_dir>/<sequence table name> folder.
        Device must be ready.
        """
        self.controller.send(Command.SAVE_METHOD_CMD)
        self.controller.send(Command.SAVE_SEQUENCE_CMD)

        if not self.table_state:
            self.table_state = self.load()

        total_runtime = 0
        for entry in self.table_state.rows:
            curr_method_runtime = self.method_controller.get_total_runtime()
            loaded_method = self.method_controller.get_method_name().removesuffix(".M")
            method_path = entry.method.split(sep="\\")
            method_name = method_path[-1]
            if loaded_method != method_name:
                method_dir = (
                    "\\".join(method_path[:-1]) + "\\" if len(method_path) > 1 else None
                )
                self.method_controller.switch(
                    method_name=method_name, alt_method_dir=method_dir
                )
                curr_method_runtime = self.method_controller.get_total_runtime()
            total_runtime += curr_method_runtime

        timestamp = time.strftime(SEQUENCE_TIME_FORMAT)
        self.send(Command.RUN_SEQUENCE_CMD.value)
        self.timeout = total_runtime * 60

        if self.check_hplc_is_running():
            folder_name = f"{self.table_state.name} {timestamp}"
            data_file = SequenceDataFiles(
                dir=folder_name, sequence_name=self.table_state.name
            )
            self.data_files.append(data_file)

            if stall_while_running:
                run_completed = self.check_hplc_done_running()
                if run_completed.is_ok():
                    self.data_files[-1] = run_completed.ok_value
                else:
                    warnings.warn("Run may have not completed.")
        else:
            raise RuntimeError("Sequence run did not start.")

    @override
    def fuzzy_match_most_recent_folder(
        self, most_recent_folder: SequenceDataFiles
    ) -> Result[SequenceDataFiles, str]:
        if os.path.isdir(most_recent_folder.dir):
            subdirs = [x[0] for x in os.walk(most_recent_folder.dir)]
            potential_folders = sorted(
                list(filter(lambda d: most_recent_folder.dir in d, subdirs))
            )
            most_recent_folder.child_dirs = [
                f
                for f in potential_folders
                if most_recent_folder.dir in f and ".M" not in f and ".D" in f
            ]
            return Ok(most_recent_folder)

        try:
            potential_folders = []
            for d in self.data_dirs:
                subdirs = [x[0] for x in os.walk(d)]
                potential_folders = sorted(
                    list(filter(lambda d: most_recent_folder.dir in d, subdirs))
                )
                if len(potential_folders) > 0:
                    break
            assert len(potential_folders) > 0
            parent_dirs = []
            for folder in potential_folders:
                path = os.path.normpath(folder)
                split_folder = path.split(os.sep)
                if most_recent_folder.dir in split_folder[-1]:
                    parent_dirs.append(folder)
            parent_dir = sorted(parent_dirs, reverse=True)[0]

            potential_folders = []
            for d in self.data_dirs:
                subdirs = [x[0] for x in os.walk(d)]
                potential_folders = sorted(
                    list(filter(lambda d: parent_dir in d, subdirs))
                )
                if len(potential_folders) > 0:
                    break
            assert len(potential_folders) > 0
            most_recent_folder.child_dirs = [
                f
                for f in potential_folders
                if parent_dir in f and ".M" not in f and ".D" in f
            ]
            return Ok(most_recent_folder)
        except Exception as e:
            error = f"Failed to get sequence folder: {e}"
            return Err(error)

    def get_data_uv(
        self, custom_path: Optional[str] = None
    ) -> List[Dict[int, AgilentHPLCChromatogram]]:
        custom_path = (
            SequenceDataFiles(dir=custom_path, child_dirs=[], sequence_name="")
            if custom_path
            else self.data_files[-1]
        )
        if len(custom_path.child_dirs) == 0:
            self.data_files[-1] = self.fuzzy_match_most_recent_folder(
                custom_path
            ).ok_value
        all_w_spectra: List[Dict[int, AgilentHPLCChromatogram]] = []
        for row in self.data_files[-1].child_dirs:
            self.get_uv_spectrum(row)
            all_w_spectra.append(self.uv)
        return all_w_spectra

    def get_data(
        self, custom_path: Optional[str] = None
    ) -> List[AgilentChannelChromatogramData]:
        custom_path = (
            SequenceDataFiles(dir=custom_path, child_dirs=[], sequence_name="")
            if custom_path
            else self.data_files[-1]
        )
        if len(custom_path.child_dirs) == 0:
            self.data_files[-1] = self.fuzzy_match_most_recent_folder(
                custom_path
            ).ok_value
        spectra: List[AgilentChannelChromatogramData] = []
        for row in self.data_files[-1].child_dirs:
            self.get_spectrum_at_channels(row)
            spectra.append(AgilentChannelChromatogramData(**self.spectra))
        return spectra

    def get_report(
        self,
        custom_path: Optional[str] = None,
        report_type: ReportType = ReportType.TXT,
    ) -> List[AgilentReport]:
        if custom_path:
            self.data_files.append(
                self.fuzzy_match_most_recent_folder(
                    most_recent_folder=SequenceDataFiles(
                        dir=custom_path, child_dirs=[], sequence_name="NA"
                    )
                ).ok_value
            )
        parent_dir = self.data_files[-1]
        spectra = self.get_data()
        reports = []
        for i, child_dir in enumerate(parent_dir.child_dirs):
            metd_report = self.get_report_details(child_dir, report_type)
            child_spectra: List[AgilentHPLCChromatogram] = list(
                spectra[i].__dict__.values()
            )
            for j, signal in enumerate(metd_report.signals):
                possible_data = child_spectra[j]
                if len(possible_data.x) > 0:
                    signal.data = possible_data
            reports.append(metd_report)
        return reports

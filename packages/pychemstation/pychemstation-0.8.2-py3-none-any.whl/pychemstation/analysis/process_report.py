import abc
import os
import re
from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List, AnyStr, Dict, Optional, Pattern

import pandas as pd
from aghplctools.ingestion.text import _no_peaks_re, _area_report_re, _header_block_re, _signal_info_re, \
    _signal_table_re, chunk_string
from result import Result, Err, Ok

from pychemstation.utils.chromatogram import AgilentHPLCChromatogram
from pychemstation.utils.tray_types import Tray, FiftyFourVialPlate


@dataclass
class AgilentPeak:
    retention_time: float
    width: float
    area: float
    height: float
    peak_number: Optional[int]
    peak_type: Optional[str]
    height_percent: Optional[float]


@dataclass
class Signals:
    wavelength: int
    peaks: List[AgilentPeak]
    data: Optional[AgilentHPLCChromatogram]


@dataclass
class AgilentReport:
    vial_location: Optional[Tray]
    signals: List[Signals]
    solvents: Optional[Dict[AnyStr, AnyStr]]


class ReportType(Enum):
    TXT = 0
    CSV = 1


class ReportProcessor(abc.ABC):
    def __init__(self, path: str):
        self.path = path

    @abstractmethod
    def process_report(self) -> Result[AgilentReport, AnyStr]:
        pass


class CSVProcessor(ReportProcessor):
    def __init__(self, path: str):
        """
        Class to process reports in CSV form.

        :param path: the parent folder that contains the CSV report(s) to parse.
        """
        super().__init__(path)

    def process_report(self) -> Result[AgilentReport, AnyStr]:
        """
        Method to parse details from CSV report.

        :returns: subset of complete report details, specifically the sample location, solvents in pumps,
         and list of peaks at each wavelength channel.
        """
        labels = os.path.join(self.path, f'REPORT00.CSV')
        if os.path.exists(labels):
            df_labels: Dict[int, Dict[int: AnyStr]] = pd.read_csv(labels, encoding="utf-16", header=None).to_dict()
            vial_location = []
            signals = {}
            solvents = {}
            for pos, val in df_labels[0].items():
                if val == "Location":
                    vial_location = df_labels[1][pos]
                elif "Solvent" in val:
                    if val not in solvents.keys():
                        solvents[val] = df_labels[2][pos]
                elif val == "Number of Signals":
                    num_signals = int(df_labels[1][pos])
                    for s in range(1, num_signals + 1):
                        df = pd.read_csv(os.path.join(self.path, f'REPORT0{s}.CSV'),
                                         encoding="utf-16", header=None)
                        peaks = df.apply(lambda row: AgilentPeak(*row), axis=1)
                        wavelength = df_labels[1][pos + s].partition(",4 Ref=off")[0][-3:]
                        signals[wavelength] = peaks
                    break

            return Ok(AgilentReport(
                signals=[Signals(wavelength=w, peaks=s, data=None) for w, s in signals.items()],
                vial_location=FiftyFourVialPlate.from_int(int(vial_location)),
                solvents=solvents
            ))

        return Err("No report found")


class TXTProcessor(ReportProcessor):
    """
    Regex matches for column and unit combinations, courtesy of Veronica Lai.
    """
    _column_re_dictionary = {
        'Peak': {  # peak index
            '#': '[ ]+(?P<Peak>[\d]+)',  # number
        },
        'RetTime': {  # retention time
            '[min]': '(?P<RetTime>[\d]+.[\d]+)',  # minutes
        },
        'Type': {  # peak type
            '': '(?P<Type>[A-Z]{1,3}(?: [A-Z]{1,2})*)',  # todo this is different from <4.8.8 aghplc tools
        },
        'Width': {  # peak width
            '[min]': '(?P<Width>[\d]+.[\d]+[e+-]*[\d]+)',
        },
        'Area': {  # peak area
            '[mAU*s]': '(?P<Area>[\d]+.[\d]+[e+-]*[\d]+)',  # area units
            '%': '(?P<percent>[\d]+.[\d]+[e+-]*[\d]+)',  # percent
        },
        'Height': {  # peak height
            '[mAU]': '(?P<Height>[\d]+.[\d]+[e+-]*[\d]+)',
        },
        'Name': {
            '': '(?P<Name>[^\s]+(?:\s[^\s]+)*)',  # peak name
        },
    }

    def __init__(self, path: str, min_ret_time: int = 0,
                 max_ret_time: int = 999,
                 target_wavelength_range: List[int] = range(200, 300)):
        """
        Class to process reports in CSV form.

        :param path: the parent folder that contains the CSV report(s) to parse.
        :param min_ret_time: peaks after this value (min) will be returned
        :param max_ret_time: peaks will only be returned up to this time (min)
        :param target_wavelength_range: range of wavelengths to return
        """
        self.target_wavelength_range = target_wavelength_range
        self.min_ret_time = min_ret_time
        self.max_ret_time = max_ret_time
        super().__init__(path)

    def process_report(self) -> Result[AgilentReport, AnyStr]:
        """
        Method to parse details from CSV report.

        :returns: subset of complete report details, specifically the sample location, solvents in pumps,
         and list of peaks at each wavelength channel.

        If you want more functionality, use `aghplctools`.
        `from aghplctools.ingestion.text import pull_hplc_area_from_txt`
        `signals = pull_hplc_area_from_txt(file_path)`
        """

        with open(os.path.join(self.path, "REPORT.TXT"), 'r', encoding='utf-16') as openfile:
            text = openfile.read()

        try:
            signals = self.parse_area_report(text)
        except ValueError as e:
            return Err("No peaks found: " + str(e))

        signals = {key: signals[key] for key in self.target_wavelength_range if key in signals}

        parsed_signals = []
        for wavelength, wavelength_dict in signals.items():
            current_wavelength_signals = Signals(wavelength=wavelength, peaks=[], data=None)
            for ret_time, ret_time_dict in wavelength_dict.items():
                if self.min_ret_time <= ret_time <= self.max_ret_time:
                    current_wavelength_signals.peaks.append(AgilentPeak(retention_time=ret_time,
                                                                        area=ret_time_dict['Area'],
                                                                        width=ret_time_dict['Width'],
                                                                        height=ret_time_dict['Height'],
                                                                        peak_number=None,
                                                                        peak_type=ret_time_dict['Type'],
                                                                        height_percent=None))
            parsed_signals.append(current_wavelength_signals)

        return Ok(AgilentReport(vial_location=None,
                                solvents=None,
                                signals=parsed_signals))

    def parse_area_report(self, report_text: str) -> Dict:
        """
        Interprets report text and parses the area report section, converting it to dictionary.
        Courtesy of Veronica Lai.

        :param report_text: plain text version of the report.
        :raises ValueError: if there are no peaks defined in the report text file
        :return: dictionary of signals in the form
            dict[wavelength][retention time (float)][Width/Area/Height/etc.]

        If you want more functionality, use `aghplctools`.
        should be able to use the `parse_area_report` method of aghplctools v4.8.8
        """
        if re.search(_no_peaks_re, report_text):  # There are no peaks in Report.txt
            raise ValueError(f'No peaks found in Report.txt')
        blocks = _header_block_re.split(report_text)
        signals = {}  # output dictionary
        for ind, block in enumerate(blocks):
            # area report block
            if _area_report_re.match(block):  # match area report block
                # break into signal blocks
                signal_blocks = _signal_table_re.split(blocks[ind + 1])
                # iterate over signal blocks
                for table in signal_blocks:
                    si = _signal_info_re.match(table)
                    if si is not None:
                        # some error state (e.g. 'not found')
                        if si.group('error') != '':
                            continue
                        wavelength = float(si.group('wavelength'))
                        if wavelength in signals:
                            # placeholder error raise just in case (this probably won't happen)
                            raise KeyError(
                                f'The wavelength {float(si.group("wavelength"))} is already in the signals dictionary')
                        signals[wavelength] = {}
                        # build peak regex
                        peak_re = self.build_peak_regex(table)
                        if peak_re is None:  # if there are no columns (empty table), continue
                            continue
                        for line in table.split('\n'):
                            peak = peak_re.match(line)
                            if peak is not None:
                                signals[wavelength][float(peak.group('RetTime'))] = {}
                                current = signals[wavelength][float(peak.group('RetTime'))]
                                for key in self._column_re_dictionary:
                                    if key in peak.re.groupindex:
                                        try:  # try float conversion, otherwise continue
                                            value = float(peak.group(key))
                                        except ValueError:
                                            value = peak.group(key)
                                        current[key] = value
                                    else:  # ensures defined
                                        current[key] = None
        return signals

    def build_peak_regex(self, signal_table: str) -> Pattern[AnyStr]:
        """
        Builds a peak regex from a signal table. Courtesy of Veronica Lai.

        :param signal_table: block of lines associated with an area table
        :return: peak line regex object (<=3.6 _sre.SRE_PATTERN, >=3.7 re.Pattern)
        """
        split_table = signal_table.split('\n')
        if len(split_table) <= 4:  # catch peak table with no values
            return None
        # todo verify that these indicies are always true
        column_line = split_table[2]  # table column line
        unit_line = split_table[3]  # column unit line
        length_line = [len(val) + 1 for val in split_table[4].split('|')]  # length line

        # iterate over header values and units to build peak table regex
        peak_re_string = []
        for header, unit in zip(
                chunk_string(column_line, length_line),
                chunk_string(unit_line, length_line)
        ):
            if header == '':  # todo create a better catch for an undefined header
                continue
            try:
                peak_re_string.append(
                    self._column_re_dictionary[header][unit]  # append the appropriate regex
                )
            except KeyError:  # catch for undefined regexes (need to be built)
                raise KeyError(f'The header/unit combination "{header}" "{unit}" is not defined in the peak regex '
                               f'dictionary. Let Lars know.')
        return re.compile(
            '[ ]+'.join(peak_re_string)  # constructed string delimited by 1 or more spaces
            + '[\s]*'  # and any remaining white space
        )

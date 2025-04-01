from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Union


class Num(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9

    @classmethod
    def from_num(cls, num: int):
        num_mapping = {
            1: Num.ONE,
            2: Num.TWO,
            3: Num.THREE,
            4: Num.FOUR,
            5: Num.FIVE,
            6: Num.SIX,
            7: Num.SEVEN,
            8: Num.EIGHT,
            9: Num.NINE,
        }

        if num in num_mapping:
            return num_mapping[num]
        else:
            raise ValueError("Num must be between 1 and 9")


class Plate(Enum):
    ONE = -96
    TWO = 4000

    @classmethod
    def from_num(cls, plate: int) -> Plate:
        if 1 <= plate <= 2:
            return Plate.ONE if plate == 1 else Plate.TWO
        raise ValueError("Plate is one or 1 or 2")


class Letter(Enum):
    A = 4191
    B = 4255
    C = 4319
    D = 4383
    E = 4447
    F = 4511

    @classmethod
    def from_str(cls, let: str) -> Letter:
        letter_mapping = {
            "A": Letter.A,
            "B": Letter.B,
            "C": Letter.C,
            "D": Letter.D,
            "E": Letter.E,
            "F": Letter.F,
        }

        if let in letter_mapping:
            return letter_mapping[let]
        else:
            raise ValueError("Letter must be one of A to F")


@dataclass
class FiftyFourVialPlate:
    """
    Class to represent the 54 vial tray. Assumes you have:
    2 plates (P1 or P2)
    6 rows (A B C D E F)
    9 columns (1 2 3 4 5 6 7 8 9)

    valid vial locations: P1-A2, P2-F9
    invalid vial locations: P3-A1, P1-Z3, P2-B10
    """

    plate: Plate
    letter: Letter
    num: Num

    def value(self) -> int:
        return self.plate.value + self.letter.value + self.num.value

    @classmethod
    def from_str(cls, loc: str):
        """
        Converts a string representing the vial location into numerical representation for Chemstation.

        :param loc: vial location
        :return: `FiftyFourVialPlate` object representing the vial location
        :raises: ValueError if string is invalid tray location
        """
        if len(loc) != 5:
            raise ValueError(
                "Plate locations must be PX-LY, where X is either 1 or 2 and Y is 1 to 9"
            )
        try:
            plate = int(loc[1])
            letter = loc[3]
            num = int(loc[4])
            return FiftyFourVialPlate(
                plate=Plate.from_num(plate),
                letter=Letter.from_str(letter),
                num=Num.from_num(num),
            )
        except Exception:
            raise ValueError(
                "Plate locations must be PX-LY, where X is either 1 or 2 and Y is 1 to 9"
            )

    @classmethod
    def from_int(cls, num: int) -> Tray:
        """
        Converts an integer representation of a vial location to a `FiftyFourVialPlate` or `TenVialColumn` object

        :param num: numerical representation of a vial location
        :return: the proper vial location object
        :raises: ValueError no matching can be made
        """
        if num in range(1, 11):
            return TenVialColumn(num)

        row_starts = [
            # plate 1
            FiftyFourVialPlate.from_str("P1-F1"),
            FiftyFourVialPlate.from_str("P1-E1"),
            FiftyFourVialPlate.from_str("P1-D1"),
            FiftyFourVialPlate.from_str("P1-C1"),
            FiftyFourVialPlate.from_str("P1-B1"),
            FiftyFourVialPlate.from_str("P1-A1"),
            # plate 2
            FiftyFourVialPlate.from_str("P2-F1"),
            FiftyFourVialPlate.from_str("P2-E1"),
            FiftyFourVialPlate.from_str("P2-D1"),
            FiftyFourVialPlate.from_str("P2-C1"),
            FiftyFourVialPlate.from_str("P2-B1"),
            FiftyFourVialPlate.from_str("P2-A1"),
        ]

        # find which row
        possible_row = None
        for i in range(0, 6):
            p1_val = row_starts[i].value()
            p2_val = row_starts[6 + i].value()
            if num >= p2_val:
                possible_row = row_starts[6 + i]
            elif p1_val <= num < row_starts[-1].value():
                possible_row = row_starts[i]
            if possible_row:
                break

        # determine which num
        if possible_row:
            starting_loc = possible_row
            base_val = starting_loc.plate.value + starting_loc.letter.value
            for i in range(1, 10):
                if num - i == base_val:
                    return FiftyFourVialPlate(
                        plate=starting_loc.plate,
                        letter=starting_loc.letter,
                        num=Num.from_num(i),
                    )
        raise ValueError("Number didn't match any location. " + str(num))


class TenVialColumn(Enum):
    """
    Class to represent the 10 vial locations.
    """

    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10


Tray = Union[FiftyFourVialPlate, TenVialColumn]

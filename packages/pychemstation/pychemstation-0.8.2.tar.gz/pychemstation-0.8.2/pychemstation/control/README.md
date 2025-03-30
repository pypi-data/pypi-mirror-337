#  Examples of usecases

## Initialization
```python
from pychemstation.control import HPLCController

DEFAULT_METHOD_DIR = "C:\\ChemStation\\1\\Methods\\"
DATA_DIR = "C:\\Users\\Public\\Documents\\ChemStation\\3\\Data"
SEQUENCE_DIR = "C:\\USERS\\PUBLIC\\DOCUMENTS\\CHEMSTATION\\3\\Sequence"
DEFAULT_COMMAND_PATH = "C:\\Users\\User\\Desktop\\Lucy\\"

hplc_controller = HPLCController(data_dir=DATA_DIR,
                                 comm_dir=DEFAULT_COMMAND_PATH,
                                 method_dir=DEFAULT_METHOD_DIR,
                                 sequence_dir=SEQUENCE_DIR)
```

## Switching a method
```python
hplc_controller.switch_method("General-Poroshell")
```

## Editing a method

```python
from pychemstation.utils.method_types import *

new_method = MethodDetails(
    name="My_Method",
    params=HPLCMethodParams(
        organic_modifier=7,
        flow=0.44),
    timetable=[
        TimeTableEntry(
            start_time=0.10,
            organic_modifer=7,
            flow=0.34
        ),
        TimeTableEntry(
            start_time=1,
            organic_modifer=99,
            flow=0.55
        )
    ],
    stop_time=5,
    post_time=2
)

hplc_controller.edit_method(new_method)
```

## Running a method and get data from last run method
```python
hplc_controller.run_method(experiment_name="test_experiment")
chrom = hplc_controller.get_last_run_method_data()
channel_a_time = chrom.A.x
```

## Switching a sequence
```python
hplc_controller.switch_sequence(sequence_name="hplc_testing")
```
## Editing a Sequence Row
```python
from pychemstation.utils.sequence_types import *
from pychemstation.utils.tray_types import *

hplc_controller.edit_sequence_row(SequenceEntry(
    vial_location=FiftyFourVialPlate(plate=Plate.TWO, letter=Letter.A, num=Num.SEVEN).value(),
    method="General-Poroshell",
    num_inj=3,
    inj_vol=4,
    sample_name="Blank",
    sample_type=SampleType.BLANK,
    inj_source=InjectionSource.HIP_ALS
), 1)
```

## Editing entire Sequence Table
```python
from pychemstation.utils.tray_types import *
from pychemstation.utils.sequence_types import *

seq_table = SequenceTable(
    name=DEFAULT_SEQUENCE,
    rows=[
        SequenceEntry(
            vial_location=FiftyFourVialPlate(plate=Plate.TWO, letter=Letter.A, num=Num.SEVEN).value(),
            method="General-Poroshell",
            num_inj=3,
            inj_vol=4,
            sample_name="Control",
            sample_type=SampleType.CONTROL,
            inj_source=InjectionSource.MANUAL
        ),
        SequenceEntry(
            vial_location=TenVialColumn.ONE.value,
            method="General-Poroshell",
            num_inj=1,
            inj_vol=1,
            sample_name="Sample",
            sample_type=SampleType.SAMPLE,
            inj_source=InjectionSource.AS_METHOD
        ),
        SequenceEntry(
            vial_location=10,
            method="General-Poroshell",
            num_inj=3,
            inj_vol=4,
            sample_name="Blank",
            sample_type=SampleType.BLANK,
            inj_source=InjectionSource.HIP_ALS
        ),
    ]
)
hplc_controller.edit_sequence(seq_table)
```

## Running a sequence and get data from last run sequence
```python
hplc_controller.run_sequence(seq_table)
chroms = hplc_controller.get_last_run_sequence_data()
channel_A_time = chroms[0].A.x
```
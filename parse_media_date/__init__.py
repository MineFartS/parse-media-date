from philh_myftp_biz.time import from_ymdhms, from_stamp
from philh_myftp_biz.num import is_int
from philh_myftp_biz.pc import Path
from typing import SupportsInt, Any
from re import split, findall

def _from_ymdhms(
    year : SupportsInt = None,
    month: SupportsInt = None,
    day  : SupportsInt = None
) -> from_stamp | None:

    try:
        
        return from_ymdhms(
            year = int(year),
            month = int(month),
            day = int(day)
        )

    except TypeError, ValueError:
        pass

def _from_stamp(
    stamp: Any
) -> from_stamp | None:

    try:
        
        return from_stamp(stamp)

    except ValueError:
        pass

def parse(file:Path) -> from_stamp:

    #=========================================================================
    # Ex: "RPReplay_Final1593809676.mp4"

    if file.name.startswith('RPReplay_Final'):

        stamp = _from_stamp(file.name.split('Final')[1])

        if stamp:
            return stamp

    #=========================================================================
    # Ex: "FinalVideo_1639183283.358880.mov"

    if file.name.startswith('FinalVideo_'):

        stamp = _from_stamp(file.name.split('_')[1])

        if stamp:
            return stamp
    
    #=========================================================================
    # Ex: "2020-04-10_15-20-14_445.jpg"

    parts: list[str] = findall(
        pattern = r'\d{4}[-_]\d{2}[-_]\d{2}',
        string = file.name
    )

    for part in parts:

        stamp = _from_ymdhms(*part.split('-'))

        if stamp:
            return stamp
        
    #=========================================================================
    # Ex: "629568258.099773 (1).jpg"

    parts: list[str] = findall(
        pattern = r'\d{7,10}\.\d{6}',
        string = file.name
    )

    for part in parts:

        stamp = _from_stamp(part)

        if stamp:
            return stamp

    #=========================================================================
    # Ex: "2021_0323_105922_001.JPG"

    parts: list[str] = findall(
        pattern = r'[19|20]\d{3}_[0|1]\d{1}[0-3]\d{1}_',
        string = file.name
    )

    for part in parts:

        stamp = _from_ymdhms(
            year  = part[0:4],
            month = part[5:7],
            day   = part[7:9]
        )

        if stamp:
            return stamp

    #=========================================================================
    # Ex: "8-27-2019_Toy Video Part 2.mp4"

    parts: list[str] = findall(
        pattern = r'\d{1,2}-\d{1,2}-\d{4}',
        string = file.name
    )

    for part in parts:

        month, day, year = part.split('-')

        stamp = _from_ymdhms(year, month, day)

        if stamp:
            return stamp

    #=========================================================================
    # Ex: "WIN_20161228_01_20_10_Pro.jpg"

    parts: list[str] = split(
        pattern = r'[-_\s]',
        string = file.name
    )

    for part in parts:

        CHARCOUNT = len(part) == 8
        INTEGER = is_int(part)
        
        if CHARCOUNT and INTEGER:
                
            stamp = _from_ymdhms(
                year = part[:4],
                month = part[4:6],
                day = part[6:8]
            )

            if stamp:
                return stamp
    
    #=========================================================================

    return file.ctime

    #=========================================================================

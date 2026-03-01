from philh_myftp_biz.time import from_ymdhms, from_stamp
from philh_myftp_biz.num import is_int
from philh_myftp_biz.pc import Path
from typing import SupportsInt
from re import split, findall

def _from_ymdhms(
    year : SupportsInt = None,
    month: SupportsInt = None,
    day  : SupportsInt = None
):

    try:
        
        stamp = from_ymdhms(
            year = int(year),
            month = int(month),
            day = int(day)
        )

        return stamp

    except TypeError, ValueError:
        pass

def parse(file:Path) -> from_stamp:

    #=========================================================================

    iso_parts: list[str] = findall(
        pattern = r'\d{4}[-_]\d{2}[-_]\d{2}',
        string = file.name()
    )

    for part in iso_parts:

        stamp = _from_ymdhms(*part.split('-'))

        if stamp:
            return stamp
        
    #=========================================================================
    
    if file.name().startswith('RPReplay_Final'):

        stamp = int(file.name().split('Final')[1])

        return from_stamp(stamp)

    elif file.name().startswith('FinalVideo_'):

        stamp = float(file.name().split('_')[1])

        return from_stamp(stamp)
    
    #=========================================================================

    parts: list[str] = split(
        pattern = r'[-_\s]',
        string = file.name()
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

    return file.ctime()

    #=========================================================================

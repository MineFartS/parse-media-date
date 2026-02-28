from philh_myftp_biz.time import from_ymdhms, from_stamp
from philh_myftp_biz.num import is_int
from philh_myftp_biz.pc import Path
from re import split

def parse(file:Path) -> from_stamp:
    
    if file.name().startswith('RPReplay_Final'):

        stamp = int(file.name().split('Final')[1])

        return from_stamp(stamp)

    parts: list[str] = split(
        pattern = r'[-_\s]',
        string = file.name()
    )

    for part in parts:

        CHARCOUNT = len(part) == 8
        INTEGER = is_int(part)
        
        if CHARCOUNT and INTEGER:

            try:
                
                stamp = from_ymdhms(
                    year = int(part[:4]),
                    month = int(part[4:6]),
                    day = int(part[6:8])
                )

                return stamp

            except TypeError, ValueError:
                pass

    return file.ctime()

# import nicknames_poroparse
import puuids_parse
import gather_matchdata
import time
from mcf_threads import MCFThread
# from mcf_data import REGIONS_TUPLE
from pprint import pprint


def main():

    puuids_base = puuids_parse.parse_games() # AREA::puuid
    # print(puuids_base)

    base_eu = set()
    base_asia = set()
    base_americas = set()
    base_sea = set()

    for area_puuid in puuids_base:
        area, puuid = area_puuid.split('::')
        match area:
            case 'europe':
                base_eu.add(puuid)
            case 'asia':
                base_asia.add(puuid)
            case 'americas':
                base_americas.add(puuid)
            case 'sea':
                base_sea.add(puuid)
            case _:
                pass
    
    threads = [
        MCFThread(func=gather_matchdata.gathering, args=(base_eu, 'europe', ), region='europe'),
        MCFThread(func=gather_matchdata.gathering, args=(base_asia, 'asia', ), region='asia'),
        MCFThread(func=gather_matchdata.gathering, args=(base_americas, 'americas', ), region='americas'),
        MCFThread(func=gather_matchdata.gathering, args=(base_sea, 'sea', ), region='sea'),
        ]

    for thr in threads:
         thr.start()

    while True:
        thr_status = [thr.is_alive() for thr in threads]

        if not any(thr_status):
            print('THREADS COMPLETED -- RESTART')
            break
        time.sleep(5)

if __name__ == '__main__':
    while True:
        main()


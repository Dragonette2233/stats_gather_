import puuids_parse
import gather_matchdata
import time
from mcf_threads import MCFThread
import logging

# Определяем уровень логирования (DEBUG - наиболее детальный, ERROR - наименее детальный)
logging.basicConfig(level=logging.INFO)

# Формат сообщения лога
# %(asctime)s - Дата и время
# %(levelname)s - Уровень логирования
# %(message)s - Текст сообщения
format_str = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=format_str)

# Создаем объект логгера
logger = logging.getLogger(__name__)

# Примеры использования логгера
# logger.debug('Это сообщение уровня DEBUG')
# logger.info('Это сообщение уровня INFO')
# logger.warning('Это сообщение уровня WARNING')
# logger.error('Это сообщение уровня ERROR')
# logger.critical('Это сообщение уровня CRITICAL')




def main():

    puuids_base = puuids_parse.parse_games() # AREA::puuid

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


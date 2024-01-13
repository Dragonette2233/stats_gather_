import requests
import logging
from mcf_data import (
    headers_timeout,
    GATHERED_MATCHES,
    ALL_CHAMPIONS_IDs,
    ten_roles_dict,
    SET_LCK,
)
import time

logger = logging.getLogger(__name__)

def gathering(puuids_set: set, area: str):

    def _converted_roles(champions_list: list[str]) -> str:

        converted_list = []

        for chamipion in champions_list:
            for role, champs in ten_roles_dict.items():
                if chamipion.lower().capitalize() in champs:
                    converted_list.append(role)
        
        return ''.join(sorted(converted_list))

    logger.debug(f'[{area}] Circle rounded')

    for puuid in puuids_set:
        while True:
            try:

                result = requests.get(
                    url=f'https://{area}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20',
                    **headers_timeout
                ).json()
                break
            except (requests.exceptions.ConnectTimeout, 
                    requests.exceptions.ConnectionError,
                    requests.exceptions.ReadTimeout):
                time.sleep(3)
                continue

        for game_id in result:

            if game_id not in GATHERED_MATCHES:
                while True:
                    try:
                        result = requests.get(
                            url=f'https://{area}.api.riotgames.com/lol/match/v5/matches/{game_id}',
                                **headers_timeout
                                ).json()['info']
                        break
                    except (requests.exceptions.ConnectTimeout, 
                            requests.exceptions.ConnectionError,
                            requests.exceptions.ReadTimeout):
                        logger.warning(f'[{area}] Connection error. Sleep for 3 seconds...')
                        time.sleep(3)
                        continue
                    except KeyError:
                        result = None
                        logger.warning(f'[{area}] Key Error occured. Breaking...')
                        break
                
                if result:
                    kills = sum(result['participants'][k]['kills'] for k in range(len(result['participants'])))
                    if kills > 50 and result['gameMode'] == 'ARAM':

                        champions_ids = [result['participants'][p]['championId'] for p in range(10)]
                        champions_names = [ALL_CHAMPIONS_IDs.get(champions_ids[i]) for i in range(10)]
                        # team_blue = champions_names[0:5]
                        # team_red = champions_names[5:10]

                        roles_blue = _converted_roles(champions_names[0:5])
                        roles_red = _converted_roles(champions_names[5:10])

                        if result['teams'][0]['win']:
                            # res_value = f"{'_'.join(team_blue)} -- {'_'.join(team_red)} -- {kills}"
                            res_value_2 = f"{roles_blue}_{roles_red}_{kills}_{game_id[-4:]}"
                        else:
                            # res_value = f"{'_'.join(team_red)} -- {'_'.join(team_blue)} -- {kills}"
                            res_value_2 = f"{roles_red}_{roles_blue}_{kills}_{game_id[-4:]}"
                        
                        with SET_LCK:
                            GATHERED_MATCHES.add(game_id)
                            with open('STATS_all.txt', 'a+') as stats_file:
                                stats_file.writelines(res_value_2 + '\n')
                        
                        if area == 'europe':
                            time.sleep(1.21)
                        else:
                            time.sleep(0.4)

    logger.debug(f'[{area}] Circle ended')
            
            
            
                

    
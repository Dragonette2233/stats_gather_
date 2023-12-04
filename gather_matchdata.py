import requests
from mcf_data import (
    headers_timeout,
    GATHERED_MATCHES,
    ALL_CHAMPIONS_IDs,
    ten_roles_dict,
    SET_LCK,
)
import time

def gathering(puuids_set: set, area: str):

    def _converted_roles(champions_list: list[str]) -> str:

        converted_list = []

        for chamipion in champions_list:
            for role, champs in ten_roles_dict.items():
                if chamipion.lower().capitalize() in champs:
                    converted_list.append(role)
        
        return ''.join(sorted(converted_list))

    print(f'Circle rounded in {area}')

    for puuid in puuids_set:
        # print(item)
        # area, puuid = item.split('::')
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
                        print('Connection error. Sleep for 3 seconds...')
                        time.sleep(3)
                        continue
                
                kills = sum(result['participants'][k]['kills'] for k in range(10))
                if kills > 50:

                    champions_ids = [result['participants'][p]['championId'] for p in range(10)]
                    champions_names = [ALL_CHAMPIONS_IDs.get(champions_ids[i]) for i in range(10)]
                    # team_blue = champions_names[0:5]
                    # team_red = champions_names[5:10]

                    roles_blue = _converted_roles(champions_names[0:5])
                    roles_red = _converted_roles(champions_names[5:10])

                    if result['teams'][0]['win']:
                        # res_value = f"{'_'.join(team_blue)} -- {'_'.join(team_red)} -- {kills}"
                        res_value_2 = f"{roles_blue}_{roles_red}_{kills}"
                    else:
                        # res_value = f"{'_'.join(team_red)} -- {'_'.join(team_blue)} -- {kills}"
                        res_value_2 = f"{roles_red}_{roles_blue}_{kills}"
                    
                    with SET_LCK:
                        GATHERED_MATCHES.add(game_id)
                        with open('STATS_all.txt', 'a+') as stats_file:
                            stats_file.writelines(res_value_2 + '\n')
                    # print(res_value)
                    # print(res_value_2)
                    # input()
                    time.sleep(1.21)

    print(f'Circle ended in {area}')
            
            
            
                

    
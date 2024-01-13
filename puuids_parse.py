import asyncio
import logging
import sys
from aiohttp import ClientSession
from aiohttp.client_exceptions import (
    ClientProxyConnectionError,
    ClientConnectionError
)
from mcf_data import (
    REGIONS_TUPLE,
    FEATURED_GAMES_URL,
    headers_timeout
)

logger = logging.getLogger(__name__)

def parse_games():
    """
        This function parsing games from Riot API Featured Games into
        GameData.json and returning count of missing regions
    
    """

    async def parsing(region):
        nonlocal puuids_set

        async with ClientSession() as session:
            async with session.get(url=FEATURED_GAMES_URL.format(region=region), 
                                   **headers_timeout) as response:
                
                if response.status == 200:
                    data = await response.json()
                    gameList = data['gameList']

                
                try:
                    if len(gameList) < 1:
                        # missing_regions += 1
                        return
                except (KeyError, NameError):
                    # missing_regions += 1
                    return

        
                # puuids_list = []
                for s in range(0, len(gameList)):
                    
                    puuids = [gameList[s]['participants'][k]['puuid'] for k in range(len(gameList[s]['participants']))]
                    route = gameList[s]['platformId'] # BR1 | KR ...

                    for _, reg_index, area in REGIONS_TUPLE:
                        if route == reg_index.upper(): 
                            puuids_regions = ['::'.join([area, pd]) for pd in puuids]
                            puuids_set.update(puuids_regions)
                               
    async def main_aram():

        nonlocal puuids_set

        tasks = []
        for region in REGIONS_TUPLE:
            tasks.append(asyncio.create_task(parsing(region[1])))

        for task in tasks:
            try: 
                await asyncio.gather(task)
            except asyncio.exceptions.TimeoutError:
                await asyncio.sleep(3)
                continue
                # missing_regions += 1
            except (ClientConnectionError, ClientProxyConnectionError):
                await asyncio.sleep(3)
                continue
                # time.sleep(2)
                # missing_regions = 20
                
    puuids_set = set()
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main_aram())

    return puuids_set

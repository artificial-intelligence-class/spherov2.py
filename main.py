import asyncio

from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI


async def main():
    toy = await scanner.find_R2D2()
    async with SpheroEduAPI(toy) as api:
        await api.spin(360, 1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

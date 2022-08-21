import aiohttp

import valorant.identification


class Inventory:
    def __init__(self, access_token, entitlements_token, user_id, region="na"):
        self.access_token = access_token
        self.entitlements_token = entitlements_token
        self.user_id = user_id
        self.region = region

    async def load_owned(self):
        url = f"https://pd.{self.region}.a.pvp.net/store/v1/entitlements/{self.user_id}/e7c63390-eda7-46e0-bb7a-a6abdacd2433"  # noqa
        headers = {
            "X-Riot-Entitlements-JWT": self.entitlements_token,
            "Authorization": f"Bearer {self.access_token}"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                print(await resp.text())

        await valorant.identification.themes.load_api_data()
        await valorant.identification.tiers.load_api_data()
        await valorant.identification.weapons.load_api_data()

        print(valorant.identification.weapons.data)

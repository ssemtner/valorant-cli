import aiohttp


class ResponseStatusException(Exception):
    """Raised when the response status is not okay"""


class Identifier:
    def __init__(self, *, api_url, item_formatter, data_formatter=None):
        self.api_url = api_url
        self.format_item = item_formatter

        if data_formatter is not None:
            self.format_data = lambda data: data_formatter(data, self.format_item)
        else:
            self.format_data = lambda data: {item["uuid"]: self.format_item(item) for item in data}

        self.data = {}
        self.loaded = False
        self.error = False

    async def load_api_data(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.api_url) as resp:
                    json = await resp.json()
                    if json["status"] != 200:
                        raise ResponseStatusException
                    data = json["data"]

                    self.data = self.format_data(data)

        except KeyError:
            print("keyerror")
            self.error = True

        except ResponseStatusException:
            print("status wrong")
            self.error = True

    def identify(self, uuid):
        try:
            return self.data[uuid]
        except KeyError:
            return None


tiers = Identifier(
    api_url="https://valorant-api.com/v1/contenttiers",
    item_formatter=lambda item: {
        "name": item["devName"],
        "rank": item["rank"],
        "color": item["highlightColor"],
        "icon": item["displayIcon"]
    }
)

themes = Identifier(
    api_url="https://valorant-api.com/v1/themes",
    item_formatter=lambda item: {
        "name": item["displayName"],
        "icon": item["displayIcon"]
    }
)

def weapon_data_formatter(data, formatter):
    result = {}

    for weapon in data:
        for skin in weapon["skins"]:
            result[skin["uuid"]] = formatter(skin)

    return result


weapons = Identifier(
    api_url="https://valorant-api.com/v1/weapons",
    item_formatter=lambda item: {
        "name": item["displayName"],
        "theme": themes.identify(item["themeUuid"]),
        "tier": tiers.identify(item["contentTierUuid"]),
        "levels": {level["uuid"]: {
            "name": level["displayName"],
            "level_item": level["levelItem"],
            "icon": level["displayIcon"],
            "video": level["streamedVideo"]
        } for level in item["levels"]},
        "chromas": {chroma["uuid"]: {
            "name": chroma["displayName"],
            "icon": chroma["displayIcon"],
            "render": chroma["fullRender"],
            "swatch": chroma["swatch"],
            "video": chroma["streamedVideo"]
        } for chroma in item["chromas"]}
    },
    data_formatter=weapon_data_formatter
)

# https://valorant-api.com/v1/weapons

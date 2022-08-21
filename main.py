import asyncio
import sys

import valorant
import riot_auth

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

CREDS = "username", "password"


async def main():
    auth = riot_auth.RiotAuth()
    await auth.authorize(*CREDS)
    print(f"Access Token Type: {auth.token_type}\n")
    print(f"Access Token: {auth.access_token}\n")
    print(f"Entitlements Token: {auth.entitlements_token}\n")
    print(f"User ID: {auth.user_id}")
    inventory = valorant.Inventory(auth.access_token, auth.entitlements_token, auth.user_id)
    await inventory.load_owned()

asyncio.run(main())

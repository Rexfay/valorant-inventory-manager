import requests, os
from valclient.client import Client as ValClient
from dotenv import load_dotenv

load_dotenv()

class Client:

    def __init__(self):

        self.client = ValClient(auth={"username": os.getenv("VALORANT_USERNAME"), "password": os.getenv("VALORANT_PASSWORD")})
        self.client.activate()

        self.all_weapon_data = requests.get("https://valorant-api.com/v1/weapons").json()["data"]
        self.all_buddy_data = requests.get("https://valorant-api.com/v1/buddies").json()["data"]

    def fetch_loadout(self):
        loadout = self.client.fetch_player_loadout()

        payload = {}

        for weapon in loadout['Guns']:
            # skin stuff
            weapon_uuid = weapon['ID']
            weapon_data = next(item for item in self.all_weapon_data if item["uuid"] == weapon_uuid)
            skin_data = next(item for item in weapon_data["skins"] if item["uuid"] == weapon["SkinID"])
            level_data = next(item for item in skin_data["levels"] if item["uuid"] == weapon["SkinLevelID"])
            chroma_data = next(item for item in skin_data["chromas"] if item["uuid"] == weapon["ChromaID"])

            # buddy stuff
            if weapon.get("CharmID"):
                buddy_uuid = weapon['CharmID']
                buddy_data = next(item for item in self.all_buddy_data if item["uuid"] == buddy_uuid)


            payload[weapon_uuid] = {}
            pld = payload[weapon_uuid]
            pld["weapon_name"] = weapon_data["displayName"]
            pld["skin_name"] = skin_data["displayName"]
            pld["skin_uuid"] = skin_data["uuid"]
            pld["level_uuid"] = level_data["uuid"]
            pld["chroma_uuid"] = chroma_data["uuid"]
            pld["skin_image"] = chroma_data["fullRender"]

            pld["buddy_name"] = buddy_data["displayName"]
            pld["buddy_image"] = buddy_data["displayIcon"]

        return payload
from senju.haiku import Haiku
from senju.store_manager import StoreManager

haiku = Haiku(["Red suit, vents unseen,"," Sus behavior, crew unsure,"," Vote him, task complete."])
store = StoreManager()
store.save_haiku(haiku)


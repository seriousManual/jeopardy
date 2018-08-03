import yaml

from . import SIG_PLAYER_MODEL_CHANGED

class ModelPersistor():

	def __init__(self, playerManager, filename="log.yml"):
		self.file = open(filename, "a")
		self.playerManager = playerManager

		playerManager.connect(SIG_PLAYER_MODEL_CHANGED, self.persistModel)

	def persistModel(self, *args):
		state = {}
		state["players"] = [{"key": p.key, "name": p.name} for p in self.playerManager.getPlayers()]
		self.file.write(yaml.safe_dump(state, explicit_start = True))
		self.file.flush()

class ModelLoader():

	def __init__(self, playerManager, gameStateModel, filename="log.yml"):
		self.filename = filename
		self.playerManager = playerManager
		self.gameStateModel = gameStateModel

	def loadModel(self):
		with open(self.filename, "r") as file:
			stateDocuments = yaml.safe_load_all(file)

			for state in stateDocuments:
				pass

		for player in state["players"]:
			self.playerManager.addPlayer(player["name"], player["key"])

		categories = list(self.gameStateModel.getCategoryNames())
		for index, results in state["results"].items():
			row, col = map(int, index.split("/"))
			for result in results:
				self.gameStateModel.addResult(categories[col], row, 
					self.playerManager.getPlayerByKey(result["player"]), result["correct"], result["wager"])

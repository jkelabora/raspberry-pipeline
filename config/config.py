import json

class Config:

    def __init__(self):
      f = file('config/pipelines.json', "r")
      self.data = json.load(f)

    def pipelines(self):
      return self.data['pipelines']

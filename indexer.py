
class Index(object):
    def __init__(self):
          self.inverted_index = {}
          self.base_directory = ""
          self.pages_get_URL = []
    
    def index(self, dir_name):
         self.base_directory = dir_name

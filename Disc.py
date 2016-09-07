class Disc:
    def __init__(self, Title, Artist, Cover, Id):
        self.Artist=Artist
        self.Title=Title
        self.Cover=Cover
        self.JukeboxID=int(Id)

    def __repr__(self):
        return repr((self.name, self.Artist, self.Title, self.Cover, self.JukeboxID))
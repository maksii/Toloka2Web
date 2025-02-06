class RequestData:
    url: str = ""
    season: int = 0
    index: int = 0
    correction: int = 0
    title: str = ""
    codename: str = ""
    force: bool = False
    path: str = ""
    def __init__(self, url = "", season = 0, index = 0, correction = 0, title = "", codename = "", force=False, path=""):
        self.url = url
        self.season = season
        self.index = index
        self.correction = correction
        self.title = title
        self.codename = codename
        self.force = force
        self.path = path

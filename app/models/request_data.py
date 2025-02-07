"""Request data model for handling media requests."""
from dataclasses import dataclass

@dataclass
class RequestData:
    """Data class for handling media request parameters.
    
    Attributes:
        url: Request URL
        season: Season number
        index: Episode index
        correction: Episode number correction
        title: Media title
        codename: Internal codename
        force: Force processing flag
        path: File path
    """
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

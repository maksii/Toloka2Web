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
        partial: Whether this release is a partial/ongoing season (maps to --partial CLI arg)
        release_group: Name of the release group
        meta: Additional metadata (e.g. WEBDL, resolution)
    """

    url: str = ""
    season: int = 0
    index: int = 0
    correction: int = 0
    title: str = ""
    codename: str = ""
    force: bool = False
    path: str = ""
    partial: bool = True
    release_group: str = ""
    meta: str = ""

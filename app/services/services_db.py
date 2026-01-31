from typing import List, Optional, Dict
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import create_engine, or_
from sqlalchemy.ext.automap import automap_base
import requests
import os

from app.services.base_service import BaseService

class DatabaseService(BaseService):
    """Service for handling database operations."""
    
    # Database models
    Anime = None
    Type = None
    Status = None
    Franchise = None
    RelatedAnime = None
    Fundub = None
    FundubSynonym = None
    AnimeFundub = None
    Episode = None
    Session = None

    @classmethod
    def initialize_database(cls) -> None:
        """Initialize database connection and map models."""
        engine = create_engine('sqlite:///data/anime_data.db')
        cls.Session = sessionmaker(bind=engine)

        # Reflect the existing database into a new model
        Base = automap_base()
        Base.prepare(engine, reflect=True)

        # Map the models
        cls.Anime = Base.classes.anime
        cls.Type = Base.classes.type
        cls.Status = Base.classes.status
        cls.Franchise = Base.classes.franchise
        cls.RelatedAnime = Base.classes.related_anime
        cls.Fundub = Base.classes.fundub
        cls.FundubSynonym = Base.classes.fundub_synonym
        cls.AnimeFundub = Base.classes.anime_fundub
        cls.Episode = Base.classes.episode

    @classmethod
    def get_anime_by_id(cls, anime_id: int) -> Dict:
        """Get anime by ID with related data."""
        session = cls.Session()
        try:
            anime = session.query(cls.Anime).options(
                joinedload(cls.Anime.type).load_only(cls.Type.name),
                joinedload(cls.Anime.status).load_only(cls.Status.name),
                joinedload(cls.Anime.franchise)
            ).get(anime_id)
            return cls.serialize(anime)
        finally:
            session.close()

    @classmethod
    def get_anime_by_name(cls, partial_name: str) -> List[Dict]:
        """Search anime by partial name match."""
        session = cls.Session()
        try:
            animes = session.query(cls.Anime).filter(
                or_(
                    cls.Anime.titleUa.ilike(f'%{partial_name}%'),
                    cls.Anime.titleEn.ilike(f'%{partial_name}%')
                )
            ).all()
            return cls.serialize(animes)
        finally:
            session.close()

    @classmethod
    def get_related_animes(cls, anime_id: int) -> List[Dict]:
        """Get related animes for a given anime ID."""
        session = cls.Session()
        try:
            related_animes = session.query(cls.Anime).join(
                cls.RelatedAnime, cls.Anime.id == cls.RelatedAnime.anime_id2
            ).filter(cls.RelatedAnime.anime_id1 == anime_id).options(
                joinedload(cls.Anime.type).load_only(cls.Type.name),
                joinedload(cls.Anime.status).load_only(cls.Status.name),
                joinedload(cls.Anime.franchise)
            ).all()
            return cls.serialize(related_animes)
        finally:
            session.close()

    @classmethod
    def list_all_studios(cls) -> List[Dict]:
        """Get all studios."""
        session = cls.Session()
        try:
            studios = session.query(cls.Fundub).all()
            return cls.serialize(studios)
        finally:
            session.close()

    @classmethod
    def list_all_anime(cls) -> List[Dict]:
        """Get all anime with related data."""
        session = cls.Session()
        try:
            animes = session.query(cls.Anime).options(
                joinedload(cls.Anime.type).load_only(cls.Type.name),
                joinedload(cls.Anime.status).load_only(cls.Status.name),
                joinedload(cls.Anime.franchise)
            ).all()
            return cls.serialize(animes)
        finally:
            session.close()

    @classmethod
    def search_studio_by_name(cls, partial_name: str) -> List[Dict]:
        """Search studios by partial name match."""
        session = cls.Session()
        try:
            synonym_subquery = session.query(cls.FundubSynonym.fundub_id).filter(
                cls.FundubSynonym.synonym.ilike(f'%{partial_name}%')
            ).subquery()

            studios = session.query(cls.Fundub).filter(
                or_(
                    cls.Fundub.name.ilike(f'%{partial_name}%'),
                    cls.Fundub.id.in_(synonym_subquery)
                )
            ).all()
            return cls.serialize(studios)
        finally:
            session.close()

    @classmethod
    def search_studio_by_id(cls, studio_id: int) -> Optional[Dict]:
        """Get studio by ID."""
        session = cls.Session()
        try:
            studio = session.query(cls.Fundub).get(studio_id)
            return cls.serialize(studio) if studio else None
        finally:
            session.close()

    @classmethod
    def get_studios_by_anime_id(cls, anime_id: int) -> List[Dict]:
        """Get all studios for a given anime ID."""
        session = cls.Session()
        try:
            studios = session.query(cls.Fundub).join(
                cls.AnimeFundub, cls.Fundub.id == cls.AnimeFundub.fundub_id
            ).filter(cls.AnimeFundub.anime_id == anime_id).distinct().all()
            return cls.serialize(studios)
        finally:
            session.close()

    @classmethod
    def get_anime_by_studio_id(cls, studio_id: int) -> List[Dict]:
        """Get all anime for a given studio ID."""
        session = cls.Session()
        try:
            animes = session.query(cls.Anime).join(
                cls.AnimeFundub, cls.Anime.id == cls.AnimeFundub.anime_id
            ).filter(cls.AnimeFundub.fundub_id == studio_id).distinct().all()
            return cls.serialize(animes)
        finally:
            session.close()

    @classmethod
    def get_episodes_by_anime_id(cls, anime_id: int) -> List[Dict]:
        """Get all episodes for a given anime ID."""
        session = cls.Session()
        try:
            episodes = session.query(cls.Episode).filter_by(anime_id=anime_id).all()
            return cls.serialize(episodes)
        finally:
            session.close()

    @classmethod
    def update_database(cls) -> Dict[str, str]:
        """Update the local database from GitHub."""
        url = "https://github.com/maksii/Stream2MediaServer/raw/main/data/anime_data.db"
        local_db_path = "data/anime_data.db"
        
        try:
            os.makedirs(os.path.dirname(local_db_path), exist_ok=True)
            response = requests.get(url)
            response.raise_for_status()
            
            with open(local_db_path, 'wb') as f:
                f.write(response.content)
                
            return {"status": "success", "message": "Database has been updated successfully."}
        except requests.RequestException as e:
            return {"status": "error", "message": f"Failed to download the database: {str(e)}"}
        except Exception as e:
            return {"status": "error", "message": f"An error occurred: {str(e)}"}

# Initialize database on module import
DatabaseService.initialize_database()
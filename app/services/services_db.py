from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import or_

# Global variables for database models
Anime, Type, Status, Franchise, RelatedAnime, Fundub, FundubSynonym, AnimeFundub, Episode = (None,) * 9
Session = None

def initialize_database():
    global Anime, Type, Status, Franchise, RelatedAnime, Fundub, FundubSynonym, AnimeFundub, Episode, Session

    # Database setup
    engine = create_engine('sqlite:///data/anime_data.db')
    Session = sessionmaker(bind=engine)

    # Reflect the existing database into a new model
    Base = automap_base()
    Base.prepare(engine, reflect=True)

    # Map the models
    Anime = Base.classes.anime
    Type = Base.classes.type
    Status = Base.classes.status
    Franchise = Base.classes.franchise
    RelatedAnime = Base.classes.related_anime
    Fundub = Base.classes.fundub
    FundubSynonym = Base.classes.fundub_synonym
    AnimeFundub = Base.classes.anime_fundub
    Episode = Base.classes.episode

# Service functions
def get_anime_by_id(anime_id):
    session = Session()
    anime = session.query(Anime).options(
        joinedload(Anime.type).load_only(Type.name),
        joinedload(Anime.status).load_only(Status.name),
        joinedload(Anime.franchise)
    ).get(anime_id)
    session.close()
    return serialize(anime)

def get_anime_by_name(partial_name):
    session = Session()
    animes = session.query(Anime).filter(
        or_(
            Anime.titleUa.ilike(f'%{partial_name}%'),
            Anime.titleEn.ilike(f'%{partial_name}%')
        )
    ).all()
    session.close()
    return serialize(animes)

def get_related_animes(anime_id):
    session = Session()
    related_animes = session.query(Anime).join(
        RelatedAnime, Anime.id == RelatedAnime.anime_id2
    ).filter(RelatedAnime.anime_id1 == anime_id).options(
        joinedload(Anime.type).load_only(Type.name),
        joinedload(Anime.status).load_only(Status.name),
        joinedload(Anime.franchise)
    ).all()
    session.close()
    return serialize(related_animes)

def list_all_studios():
    session = Session()
    studios = session.query(Fundub).all()
    session.close()
    return serialize(studios)

def list_all_anime():
    session = Session()
    studios = session.query(Anime).options(
        joinedload(Anime.type).load_only(Type.name),
        joinedload(Anime.status).load_only(Status.name),
        joinedload(Anime.franchise)
    ).all()
    session.close()
    return serialize(studios)

def search_studio_by_name(partial_name):
    session = Session()
    # Create an alias for Fundub to join with FundubSynonym
    FundubSynonym = Base.classes.fundub_synonym
    synonym_subquery = session.query(FundubSynonym.fundub_id).filter(
        FundubSynonym.synonym.ilike(f'%{partial_name}%')
    ).subquery()

    studios = session.query(Fundub).filter(
        or_(
            Fundub.name.ilike(f'%{partial_name}%'),
            Fundub.id.in_(synonym_subquery)
        )
    ).all()
    session.close()
    return serialize(studios)

def search_studio_by_id(studio_id):
    session = Session()
    studios = session.query(Fundub).filter(Fundub.id == studio_id).all()
    session.close()
    return serialize(studios)

def get_studios_by_anime_id(anime_id):
    session = Session()
    studios = session.query(Fundub).join(
        AnimeFundub, Fundub.id == AnimeFundub.fundub_id
    ).filter(AnimeFundub.anime_id == anime_id).distinct().all()
    session.close()
    return serialize(studios)

def get_anime_by_studio_id(studio_id):
    session = Session()
    animes = session.query(Anime).join(
        AnimeFundub, Anime.id == AnimeFundub.anime_id
    ).filter(AnimeFundub.fundub_id == studio_id).distinct().all()
    session.close()
    return serialize(animes)

def get_episodes_by_anime_id(anime_id):
    session = Session()
    episodes = session.query(Episode).filter_by(anime_id=anime_id).all()
    session.close()
    return serialize(episodes)

# Helper function to serialize SQLAlchemy objects to JSON
def serialize(data):
    if isinstance(data, list):
        # Recursively serialize each item in the list
        return [serialize(item) for item in data]
    elif hasattr(data, '__dict__'):
        # Serialize SQLAlchemy model objects
        result = {}
        for column in data.__dict__:
            if not column.startswith('_'):  # Skip private and protected attributes
                attr = getattr(data, column)
                if hasattr(attr, '__dict__') or isinstance(attr, list):
                    # Recursively serialize nested objects or lists
                    result[column] = serialize(attr)
                else:
                    # Serialize simple attributes
                    result[column] = attr
        return result
    else:
        # Return simple data types directly
        return data
    
import requests
import os

def update_database():
    # URL of the database file in the GitHub repository
    url = "https://github.com/maksii/Stream2MediaServer/raw/main/data/anime_data.db"
    
    # Local path where the database should be stored
    local_db_path = "data/anime_data.db"
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(local_db_path), exist_ok=True)
    
    # Download the file
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        with open(local_db_path, 'wb', encoding='utf-8') as f:
            f.write(response.content)
        print("Database has been updated successfully.")
    except requests.RequestException as e:
        print(f"Failed to download the database: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    initialize_database()
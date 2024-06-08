from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import or_

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
#FundubSynonym = Base.classes.fundub_synonym
#AnimeFundub = Base.classes.anime_fundub
Episode = Base.classes.episode

# Service functions
def get_anime_by_id(anime_id):
    session = Session()
    anime = session.query(Anime).options(
        joinedload(Anime.type).load_only("name"),
        joinedload(Anime.status).load_only("name"),
        joinedload(Anime.franchise)
    ).get(anime_id)
    session.close()
    return anime

def get_anime_by_name(partial_name):
    session = Session()
    animes = session.query(Anime).filter(
        or_(
            Anime.titleUa.ilike(f'%{partial_name}%'),
            Anime.titleEn.ilike(f'%{partial_name}%')
        )
    ).all()
    session.close()
    return animes

def get_related_animes(anime_id):
    session = Session()
    related_animes = session.query(Anime).join(
        RelatedAnime, Anime.id == RelatedAnime.anime_id2
    ).filter(RelatedAnime.anime_id1 == anime_id).all()
    session.close()
    return related_animes

def list_all_studios():
    session = Session()
    studios = session.query(Fundub).all()
    session.close()
    return studios

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
    return studios

def get_studios_by_anime_id(anime_id):
    session = Session()
    studios = session.query(Fundub).join(
        AnimeFundub, Fundub.id == AnimeFundub.fundub_id
    ).filter(AnimeFundub.anime_id == anime_id).distinct().all()
    session.close()
    return studios

def get_animes_by_studio_id(studio_id):
    session = Session()
    animes = session.query(Anime).join(
        AnimeFundub, Anime.id == AnimeFundub.anime_id
    ).filter(AnimeFundub.fundub_id == studio_id).distinct().all()
    session.close()
    return animes

def get_episodes_by_anime_id(anime_id):
    session = Session()
    episodes = session.query(Episode).filter_by(anime_id=anime_id).all()
    session.close()
    return episodes

# Helper function to serialize SQLAlchemy objects to JSON
def serialize(data):
    if isinstance(data, list):
        return [serialize(item) for item in data]
    elif hasattr(data, '__dict__'):
        return {column: getattr(data, column) for column in data.__dict__ if not column.startswith('_')}
    else:
        return data
from database.repositories.BaseRepository import BaseRepository
from database.models.cards import Cards

class CardRepository(BaseRepository):
    model = Cards

from datetime import datetime
from decimal import Decimal
from sqlalchemy import update, delete, or_
import geopy.distance

from app.db.session import get_db
from app.crud.hero import put_hero
from app.models.hero import Hero
from app.models.occurrence import Occurrence, OccurrenceRanks, Attendance

db = get_db()

rank_to_strength_dict = {
    1:8,
    2:4,
    3:2,
    4:1
}

def get_pending_occurrences():
    return db.query(Occurrence).\
        filter(Occurrence.finish == None).\
            order_by(Occurrence.create.asc()).\
                all()

def get_available_heroes(occ_rank: OccurrenceRanks):
    query = db.query(Hero.id,Hero.name,Hero.lat,Hero.long,Hero.rank,Hero.available).\
        distinct(Hero.id).\
            filter(Hero.available == True)

    if occ_rank is not None:
        query = query.filter(Hero.rank.in_(occ_rank.get_possible_attending_hero_rank()))

    query = query.join(Hero.occurrences.of_type(Attendance), isouter=True).\
        join(Attendance.occurrence.of_type(Occurrence), isouter=True).\
            where(or_(Occurrence.finish <= datetime.now(),Hero.occurrences == None)).\
                order_by(Occurrence.create.desc())

    return query.all()

def main():
    while True:
        alloc_hero_for_pending_occ()

def alloc_hero_for_pending_occ():
    pending_occurrences = get_pending_occurrences()

    for occurrence in pending_occurrences:
        occurrence_hero_alloc(occurrence)

def calculate_distance(hero, coord_to) -> Decimal:
    return geopy.distance.geodesic((hero.lat,hero.long), coord_to).km

def occurrence_hero_alloc(occ: Occurrence):
    available_heroes: list = get_available_heroes(occ.rank)
    if len(available_heroes) == 0:
        
        return None
    occ_strength = rank_to_strength_dict[occ.rank.value]

    closest_party = []
    party_strength = 0
    available_heroes.sort(key=lambda h: calculate_distance(h, (occ.lat,occ.long)))

    #gathering enough heroes for the occurrence or finding it
    for hero in available_heroes:
        hero_strength = rank_to_strength_dict[hero.rank.value]
        if hero_strength == occ_strength:
            closest_party = [hero]
            party_strength = hero_strength
        else:
            closest_party.append(hero)
            party_strength += hero_strength

        if party_strength >= occ_strength:
            break

    # Removing excess of strength
    if party_strength > occ_strength:
        excess = party_strength - occ_strength
        for hero in closest_party.copy():
            hero_strength = rank_to_strength_dict[hero.rank.value]
            if hero_strength <= excess:
                party_strength -= hero_strength
                closest_party.remove(hero)

            if party_strength == occ_strength:
                break

    if not closest_party:
        return None
    
    for hero in closest_party:
        attend = Attendance()
        attend.hero_id = hero.id
        occ.heroes.append(attend)

    stmt = update(Occurrence).where(Occurrence.id == occ.id).values(
        start=datetime.now(),
        finish=occ.calculate_finish_time()
    ).execution_options(synchronize_session="fetch")

    db.execute(stmt)
    db.commit()


    return occ

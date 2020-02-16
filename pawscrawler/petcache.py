from pawscrawler.models import Pet, PollRecord
from pawscrawler import petmanager
from datetime import datetime, timedelta
import pytz

def update_pet_status(id, status):
    pet = Pet.objects.get(pk=id)
    pet.status = status
    pet.save()

def get_cached_pets():
    now = pytz.UTC.localize(datetime.utcnow())
    cachelength = timedelta(minutes=30)
    pollrecords = PollRecord.objects.all()

    if pollrecords.count() < 1:
        pollrecords = [PollRecord(retrievaltime=now - cachelength)]

    pollrecord = pollrecords[0]

    if pollrecord.retrievaltime <= (now - cachelength):
        pets = __merge_pets(pollrecord, now)
    else:
        pets = Pet.objects.all()

    formattedpets = map(lambda x: FormattedPet(x), pets) 

    return formattedpets

def __merge_pets(pollrecord, now):
    cached_pets = Pet.objects.all()
    pet_urls = petmanager.get_pet_urls()
    
    final_pets = []

    new_pet_urls = set()
    [new_pet_urls.add(i) for i in pet_urls]

    cached_pet_map = {}
    for pet in cached_pets:
        if pet.url in new_pet_urls:
            cached_pet_map[pet.url] = pet
        else:
            pet.delete()

    for pet_url in pet_urls:
        if pet_url not in cached_pet_map:
            pet = petmanager.parse_pet(pet_url)
            pet.status = 0
            final_pets.append(pet)
            pet.save()
        else:
            final_pets.append(cached_pet_map[pet_url])

    pollrecord.retrievaltime = now
    pollrecord.save()

    return final_pets

def __merge_petsOLD(pollrecord, now):
    cached_pets = Pet.objects.all()
    pets = petmanager.get_pets([t.url for t in cached_pets])
    
    final_pets = []
    [final_pets.append(i) for i in cached_pets] 

    cached_pet_urls = set()
    [cached_pet_urls.add(i.url) for i in cached_pets]

    for pet in pets:
        if pet.url not in cached_pet_urls:
            pet.status = 0
            final_pets.append(pet)
            pet.save()

    pollrecord.retrievaltime = now
    pollrecord.save()

    return final_pets

class FormattedPet:
    def __init__(self, pet):
        self.id = pet.id
        self.name = pet.name
        self.breed = pet.breed
        self.gender = pet.gender
        self.weight = str(round(pet.weight)) + " lbs"
        self.location = pet.location
        self.url = pet.url
        self.status = pet.status

        if pet.age < 1:
            self.age = str(round(pet.age * 12)) + " months"
        else:
            self.age = str(round(pet.age)) + " years"
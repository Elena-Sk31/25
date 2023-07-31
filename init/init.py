from os import environ
from random import randint
from tempfile import mktemp

from dotenv import load_dotenv
from faker import Faker

from api import PetFriends

load_dotenv()


valid_email = environ.get('USERNAME')
valid_password = environ.get('PASSWORD')


if __name__ == '__main__':
    pf = PetFriends()
    faker = Faker()

    names = set()

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    for pet in my_pets['pets']:
        pf.delete_pet(auth_key, pet['id'])

    for _ in range(randint(30, 80)):
        # Формируем уникальные имена
        while True:
            name = faker.first_name()

            if name not in names:
                names.add(name)
                break

        animal_type = faker.language_name()
        age = randint(0, 20)

        _, pet = pf.create_pet_simple(auth_key, name, animal_type, age)

        if randint(0, 2):
            pet_photo = mktemp() + '.jgp'

            with open(pet_photo, 'wb') as f:
                f.write(faker.image(image_format='jpeg'))

            pf.set_photo(auth_key, pet['id'], pet_photo)

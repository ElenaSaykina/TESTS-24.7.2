import sys
sys.path.append('C:/Users/Admin/PycharmProjects/module-24-pets')
from api import PetFriends
from settings import valid_email, valid_password
import os


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Карбоскин', animal_type='котяра',
                                     age='99', pet_photo='images/cat2.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")



# 1

def test_get_api_key_with_invalid_user():
        """Запрашиваем API key с невалидными данными."""
        email, password = "invalid@example.com", "wrongpassword"
        status, result = pf.get_api_key(email, password)
        assert status == 403
        assert 'key' not in result


# 2

def test_add_new_pet_with_missing_data():
    """Добавляем питонца с неполноценными данными."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name='Хрюша', animal_type='', age='')
    assert status == 400


# 3

def test_add_new_pet_with_excessive_age():
    """Добавляем питомца со слишком большим возрастом."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name='Fido', animal_type='Dog', age='99999')
    assert status == 400

# 4

def test_delete_non_existent_pet():
    """Удаляем несуществующего питомца."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.delete_pet(auth_key, pet_id='nonexistentid123')
    assert status == 404


# 5

def test_update_pet_with_invalid_age():
    """Обновляем питомца с неверным возрастом."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pets = pf.get_list_of_pets(auth_key, "my_pets")
    if pets['pets']:
        status, result = pf.update_pet_info(auth_key, pets['pets'][0]['id'], 'Rex', 'Dog', 'invalid-age')
        assert status == 400
    else:
        raise Exception("No pets available to update")

# 6

def test_get_pet_with_invalid_id():
    """запрашиваем информацию питомца с неверным ID."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_pet_by_id(auth_key, 'thisisnotavalidid')
    assert status == 400


# 7

def test_upload_photo_for_non_existent_pet():
    """загружаем фото для несуществуюэего питомца."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), 'images/cat2.jpg')
    status, result = pf.set_pet_photo(auth_key, 'nonexistentpetid', pet_photo)
    assert status == 404

# 8

def test_create_pet_simple_with_empty_fields():
    """Создаем питомца с пустыми полями."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, '', '', '')
    assert status == 400


# 9

def test_create_pet_simple_with_special_characters():
    """Создаем имя с непредусмотренными символами."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, 'Sn@ppy', 'Dog', '5')
    assert status == 200

# 10

def test_get_all_pets_with_invalid_filter():
    """Запрашиваем список с несуществующим филтром."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter='invalidfilter')
    assert status == 400
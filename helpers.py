from faker import Faker

fake = Faker()

# Генерация email
def mail_generator():
    return fake.ascii_free_email()

# Генерация пароля
def password_generator():
    return fake.password(length=10, special_chars=False)

# Генерация имени
def name_generator():
    return fake.name()

# Создание payload для нового пользователя
def payload_new_user():
    return {
        "email": mail_generator(),
        "password": password_generator(),
        "name": name_generator()
    }
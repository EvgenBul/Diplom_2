main_url = 'https://stellarburgers.nomoreparties.site' # главный URL точки входа

post_register_user = f'{main_url}/api/auth/register' # Метод для регистрации нового пользователя
post_login_user = f'{main_url}/api/auth/login' # Метод для входа в систему
patch_change_user_data = f'{main_url}/api/auth/user' # Метод изменения данных пользователя
get_user_data = f'{main_url}/api/auth/user' # Метод получения данных о пользователе
del_user_data = f'{main_url}/api/auth/user' # Метод удаления пользователя

post_create_order = f'{main_url}/api/orders' # Метод создания заказа
get_user_order = f'{main_url}/api/orders' # Метод получения заказа конкретного пользователя
get_all_orders = f'{main_url}/api/orders/all' # Метод получения всех заказов (максимум 50 последних)
get_ingredients = f'{main_url}/api/ingredients' # Получение данных об ингредиентах



# почта и пароль существующего пользователя.
exist_user_email = "testpc99@ya.com"
exist_user_password = "123456"

# payload существующего пользователя
exist_user_payload = {
    "email": "testpc99@ya.com",
    "password": "123456"
}

# заготовки ожидаемых текстов ответов
user_error_403_exists = {"success": False, "message": "User already exists"}
user_error_403_no_required_fields =  {"success": False, "message": "Email, password and name are required fields"}
user_error_403_unauthorized =  {"success": False, "message": "email or password are incorrect"}
user_error_401_unauthorized_user =  {"success": False, "message": "You should be authorised"}
user_error_403_token_bad_change_data =  {"success": False, "message": "jwt malformed"}
user_delete_202 = {"success": True, "message": "User successfully removed"}
no_ingredient_error_400 = {"success": False, "message": "Ingredient ids must be provided"}
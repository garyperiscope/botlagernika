from config import supabase

# 🔹 Функция сохранения данных в Supabase
def save_user(parent_name, child_name, birth_date, attended_shifts):
    supabase.table("users").insert({
        "parent_name": parent_name,
        "child_name": child_name,
        "birth_date": birth_date,
        "attended_shifts": attended_shifts
    }).execute()

# 🔹 Функция получения данных пользователя
def get_user(parent_name):
    response = supabase.table("users").select("*").eq("parent_name", parent_name).execute()
    return response.data if response.data else None

# 🔹 Функция обновления данных пользователя
def update_user(parent_name, updated_data):
    supabase.table("users").update(updated_data).eq("parent_name", parent_name).execute()



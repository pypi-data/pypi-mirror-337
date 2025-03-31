from src.edubase_api import EduBaseApi

api = EduBaseApi("2042474bbc2ab91d36b95d5f3f58138a")

employee = api.getinfo_employee()

print(employee, end='\n')
import json
import itertools

# Генерация всех возможных комбинаций ролей
roles = [f'{i}' for i in range(10)]  # 10 возможных ролей
all_combinations = list(itertools.combinations(roles, 5))  # Все возможные комбинации для одной команды

# Создание словаря для хранения уникальных комбинаций ролей
teams = {}

# Создание комбинаций для двух команд 5x5
for team1 in all_combinations:
    for team2 in all_combinations:
        if team1 != team2:
            key = ''.join(team1) + '_' + ''.join(team2)
            teams[key] = []

            if len(teams) >= 63504:  # Прерываем цикл после создания нужного количества комбинаций
                break
    else:
        continue
    break

# Запись данных в JSON файл
filename = 'teams_roles.json'
with open(filename, 'w') as file:
    json.dump(teams, file, indent=4)

print(f"Создан файл '{filename}' с {len(teams)} уникальными ключами команд и их ролями.")

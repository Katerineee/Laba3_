import random
import pandas as pd

# Константи
NUM_GROUPS = 5
NUM_SUBGROUPS = 2
NUM_LECTORS = 10
NUM_ROOMS = 7
NUM_SLOTS = 20

# Генерація груп
groups = [{"group_id": i + 1, "students": random.randint(20, 40)} for i in range(NUM_GROUPS)]

# Генерація предметів
subjects = [
    {"subject": f"Subject_{i + 1}", "hours": random.randint(30, 60), "lectures": True, "practicals": True}
    for i in range(8)
]

# Генерація викладачів
lectors = [
    {"lector_id": i + 1, "subjects": random.sample([s["subject"] for s in subjects], k=random.randint(1, 5))}
    for i in range(NUM_LECTORS)
]

# Генерація аудиторій
rooms = [{"room_id": i + 1, "capacity": random.randint(30, 50)} for i in range(NUM_ROOMS)]

# Генерація часових слотів
slots = [f"Day_{d} Slot_{s}" for d in range(1, 6) for s in range(1, 5)]


# Функція генерації початкового розкладу
def generate_schedule(groups, subjects, lectors, rooms, slots):
    schedule = []
    for slot in slots:
        group = random.choice(groups)
        subject = random.choice(subjects)
        lector = random.choice([l for l in lectors if subject["subject"] in l["subjects"]])
        room = random.choice([r for r in rooms if r["capacity"] >= group["students"]])

        schedule.append({
            "slot": slot,
            "group_id": group["group_id"],
            "subject": subject["subject"],
            "lector_id": lector["lector_id"],
            "room_id": room["room_id"]
        })
    return schedule


# Функція оцінки фітнесу
def fitness_function(schedule):
    penalty = 0

    # Жорсткі умови
    # 1. Один лектор одночасно в одному слоті
    lectors_conflicts = pd.DataFrame(schedule).groupby(["slot", "lector_id"]).size()
    penalty += sum(lectors_conflicts - 1)

    # 2. Одна група одночасно в одному слоті
    group_conflicts = pd.DataFrame(schedule).groupby(["slot", "group_id"]).size()
    penalty += sum(group_conflicts - 1)

    # 3. Одна аудиторія одночасно в одному слоті
    room_conflicts = pd.DataFrame(schedule).groupby(["slot", "room_id"]).size()
    penalty += sum(room_conflicts - 1)

    return penalty


# Функція схрещування
def crossover(parent1, parent2):
    mid = len(parent1) // 2
    return parent1[:mid] + parent2[mid:]


# Функція мутації
def mutate(schedule):
    idx = random.randint(0, len(schedule) - 1)
    schedule[idx]["slot"] = random.choice(slots)


# Генетичний алгоритм
def genetic_algorithm(groups, subjects, lectors, rooms, slots, generations=100, population_size=10):
    population = [generate_schedule(groups, subjects, lectors, rooms, slots) for _ in range(population_size)]

    for generation in range(generations):
        population = sorted(population, key=fitness_function)
        print(f"Generation {generation}: Best fitness = {fitness_function(population[0])}")

        next_generation = population[:population_size // 2]
        while len(next_generation) < population_size:
            parent1, parent2 = random.sample(next_generation, 2)
            child = crossover(parent1, parent2)
            if random.random() < 0.1:
                mutate(child)
            next_generation.append(child)
        population = next_generation

    return sorted(population, key=fitness_function)[0]


# Генерація початкового розкладу
initial_schedule = generate_schedule(groups, subjects, lectors, rooms, slots)

# Виконання генетичного алгоритму
final_schedule = genetic_algorithm(groups, subjects, lectors, rooms, slots)

# Експорт результату в CSV
final_df = pd.DataFrame(final_schedule)
final_df.to_csv("final_schedule.csv", index=False)

# Вивід розкладу в консоль
print(final_df)

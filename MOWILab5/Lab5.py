import random
import pandas as pd

def fitness(chromosomes):
    score = 0

    chromosomes_by_class = {1: [],
                            2: [],
                            3: []}

    for k in chromosomes:
        day, class_num, teacher, subject, room, time = k
        chromosomes_by_class[class_num].append(k)

    for class_num, list_chromosomes in chromosomes_by_class.items():
        total_lesson = 0
        for chromosome in list_chromosomes:
            total_lesson += 1
        if total_lesson == 24:
          score += 1

    chromosomes_by_class_day = {1: {1: [], 2: [], 3: [], 4: [], 5: []},
                                2: {1: [], 2: [], 3: [], 4: [], 5: []},
                                3: {1: [], 2: [], 3: [], 4: [], 5: []}}

    for k in chromosomes:
        day, class_num, teacher, subject, room, time = k
        chromosomes_by_class_day[class_num][day].append(k)

    for class_num, weeks in chromosomes_by_class_day.items():
        for num_day, lessons in weeks.items():
          num_lesson = len(lessons)
          if num_lesson > 2 and num_lesson < 6:
              score += 1

    for class_num, list_chromosomes in chromosomes_by_class.items():
        subjects = set()
        for chromosome in list_chromosomes:
            subject = chromosome[3]
            subjects.add(subject)
        if len(subjects) == 8:
            score += 1

    for class_num, weeks in chromosomes_by_class_day.items():
        for num_day, lessons in weeks.items():
            sorted_lessons = sorted(lessons, key=lambda x: x[-1], reverse=True)
            for i in range(len(sorted_lessons) - 1):
                current_time = sorted_lessons[i][-1]
                next_time = sorted_lessons[i + 1][-1]
                if next_time - current_time == 1:
                    score += 1

    checked_values = {}

    for chromosome in chromosomes:
        day, _, teacher, _, room, time = chromosome

        key = (day, room, time)

        if key in checked_values:
            for checked_chromosome in checked_values[key]:
                _, _, checked_teacher, _, checked_room, _ = checked_chromosome
                if checked_teacher == teacher and checked_room == room:
                    return 0
            else:
                checked_values[key].append(chromosome)
        else:
            checked_values[key] = [chromosome]

    chromosomes_by_class_mainteacher = {1: [],
                                        2: [],
                                        3: []}

    for k in chromosomes:
        day, class_num, teacher, subject, room, time = k
        if(teacher == class_num):
            chromosomes_by_class_mainteacher[class_num].append(k)

    for class_num, list_chromosomes in chromosomes_by_class_mainteacher.items():
        total_lesson = len(list_chromosomes)
        if total_lesson > 11:
            score += 1

    teacher_subjects = {
        1: [1, 2],
        2: [3],
        3: [4],
        4: [5, 6],
        5: [7, 8]
    }
    for k in chromosomes:
        if k[3] in teacher_subjects.get(k[2], []):
            score += 1

    room_subjects = {
        1: [1, 2],
        2: [1, 2, 4],
        3: [3],
        4: [5],
        5: [6,7],
        6: [8]
    }
    for k in chromosomes:
        if k[3] in room_subjects.get(k[4], []):
            score += 1
    return score

def create_chromosome(class_num=None):
    day = random.randint(1, 5)  # день тижня (від 1 до 5)
    if class_num is None:
        class_num = random.randint(1, 3) # клас (від 1 до 3)
    teacher = random.randint(1, 5)  # вчитель (від 1 до 5)
    subject = random.randint(1, 8)  # предмет (від 1 до 8)
    room = random.randint(1, 6)  # кімната (від 1 до 6)
    time = random.randint(1, 5)  # час (від 1 до 5)

    chromosome = [day, class_num, teacher, subject, room, time]

    return chromosome

def generate_chromosomes():
    chromosomes = []
    for day in range(0,5):
        num_less = random.randint(3,5)
        for less in range(0,num_less):
            chromosomes.append(create_chromosome(1))
    for day in range(0,5):
        num_less = random.randint(3,5)
        for less in range(0,num_less):
            chromosomes.append(create_chromosome(2))
    for day in range(0,5):
        num_less = random.randint(3,5)
        for less in range(0,num_less):
            chromosomes.append(create_chromosome(3))

    return chromosomes

def generate_initial_population(population_size):
    population = []
    for i in range(population_size):
        population.append(generate_chromosomes())
    return population

def crossover_population(chromosomes1, chromosomes2):
    crossover_point = random.randint(1, len(chromosomes1) - 1)
    new_chromosomes = chromosomes1[:crossover_point] + chromosomes2[crossover_point:]

    day_chromosomes = {}
    for chromosome in new_chromosomes:
        day = chromosome[0]
        if day not in day_chromosomes:
            day_chromosomes[day] = []
        day_chromosomes[day].append(chromosome)

    for day in day_chromosomes:
        for class_num in range(1, 4):
            class_lessons = [c for c in day_chromosomes[day] if c[1] == class_num]
            while len(class_lessons) < 3:
                new_chromosome = create_chromosome(class_num)
                if new_chromosome not in class_lessons:
                    day_chromosomes[day].append(new_chromosome)
                    class_lessons.append(new_chromosome)
            while len(class_lessons) > 5:
                remove_index = random.randint(0, len(class_lessons) - 1)
                day_chromosomes[day].remove(class_lessons[remove_index])
                class_lessons.remove(class_lessons[remove_index])

    new_chromosomes = []
    for day in day_chromosomes:
        new_chromosomes += day_chromosomes[day]

    return new_chromosomes

def apply_mutation(child, mutation_rate):
    num_mutation = random.randint(0, 30)
    if random.random() < mutation_rate:
        child[num_mutation][4] = random.randint(1, 6)
    return child

def select_parents(population, fitness_scores):
    total_fitness = sum(fitness_scores)

    if total_fitness == 0:
        probabilities = [1 / len(population)] * len(population)
    else:
        probabilities = [score / total_fitness for score in fitness_scores]

    parent1 = random.choices(population, weights=probabilities)[0]
    parent2 = random.choices(population, weights=probabilities)[0]

    return parent1, parent2

def select_survivors(population, fitness_scores, num_survivors):
    sorted_population = [chromosome for _, chromosome in sorted(zip(fitness_scores, population), reverse=True)]
    return sorted_population[:num_survivors]

def run_genetic_algorithm(population_size, num_generations, mutation_rate):
    populations = generate_initial_population(population_size)
    for i in range(num_generations):
        fitness_scores = [fitness(population) for population in populations]
        parents = [select_parents(populations, fitness_scores) for i in range(population_size)]
        children = [crossover_population(parent1, parent2) for parent1, parent2 in parents]
        populations = [apply_mutation(child, mutation_rate) for child in children]
        populations = select_survivors(populations, fitness_scores, population_size)
    best_chromosome = max(populations, key=fitness)
    return best_chromosome

finish_chromosomes = run_genetic_algorithm(200, 40, 0.3)

df = pd.DataFrame(columns=["День", "Клас", "Вчитель", "Предмет", "Приміщення"])

for chromosome in finish_chromosomes:
    day, class_num, teacher, subject, room, time = chromosome
    df = pd.concat([df, pd.DataFrame({
        "День": [day],
        "Клас": [class_num],
        "Вчитель": [teacher],
        "Предмет": [subject],
        "Приміщення": [room]
    })])

for day in range(1, 6):
    print(f"День {day}:")
    day_df = df[df["День"] == day]
    class_1_df = day_df[day_df["Клас"] == 1].reset_index(drop=True)
    class_2_df = day_df[day_df["Клас"] == 2].reset_index(drop=True)
    class_3_df = day_df[day_df["Клас"] == 3].reset_index(drop=True)
    print(class_1_df)
    print()
    print(class_2_df)
    print()
    print(class_3_df)
    print()

print(f"Fit: {fitness(finish_chromosomes)}")
import random
from datetime import datetime

cities = ["Riga", "Daugavpils", "Liepaja", "Jelgava", "Jurmala", "Ventspils", "Rezekne", "Valmiera", "Ogre", "Jekabpils"]
city_count = 10


distances = {
    ("Riga", "Daugavpils"): 230, 
    ("Riga", "Liepaja"): 194, 
    ("Riga", "Jelgava"): 43, 
    ("Riga", "Jurmala"): 25,
    ("Riga", "Ventspils"): 189, 
    ("Riga", "Rezekne"): 242, 
    ("Riga", "Valmiera"): 107, 
    ("Riga", "Ogre"): 37,
    ("Riga", "Jekabpils"): 145, 
    ("Daugavpils", "Liepaja"): 272, 
    ("Daugavpils", "Jelgava"): 191,
    ("Daugavpils", "Jurmala"): 255,
    ("Daugavpils", "Ventspils"): 303, 
    ("Daugavpils", "Rezekne"): 88, 
    ("Daugavpils", "Valmiera"): 214,
    ("Daugavpils", "Ogre"): 197, 
    ("Daugavpils", "Jekabpils"): 91, 
    ("Liepaja", "Jelgava"): 150, 
    ("Liepaja", "Jurmala"): 187,
    ("Liepaja", "Ventspils"): 112, 
    ("Liepaja", "Rezekne"): 330, 
    ("Liepaja", "Valmiera"): 268, 
    ("Liepaja", "Ogre"): 223,
    ("Liepaja", "Jekabpils"): 303, 
    ("Jelgava", "Jurmala"): 60, 
    ("Jelgava", "Ventspils"): 180, 
    ("Jelgava", "Rezekne"): 232,
    ("Jelgava", "Valmiera"): 137, 
    ("Jelgava", "Ogre"): 78, 
    ("Jelgava", "Jekabpils"): 160, 
    ("Jurmala", "Ventspils"): 150,
    ("Jurmala", "Rezekne"): 267, 
    ("Jurmala", "Valmiera"): 132, 
    ("Jurmala", "Ogre"): 61, 
    ("Jurmala", "Jekabpils"): 185,
    ("Ventspils", "Rezekne"): 390, 
    ("Ventspils", "Valmiera"): 291, 
    ("Ventspils", "Ogre"): 248,
    ("Ventspils", "Jekabpils"): 341,
    ("Rezekne", "Valmiera"): 146, 
    ("Rezekne", "Ogre"): 219, 
    ("Rezekne", "Jekabpils"): 86, 
    ("Valmiera", "Ogre"): 92,
    ("Valmiera", "Jekabpils"): 160, 
    ("Ogre", "Jekabpils"): 125
}

initial_population = {
    "Riga": 632614, "Daugavpils": 82604, "Liepaja": 68945, "Jelgava": 55972,
    "Jurmala": 49325, "Ventspils": 34377, "Rezekne": 27820, "Valmiera": 24879,
    "Ogre": 24356, "Jekabpils": 22056
}

infected_population = {city: int(initial_population[city] * random.uniform(0, 0.05)) for city in cities}


def get_distance(city1, city2):
    if city1 == city2:
        return 0
    return distances.get((city1, city2)) or distances.get((city2, city1))


def update_infected_population(city, hours):
    global infected_population
    infected_population[city] *= infect_coef ** hours
    infected_population[city] = int(infected_population[city])


def display_cities():
    print("No.    City                  Population / Infected /       %")
    display_line()
    for i, city in enumerate(cities):
        infected_percentage = (infected_population[city] / initial_population[city]) * 100
        if city == current_city:
            s = '>>'
        else:
            s = '  '  
        print(f"{s} {i+1:2}  {city:20}  {initial_population[city]:10} / {infected_population[city]:8} /   {infected_percentage:.2f}%")
    display_line()


def display_gamer_status():
    display_line()
    print(f"Vaccines: {current_vaccines:5} of {max_vaccines:5}                  Your time: {total_time: 5.2f}", end='\n')
    display_line()


def display_title():
    print("\nMISSION IMPOSSIBLE") 
    print("-"*90, end='\n')
    print("  Your goal is keep low infection level as long as possible. Each hour it is raising up.", end="\n")
    print("  You can transfer from one city to other by entering city no..", end="\n")    
    print("  Yoсдуфкu can produce (P or P[count]) vaccine to increase You stock.", end="\n")
    print("  You can use (U or U[count]) vaccine in current city to decrease infection level.", end="\n")
    print("  All actions, includinng You choice time. spend time to increase infection level", end="\n")
    print("  Game is over when infection level will 10% or more in any city", end="\n")
    print("  To finish game enter Q", end="\n")
    print("-"*90, end='\n')


def display_line():
    print("-"*60, end='\n')


def check_game_over():
    mission_completed = True
    for city in cities:
        mission_completed = mission_completed and (infected_population[city] <= 1)
        if infected_population[city] / initial_population[city] > 0.1:
            print(f"\nMISSION FAILED! Infection level in {city} is over 10%. Call Ethan Hunt to save our souls!")
            return True
        
    if mission_completed:
        print(f"\nMISSION COMPLETED! Ethan Hunt has been dismissed. You are our NEW HERO!")
        return True
    
    return False


def handle_user_action():
    global current_city
    global current_vaccines
    global total_time 
    global infected_population

    game_over = False
    
    start_time = datetime.now()
    choice = input("Your choice: ")
    choice = choice.replace(" ", "").lower()
    end_time = datetime.now()
    action_time = (end_time - start_time).total_seconds() / 10.0
    
    try:
        if choice == 'exit' or choice == 'e' or choice == 'q' or choice == 's':
            game_over = True
        elif choice[0] in ('p'):
            # Produce new vaccines
            if len(choice[1:]) == 0:
                qty = max_vaccines
            else:
                qty = int(choice[1:]) 
            if qty < 0:
                qty = 0
            if max_vaccines - current_vaccines < qty:
                qty = max_vaccines - current_vaccines
            current_vaccines += qty    
            action_time += float(qty) / float(produce_speed)     
        elif choice[0] in ('u'):
            # Use vaccines
            if len(choice[1:]) == 0:
                qty = current_vaccines
            else:
                qty = int(choice[1:]) 
            if qty < 0:
                qty = 0    
            if infected_population[current_city] < qty:
                qty = infected_population[current_city]
            infected_population[current_city] -= qty  
            current_vaccines -= qty      
            action_time += float(qty) / float(usage_speed)  
        else:
            chosen_index = int(choice) - 1
            if 0 <= chosen_index < len(cities):
                chosen_city = cities[chosen_index]
                if chosen_city == current_city:
                    print("You are in this city. Select another city.")
                else:
                    distance = get_distance(current_city, chosen_city)
                    action_time += float(distance) / float(transfer_speed)
                    current_city = chosen_city
            else:
                print("Incorrect number of city.")
    except ValueError:
        print("Incorrect input. Correct examples: 2, 10, P, U, P250, U100")

    for city in cities:
        update_infected_population(city, action_time)
    total_time += action_time

    return game_over


def init_game():
    global cities
    global current_city 
    global max_vaccines 
    global current_vaccines
    global total_time 
    global transfer_speed
    global produce_speed 
    global usage_speed 
    global infect_coef

    current_city = random.choice(cities)
    max_vaccines = 2000
    current_vaccines = random.randint(100, max_vaccines)
    produce_speed = 500
    usage_speed = 500
    transfer_speed = 70
    infect_coef = 1.05

    total_time = 0.00


def main():
    display_title()

    while True:
        print("\n"*2)
        display_gamer_status()
        display_cities()
        if check_game_over():
            break
        if handle_user_action():   
            break 
       

init_game()
main()
from definitions import *

def main():
    location = "NonlinearMap.csv"
    location1 = "PostOffices.csv"

    school_cities = {} #key value pair of schools and the cities they're located in
    delivery_map = load_map(location, school_cities) #linked list representation of the graph modeled using a dictionary

    post_offices = load_postOffice(location1) #the distances between post offices will be stored here

    clear_terminal()

    cities = []

    for loc in school_cities.values():
        if not loc in set(cities):
            cities.append(loc)
    
    if len(school_cities) < 1:
        print("Failed to load map!")

    else:
        choice = ""
        while choice != len(cities) + 1:
            clear_terminal()
            for i in range(0, len(cities)):
                print(f"{i+1} - {cities[i][:-12]}")
            print(f"{len(cities)+1} - Exit")

            choice = input("Where do you want to start? ")

            if choice.isdigit():
                choice = int(choice)
                if choice >= 1 and choice <= len(cities):
                    deliver_mails(cities[choice-1], delivery_map, school_cities, post_offices)
                elif choice < 1 or choice > len(cities) + 1:
                    print("Invalid Input")
                    input("Press 'Enter' to continue...")
            else:
                print("Invalid Input!")
                input("Press 'Enter' to continue...")

if __name__ == "__main__":
    main()
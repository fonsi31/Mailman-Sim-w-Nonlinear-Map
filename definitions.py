import csv
import os
from time import sleep
import shutil

motorcycle = r"""
--------------------         `   `.
       <```--...       .---.//  < `.
         `..     `.___ /       ___`.'
          _ `_.       `     .'\\__
        .'---`.`.          / .'---`.
       /.'  _`.\_\        / /.'\\ `.\
       ||  <__||_|        | ||  ~  ||
       \`.___.'/ /________\ \`.___.'/
        `.___.'              `.___.' 
"""

terminal_width = shutil.get_terminal_size().columns
motorcycle_width = max(len(line) for line in motorcycle.splitlines())
motorcycle_center = (motorcycle_width // 2) + 6 #Added 6 units since the cargo box forces the center to go further left of the motorcycle

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def load_map(file_name, schools):
    file_path = os.path.join(os.path.dirname(__file__), file_name)

    if not os.path.exists(file_path):
        print("File not found!")
        print("Press 'enter' to continue...")
        return {}
    
    with open(file_path, "r", newline="") as file:
        try:
            temp = csv.reader(file)
            next(temp, None)
            delivery_map = {}

            for line in temp:

                src = line[1]
                dest = line[2]
                distance = float(line[3])

                if src not in delivery_map:
                    delivery_map[src] = {
                        dest: distance
                    }
                    schools[src] = line[0] + " Post Office"
                else:
                    delivery_map[src][dest] = float(line[3])
                
                if dest not in delivery_map:
                    delivery_map[dest] = {
                        src: distance
                    }
                    schools[dest] = line[0] + " Post Office"
                else:
                    delivery_map[dest][src] = distance

            return delivery_map
        
        except Exception as e:
            print("Error: ", e)
            input("Press 'Enter' to continue...")
            return {}
  
def load_postOffice(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)

    if not os.path.exists(file_path):
        print("File not found!")
        print("Press 'enter' to continue...")
        return {}

    with open(file_path, "r", newline="") as file:
        try:
            temp = csv.reader(file)
            next(temp, None)
            postOffices = {}
            for line in temp:

                src = line[0]
                dest = line[1]
                distance = float(line[2])

                if src not in postOffices: # [:-12] notation cuts off the 12 rightmost units of the string removing " Post Office" for consistent format across data
                    postOffices[src] = {
                        dest: distance
                    }
                else:
                    postOffices[src][dest] = distance

                if dest not in postOffices:
                    postOffices[dest] = {
                        src: distance
                    }
                else: 
                    postOffices[dest][src] = distance
            return postOffices

        except Exception as e:
            print("Error: ", e)
            input("Press 'Enter' to continue")
            return {}

def display_animation(path, mails, current_city): #mails is sorted in an ascending order
    clear_terminal()
    post_office = current_city + " Post Office"
    road = "-" * 25

    route = """"""
    shift_right = " " * 8 # shifts the route by n units of white spaces to the right
    route = shift_right + " " * (len(post_office) // 2) + "○" + "\n" + shift_right + post_office #base form of the route
    routes = []
    dropoff_points = []
    for node in path: #Draw route
        before = route #take a snapshot of the route before you add another road in case the route will be too long after adding another road
        lines = route.splitlines()
        lines[0] += road + "○"

        if node in mails:
            dropoff_points.append(len(lines[0]))

        route = "\n".join(lines)   
        route += " " * 6 + node[:19]
        route_width = max(len(line) for line in route.splitlines())

        if route_width >= terminal_width:
            dropoff_points.pop()
            routes.append(before)
            route = shift_right + " " * (len(post_office) // 2) + "○" + "\n" + shift_right + post_office #reset route to its base form and add remaining roads
            lines = route.splitlines()
            lines[0] += road + "○"
            dropoff_points.append(len(lines[0]))
            route = "\n".join(lines)
            route += " " * 6 + node[:19]

    routes.append(route)

    position = 0 
    i = 0 # index of the current route visible on the terminal
    j = 0 #index for the current dropoff point
    reversed_mails = mails[::-1] #reverse the sorted mails to emulate a stack in which the nearest mail will be popped first
    while len(reversed_mails) > 0:
        deliveries = """"""
        for mail in reversed_mails: #draws the cargo box
            deliveries = "|" + mail[:19] + "|\n" + deliveries
            deliveries = "--------------------\n" + deliveries
        deliveries = deliveries.rstrip("\n")
        figure = deliveries + motorcycle
        flag = True #permission to print the figure
        offset = " " * position
        frame = "\n".join(offset + line for line in figure.splitlines()) #keeps appending space before the frame making it look like its moving
        if motorcycle_width + len(offset) >= terminal_width:
            position = -1
            flag = False
            if i < len(routes):
                i += 1
        print(f"Path: {path}")
        print(f"mails: {mails}")
        print(f"Droppoff Points: {dropoff_points}")
        if position + motorcycle_center == dropoff_points[j]:
            reversed_mails.pop()
            if j < len(dropoff_points):
                j += 1
        position += 1
        if flag:
            print(frame)
        print(routes[i])
        sleep(0.25) 
        clear_terminal()

    #draw and print the figure one last time
    deliveries = """"""
    for mail in reversed_mails: #draws the cargo box
        deliveries = "|" + mail[:19] + "|\n" + deliveries
        deliveries = "--------------------\n" + deliveries
    deliveries = deliveries.rstrip("\n")
    figure = deliveries + motorcycle
    offset = " " * position
    frame = "\n".join(offset + line for line in figure.splitlines())
    return frame + "\n" + routes[i]

def shortest_path(destinations, map, start): #djikstra's algorithm
    shortest_path = [] 

    visited_dest = set()

    while len(visited_dest) < len(destinations): #perform djikstra from each destination
        min_cost = {} #key value pairs of nodes and their minimum cost

        for vertex in map.keys():
            min_cost[vertex] = float('inf')
        min_cost[start] = 0
    
        visited = set()

        current_loc = start

        previous = {}

        while len(visited) < len(min_cost): #Implementation of djikstra itself
            for vertex, distance in map[current_loc].items(): #explores neighbors of current node
                new_cost = distance + min_cost[current_loc]
                if new_cost < min_cost[vertex]:
                    min_cost[vertex] = new_cost
                    previous[vertex] = current_loc

            visited.add(current_loc)
            
            if len(visited) == len(min_cost):
                break

            current_loc = min((vertex for vertex in min_cost if vertex not in visited), key=min_cost.get)

            if min_cost[current_loc] == float('inf'):
                break

        temp = []
        if len(visited_dest) < len(destinations):
            nearest_dest = min((vertex for vertex in destinations if vertex not in visited_dest),
                              key=min_cost.get) #Nearest unvisited destination of the current destination
        
        #from all the neighbors of cnode, which of its neighbor's min_cost and the distance between them
        #would yield a sum equal to the min_cost of cnode

            if min_cost[nearest_dest] == float('inf'):
                break

            visited_dest.add(nearest_dest)

            current_node = nearest_dest
            temp.append(current_node)

            while current_node != start: #construct the path between 2 destinations
                temp.append(previous[current_node])
                current_node = previous[current_node]
            
            start = nearest_dest

        else:
            temp.append(start)

        temp.reverse()

        if shortest_path:
            shortest_path.extend(temp[1:])
        else:
            shortest_path.extend(temp)
    
    return shortest_path
        
def deliver_mails(starting_city, delivery_map, school_cities, post_offices):
    clear_terminal()

    current_city = starting_city #Current city is the postoffice of the city
    destinations = []
    diff_cities = []
    diff_cities.append(starting_city)

    print(f"We are going to {current_city} to get the mails to be delivered")
    print(motorcycle)

    mails_no = input("How many mails are there? ")
    while not mails_no.isdigit() or int(mails_no) < 0:
        mails_no = input("How many mails are there? ")

    mails_no = int(mails_no)

    for i in range(0, mails_no): #The user inputs the destination for mail deliveries
        destination = input(f"Destination of mail {i+1}: ")
        while destination not in delivery_map:
            destination = input(f"Destination of mail {i+1}: ")
        if destination not in destinations:
            destinations.append(destination)
        if not school_cities[destination] in diff_cities:
            diff_cities.append(school_cities[destination])

    diff_cities = shortest_path(diff_cities, post_offices, starting_city)
    
    cities_visited = 0 #increment everytime the rider finishes delivering all the mails in one city

    while cities_visited < len(diff_cities):
        if cities_visited >= 1:
            print("Let us go to the next Post Office.")
            input("Press 'Enter' to go to the next Post Office")
            clear_terminal()
            current_city = diff_cities[cities_visited]
            print(f"We are going to {current_city} to get the mails to be delivered")
            print(motorcycle)
            mails_no = input("How many mails are there? ")
            while not mails_no.isdigit() or int(mails_no) < 0:
                mails_no = input("How many mails are there? ") #additional mails if the user wants to add
            mails_no = int(mails_no)
            new_cities = []
            for i in range(0, mails_no): #The user inputs the destination for mail deliveries
                destination = input(f"Destination of mail {i+1}: ")
                while destination not in delivery_map:
                    destination = input(f"Destination of mail {i+1}: ")
                if destination not in destinations:
                    destinations.append(destination)
                if school_cities[destination] not in new_cities:
                    new_cities.append(school_cities[destination])
            new_cities = shortest_path(new_cities, post_offices, current_city)
            print(f"New Cities: {new_cities}")
            input("Press enter to continue")
            if len(new_cities) > 0:
                new_cities.pop(0) #pop the 1st city since the returned sorted array includes the current city
            diff_cities.extend(new_cities)
        
        segregated_mails = []
        for loc in destinations[:]:
            if school_cities[loc] == current_city:
                segregated_mails.append(loc)
                destinations.remove(loc)
        
        if len(segregated_mails) > 0:
            optimal_path = shortest_path(segregated_mails, delivery_map, current_city)
            print(f"Optimal Path: {optimal_path}")
            input("Press enter to continue...")
            optimal_path.pop(0) #pop the 1st loc since the returned sorted array includes the post office as the 1st loc

            segregated_mails = set(segregated_mails)
            sorted_mails = []

            for node in optimal_path:
                if node in segregated_mails:
                    sorted_mails.append(node)

            figure = display_animation(optimal_path, sorted_mails, current_city)

            if cities_visited == len(diff_cities) - 1:
                print(figure)
            
            else:
                post_office = current_city
                motorcycle_copy = motorcycle
                motorcycle_copy = motorcycle_copy.rstrip("\n")
                print(motorcycle_copy)
                print(" " * (motorcycle_width//2-8) + " " * (len(post_office) // 2) + "○")
                print(" " * (motorcycle_width//2-8) + post_office)
            
            print()
            print(f"All mails for {current_city[:-12]} are delivered!")
 
        cities_visited += 1

    print("We are done for today, but you may choose to deliver new mails for other Post Offices again")
    input("Press 'Enter' to go back to the Main Menu")
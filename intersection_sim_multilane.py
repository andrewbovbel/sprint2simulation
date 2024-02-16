import random

"""
2PX3 Intersection Simulation Starting Code 

Simulation for a "cautious" intersection. Modelling choices:
1) A vehicles arrives from N, E, S, or W and must wait for other cars
ahead of them to clear the intersection.
2) Only one car can be "clearing" the intersection at once.
3) Before a car can begin to clear the intersection, it must come to a stop
4) Cars will clear the intersection in a one-at-a-time counter-clockwise manner

Dr. Vincent Maccio 2022-02-01 
"""

#Constants
ARRIVAL = "Arrival"
DEPARTURE = "Departure"
STOP = "Stop"
N = "North"
E = "East"
S = "South"
W = "West"
MEAN_ARRIVAL_TIME = 10
PRINT_EVENTS = False
STOP_TIME = 5
STOP_TIME_SHIFT = 0
CLEAR_TIME = 7
CLEAR_TIME_SHIFT = 0
MAX_IN_INTERSECTION = 2

class Driver:

    stop_time_low = STOP_TIME - STOP_TIME_SHIFT 
    stop_time_high = STOP_TIME + STOP_TIME_SHIFT
    clear_time_low = CLEAR_TIME - CLEAR_TIME_SHIFT
    clear_time_high = CLEAR_TIME + CLEAR_TIME_SHIFT
    has_stopped = False

    def __init__(self, name, arrival_time):
        self.name = name
        self.arrival_time = arrival_time
    
    #Returns driver instance stop time
    def get_stop_time(self):
        r = random.random()
        if r < 0.5:
            return  self.stop_time_low
        return self.stop_time_high

    #Returns driver instance clear time
    def get_clear_time(self):
        r = random.random()
        if r < 0.5:
            self.clear_time_low
        return self.clear_time_high


class Event:

    def __init__(self, event_type, time, direction):
        self.type = event_type
        self.time = time
        self.direction = direction 


class EventQueue:

    def __init__(self):
        self.events = []

    #Add event (will get sent to the back of the queue)
    def add_event(self, event):
        #print("Adding event: " + event.type + ", clock: " + str(event.time))
        self.events.append(event)

    #Get the next event in the queue and pop it (remove it)
    #Returns removed next event
    def get_next_event(self):
        min_time = 9999999999999
        min_index = 0
        for i in range(len(self.events)):
            if self.events[i].time < min_time:
                min_time = self.events[i].time
                min_index = i
        event = self.events.pop(min_index)
        #print("Removing event: " + event.type + ", clock: " + str(event.time))
        return event


class Simulation:

    upper_arrival_time = 2 * MEAN_ARRIVAL_TIME

    def __init__(self, total_arrivals):
        self.num_of_arrivals = 0
        self.total_arrivals = total_arrivals
        self.clock = 0

        """
        Each road is represented as a list of waiting cars. 
        """
        self.north, self.east, self.south, self.west = [], [], [], []
        self.north_ready = False
        self.east_ready = False
        self.south_ready = False
        self.west_ready = False
        self.intersection_free = True
        self.events = EventQueue()
        self.generate_arrival()
        self.print_events = PRINT_EVENTS
        self.data = []
        self.num_in_intersection = 0

    #Enable printing events as the simulation runs
    def enable_print_events(self):
        self.print_events = True
    
    #Method that runs the simulation
    def run(self):
        while self.num_of_arrivals <= self.total_arrivals:
            if self.print_events:
                self.print_state()
            self.execute_next_event()
            
    #Execute the next event in the queue
    #(Get next event, and execute appropriate method depending on event type)
    def execute_next_event(self):
        event = self.events.get_next_event()
        self.clock = event.time
        if event.type == ARRIVAL:
            self.execute_arrival(event)
        if event.type == DEPARTURE:
            self.execute_departure(event)
        if event.type == STOP:
            self.execute_stop(event)

    #Driver leaving intersection event
    def execute_departure(self, event):
        if self.print_events:
            print(str(self.clock)+ ": A driver from the " + event.direction + " has cleared the intersection.")

        self.num_in_intersection -= 1
        #Lots of "traffic logic" below. It's just a counter-clockwise round-robin.
        if event.direction == N:
            
            #No drivers left to depart from the North
            if self.north == [] or not self.north[0].has_stopped:
                self.north_ready = False
        
            #Carry on to other direction waitlists
            if self.west_ready:
                self.depart_from(W)
            elif self.south_ready:
                self.depart_from(S)
            elif self.east_ready:
                self.depart_from(E)
            elif self.north_ready:
                self.depart_from(N)

        if event.direction == E:

            #No drivers left to depart from the East
            if self.east == [] or not self.east[0].has_stopped:
                self.east_ready = False
        
            #Carry on to other direction waitlists
            if self.north_ready:
                self.depart_from(N)
            elif self.west_ready:
                self.depart_from(W)
            elif self.south_ready:
                self.depart_from(S)
            elif self.east_ready:
                self.depart_from(E)
            

        if event.direction == S:

            #No drivers left to depart from the South
            if self.south == [] or not self.south[0].has_stopped:
                self.south_ready = False
        
            #Carry on to other direction waitlists
            if self.east_ready:
                self.depart_from(E)
            elif self.north_ready:
                self.depart_from(N)
            elif self.west_ready:
                self.depart_from(W)
            elif self.south_ready:
                self.depart_from(S)

        if event.direction == W:

            #No drivers left to depart from the West
            if self.west == [] or not self.west[0].has_stopped:
                self.west_ready = False
        
            #Carry on to other direction waitlists
            if self.south_ready:
                self.depart_from(S)
            elif self.east_ready:
                self.depart_from(E)
            elif self.north_ready:
                self.depart_from(N)
            elif self.west_ready:
                self.depart_from(W)
                
    
    #Create departure event for the first driver from the queue in the passed direction
    def depart_from(self, direction):
        
        #Make departure event for first car in North queue
        if direction == N:
            clear_time = self.clock + self.north[0].get_clear_time()
            new_event = Event(DEPARTURE, clear_time, N)
            driver = self.north.pop(0) #Car progessing into the intersection
            if self.north == [] or not self.north[0].has_stopped:
                self.north_ready = False

        #Make departure event for first car in East queue 
        if direction == E:
            clear_time = self.clock + self.east[0].get_clear_time()
            new_event = Event(DEPARTURE, clear_time, E)
            driver = self.east.pop(0) #Car progessing into the intersection
            if self.east == [] or not self.east[0].has_stopped:
                self.east_ready = False
            
        #Make departure event for first car in South queue
        if direction == S:
            clear_time = self.clock + self.south[0].get_clear_time()
            new_event = Event(DEPARTURE, clear_time, S)
            driver = self.south.pop(0) #Car progessing into the intersection
            if self.south == [] or not self.south[0].has_stopped:
                self.south_ready = False

        #Make departure event for first car in West queue 
        if direction == W:
            clear_time = self.clock + self.west[0].get_clear_time()
            new_event = Event(DEPARTURE, clear_time, W)
            driver = self.west.pop(0) #Car progessing into the intersection
            if self.west == [] or not self.west[0].has_stopped:
                self.west_ready = False
            
        self.events.add_event(new_event)
        self.num_in_intersection += 1
        self.data.append(clear_time - driver.arrival_time)

    #Stop driver at intersection, and call depart method to add depart event to queue
    def execute_stop(self, event):
        if self.print_events:
            print(str(self.clock)+ ": A driver from the " + event.direction + " has stopped.")
        
        if event.direction == N:
            self.north_ready = True
            self.record_stop(self.north)
            if self.num_in_intersection < MAX_IN_INTERSECTION:
                self.depart_from(N)

        if event.direction == E:
            self.east_ready = True
            self.record_stop(self.east)
            if self.num_in_intersection < MAX_IN_INTERSECTION:
                self.depart_from(E)

        if event.direction == S:
            self.south_ready = True
            self.record_stop(self.south)
            if self.num_in_intersection < MAX_IN_INTERSECTION:
                self.depart_from(S)

        if event.direction == W:
            self.west_ready = True
            self.record_stop(self.west)
            if self.num_in_intersection < MAX_IN_INTERSECTION:
                self.depart_from(W)

    def record_stop(self, cars):
        i = 0
        while cars[i].has_stopped:
            i += 1
        cars[i].has_stopped = True
      
    #Start arrival event 
    def execute_arrival(self, event):
        driver = Driver(self.num_of_arrivals, self.clock)
        if self.print_events:
            print(str(self.clock)+ ": A driver arrives from the " + event.direction + ".")

        if event.direction == N:
            if self.north == []: #Car needs to stop before clearing
                self.north_ready = False
            self.north.append(driver)
            new_event = Event(STOP, self.clock + driver.get_stop_time(), N)
            self.events.add_event(new_event)
            
        elif event.direction == E:
            if self.east == []: #Car needs to stop before clearing
                self.east_ready = False
            self.east.append(driver)
            new_event = Event(STOP, self.clock + driver.get_stop_time(), E)
            self.events.add_event(new_event)
            
        elif event.direction == S:
            if self.south == []: #Car needs to stop before clearing
                self.south_ready = False
            self.south.append(driver)
            new_event = Event(STOP, self.clock + driver.get_stop_time(), S)
            self.events.add_event(new_event)
            
        else:
            if self.west == []: #Car needs to stop before clearing
                self.west_ready = False
            self.west.append(driver)
            new_event = Event(STOP, self.clock + driver.get_stop_time(), W)
            self.events.add_event(new_event)
            
        self.generate_arrival() #Generate the next arrival

    #Generate a car arriving at the intersection
    def generate_arrival(self):
        #Generates a random number uniformily between 0 and upper_arrival_time
        inter_arrival_time = random.random() * self.upper_arrival_time
        time = self.clock + inter_arrival_time
        
        r = random.random()
        #Equally likely to arrive from each direction
        if r < 0.25:
            self.events.add_event(Event(ARRIVAL, time, N))
        elif r < 0.5:
            self.events.add_event(Event(ARRIVAL, time, E))
        elif r < 0.75:
            self.events.add_event(Event(ARRIVAL, time, S))
        else:
            self.events.add_event(Event(ARRIVAL, time, W))
        self.num_of_arrivals += 1 #Needed for the simulation to terminate

    def print_state(self):
        print("[N,E,S,W] = ["+ str(len(self.north)) + ","+ str(len(self.east)) +","+ str(len(self.south)) +","+ str(len(self.west)) +"]")
        print("Number in the intersection: " + str(self.num_in_intersection))

    def generate_report(self):
        #Define a method to generate statistical results based on the time values stored in self.data
        #These could included but are not limited to: mean, variance, quartiles, etc. 
        print()
        


def average(L):
    return sum(L)/len(L)

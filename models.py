from datetime import datetime, timedelta, time 
from enum import Enum 
from abc import ABC, abstractmethod 

# ==========================================
# 1. ENUMERATIONS
# ==========================================
class SeatStatus(Enum): 
    AVAILABLE = "AVAILABLE" 
    RESERVED = "RESERVED" 

class BookingStatus(Enum):
    PENDING = "PENDING" 
    PAID = "PAID" 
    REFUNDED = "REFUNDED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED" 

class TicketStatus(Enum): 
    CONFIRMED = "CONFIRMED" 
    EXPIRED = "EXPIRED" 
    USED = "USED" 

class RouteStatus(Enum): 
    OPEN = "OPEN"
    DECOMMISSIONED = "DECOMMISSIONED" 

class TripStatus(Enum):
    OPEN = "OPEN"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"

class TrainStatus(Enum): 
    COMMISSIONED = "COMMISSIONED" 
    DECOMMISSIONED = "DECOMMISSIONED" 

class CarriageClass(Enum): 
    Normal = "Normal" 
    Business = "Business" 

# ==========================================
# 2. RAILWAY SYSTEM CORE
# ==========================================
class RailwaySystem: 
    def __init__(self): 
        self.__users = [] 
        self.__customers = [] 
        self.__staffs = [] 
        self.__trains = [] 
        self.__stations = [] 
        self.__routes = [] 
        self.__schedules = []
        self.__trips = []
        self.__payments = []
        self.__foods = []
        self.__starting_fee = 30 
        self.__fee = 5 
        self.__service_fee = 10

#====== ADD======
    def add_customer(self, customer): 
        for n_customer in self.__customers: 
            if n_customer.get_user_id() == customer.get_user_id(): 
                raise KeyError(f"There is customer code {customer.get_user_id()} already") 
        self.__customers.append(customer) 
        self.__users.append(customer) 

    def add_staff(self, staff): 
        for n_staff in self.__staffs: 
            if n_staff.get_user_id() == staff.get_user_id(): 
                raise KeyError(f"There is staff code {staff.get_user_id()} already") 
        self.__staffs.append(staff) 
        self.__users.append(staff) 

    def add_route(self, route): 
        for n_route in self.__routes: 
            if n_route.get_route_id() == route.get_route_id(): 
                raise KeyError(f"There is route code {route.get_route_id()} already") 
        self.__routes.append(route) 

    def add_schedule(self, schedule):
        for n_schedule in self.__schedules: 
            if n_schedule.get_route().get_route_id() == schedule.get_route().get_route_id(): 
                raise KeyError(f"There is schedule for route code {n_schedule.get_route().get_route_id()} already") 
        self.__schedules.append(schedule) 

    def add_trip(self, trip):
        for n_trip in self.__trips:
            if n_trip.get_trip_id() == trip.get_trip_id():
                raise KeyError(f"There is trip code {trip.get_trip_id()} already") 
        self.__trips.append(trip)

    def add_station(self, station): 
        for n_station in self.__stations: 
            if n_station.get_station_id() == station.get_station_id(): 
                raise KeyError(f"There is station code {station.get_station_id()} already") 
        self.__stations.append(station) 

    def add_train(self, train): 
        for n_train in self.__trains:
             if n_train.get_train_id() == train.get_train_id(): 
                raise KeyError(f"There is train code {train.get_train_id()} already") 
        self.__trains.append(train)

    def add_payments(self, payment):
        for n_payment in self.__payments:
            if n_payment.get_id() == payment.get_id():
                raise KeyError(f"There is this payment code already") 
        self.__payments.append(payment)

    def add_food(self, food):
        self.__foods.append(food)

#======REMOVE=======
    def remove_route(self, route): 
        for n_route in self.__routes: 
            if n_route.get_route_id() == route.get_route_id(): 
                if n_route.get_status() == RouteStatus.DECOMMISSIONED: 
                    raise ValueError("Route already decommissioned")
                n_route.set_status(RouteStatus.DECOMMISSIONED) 
                return 
        raise KeyError("Route not found") 

    def remove_train(self, train): 
        for n_train in self.__trains: 
            if n_train.get_train_id() == train.get_train_id(): 
                if n_train.get_status() == TrainStatus.DECOMMISSIONED: 
                    raise ValueError("Train already decommissioned") 
                n_train.set_status(TrainStatus.DECOMMISSIONED)
                return
        raise KeyError("Train not found")
    
    def cancel_trip(self, trip):
        for n_trip in self.__trips:
            if n_trip.get_trip_id() == trip.get_trip_id():
                for reserve in list(n_trip.get_reserves()): 
                    cus_booking = reserve.get_reserved_customer().get_user_bookings()
                    for booking in cus_booking:
                        if booking.get_booking_trip().get_trip_id() == n_trip.get_trip_id():
                            booking.cancel()
                n_trip.set_status(TripStatus.CANCELLED)
                return
        raise KeyError("Trip not found")
    
    def sell_food(self, food):
        for n_food in self.__foods:
            if n_food.get_name() == food.get_name():
                self.__foods.remove(food)
                return
        raise KeyError("Food not found")

#======SHOW======
    def show_admin_route(self): 
        routes = [] 
        for route in self.__routes: 
            dep_time = []
            for schedule in self.__schedules:
                if schedule.get_route().get_route_id() == route.get_route_id():
                    n_time = schedule.get_times()
                    for depart_time in n_time:
                        dep_time.append(depart_time.strftime("%H:%M"))
            stations = [] 
            for stop in route.get_stop(): 
                stations.append(f"{stop.get_station_name()}") 
            routes.append(f"Route Code : {route.get_route_id()}") 
            routes.append(f"Route Name : {route.get_route_name()}") 
            routes.append(f"Distance : {route.get_route_distance()} km") 
            routes.append(f"Stations : {stations}") 
            routes.append(f"Departure Time : {dep_time}")  
            routes.append(f"Status : {route.get_status().value}") 
            routes.append("--------------------------------------------------------------") 
        return routes 

    def show_route(self): 
        routes = [] 
        for route in self.__routes: 
            if route.get_status() == RouteStatus.DECOMMISSIONED: 
                continue 
            dep_time = []
            for schedule in self.__schedules:
                if schedule.get_route().get_route_id() == route.get_route_id():
                    n_time = schedule.get_times()
                    for depart_time in n_time:
                        dep_time.append(depart_time.strftime("%H:%M"))
            stations = [] 
            for stop in route.get_stop(): 
                stations.append(f"{stop.get_station_name()}") 
            routes.append(f"Route Code : {route.get_route_id()}") 
            routes.append(f"Route Name : {route.get_route_name()}") 
            routes.append(f"Distance : {route.get_route_distance()} km") 
            routes.append(f"Stations : {stations}") 
            routes.append(f"Departure Time : {dep_time}") 
            routes.append("--------------------------------------------------------------") 
        return routes 

    def show_admin_train(self): 
        trains = [] 
        for train in self.__trains: 
            trains.append(f"Train Code: {train.get_train_id()}") 
            trains.append(f"Number of Carriage: Normal:{train.get_normal_carriage()} | Business:{train.get_business_carriage()}") 
            trains.append(f"Full capacity: {train.get_total_seats()}") 
            trains.append(f"Status: {train.get_status().value}") 
            trains.append("-------------------------------------------------------------") 
        return trains 
    
    def show_admin_trip(self):
        trips = []
        for trip in self.__trips:
            if trip.get_status() == TripStatus.OPEN:
                trips.append(f"Trip Code: {trip.get_trip_id()}")
                trips.append(f"Route Code: {trip.get_route().get_route_id()}")
                trips.append(f"Train Code: {trip.get_train().get_train_id()} | Capacity : {trip.get_train().get_total_seats()} | Reserved : {trip.get_train().get_used_seats(trip)} | Remaining : {trip.get_train().get_remaining_seats(trip)}")
                trips.append(f"Date: {trip.get_date()}")
                trips.append(f"Depart Time: {trip.get_time().strftime('%H:%M')}")
                trips.append("-------------------------------------------------------------") 
        return trips

#======SEARCH======
    def search_route_by_num(self, num): 
        for route in self.__routes: 
            if route.get_status() == RouteStatus.OPEN: 
                if route.get_route_id() == num: 
                    return route 
        raise KeyError("Route not found")
    
    def search_route_any_status(self, route_id): 
        for route in self.__routes: 
            if route.get_route_id() == route_id: 
                return route 
        raise KeyError("Route not found") 
    
    def search_schedule(self, depart_s, arrive_s, search_time = None):
        for schedule in self.__schedules:
            route = schedule.get_route()
            try:
                route.get_stop_index(depart_s)
                route.get_stop_index(arrive_s)
                if search_time:
                    if search_time not in schedule.get_times():
                        continue
                return schedule
            except KeyError:
                continue
        raise KeyError("Schedule not found")
    
    def search_schedule_by_route(self, route_id):
        for schedule in self.__schedules:
            if schedule.get_route().get_route_id() == route_id:
                return schedule
        raise KeyError("Schedule not found")
    
    def search_trip(self, trip_id):
        for trip in self.__trips:
            if trip.get_trip_id() == trip_id:
                return trip
        raise KeyError("Trip not found") 

    def search_train_by_num(self, num): 
        for train in self.__trains: 
            if train.get_status() == TrainStatus.COMMISSIONED: 
                if train.get_train_id() == num: 
                    return train 
        raise KeyError("Train not found") 

    def search_train_any_status(self, train_id): 
        for train in self.__trains: 
            if train.get_train_id() == train_id: 
                return train 
        raise KeyError("Train not found") 

    def search_station_by_name(self, name): 
        for station in self.__stations: 
            if station.get_station_name().lower() == name.lower(): 
                return station 
        raise KeyError("Station not found") 

    def search_customer_by_num(self, num): 
        for customer in self.__customers: 
            if customer.get_user_id().lower() == num.lower(): 
                return customer 
        raise KeyError("Customer not found") 

    def search_staff_by_num(self, num): 
        for staff in self.__staffs: 
            if staff.get_user_id().lower() == num.lower(): 
                return staff 
        raise KeyError("Staff not found") 
    
    def search_payment(self, num):
        for payment in self.__payments:
            if payment.get_id() == num:
                return payment
        raise KeyError("Payment not found")
    
    def search_food_by_name(self, num):
        for food in self.__foods:
            if food.get_name() == num:
                return food
        raise KeyError("Food not found")

#======CHANGE======
    def change_fee(self, starting, fee, service): 
        self.__starting_fee = starting 
        self.__fee = fee 
        self.__service_fee = service

#======GET======
    def get_routes(self): return self.__routes 
    def get_schedule(self): return self.__schedules
    def get_trips(self): return self.__trips
    def get_stations(self): return self.__stations 
    def get_starting_fee(self): return self.__starting_fee 
    def get_fee(self): return self.__fee 
    def get_service_fee(self): return self.__service_fee

# ==========================================
# 3. ROUTE & SCHEDULE MODULE
# ==========================================
class Route: 
    __route_id_counter = 1 
    def __init__(self): 
        self.__r_code = "R" + str(Route.__route_id_counter) 
        Route.__route_id_counter += 1 
        self.__name = None 
        self.__distance = 0 
        self.__stations = [] 
        self.__f_station = None 
        self.__l_station = None 
        self.__status = RouteStatus.OPEN 

    def add_station(self, station, distance): 
        for n_station in self.__stations: 
            if n_station.get_station_id() == station.get_station_id(): 
                raise KeyError(f"There is station code {station.get_station_id()} already") 
        stop = Stop(station, distance) 
        self.__stations.append(stop) 
        self.__f_station = self.__stations[0] 
        self.__l_station = self.__stations[len(self.__stations) - 1] 
        self.__distance = sum([s.get_station_distance() for s in self.__stations])
        self.__name = "-".join([self.__f_station.get_station_name(), self.__l_station.get_station_name()]) 

    def set_status(self, status): 
        self.__status = status 

    def search_station_by_name(self, name): 
        for stop in self.__stations: 
            if stop.get_station_name().lower() == name.lower(): 
                return stop 
        raise KeyError("Station not found") 
    
#======GET=======
    def get_stop_index(self, station): 
        for i, stop in enumerate(self.__stations): 
            if stop.get_station_id() == station.get_station_id(): 
                return i 
        raise KeyError("Station not found") 

    def get_stop_distance(self, start, end): 
        start_index = self.get_stop_index(start) 
        end_index = self.get_stop_index(end) 
        distance = 0 
        for i, stop in enumerate(self.__stations): 
            if start_index < i <= end_index: 
                distance += stop.get_station_distance() 
        return distance 

    def get_route_id(self): return self.__r_code 
    def get_route_name(self): return self.__name 
    def get_route_distance(self): return self.__distance
    def get_stop(self): return self.__stations 
    def get_status(self): return self.__status 

class Schedule:
    def __init__(self, route):
        self.__route = route
        self.__standard_times = []

    def add_standard_time(self, hour, minute):
        self.__standard_times.append(time(hour, minute))

    def search_time(self, hour, minute):
        search_time = time(hour, minute)
        for n_time in self.__standard_times:
            if n_time == search_time:
                return n_time
        raise ValueError("No schedule of this time found")
    
    def get_route(self): return self.__route
    def get_times(self): return self.__standard_times

class Trip:
    def __init__(self, route, train, date, depart_time):
        self.__id = f"{route.get_route_id()}-{date.strftime('%Y%m%d')}-{depart_time.strftime('%H%M')}"
        self.__route = route
        self.__train = train
        self.__date = date
        self.__depart_time = depart_time
        self.__status = TripStatus.OPEN
        self.__reservations = []

    def reserve(self, date, customer, start, end, carriage, seat): 
        if start >= end: raise ValueError("Invalid segment") 
        if not self.is_available(date, start, end, carriage, seat): 
            raise ValueError("Already reserved") 
        reservation = ReservedSeat(date, customer, start, end, self.__train, carriage, seat) 
        self.__reservations.append(reservation)

    def release(self, date, start, end, carriage, seat): 
        for r in self.__reservations: 
            if r.get_reserved_date() == date and r.get_reserved_start_station() == start and r.get_reserved_end_station() == end and r.get_carriage() == carriage and r.get_seat() == seat: 
                self.__reservations.remove(r)
                return

    def is_available(self, date, start , end, carriage, seat):
        for r in self.__reservations:
            if r.get_carriage() == carriage and r.get_seat() == seat:
                if r.is_overlap(date, start, end):
                    return False
        return True
    
    def count_used_seat(self):
        used = []
        for r in self.__reservations:
            pair = (r.get_carriage(), r.get_seat())

            if pair not in used:
                used.append(pair)
        return len(used)

    def get_remaining_seats(self):
        return self.__train.get_total_seats() - self.count_used_seat()
    
    def show_seat_in_all_carriage(self, start, end): 
        seats = [] 
        for carriage in self.__train.get_train_carriages(): 
            for seat in carriage.get_carriage_seats(): 
                # ให้ Trip เป็นคนเช็คว่าที่นั่งว่างไหม
                if self.is_available(self.__date.date(), start, end, carriage, seat): 
                    status = SeatStatus.AVAILABLE 
                else: 
                    status = SeatStatus.RESERVED 
                seat_view = SeatStatusView(carriage.get_carriage_id(), seat.get_seat_id(), carriage.get_carriage_class(), status) 
                seats.append(seat_view) 
        return seats
    
    def get_arrival_time(self, station, travel_date):
        end_stop = self.__route.search_station_by_name(station.get_station_name())
        end_index = self.__route.get_stop_index(end_stop)
        
        total_distance = 0
        stops = self.__route.get_stop()
        for i in range(1, end_index + 1):
            total_distance += stops[i].get_station_distance()

        speed = self.__train.get_speed()

        travel_minute = (total_distance / speed) * 60

        base_datetime = datetime.combine(travel_date, self.__depart_time) 
        return base_datetime + timedelta(minutes=travel_minute) 
    
    def set_status(self, status):
        self.__status = status

    def set_train(self, status):
        self.__train = status

    def get_trip_id(self): return self.__id
    def get_route(self): return self.__route
    def get_train(self): return self.__train
    def get_date(self): return self.__date
    def get_time(self): return self.__depart_time
    def get_reserves(self): return self.__reservations
    def get_status(self): return self.__status

class Station: 
    __station_id_counter = 1 
    def __init__(self, name): 
        self.__st_code = "St" + str(Station.__station_id_counter) 
        Station.__station_id_counter += 1 
        self.__st_name = name 
         
    def get_station_id(self): return self.__st_code 
    def get_station_name(self): return self.__st_name

class Stop: 
    def __init__(self, station, distance): 
        self.__station = station 
        self.__current_trip = []
        self.__distance = distance 

    def get_station_id(self): return self.__station.get_station_id() 
    def get_station_name(self): return self.__station.get_station_name() 
    def get_station_distance(self): return self.__distance 
    def get_current_trip(self): return self.__current_trip
    def trip_enter(self, trip): self.__current_trip.append(trip) 
    def trip_exit(self, trip): self.__current_trip.remove(trip)

class ReservedSeat: 
    def __init__(self, date, customer, start, end, train, carriage, seat):
        self.__reserved_date = date 
        self.__customer = customer
        self.__start_station_index = start 
        self.__end_station_index = end 
        self.__train = train
        self.__carriage = carriage
        self.__seat = seat

    def is_overlap(self, date , start, end): 
        if self.__reserved_date != date: return False 
        return not(end <= self.__start_station_index or start >= self.__end_station_index) 
    
    def get_reserved_date(self): return self.__reserved_date 
    def get_reserved_customer(self): return self.__customer
    def get_reserved_start_station(self): return self.__start_station_index 
    def get_reserved_end_station(self): return self.__end_station_index 
    def get_train(self): return self.__train
    def get_carriage(self): return self.__carriage
    def get_seat(self) : return self.__seat

# ==========================================
# 4. TRAIN & CARRIAGE MODELS
# ==========================================
class Train(ABC): 
    __train_id_counter = 1 
    def __init__(self, Normal_num, Business_num): 
        self.__t_code = "Tr" + str(Train.__train_id_counter) 
        Train.__train_id_counter += 1 
        self.__carriages = [] 
        for i in range(Normal_num): 
            self.add_carriage(NormalCarriage()) 
        for j in range(Business_num): 
            self.add_carriage(BusinessCarriage()) 
        self.__status = TrainStatus.COMMISSIONED 

    def add_carriage(self, carriage): 
        self.__carriages.append(carriage) 

    def get_total_seats(self):
        return self.count_all_seat_in_carriage()
    
    def get_used_seats(self, trip):
        return trip.count_used_seat()
    
    def get_remaining_seats(self, trip):
        return self.get_total_seats() - self.get_used_seats(trip)

    def count_all_seat_in_carriage(self): 
        count = 0 
        for carriage in self.__carriages: 
            count += carriage.count_all_seats() 
        return count 

    def get_normal_carriage(self): 
        count = 0 
        for carriage in self.__carriages: 
            if isinstance(carriage, NormalCarriage): 
                count += 1 
        return count 

    def get_business_carriage(self): 
        count = 0 
        for carriage in self.__carriages: 
            if isinstance(carriage, BusinessCarriage): 
                count += 1 
        return count 

    def search_carriage_by_num(self, num): 
        for Car in self.__carriages: 
            if Car.get_carriage_id() == num: 
                return Car 
        raise KeyError("Carriage not found") 

    def set_status(self, status): self.__status = status 
    def get_train_id(self): return self.__t_code 
    def get_train_carriages(self): return self.__carriages 
    def get_status(self): return self.__status 
    @abstractmethod
    def get_class(self): pass
    @abstractmethod
    def get_speed(self): pass

class CommuterTrain(Train):
    def __init__(self, normal_num, business_num):
        super().__init__(normal_num, business_num)
        self.__class = "Commuter"
        self.__speed = 100
    def get_class(self): return self.__class
    def get_speed(self): return self.__speed

class SpeederTrain(Train):
    def __init__(self, normal_num, business_num):
        super().__init__(normal_num, business_num)
        self.__class = "Speeder"
        self.__speed = 250
    def get_class(self): return self.__class
    def get_speed(self): return self.__speed

class SplinterTrain(Train):
    def __init__(self, normal_num, business_num):
        super().__init__(normal_num, business_num)
        self.__class = "Splinter"
        self.__speed = 500
    def get_class(self): return self.__class
    def get_speed(self): return self.__speed 

class Carriage(ABC): 
    __carriage_id_counter = 1 
    def __init__(self): 
        self.__no = "Ca" + str(Carriage.__carriage_id_counter) 
        Carriage.__carriage_id_counter += 1 
        self.__seats = [] 
        for i in range(1, 11): 
            for j in range(ord('A'), ord('E') + 1): 
                seat_no = f"{i}{chr(j)}" 
                seat = Seat(seat_no) 
                self.__seats.append(seat) 

    def count_all_seats(self): 
        return len(self.__seats) 
    
    def get_used_seats(self, trip):
        count = 0
        for r in trip.get_reserves():
            if r.get_carriage() == self:
                count += 1
        return count
    
    def get_remaining_seats(self, trip):
        return self.count_all_seats() - self.get_used_seats(trip)

    def search_seat_by_num(self, num): 
        for seat in self.__seats: 
            if seat.get_seat_id().lower() == num.lower(): 
                return seat 
        raise KeyError("Seat not found") 

    def get_carriage_id(self): return self.__no 
    @abstractmethod 
    def get_carriage_class(self): pass 
    def get_carriage_seats(self): return self.__seats 
    @abstractmethod 
    def get_carriage_fee(self): pass 

class NormalCarriage(Carriage): 
    def __init__(self): 
        super().__init__() 
        self.__carriage_fee = 1 
    def get_carriage_class(self): return CarriageClass.Normal 
    def get_carriage_fee(self): return self.__carriage_fee 

class BusinessCarriage(Carriage): 
    def __init__(self): 
        super().__init__() 
        self.__carriage_fee = 1.5 
    def get_carriage_class(self): return CarriageClass.Business 
    def get_carriage_fee(self): return self.__carriage_fee 

class Seat: 
    def __init__(self, no): 
        self.__no = no 

    def get_seat_id(self): return self.__no 

class SeatStatusView: 
    def __init__(self, carriage_id, seat_id, s_class, status): 
        self.__carriage_id = carriage_id 
        self.__seat_id = seat_id 
        self.__class = s_class 
        self.__status = status 

    def get_data(self): 
        data = [] 
        data.append(f"Carriage: {self.__carriage_id}") 
        data.append(f"Seat: {self.__seat_id}") 
        data.append(f"Class: {self.__class.value}") 
        data.append(f"Status: {self.__status.value}") 
        data.append("----------------------------------") 
        return data
    
# ==========================================
# 5. CUSTOMER & STAFF MODULE
# ==========================================
class User(ABC): 
    def __init__(self, name, email, phone): 
        self.__name = name 
        self.__email = email 
        if len(phone) != 10:
            raise ValueError("Invalid Phone")
        self.__phone = phone 

    def set_user_name(self, name): self.__name = name 
    def set_user_email(self, email): self.__email = email 
    def set_user_phone(self, phone): 
        if len(phone) != 10:
            raise ValueError("Invalid Phone")
        self.__phone = phone
    @abstractmethod 
    def get_user_id(self): pass 
    def get_user_name(self): return self.__name 
    def get_user_email(self): return self.__email 
    def get_user_phone(self): return self.__phone 

class Customer(User): 
    __customer_id_counter = 1 
    def __init__(self, name, email, phone): 
        super().__init__(name, email, phone) 
        self.__id = "C" + str(Customer.__customer_id_counter) 
        Customer.__customer_id_counter += 1 
        self.__reward_point = 0 
        self.__bookings = [] 
        self.__tickets = [] 

    def add_booking(self, booking): 
        self.__bookings.append(booking) 

    def add_ticket(self, ticket): 
        self.__tickets.append(ticket) 

    def cancel_booking(self, booking): 
        trans = Transaction() 
        try: 
            result = booking.cancel() 
            trans.commit() 
        except Exception as e: 
            trans.rollback() 
            raise e 
        return result
    
    def refund_booking(self, booking):
        trans = Transaction() 
        try: 
            result = booking.refund() 
            trans.commit() 
        except Exception as e: 
            trans.rollback() 
            raise e 
        return result
    
    def buy_food(self, system, food):
        count = 0
        for ticket in self.__tickets:
           if ticket.get_ticket_status() == TicketStatus.CONFIRMED:
               count += 1
        if count > 0:
            system.sell_food(food)
        else:
            raise ValueError("No ticket available")
           
    
    def remove_ticket(self, ticket):
        self.__tickets.remove(ticket)

    def collect_points(self, distance): self.__reward_point += distance 

    def deduct_points(self, distance): self.__reward_point -= distance   

    def search_booking_by_num(self, num): 
        for booking in self.__bookings: 
            if booking.get_booking_id() == num: return booking 
        raise KeyError("Booking not found") 

    def search_ticket_by_num(self, num): 
        for ticket in self.__tickets: 
            if ticket.get_ticket_id() == num: return ticket 
        raise KeyError("Ticket not found") 

    def get_user_id(self): return self.__id 
    def get_reward_point(self): return self.__reward_point 
    def pay_booking(self, booking, payment, payment_code): return booking.pay(payment, payment_code)
    def get_discount(self): return 1 
    def get_user_bookings(self): return self.__bookings 
    def get_user_tickets(self): return self.__tickets 

class Member(Customer): 
    def get_discount(self): return 0.9 

class Senior(Customer): 
    def get_discount(self): return 0.85 

class Staff(User): 
    __staff_id_counter = 1 
    def __init__(self, name, email, phone): 
        super().__init__(name, email, phone) 
        self.__id = "S" + str(Staff.__staff_id_counter) 
        Staff.__staff_id_counter += 1 
        self.__usage_histories = [] 

    def add_history(self, person1, person2, action, time): 
        if person2 is None: 
            info = f"{person1} is {action}" 
        else: 
            info = f"{person1} is {action} {person2}" 
        history = UsageHistory(action, time, info) 
        self.__usage_histories.append(history) 

    def remove_last_history(self): self.__usage_histories.pop() 
    def get_user_id(self): return self.__id 
    def get_usage_histories(self): 
        histories = [] 
        for history in self.__usage_histories: 
            histories.append(history.get_history()) 
        return histories 

class StationOfficer(Staff): 
    def __init__(self, name, email, phone, station): 
        super().__init__(name, email, phone) 
        self.__assign_station = station 

    def verify_ticket(self, ticket, customer): 
        trans = Transaction() 
        try: 
            old_status = ticket.get_ticket_status() 

            trans.add_rollback(lambda: ticket.set_ticket_status(old_status) if ticket.get_ticket_status() != TicketStatus.EXPIRED else None)
            ticket.validate_ticket(self.__assign_station, customer) 
            ticket.use_ticket() 

            self.add_history(self.get_user_id(), customer.get_user_id(), 'Verify Ticket', datetime.now()) 
            trans.add_rollback(lambda: self.remove_last_history()) 
            trans.commit() 
        except Exception as e: 
            trans.rollback() 
            raise e 
        return "Access Granted" 

    def get_assign_station(self): return self.__assign_station 

class SystemAdministrator(Staff): 
    def add_route(self, system, route): 
        system.add_route(route) 
        self.add_history(self.get_user_id(), route.get_route_id(), 'Add Route', datetime.now()) 
        return f"Route: {route.get_route_id()}, Name: {route.get_route_name()} added successfully" 

    def remove_route(self, system, route): 
        system.remove_route(route) 
        self.add_history(self.get_user_id(), route.get_route_id(), 'Remove Route', datetime.now()) 
        return "route removed successfully" 
    
    def add_schedule(self, system, route_id):
        schedule = Schedule(system.search_route_by_num(route_id))
        system.add_schedule(schedule)
        route = system.search_schedule_by_route(route_id).get_route()
        self.add_history(self.get_user_id(), route.get_route_id(), 'Add Route Schedule', datetime.now()) 
        return f"Route: {route.get_route_id()}, Name: {route.get_route_name()} added  Schedule successfully"
    
    def add_schedule_time(self, system, route_id, hour, minute):
        schedule = system.search_schedule_by_route(route_id)
        route = schedule.get_route()
        schedule.add_standard_time(hour, minute)
        self.add_history(self.get_user_id(), route.get_route_id(), 'Add Route Schedule Time', datetime.now()) 
        return f"Route: {route.get_route_id()}, Name: {route.get_route_name()} added  Schedule {hour}:{minute} successfully"

    def add_train(self, system, train): 
        system.add_train(train) 
        self.add_history(self.get_user_id(), train.get_train_id(), 'Add Train', datetime.now()) 
        return f"Train: {train.get_train_id()} added successfully" 

    def remove_train(self, system, train): 
        system.remove_train(train) 
        self.add_history(self.get_user_id(), train.get_train_id(), 'Remove Train', datetime.now()) 
        return "train removed successfully" 
    
    def add_trip(self, system, trip):
        system.add_trip(trip)
        self.add_history(self.get_user_id(), trip.get_trip_id(), 'Add Trip', datetime.now())
        return f"Trip: {trip.get_trip_id()} added successfully"
    
    def cancel_trip(self, system, trip):
        system.cancel_trip(trip)
        self.add_history(self.get_user_id(), trip.get_trip_id(), 'Cancel Trip', datetime.now())
        return f"Trip: {trip.get_trip_id()} cancelled successfully"

class UsageHistory: 
    def __init__(self, type, time, info): 
        self.__type = type 
        self.__time = time 
        self.__info = info 
    def get_history(self): return f"{self.__type}: {self.__time} : {self.__info}" 

# ==========================================
# 6. PAYMENT MODULE
# ==========================================
class Payment(ABC):
    def __init__(self, amount, id):
        self.__account_id = id
        self.__amount = amount
    @abstractmethod
    def process(self, amount):
        pass
    def validate(self, receive_id):
        if self.__account_id == receive_id:
            return True
        return False
    def get_id(self):
        return self.__account_id
    def get_amount(self):
        return self.__amount

class EWalletPayment(Payment):
    def process(self, amount):
        new_amount = (self.get_amount() - amount) * 0.9
        self._Payment__amount = new_amount
        return f"EWallet:{self.get_id()}:{new_amount}"

class CardPayment(Payment):
    def process(self, amount):
        new_amount = self.get_amount() - amount
        self._Payment__amount = new_amount
        return f"CARD:{self.get_id()}:{new_amount}"

class BankTransferPayment(Payment):
    def process(self, amount):
        new_amount = (self.get_amount() - amount) * 0.95
        self._Payment__amount = new_amount
        return f"Bank:{self.get_id()}:{new_amount}"
class DirectDebitPayment(Payment):
    def process(self, amount):
        new_amount = (self.get_amount() - amount) * 0.85
        self._Payment__amount = new_amount
        return f"Debit:{self.get_id()}:{new_amount}"

# ==========================================
# 7. BOOKING & TRIP MODULE
# ==========================================
class Booking: 
    __booking_id_counter = 1 
    def __init__(self, customer, trip, date, departure_s, arrival_s, train, carriage, seat, system): 
        self.__create_date = datetime.now() 
        self.__cancel_date = None 
        self.__confirm_date = None 
        self.__id = "B" + str(Booking.__booking_id_counter) 
        Booking.__booking_id_counter += 1 
        self.__customer = customer 
        self.__trip = trip
        self.__route = trip.get_route() 
        self.__date = date 
        self.__departure_s = departure_s 
        self.__arrival_s = arrival_s 
        self.__train = train 
        self.__carriage = carriage 
        self.__seat = seat 
        self.__distance = self.__route.get_stop_distance(departure_s, arrival_s) 
        self.__booking_price = (((self.__distance * system.get_fee() + system.get_starting_fee()) * carriage.get_carriage_fee())* customer.get_discount()) + system.get_service_fee() 
        self.__booking_status = BookingStatus.PENDING 
        dep = self.__route.get_stop_index(departure_s) 
        arr = self.__route.get_stop_index(arrival_s) 
        if dep >= arr: raise ValueError("Invalid direction") 
        self.__segment = (dep, arr) 
        self.__trip.reserve(self.__date.date(), self.__customer, dep, arr, self.__carriage, self.__seat) 
        self.__payment = None

    def pay_with_points(self):
        if self.__booking_status != BookingStatus.PENDING: 
            raise ValueError("Cannot pay") 
        departure_time = self.__trip.get_arrival_time(self.__departure_s, self.__date.date()) 
        if departure_time < datetime.now(): 
            self.__booking_status = BookingStatus.EXPIRED 
            raise ValueError("Booking expired") 
        self.__booking_status = BookingStatus.PAID 
        if self.__customer.get_reward_point() < self.__distance:
            raise ValueError("Not enough points")
        self.__customer.deduct_points(self.__distance)
        self.__booking_price = 0

        ticket = Ticket(self.__customer, self.__trip, self.__departure_s, self.__arrival_s, self.__train, self.__carriage, self.__seat, self.__booking_price, "Point") 
        self.__customer.add_ticket(ticket)  
        self.__confirm_date = datetime.now() 
        return ticket.get_ticket_id() 

    def pay(self, payment: Payment, code): 
        if self.__booking_status != BookingStatus.PENDING: 
            raise ValueError("Cannot pay") 
        departure_time = self.__trip.get_arrival_time(self.__departure_s, self.__date.date()) 
        if departure_time < datetime.now(): 
            self.__booking_status = BookingStatus.EXPIRED 
            raise ValueError("Booking expired") 
        self.__booking_status = BookingStatus.PAID 
        price = self.__booking_price 
        if not payment.validate(code):
            raise ValueError(f"Invalid payment validation code")
        if payment.get_amount() < price:
            raise ValueError(f"Insufficient payment amount. Required: {price}")
        payment.process(price)
        self.__payment = payment
        ticket = Ticket(self.__customer, self.__trip, self.__departure_s, self.__arrival_s, self.__train, self.__carriage, self.__seat, price, payment) 
        self.__customer.add_ticket(ticket) 
        self.__customer.collect_points(self.__distance) 
        self.__confirm_date = datetime.now() 
        return ticket.get_ticket_id() 

    def cancel(self): 
        dep, arr = self.__segment 
        if self.__booking_status not in [BookingStatus.PENDING, BookingStatus.PAID]: 
            raise ValueError("Cannot cancel booking") 
        departure_time = self.__trip.get_arrival_time(self.__departure_s, self.__date.date()) 
        if departure_time < datetime.now(): 
            self.__booking_status = BookingStatus.EXPIRED 
            result = "expired" 
        else: 
            self.__booking_status = BookingStatus.CANCELLED 
            result = f"Booking Id: {self.__id} cancelled" 
        self.__cancel_date = datetime.now() 
        self.__trip.release(self.__date.date(), dep, arr, self.__carriage, self.__seat) 
        return result
    
    def refund(self):
        dep, arr = self.__segment 
        if self.__booking_status not in [BookingStatus.PAID]: 
            raise ValueError("Cannot refund booking") 
        departure_time = self.__trip.get_arrival_time(self.__departure_s, self.__date.date()) 
        if departure_time < datetime.now(): 
            self.__booking_status = BookingStatus.EXPIRED 
            result = "expired" 
        else: 
            if self.__booking_price == 0: 
                self.__customer.collect_points(100) 
            else: 
                self.__customer.deduct_points(self.__distance)
                self.__payment.process(-self.__booking_price) 
                for ticket in list(self.__customer.get_user_tickets()):
                    if ticket.get_ticket_customer().get_user_id() == self.__customer.get_user_id():
                        if ticket.get_ticket_departure().get_station_name() == self.__departure_s.get_station_name():
                            if ticket.get_ticket_arrival().get_station_name() == self.__arrival_s.get_station_name():
                                self.__customer.remove_ticket(ticket)
            self.__booking_status = BookingStatus.REFUNDED 
            result = f"Booking Id: {self.__id} refunded"  
        self.__cancel_date = datetime.now() 
        self.__trip.release(self.__date.date(), dep, arr, self.__carriage, self.__seat) 
        return result
    
    def change_trip(self, date_s, system):
        dep, arr = self.__segment
        new_date = datetime.strptime(date_s, "%Y-%m-%d")
        depart_time = self.__trip.get_time()
        before_trip = self.__trip
        self.__trip.release(self.__date.date(), dep, arr, self.__carriage, self.__seat)
        code = f"{self.__route.get_route_id()}-{new_date.strftime('%Y%m%d')}-{depart_time.strftime('%H%M')}"
        self.__date = new_date
        trip = system.search_trip(code)
        self.__trip = trip
        self.__trip.reserve(self.__date.date(), self.__customer, dep, arr, self.__carriage, self.__seat)
    
        result = f"Booking Id: {self.__id} | before : {before_trip.get_trip_id()} | after : {self.__trip.get_trip_id()}"
        return result


    def get_booking_create_date(self): return self.__create_date 
    def get_booking_cancel_date(self): return self.__cancel_date 
    def get_booking_confirm_date(self): return self.__confirm_date 
    def get_booking_id(self): return self.__id 
    def get_booking_trip(self): return self.__trip 
    def get_booking_route(self): return self.__route 
    def get_booking_date(self): return self.__date 
    def get_booking_departure(self): return self.__departure_s 
    def get_booking_arrival(self): return self.__arrival_s 
    def get_booking_train(self): return self.__train 
    def get_booking_carriage(self): return self.__carriage 
    def get_booking_seat(self): return self.__seat 
    def get_booking_price(self): return self.__booking_price 
    def get_booking_status(self): return self.__booking_status 
    def get_segment(self): return self.__segment 
    def get_payment(self): return self.__payment

class Ticket: 
    __ticket_id_counter = 1 
    def __init__(self, customer, trip, departure_s, arrival_s, train, carriage, seat, ticket_price, payment): 
        self.__create_date = datetime.now() 
        self.__validation_date = None 
        self.__id = "T" + str(Ticket.__ticket_id_counter) 
        Ticket.__ticket_id_counter += 1 
        self.__customer = customer 
        self.__trip = trip 
        self.__departure_s = departure_s 
        self.__date = trip.get_date() 
        self.__departure_time = trip.get_time() 
        self.__arrival_s = arrival_s 
        self.__arrival_time = self.__trip.get_arrival_time(self.__arrival_s, self.__date.date()) 
        self.__train = train 
        self.__carriage = carriage 
        self.__seat = seat 
        self.__ticket_price = ticket_price 
        self.__ticket_status = TicketStatus.CONFIRMED 
        self.__payment = payment

    def validate_ticket(self, station, customer): 
        self.check_station(station) 
        self.check_customer(customer) 
        self.check_date() 
        if self.__ticket_status == TicketStatus.USED: 
            raise ValueError("Ticket already used") 
        return True 

    def check_customer(self, customer): 
        if self.__customer.get_user_name() == customer.get_user_name(): 
            return True 
        raise ValueError("Wrong Customer") 

    def check_station(self, station): 
        if station.get_station_id() != self.__departure_s.get_station_id(): 
            raise ValueError("Wrong Station") 
        return True 

    def check_date(self): 
        now = datetime.now() 
        ticket_time = self.__trip.get_arrival_time(self.__departure_s, self.__date.date()) 
        if now < ticket_time - timedelta(days=1): 
            raise ValueError("Too early") 
        if now > ticket_time + timedelta(minutes=20): 
            self.__ticket_status = TicketStatus.EXPIRED 
            raise ValueError("Expired") 
        return True 

    def use_ticket(self): 
        if self.__ticket_status == TicketStatus.USED: 
            raise ValueError("Ticket already used") 
        self.__validation_date = datetime.now() 
        self.__ticket_status = TicketStatus.USED 
        return "updated" 

    def set_ticket_status(self, status): self.__ticket_status = status 
    def get_ticket_create_date(self): return self.__create_date 
    def get_ticket_validation_date(self): return self.__validation_date 
    def get_ticket_id(self): return self.__id 
    def get_ticket_customer(self): return self.__customer
    def get_ticket_trip(self): return self.__trip 
    def get_ticket_route(self): return self.__trip.get_route() 
    def get_ticket_date(self): return self.__date 
    def get_ticket_departure(self): return self.__departure_s 
    def get_ticket_depart_time(self): return self.__departure_time 
    def get_ticket_arrival(self): return self.__arrival_s 
    def get_ticket_arrive_time(self): return self.__arrival_time 
    def get_ticket_train(self): return self.__train 
    def get_ticket_carriage(self): return self.__carriage 
    def get_ticket_seat(self): return self.__seat 
    def get_ticket_price(self): return self.__ticket_price 
    def get_ticket_status(self): return self.__ticket_status 
    def get_payment(self): return self.__payment

class Transaction: 
    def __init__(self): 
        self.__rollback_actions = [] 
    def add_rollback(self, action): 
        self.__rollback_actions.append(action) 
    def commit(self): 
        self.__rollback_actions.clear() 
    def rollback(self): 
        for action in reversed(self.__rollback_actions): 
            action()

class Food:
    def __init__(self, name, price):
        self.__name = name
        self.__price = price

    def get_name(self):
        return self.__name
    def get_price(self):
        return self.__price

# ==========================================
# 8. INITIALIZATION
# ==========================================
def create_instance(): 
    arl = RailwaySystem() 
    
    Train1 = CommuterTrain(1, 1) 
    Train2 = SpeederTrain(2, 1) 
    Train3 = SplinterTrain(3, 2) 
    
    Route1 = Route() 
    Route2 = Route() 
    Route3 = Route() 
    
    Phrajomklao = Station("Phrajomklao") 
    Ladkrabang = Station("Ladkrabang") 
    Soiwatlanboon = Station("Soiwatlanboon") 
    Baanthubchang = Station("Baanthupchang") 
    Huamak = Station("Huamak") 
    Sukhumvit = Station("Sukhumvit") 
    Klongtan = Station("Klongtan") 
    Asoke = Station("Asoke") 
    Phrayathai = Station("Phrayathai") 
    Hualamphong = Station("Hualamphong") 
    Bangsue = Station("Bangsue") 
    Donmueng = Station("Donmueng") 
    Rangsit = Station("Rangsit") 
    Ayutthaya = Station("Ayutthaya") 
    
    Sch1 = Schedule(Route1) 
    Sch2 = Schedule(Route2) 
    Sch3 = Schedule(Route3) 

    burger = Food("Burger", 50)
    chicken = Food("Fried Chicken", 100)

    arl.add_food(burger)
    arl.add_food(chicken)
    
    Sch1.add_standard_time(8, 30) 
    Sch1.add_standard_time(9, 30) 
    Sch2.add_standard_time(9, 00) 
    Sch2.add_standard_time(10, 00) 
    Sch3.add_standard_time(8, 45) 
    Sch3.add_standard_time(9, 45) 
    
    Route1.add_station(Phrajomklao, 1) 
    Route1.add_station(Ladkrabang, 3) 
    Route1.add_station(Soiwatlanboon, 3) 
    Route1.add_station(Baanthubchang, 3) 
    Route1.add_station(Huamak, 5) 
    Route1.add_station(Sukhumvit, 4) 
    Route1.add_station(Klongtan, 1) 
    Route1.add_station(Asoke, 3) 
    Route1.add_station(Phrayathai, 3) 
    Route1.add_station(Hualamphong, 4) 
    
    Route2.add_station(Hualamphong, 1) 
    Route2.add_station(Bangsue, 8) 
    Route2.add_station(Donmueng, 22) 
    Route2.add_station(Rangsit, 30) 
    Route2.add_station(Ayutthaya, 71) 
    
    Route3.add_station(Hualamphong, 4) 
    Route3.add_station(Phrayathai, 3) 
    Route3.add_station(Asoke, 3) 
    Route3.add_station(Klongtan, 1) 
    Route3.add_station(Sukhumvit, 4) 
    Route3.add_station(Huamak, 5) 
    Route3.add_station(Baanthubchang, 3) 
    Route3.add_station(Soiwatlanboon, 3) 
    Route3.add_station(Ladkrabang, 3) 
    Route3.add_station(Phrajomklao, 1) 
    
    arl.add_station(Phrajomklao) 
    arl.add_station(Ladkrabang) 
    arl.add_station(Soiwatlanboon) 
    arl.add_station(Baanthubchang) 
    arl.add_station(Huamak) 
    arl.add_station(Sukhumvit) 
    arl.add_station(Klongtan) 
    arl.add_station(Asoke) 
    arl.add_station(Phrayathai) 
    arl.add_station(Hualamphong) 
    arl.add_station(Bangsue) 
    arl.add_station(Donmueng) 
    arl.add_station(Rangsit) 
    arl.add_station(Ayutthaya) 
    
    arl.add_train(Train1) 
    arl.add_train(Train2) 
    arl.add_train(Train3) 
    
    arl.add_route(Route1) 
    arl.add_route(Route2) 
    arl.add_route(Route3) 
    
    arl.add_schedule(Sch1) 
    arl.add_schedule(Sch2) 
    arl.add_schedule(Sch3) 

    arl.add_payments(CardPayment(2000, "123456"))
    arl.add_payments(EWalletPayment(5000, "234567"))

    
    John = StationOfficer("John", "Black@gmail.com", "0812345678", Phrajomklao) 
    Jake = StationOfficer("Jake", "Blacker@gmail.com", "0812345678", Hualamphong) 
    Jeff = SystemAdministrator("Jeff", "Blackest@gmail.com", "0812345678") 
    
    Jack = Customer("Jack", "White@gmail.com", "0812345678") 
    Jill = Member("Jill", "Whiter@gmail.com", "0812345678") 
    Josh = Senior("Josh", "Whitest@gmail.com", "0812345678") 
    
    arl.add_staff(John) 
    arl.add_staff(Jake) 
    arl.add_staff(Jeff) 
    
    arl.add_customer(Jack) 
    arl.add_customer(Jill) 
    arl.add_customer(Josh) 

    carriage = Train1.search_carriage_by_num("Ca1") 
    jack_chair = carriage.search_seat_by_num("1A") 
    jill_chair = carriage.search_seat_by_num("1B") 
    josh_chair = carriage.search_seat_by_num("1C") 
    
    st_start = arl.search_station_by_name("Phrajomklao") 
    st_end = arl.search_station_by_name("Hualamphong") 
    
    booking_date = datetime.today() + timedelta(days=1) 
    
    for day_offset in range(30): 
        current_date = booking_date + timedelta(days=day_offset) 
        t1 = Trip(Route1, Train1, current_date, Sch1.search_time(8, 30)) 
        t2 = Trip(Route1, Train1, current_date, Sch1.search_time(9, 30)) 
        t3 = Trip(Route2, Train2, current_date, Sch2.search_time(9, 00)) 
        t4 = Trip(Route2, Train2, current_date, Sch2.search_time(10, 00)) 
        t5 = Trip(Route3, Train3, current_date, Sch3.search_time(8, 45)) 
        t6 = Trip(Route3, Train3, current_date, Sch3.search_time(9, 45)) 
        arl.add_trip(t1)
        arl.add_trip(t2)
        arl.add_trip(t3)
        arl.add_trip(t4)
        arl.add_trip(t5)
        arl.add_trip(t6)

        if day_offset == 0:
            b1 = Booking(Jack, t1, current_date, st_start, st_end, Train1, carriage, jack_chair, arl) 
            Jack.add_booking(b1) 
            b2 = Booking(Jill, t1, current_date, st_start, st_end, Train1, carriage, jill_chair, arl) 
            Jill.add_booking(b2) 
            b3 = Booking(Josh, t1, current_date, st_start, st_end, Train1, carriage, josh_chair, arl) 
            Josh.add_booking(b3) 

            t1.get_arrival_time(st_end, current_date.date())
    
    
    for station in t1.get_route().get_stop():
            station.trip_enter(t1)

    return arl
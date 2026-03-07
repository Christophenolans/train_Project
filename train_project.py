from fastapi import FastAPI 
from fastapi import HTTPException 
from datetime import datetime, timedelta, time 
from enum import Enum 
from abc import ABC, abstractmethod 
import uvicorn 

app = FastAPI() 

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
    def __init__(self, name): 
        self.__name = name 
        self.__users = [] 
        self.__customers = [] 
        self.__staffs = [] 
        self.__trains = [] 
        self.__stations = [] 
        self.__routes = [] 
        self.__schedules = []
        self.__trips = []
        self.__starting_fee = 30 
        self.__fee = 5 

#====== ADD======
    def addCustomer(self, customer): 
        for n_customer in self.__customers: 
            if n_customer.getUserId() == customer.getUserId(): 
                raise KeyError(f"There is customer code {customer.getUserId()} already") 
        self.__customers.append(customer) 
        self.__users.append(customer) 

    def addStaff(self, staff): 
        for n_staff in self.__staffs: 
            if n_staff.getUserId() == staff.getUserId(): 
                raise KeyError(f"There is staff code {staff.getUserId()} already") 
        self.__staffs.append(staff) 
        self.__users.append(staff) 

    def addRoute(self, route): 
        for n_route in self.__routes: 
            if n_route.getRouteId() == route.getRouteId(): 
                raise KeyError(f"There is route code {route.getRouteId()} already") 
        self.__routes.append(route) 

    def addSchedule(self, schedule):
        for n_schedule in self.__schedules: 
            if n_schedule.getRoute().getRouteId() == schedule.getRoute().getRouteId(): 
                raise KeyError(f"There is schedule for route code {n_schedule.getRoute().getRouteId()} already") 
        self.__schedules.append(schedule) 

    def addTrip(self, trip):
        for n_trip in self.__trips:
            if n_trip.getTripId() == trip.getTripId():
                raise KeyError(f"There is trip code {trip.getTripId()} already") 
        self.__trips.append(trip)

    def addStation(self, station): 
        for n_station in self.__stations: 
            if n_station.getStationId() == station.getStationId(): 
                raise KeyError(f"There is station code {station.getStationId()} already") 
        self.__stations.append(station) 

    def addTrain(self, train): 
        for n_train in self.__trains:
             if n_train.getTrainId() == train.getTrainId(): 
                raise KeyError(f"There is train code {train.getTrainId()} already") 
        self.__trains.append(train)

#======REMOVE=======
    def removeRoute(self, route): 
        for n_route in self.__routes: 
            if n_route.getRouteId() == route.getRouteId(): 
                if n_route.getStatus() == RouteStatus.DECOMMISSIONED: 
                    raise ValueError("Route already decommissioned")
                n_route.setStatus(RouteStatus.DECOMMISSIONED) 
                return 
        raise KeyError("Route not found") 

    def removeTrain(self, train): 
        for n_train in self.__trains: 
            if n_train.getTrainId() == train.getTrainId(): 
                if n_train.getStatus() == TrainStatus.DECOMMISSIONED: 
                    raise ValueError("Train already decommissioned") 
                n_train.setStatus(TrainStatus.DECOMMISSIONED)
                return
        raise KeyError("Train not found")
    
    def cancelTrip(self, trip):
        for n_trip in self.__trips:
            if n_trip.getTripId() == trip.getTripId():
                for reserve in list(n_trip.getReserves()): 
                    cus_booking = reserve.getReservedCustomer().getUserBookings()
                    for booking in cus_booking:
                        if booking.getBookingTrip().getTripId() == n_trip.getTripId():
                            booking.cancel()
                n_trip.setStatus(TripStatus.CANCELLED)
                return
        raise KeyError("Trip not found")

#======SHOW======
    def showAdminRoute(self): 
        routes = [] 
        for route in self.__routes: 
            dep_time = []
            for schedule in self.__schedules:
                if schedule.getRoute().getRouteId() == route.getRouteId():
                    n_time = schedule.getTimes()
                    for depart_time in n_time:
                        dep_time.append(depart_time.strftime("%H:%M"))
            stations = [] 
            for stop in route.getStop(): 
                stations.append(f"{stop.getStationName()}") 
            routes.append(f"Route Code : {route.getRouteId()}") 
            routes.append(f"Route Name : {route.getRouteName()}") 
            routes.append(f"Distance : {route.getRouteInfo()[0]} km") 
            routes.append(f"Stations : {stations}") 
            routes.append(f"Departure Time : {dep_time}")  
            routes.append(f"Status : {route.getStatus().value}") 
            routes.append("--------------------------------------------------------------") 
        return routes 

    def showRoute(self): 
        routes = [] 
        for route in self.__routes: 
            if route.getStatus() == RouteStatus.DECOMMISSIONED: 
                continue 
            dep_time = []
            for schedule in self.__schedules:
                if schedule.getRoute().getRouteId() == route.getRouteId():
                    n_time = schedule.getTimes()
                    for depart_time in n_time:
                        dep_time.append(depart_time.strftime("%H:%M"))
            stations = [] 
            for stop in route.getStop(): 
                stations.append(f"{stop.getStationName()}") 
            routes.append(f"Route Code : {route.getRouteId()}") 
            routes.append(f"Route Name : {route.getRouteName()}") 
            routes.append(f"Distance : {route.getRouteInfo()[0]} km") 
            routes.append(f"Stations : {stations}") 
            routes.append(f"Departure Time : {dep_time}") 
            routes.append("--------------------------------------------------------------") 
        return routes 

    def showAdminTrain(self): 
        trains = [] 
        for train in self.__trains: 
            trains.append(f"Train Code: {train.getTrainId()}") 
            trains.append(f"Number of Carriage: Normal:{train.getNormalCarriage()} | Business:{train.getBusinessCarriage()}") 
            trains.append(f"Full capacity: {train.countAllSeatInCarriage()}") 
            trains.append(f"Status: {train.getStatus().value}") 
            trains.append("-------------------------------------------------------------") 
        return trains 
    
    def showAdminTrip(self):
        trips = []
        for trip in self.__trips:
            if trip.getStatus() == TripStatus.OPEN:
                trips.append(f"Trip Code: {trip.getTripId()}")
                trips.append(f"Route Code: {trip.getRoute().getRouteId()}")
                trips.append(f"Train Code: {trip.getTrain().getTrainId()}")
                trips.append(f"Date: {trip.getDate()}")
                trips.append(f"Depart Time: {trip.getTime().strftime('%H:%M')}")
                trips.append("-------------------------------------------------------------") 
        return trips

#======SEARCH======
    def searchRouteByNum(self, num): 
        for route in self.__routes: 
            if route.getStatus() == RouteStatus.OPEN: 
                if route.getRouteId() == num: 
                    return route 
        raise KeyError("Route not found")
    
    def searchRouteAnyStatus(self, route_id): 
        for route in self.__routes: 
            if route.getRouteId() == route_id: 
                return route 
        raise KeyError("Route not found") 
    
    def searchSchedule(self, depart_s, arrive_s, search_time = None):
        for schedule in self.__schedules:
            route = schedule.getRoute()
            try:
                route.getStopIndex(depart_s)
                route.getStopIndex(arrive_s)
                if search_time:
                    if search_time not in schedule.getTimes():
                        continue
                return schedule
            except KeyError:
                continue
        raise KeyError("Schedule not found")
    
    def searchScheduleByRoute(self, route_id):
        for schedule in self.__schedules:
            if schedule.getRoute().getRouteId() == route_id:
                return schedule
        raise KeyError("Schedule not found")
    
    def searchTrip(self, trip_id):
        for trip in self.__trips:
            if trip.getTripId() == trip_id:
                return trip
        raise KeyError("Trip not found") 

    def searchTrainByNum(self, num): 
        for train in self.__trains: 
            if train.getStatus() == TrainStatus.COMMISSIONED: 
                if train.getTrainId() == num: 
                    return train 
        raise KeyError("Train not found") 

    def searchTrainAnyStatus(self, train_id): 
        for train in self.__trains: 
            if train.getTrainId() == train_id: 
                return train 
        raise KeyError("Train not found") 

    def searchStationByName(self, name): 
        for station in self.__stations: 
            if station.getStationName().lower() == name.lower(): 
                return station 
        raise KeyError("Station not found") 

    def searchUserByNum(self, num): 
        for user in self.__users: 
            if user.getUserId().lower() == num.lower(): 
                return user 
        raise KeyError("User not found") 

    def searchCustomerByNum(self, num): 
        for customer in self.__customers: 
            if customer.getUserId().lower() == num.lower(): 
                return customer 
        raise KeyError("Customer not found") 

    def searchStaffByNum(self, num): 
        for staff in self.__staffs: 
            if staff.getUserId().lower() == num.lower(): 
                return staff 
        raise KeyError("Staff not found") 

#======CHANGE======
    def changeFee(self, starting, fee): 
        self.__starting_fee = starting 
        self.__fee = fee 

#======GET======
    def getRoutes(self): return self.__routes 
    def getSchedule(self): return self.__schedules
    def getTrips(self): return self.__trips
    def getTrains(self): return self.__trains 
    def getStations(self): return self.__stations 
    def getUsers(self): return self.__users 
    def getStaffs(self): return self.__staffs 
    def getCustomer(self): return self.__customers 
    def getStartingFee(self): return self.__starting_fee 
    def getFee(self): return self.__fee 


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
        self.__train = None 
        self.__status = RouteStatus.OPEN 

    def addStation(self, station, distance): 
        for n_station in self.__stations: 
            if n_station.getStationId() == station.getStationId(): 
                raise KeyError(f"There is station code {station.getStationId()} already") 
        stop = Stop(station, distance) 
        self.__stations.append(stop) 
        self.__f_station = self.__stations[0] 
        self.__l_station = self.__stations[len(self.__stations) - 1] 
        self.__distance = sum([s.getStationDistance() for s in self.__stations])
        self.__name = "-".join([self.__f_station.getStationName(), self.__l_station.getStationName()]) 

    def addTrain(self, train): 
        self.__train = train 

    def setStatus(self, status): 
        self.__status = status 

    def searchStationByName(self, name): 
        for stop in self.__stations: 
            if stop.getStationName().lower() == name.lower(): 
                return stop 
        raise KeyError("Station not found") 
    
#======GET=======
    def getStopIndex(self, station): 
        for i, stop in enumerate(self.__stations): 
            if stop.getStationId() == station.getStationId(): 
                return i 
        raise KeyError("Station not found") 

    def getStopDistance(self, start, end): 
        start_index = self.getStopIndex(start) 
        end_index = self.getStopIndex(end) 
        distance = 0 
        for i, stop in enumerate(self.__stations): 
            if start_index < i <= end_index: 
                distance += stop.getStationDistance() 
        return distance 

    def getRouteId(self): return self.__r_code 
    def getRouteName(self): return self.__name 
    def getRouteInfo(self): return self.__distance, self.__f_station, self.__l_station 
    def getTrain(self): return self.__train 
    def getStop(self): return self.__stations 
    def getStatus(self): return self.__status 

class Schedule:
    def __init__(self, route):
        self.__route = route
        self.__standard_times = []

    def add_standard_time(self, hour, minute):
        self.__standard_times.append(time(hour, minute))

    def searchTime(self, hour, minute):
        search_time = time(hour, minute)
        for n_time in self.__standard_times:
            if n_time == search_time:
                return n_time
        raise ValueError("No schedule of this time found")
    
    def getRoute(self): return self.__route
    def getTimes(self): return self.__standard_times

class Trip:
    def __init__(self, route, train, date, depart_time):
        self.__id = f"{route.getRouteId()}-{date.strftime('%Y%m%d')}-{depart_time.strftime('%H%M')}"
        self.__route = route
        self.__train = train
        self.__date = date
        self.__depart_time = depart_time
        self.__status = TripStatus.OPEN
        self.__reservations = []

    def reserve(self, date, customer, start, end, carriage, seat): 
        if start >= end: raise ValueError("Invalid segment") 
        if not self.isAvailable(date, start, end, carriage, seat): 
            raise ValueError("Already reserved") 
        reservation = ReservedSeat(date, customer, start, end, self.__train, carriage, seat) 
        self.__reservations.append(reservation)

    def release(self, date, start, end, carriage, seat): 
        for r in self.__reservations: 
            if r.getReservedDate() == date and r.getReservedStartStation() == start and r.getReservedEndStation() == end and r.getCarriage() == carriage and r.getSeat() == seat: 
                self.__reservations.remove(r)
                return

    def isAvailable(self, date, start , end, carriage, seat):
        for r in self.__reservations:
            if r.getCarriage() == carriage and r.getSeat() == seat:
                if r.isOverlap(date, start, end):
                    return False
        return True
    
    def showSeatInAllCarriage(self, start, end): 
        seats = [] 
        for carriage in self.__train.getTrainCarriages(): 
            for seat in carriage.getCarriageSeats(): 
                if self.isAvailable(self.__date.date(), start, end, carriage, seat): 
                    status = SeatStatus.AVAILABLE 
                else: 
                    status = SeatStatus.RESERVED 
                seat_view = SeatStatusView(carriage.getCarriageId(), seat.getSeatId(), carriage.getCarriageClass(), status) 
                seats.append(seat_view) 
        return seats
    
    def getArrivalTime(self, station, travel_date):
        end_stop = self.__route.searchStationByName(station.getStationName())
        end_index = self.__route.getStopIndex(end_stop)
        
        total_distance = 0
        stops = self.__route.getStop()
        for i in range(1, end_index + 1):
            total_distance += stops[i].getStationDistance()

        speed = self.__train.getSpeed()

        travel_minute = (total_distance / speed) * 60

        base_datetime = datetime.combine(travel_date, self.__depart_time) 
        return base_datetime + timedelta(minutes=travel_minute) 
    
    def setStatus(self, status):
        self.__status = status

    def getTripId(self): return self.__id
    def getRoute(self): return self.__route
    def getTrain(self): return self.__train
    def getDate(self): return self.__date
    def getTime(self): return self.__depart_time
    def getReserves(self): return self.__reservations
    def getStatus(self): return self.__status

class Station: 
    __station_id_counter = 1 
    def __init__(self, name): 
        self.__st_code = "St" + str(Station.__station_id_counter) 
        Station.__station_id_counter += 1 
        self.__st_name = name 
        self.__current_trip = [] 

    def tripEnter(self, trip): self.__current_trip.append(trip) 
    def tripExit(self, trip): self.__current_trip.remove(trip)
    def getStationId(self): return self.__st_code 
    def getStationName(self): return self.__st_name
    def getCurrentTrip(self): return self.__current_trip

class Stop: 
    def __init__(self, station, distance): 
        self.__station = station 
        self.__distance = distance 
        self.__offset_minute = 0 

    def setStationMinute(self, time): self.__offset_minute = time 
    def getStationId(self): return self.__station.getStationId() 
    def getStationName(self): return self.__station.getStationName() 
    def getStationMinute(self): return self.__offset_minute 
    def getStationDistance(self): return self.__distance 

class ReservedSeat(): 
    def __init__(self, date, customer, start, end, train, carriage, seat):
        self.__reserved_date = date 
        self.__customer = customer
        self.__start_station_index = start 
        self.__end_station_index = end 
        self.__train = train
        self.__carriage = carriage
        self.__seat = seat

    def isOverlap(self, date , start, end): 
        if self.__reserved_date != date: return False 
        return not(end <= self.__start_station_index or start >= self.__end_station_index) 
    
    def getReservedDate(self): return self.__reserved_date 
    def getReservedCustomer(self): return self.__customer
    def getReservedStartStation(self): return self.__start_station_index 
    def getReservedEndStation(self): return self.__end_station_index 
    def getTrain(self): return self.__train
    def getCarriage(self): return self.__carriage
    def getSeat(self) : return self.__seat


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
            self.addCarriage(NormalCarriage()) 
        for j in range(Business_num): 
            self.addCarriage(BusinessCarriage()) 
        self.__status = TrainStatus.COMMISSIONED 

    def addCarriage(self, carriage): 
        self.__carriages.append(carriage) 

    def countAllSeatInCarriage(self): 
        count = 0 
        for carriage in self.__carriages: 
            count += carriage.countAllSeats() 
        return count 

    def getNormalCarriage(self): 
        count = 0 
        for carriage in self.__carriages: 
            if isinstance(carriage, NormalCarriage): 
                count += 1 
        return count 

    def getBusinessCarriage(self): 
        count = 0 
        for carriage in self.__carriages: 
            if isinstance(carriage, BusinessCarriage): 
                count += 1 
        return count 

    def searchCarriageByNum(self, num): 
        for Car in self.__carriages: 
            if Car.getCarriageId() == num: 
                return Car 
        raise KeyError("Carriage not found") 

    def setStatus(self, status): self.__status = status 
    def getTrainId(self): return self.__t_code 
    def getTrainCarriages(self): return self.__carriages 
    def getStatus(self): return self.__status 
    @abstractmethod
    def getClass(self): pass
    @abstractmethod
    def getSpeed(self): pass

class CommuterTrain(Train):
    def __init__(self, normal_num, business_num):
        super().__init__(normal_num, business_num)
        self.__class = "Commuter"
        self.__speed = 100
    def getClass(self): return self.__class
    def getSpeed(self): return self.__speed

class SpeederTrain(Train):
    def __init__(self, normal_num, business_num):
        super().__init__(normal_num, business_num)
        self.__class = "Speeder"
        self.__speed = 250
    def getClass(self): return self.__class
    def getSpeed(self): return self.__speed

class SplinterTrain(Train):
    def __init__(self, normal_num, business_num):
        super().__init__(normal_num, business_num)
        self.__class = "Splinter"
        self.__speed = 500
    def getClass(self): return self.__class
    def getSpeed(self): return self.__speed 

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

    def countAllSeats(self): 
        return len(self.__seats) 

    def searchSeatByNum(self, num): 
        for seat in self.__seats: 
            if seat.getSeatId().lower() == num.lower(): 
                return seat 
        raise KeyError("Seat not found") 

    def getCarriageId(self): return self.__no 
    @abstractmethod 
    def getCarriageClass(self): pass 
    def getCarriageSeats(self): return self.__seats 
    @abstractmethod 
    def getCarriageFee(self): pass 

class NormalCarriage(Carriage): 
    def __init__(self): 
        super().__init__() 
        self.__carriage_fee = 1 
    def getCarriageClass(self): return CarriageClass.Normal 
    def getCarriageFee(self): return self.__carriage_fee 

class BusinessCarriage(Carriage): 
    def __init__(self): 
        super().__init__() 
        self.__carriage_fee = 1.5 
    def getCarriageClass(self): return CarriageClass.Business 
    def getCarriageFee(self): return self.__carriage_fee 

class Seat: 
    def __init__(self, no): 
        self.__no = no 

    def getSeatId(self): return self.__no 

class SeatStatusView: 
    def __init__(self, carriage_id, seat_id, s_class, status): 
        self.__carriage_id = carriage_id 
        self.__seat_id = seat_id 
        self.__class = s_class 
        self.__status = status 

    def getData(self): 
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

    def setUserName(self, name): self.__name = name 
    def setUserEmail(self, email): self.__email = email 
    def setUserPhone(self, phone): 
        if len(phone) != 10:
            raise ValueError("Invalid Phone")
        self.__phone = phone
    @abstractmethod 
    def getUserId(self): pass 
    def getUserName(self): return self.__name 
    def getUserEmail(self): return self.__email 
    def getUserPhone(self): return self.__phone 

class Customer(User): 
    __customer_id_counter = 1 
    def __init__(self, name, email, phone): 
        super().__init__(name, email, phone) 
        self.__id = "C" + str(Customer.__customer_id_counter) 
        Customer.__customer_id_counter += 1 
        self.__reward_point = 0 
        self.__bookings = [] 
        self.__tickets = [] 

    def addBooking(self, booking): 
        self.__bookings.append(booking) 

    def addTicket(self, ticket): 
        self.__tickets.append(ticket) 

    def cancelBooking(self, booking): 
        trans = Transaction() 
        date = booking.getBookingDate().date() 
        segment = booking.getSegment() 
        try: 
            trans.add_rollback(lambda: booking.getBookingTrip().reserve(date, self, segment[0], segment[1], booking.getBookingCarriage(), booking.getBookingSeat())) 
            result = booking.cancel() 
            trans.commit() 
        except Exception as e: 
            trans.rollback() 
            raise e 
        return result   

    def searchBookingByNum(self, num): 
        for booking in self.__bookings: 
            if booking.getBookingId() == num: return booking 
        raise KeyError("Booking not found") 

    def searchTicketByNum(self, num): 
        for ticket in self.__tickets: 
            if ticket.getTicketId() == num: return ticket 
        raise KeyError("Ticket not found") 

    def getUserId(self): return self.__id 
    def getRewardPoint(self): return self.__reward_point 
    
    # Updated to receive payment object
    def payBooking(self, booking, payment): return booking.pay(payment) 
    
    def collectPoints(self, distance): self.__reward_point += distance 
    def getDiscount(self): return 1 
    def getUserBookings(self): return self.__bookings 
    def getUserTickets(self): return self.__tickets 

class Member(Customer): 
    def getDiscount(self): return 0.9 

class Senior(Customer): 
    def getDiscount(self): return 0.85 

class Staff(User): 
    __staff_id_counter = 1 
    def __init__(self, name, email, phone): 
        super().__init__(name, email, phone) 
        self.__id = "S" + str(Staff.__staff_id_counter) 
        Staff.__staff_id_counter += 1 
        self.__usage_histories = [] 

    def addHistory(self, person1, person2, action, time): 
        if person2 is None: 
            info = f"{person1} is {action}" 
        else: 
            info = f"{person1} is {action} {person2}" 
        history = UsageHistory(action, time, info) 
        self.__usage_histories.append(history) 

    def removeLastHistory(self): self.__usage_histories.pop() 
    def getUserId(self): return self.__id 
    def getUsageHistories(self): 
        histories = [] 
        for history in self.__usage_histories: 
            histories.append(history.getHistory()) 
        return histories 

class StationOfficer(Staff): 
    def __init__(self, name, email, phone, station): 
        super().__init__(name, email, phone) 
        self.__assign_station = station 

    def verifyTicket(self, ticket, customer): 
        trans = Transaction() 
        try: 
            old_status = ticket.getTicketStatus() 
            trip_at_station = self.__assign_station.getCurrentTrip() 
            if not trip_at_station: 
                raise ValueError("No train currently at station")
            trip_match = False
            for trip in trip_at_station: 
                if ticket.getTicketTrip().getTripId() == trip.getTripId(): 
                    trip_match = True
                    break
            if not trip_match:
                raise ValueError("Wrong trip or train")

            trans.add_rollback(lambda: ticket.setTicketStatus(old_status) if ticket.getTicketStatus() != TicketStatus.EXPIRED else None)
            ticket.validateTicket(self.__assign_station, customer) 
            ticket.useTicket() 

            self.addHistory(self.getUserId(), customer.getUserId(), 'Verify Ticket', datetime.now()) 
            trans.add_rollback(lambda: self.removeLastHistory()) 
            trans.commit() 
        except Exception as e: 
            trans.rollback() 
            raise e 
        return "Access Granted" 

    def getAssignStation(self): return self.__assign_station 

class SystemAdministrator(Staff): 
    def addRoute(self, system, route): 
        system.addRoute(route) 
        self.addHistory(self.getUserId(), route.getRouteId(), 'Add Route', datetime.now()) 
        return f"Route: {route.getRouteId()}, Name: {route.getRouteName()} added successfully" 

    def removeRoute(self, system, route): 
        system.removeRoute(route) 
        self.addHistory(self.getUserId(), route.getRouteId(), 'Remove Route', datetime.now()) 
        return "route removed successfully" 
    
    def addSchedule(self, system, route_id):
        schedule = Schedule(system.searchRouteByNum(route_id))
        system.addSchedule(schedule)
        route = system.searchScheduleByRoute(route_id).getRoute()
        self.addHistory(self.getUserId(), route.getRouteId(), 'Add Route', datetime.now()) 
        return f"Route: {route.getRouteId()}, Name: {route.getRouteName()} added  Schedule successfully"
    
    def addScheduleTime(self, system, route_id, hour, minute):
        schedule = system.searchScheduleByRoute(route_id)
        route = schedule.getRoute()
        schedule.add_standard_time(hour, minute)
        self.addHistory(self.getUserId(), route.getRouteId(), 'Add Route Schedule', datetime.now()) 
        return f"Route: {route.getRouteId()}, Name: {route.getRouteName()} added  Schedule {hour}:{minute} successfully"

    def addTrain(self, system, train): 
        system.addTrain(train) 
        self.addHistory(self.getUserId(), train.getTrainId(), 'Add Train', datetime.now()) 
        return f"Train: {train.getTrainId()} added successfully" 

    def removeTrain(self, system, train): 
        system.removeTrain(train) 
        self.addHistory(self.getUserId(), train.getTrainId(), 'Remove Train', datetime.now()) 
        return "train removed successfully" 
    
    def addTrip(self, system, trip):
        system.addTrip(trip)
        self.addHistory(self.getUserId(), trip.getTripId(), 'Add Trip', datetime.now())
        return f"Trip: {trip.getTripId()} added successfully"
    
    def cancelTrip(self, system, trip):
        system.cancelTrip(trip)
        self.addHistory(self.getUserId(), trip.getTripId(), 'Cancel Trip', datetime.now())
        return f"Trip: {trip.getTripId()} cancelled successfully"

class UsageHistory: 
    def __init__(self, type, time, info): 
        self.__type = type 
        self.__time = time 
        self.__info = info 
    def getHistory(self): return f"{self.__type}: {self.__time} : {self.__info}" 


# ==========================================
# 6. PAYMENT MODULE
# ==========================================
class Payment(ABC):
    def __init__(self, amount):
        self._amount = amount
    @abstractmethod
    def process(self):
        pass
    def getAmount(self):
        return self._amount

class EWalletPayment(Payment):
    def __init__(self, amount, wallet_id):
        super().__init__(amount)
        self.__wallet_id = wallet_id
    def process(self):
        return f"EWALLET:{self.__wallet_id}:{self._amount}"

class CardPayment(Payment):
    def __init__(self, amount, card_number):
        super().__init__(amount)
        self.__card_number = card_number
    def process(self):
        return f"CARD:{self.__card_number}:{self._amount}"

class BankTransferPayment(Payment):
    def __init__(self, amount, bank_account):
        super().__init__(amount)
        self.__bank_account = bank_account
    def process(self):
        return f"BANK:{self.__bank_account}:{self._amount}"

class CashPayment(Payment):
    def __init__(self, amount):
        super().__init__(amount)
    def process(self):
        return f"CASH:{self._amount}"

class DirectDebitPayment(Payment):
    def __init__(self, amount, account_id):
        super().__init__(amount)
        self.__account_id = account_id
    def process(self):
        return f"DIRECTDEBIT:{self.__account_id}:{self._amount}"


# ==========================================
# 7. BOOKING & TRIP MODULE
# ==========================================
class Booking: 
    booking_id_counter = 1 
    def __init__(self, customer, trip, date, departure_s, arrival_s, train, carriage, seat, system): 
        self.__create_date = datetime.now() 
        self.__cancel_date = None 
        self.__confirm_date = None 
        self.__id = "B" + str(Booking.booking_id_counter) 
        Booking.booking_id_counter += 1 
        self.__customer = customer 
        self.__trip = trip
        self.__route = trip.getRoute()
        self.__date = date 
        self.__departure_s = departure_s
        self.__arrival_s = arrival_s 
        self.__train = train 
        self.__carriage = carriage 
        self.__seat = seat 
        self.__distance = self.__route.getStopDistance(departure_s, arrival_s) 
        self.__booking_price = ((self.__distance * system.getFee() + system.getStartingFee()) * carriage.getCarriageFee())* customer.getDiscount() 
        self.__booking_status = BookingStatus.PENDING 
        self.__payment = None # Added payment tracking
        
        dep = self.__route.getStopIndex(departure_s)
        arr = self.__route.getStopIndex(arrival_s)
        if dep >= arr: raise ValueError("Invalid direction") 
        self.__segment = (dep, arr)
        self.__trip.reserve(self.__date.date(), self.__customer, dep, arr, self.__carriage, self.__seat) 

    def pay(self, payment: Payment): 
        if self.__booking_status != BookingStatus.PENDING: raise ValueError("Cannot pay") 
        departure_time = self.__trip.getArrivalTime(self.__departure_s, self.__date.date())

        if departure_time < datetime.now():
            self.__booking_status = BookingStatus.EXPIRED
            raise ValueError("Booking expired") 
        
        # Checking reward point usage logic
        price_to_pay = self.__booking_price
        if self.__customer.getRewardPoint() >= 100: 
            price_to_pay = 0 
            self.__customer.collectPoints(-100) 
            
        # Validate payment amount matches required price
        if payment.getAmount() < price_to_pay:
            raise ValueError(f"Insufficient payment amount. Required: {price_to_pay}")

        # Process OOP payment
        payment.process()
        self.__payment = payment

        self.__booking_status = BookingStatus.PAID 
        ticket = Ticket(self.__customer, self.__trip, self.__departure_s, self.__arrival_s, self.__train, self.__carriage, self.__seat, price_to_pay) 
        self.__customer.addTicket(ticket) 
        self.__customer.collectPoints(self.__distance) 
        self.__confirm_date = datetime.now() 
        return ticket.getTicketId() 

    def cancel(self): 
        dep, arr = self.__segment
        if self.__booking_status not in [BookingStatus.PENDING, BookingStatus.PAID]: 
            raise ValueError("Cannot cancel booking") 
        departure_time = self.__trip.getArrivalTime(self.__departure_s, self.__date.date()) 
        if departure_time < datetime.now(): 
            self.__booking_status = BookingStatus.EXPIRED 
            result = "expired" 
        else:
            if self.__booking_status == BookingStatus.PAID:
                if self.__booking_price == 0:
                    self.__customer.collectPoints(100) 
                else:
                    self.__customer.collectPoints(-self.__distance)
                self.__booking_status = BookingStatus.REFUNDED 
                result = f"Booking Id: {self.__id} refunded" 
            else:
                self.__booking_status = BookingStatus.CANCELLED 
                result = f"Booking Id: {self.__id} cancelled"
            self.__cancel_date = datetime.now()
            self.__trip.release(self.__date.date(), dep, arr, self.__carriage, self.__seat)
        
        return result 

    def getBookingCreateDate(self): return self.__create_date 
    def getBookingCancelDate(self): return self.__cancel_date 
    def getBookingConfirmDate(self): return self.__confirm_date 
    def getBookingId(self): return self.__id 
    def getBookingTrip(self): return self.__trip
    def getBookingRoute(self): return self.__route
    def getBookingDate(self): return self.__date 
    def getBookingDeparture(self): return self.__departure_s 
    def getBookingArrival(self): return self.__arrival_s 
    def getBookingTrain(self): return self.__train 
    def getBookingCarriage(self): return self.__carriage 
    def getBookingSeat(self): return self.__seat 
    def getBookingPrice(self): return self.__booking_price 
    def getBookingStatus(self): return self.__booking_status 
    def getSegment(self): return self.__segment 

class Ticket: 
    ticket_id_counter = 1 
    def __init__(self, customer, trip, departure_s, arrival_s, train, carriage, seat, ticket_price): 
        self.__create_date = datetime.now() 
        self.__validation_date = None 
        self.__id = "T" + str(Ticket.ticket_id_counter) 
        Ticket.ticket_id_counter += 1 
        self.__customer = customer 
        self.__trip = trip 
        self.__departure_s = departure_s 
        self.__date = trip.getDate()
        self.__departure_time = trip.getTime()
        self.__arrival_s = arrival_s 
        self.__arrival_time = self.__trip.getArrivalTime(self.__arrival_s, self.__date.date())
        self.__train = train 
        self.__carriage = carriage 
        self.__seat = seat 
        self.__ticket_price = ticket_price 
        self.__ticket_status = TicketStatus.CONFIRMED 

    def validateTicket(self, station, customer): 
        self.checkStation(station)
        self.checkCustomer(customer)
        self.checkDate() 
        if self.__ticket_status == TicketStatus.USED: raise ValueError("Ticket already used") 
        return True 
    
    def checkCustomer(self, customer):
        if self.__customer.getUserName() == customer.getUserName():
            return True
        raise ValueError("Wrong Customer")

    def checkStation(self, station): 
        if station.getStationId() != self.__departure_s.getStationId(): 
            raise ValueError("Wrong Station") 
        return True 

    def checkDate(self): 
        now = datetime.now() 
        ticket_time = self.__trip.getArrivalTime(self.__departure_s, self.__date.date())
        if now < ticket_time - timedelta(hours=1): raise ValueError("Too early") 
        if now > ticket_time + timedelta(minutes=20): 
            self.__ticket_status = TicketStatus.EXPIRED 
            raise ValueError("Expired") 
        return True 

    def useTicket(self): 
        if self.__ticket_status == TicketStatus.USED: raise ValueError("Ticket already used") 
        self.__validation_date = datetime.now() 
        self.__ticket_status = TicketStatus.USED 
        return "updated" 

    def setTicketStatus(self, status): self.__ticket_status = status 
    def getTicketCreateDate(self): return self.__create_date 
    def getTicketValidationDate(self): return self.__validation_date 
    def getTicketCustomer(self): return self.__customer
    def getTicketId(self): return self.__id 
    def getTicketTrip(self): return self.__trip
    def getTicketRoute(self): return self.__trip.getRoute()
    def getTicketDate(self): return self.__date 
    def getTicketDeparture(self): return self.__departure_s
    def getTicketDepartTime(self): return self.__departure_time
    def getTicketArrival(self): return self.__arrival_s 
    def getTicketArriveTime(self): return self.__arrival_time
    def getTicketTrain(self): return self.__train 
    def getTicketCarriage(self): return self.__carriage 
    def getTicketSeat(self): return self.__seat 
    def getTicketPrice(self): return self.__ticket_price 
    def getTicketStatus(self): return self.__ticket_status 

class Transaction: 
    def __init__(self): 
        self.__rollback_actions = [] 
    def add_rollback(self, action): self.__rollback_actions.append(action) 
    def commit(self): self.__rollback_actions.clear() 
    def rollback(self): 
        for action in reversed(self.__rollback_actions): action() 


# ==========================================
# 8. INITIALIZAION
# ==========================================
def create_instance(): 
    arl = RailwaySystem("Airport Rail Link") 
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

    Sch1.add_standard_time(8, 30)
    Sch1.add_standard_time(9, 30)

    Sch2.add_standard_time(9, 00)
    Sch2.add_standard_time(10, 00)

    Sch3.add_standard_time(8, 45)
    Sch3.add_standard_time(9, 45)

    Route1.addStation(Phrajomklao, 1) 
    Route1.addStation(Ladkrabang, 3) 
    Route1.addStation(Soiwatlanboon, 3) 
    Route1.addStation(Baanthubchang, 3) 
    Route1.addStation(Huamak, 5) 
    Route1.addStation(Sukhumvit, 4) 
    Route1.addStation(Klongtan, 1) 
    Route1.addStation(Asoke, 3)
    Route1.addStation(Phrayathai, 3)  
    Route1.addStation(Hualamphong, 4)   

    Route2.addStation(Hualamphong, 1)
    Route2.addStation(Bangsue, 8)
    Route2.addStation(Donmueng, 22)
    Route2.addStation(Rangsit, 30)
    Route2.addStation(Ayutthaya, 71)

    Route3.addStation(Hualamphong, 4)
    Route3.addStation(Phrayathai, 3)
    Route3.addStation(Asoke, 3)
    Route3.addStation(Klongtan, 1)
    Route3.addStation(Sukhumvit, 4)
    Route3.addStation(Huamak, 5)
    Route3.addStation(Baanthubchang, 3)
    Route3.addStation(Soiwatlanboon, 3)
    Route3.addStation(Ladkrabang, 3)
    Route3.addStation(Phrajomklao, 1)

    arl.addStation(Phrajomklao) 
    arl.addStation(Ladkrabang) 
    arl.addStation(Soiwatlanboon) 
    arl.addStation(Baanthubchang) 
    arl.addStation(Huamak)
    arl.addStation(Sukhumvit) 
    arl.addStation(Klongtan) 
    arl.addStation(Asoke) 
    arl.addStation(Phrayathai) 
    arl.addStation(Hualamphong)
    arl.addStation(Bangsue)
    arl.addStation(Donmueng)
    arl.addStation(Rangsit)
    arl.addStation(Ayutthaya)

    arl.addTrain(Train1) 
    arl.addTrain(Train2) 
    arl.addTrain(Train3)

    arl.addRoute(Route1) 
    arl.addRoute(Route2) 
    arl.addRoute(Route3)

    arl.addSchedule(Sch1)
    arl.addSchedule(Sch2)
    arl.addSchedule(Sch3)

    John = StationOfficer("John", "Black@gmail.com", "0812345678", Phrajomklao) 
    Jake = StationOfficer("Jake", "Blacker@gmail.com", "0812345678", Hualamphong) 
    Jeff = SystemAdministrator("Jeff", "Blackest@gmail.com", "0812345678") 
    Jack = Customer("Jack", "White@gmail.com", "0812345678") 
    Jill = Member("Jill", "Whiter@gmail.com", "0812345678") 
    Josh = Senior("Josh", "Whitest@gmail.com", "0812345678") 

    carriage = Train1.searchCarriageByNum("Ca1") 
    jack_chair = carriage.searchSeatByNum("1A") 
    jill_chair = carriage.searchSeatByNum("1B") 
    josh_chair = carriage.searchSeatByNum("1C")
    
    st_start = arl.searchStationByName("Phrajomklao")
    st_end = arl.searchStationByName("Hualamphong")

    booking_date = datetime.today() + timedelta(days=1)
    
    reference_trip = None 
        
    for day_offset in range(30):
        current_date = booking_date + timedelta(days=day_offset)
        
        t1 = Trip(Route1, Train1, current_date, Sch1.searchTime(8, 30))
        t2 = Trip(Route1, Train1, current_date, Sch1.searchTime(9, 30))
        
        t3 = Trip(Route2, Train2, current_date, Sch2.searchTime(9, 00))
        t4 = Trip(Route2, Train2, current_date, Sch2.searchTime(10, 00))

        t5 = Trip(Route3, Train3, current_date, Sch3.searchTime(8, 45))
        t6 = Trip(Route3, Train3, current_date, Sch3.searchTime(9, 45))
        
        arl.addTrip(t1)
        arl.addTrip(t2)
        arl.addTrip(t3)
        arl.addTrip(t4)
        arl.addTrip(t5)
        arl.addTrip(t6)
        
        if day_offset == 0:
            reference_trip = t1
    # ==========================================

    Phrajomklao.tripEnter(reference_trip)

    booking1 = Booking(Jack, reference_trip, booking_date, st_start, st_end, Train1, carriage, jack_chair, arl) 
    booking2 = Booking(Jill, reference_trip, booking_date, st_start, st_end, Train1, carriage, jill_chair, arl) 
    booking3 = Booking(Josh, reference_trip, booking_date, st_start, st_end, Train1, carriage, josh_chair, arl) 

    Jack.addBooking(booking1)
    Jill.addBooking(booking2) 
    Josh.addBooking(booking3) 

    arl.addCustomer(Jack) 
    arl.addCustomer(Jill) 
    arl.addCustomer(Josh) 

    arl.addStaff(John) 
    arl.addStaff(Jake) 
    arl.addStaff(Jeff) 
    
    return arl 

arl = create_instance()


# ==========================================
# 9. FASTAPI ENDPOINTS
# ==========================================
@app.post("/Customer/register", tags=["Customer"]) 
def registerCustomer(customer_name: str, customer_email: str, customer_phone:str): 
    try: 
        customer = Customer(customer_name, customer_email, customer_phone) 
        arl.addCustomer(customer) 
        return { "Message" : "created", "customer_id" : customer.getUserId() } 
    except (KeyError) as e: raise HTTPException(status_code= 400, detail=str(e)) 

@app.get("/Customer/{customer_id}/Profile", tags=["Customer Info"]) 
def viewCustomerProfile(customer_id: str): 
    try: 
        customer = arl.searchCustomerByNum(customer_id) 
        return { 
            "ID" : customer.getUserId(), 
            "Name" : customer.getUserName(), 
            "E-mail" : customer.getUserEmail(), 
            "Phone" : customer.getUserPhone(), 
            "Points" : customer.getRewardPoint() 
        } 
    except (ValueError, KeyError) as e: raise HTTPException(status_code=400, detail=str(e)) 

@app.get("/Customer/{customer_id}/Bookings", tags=["Customer Info"]) 
def viewCustomerBookings(customer_id: str): 
    try: 
        customer = arl.searchCustomerByNum(customer_id) 
        bookings = customer.getUserBookings() 
        result = [] 
        for n_booking in bookings: 
            date = n_booking.getBookingDate().strftime("%d/%m/%Y") 
            booking_data = { 
                "CreateDate": n_booking.getBookingCreateDate().strftime("%d/%m/%Y %H:%M"), 
                "BookingId": n_booking.getBookingId(), 
                "Date": date, 
                "Departure": n_booking.getBookingDeparture().getStationName(), 
                "Departure Time" : n_booking.getBookingTrip().getArrivalTime(n_booking.getBookingDeparture(), n_booking.getBookingDate().date()).strftime("%d/%m/%Y %H:%M"), 
                "Arrival": n_booking.getBookingArrival().getStationName(), 
                "Arrival Time" : n_booking.getBookingTrip().getArrivalTime(n_booking.getBookingArrival(), n_booking.getBookingDate().date()).strftime("%d/%m/%Y %H:%M"), 
                "Train": f"{n_booking.getBookingTrain().getTrainId()} | class: {n_booking.getBookingTrain().getClass()}", 
                "Carriage": n_booking.getBookingCarriage().getCarriageId(), 
                "Seat": n_booking.getBookingSeat().getSeatId(), 
                "Price" : n_booking.getBookingPrice(), 
                "Status": n_booking.getBookingStatus().value 
            } 
            if n_booking.getBookingCancelDate() is not None: 
                booking_data["CancelDate"] = n_booking.getBookingCancelDate().strftime("%d/%m/%Y %H:%M") 
            if n_booking.getBookingConfirmDate() is not None: 
                booking_data["ConfirmDate"] = n_booking.getBookingConfirmDate().strftime("%d/%m/%Y %H:%M") 
            result.append(booking_data) 
        return { "data" : result } 
    except (ValueError, KeyError) as e: raise HTTPException(status_code=400, detail=str(e)) 

@app.get("/Customer/{customer_id}/Tickets", tags=["Customer Info"]) 
def viewCustomerTickets(customer_id: str): 
    try: 
        customer = arl.searchCustomerByNum(customer_id) 
        tickets = customer.getUserTickets() 
        result = [] 
        for n_ticket in tickets: 
            ticket_data = { 
                "CreateDate": n_ticket.getTicketCreateDate().strftime("%d/%m/%Y %H:%M"), 
                "TicketId": n_ticket.getTicketId(), 
                "Date": n_ticket.getTicketDate().strftime("%d/%m/%Y"), 
                "Departure": n_ticket.getTicketDeparture().getStationName(), 
                "Departure Time": n_ticket.getTicketDepartTime().strftime("%H:%M"),
                "Arrival": n_ticket.getTicketArrival().getStationName(),
                "Arrival Time": n_ticket.getTicketArriveTime().strftime("%H:%M"),
                "Train": f"{n_ticket.getTicketTrain().getTrainId()} | class: {n_ticket.getTicketTrain().getClass()}",
                "Carriage": n_ticket.getTicketCarriage().getCarriageId(), 
                "Seat": n_ticket.getTicketSeat().getSeatId(), 
                "Status": n_ticket.getTicketStatus().value 
            } 
            if n_ticket.getTicketValidationDate() is not None: 
                ticket_data["ValidationDate"] = n_ticket.getTicketValidationDate().strftime("%d/%m/%Y %H:%M") 
            result.append(ticket_data) 
        return { "data" : result } 
    except (ValueError, KeyError) as e: raise HTTPException(status_code=400, detail=str(e)) 

@app.put("/Customer/{customer_id}/Profile/Edit", tags=["Customer Info"]) 
def updateCustomer(customer_id: str, customer_name: str, customer_email: str, customer_phone: str): 
    try: 
        customer = arl.searchCustomerByNum(customer_id) 
        customer.setUserName(customer_name) 
        customer.setUserEmail(customer_email) 
        customer.setUserPhone(customer_phone) 
        return { "Id" : customer.getUserId(), "Name" : customer.getUserName(), "Email" : customer.getUserEmail(), "Phone" : customer.getUserPhone() } 
    except (ValueError, KeyError) as e: raise HTTPException(status_code=400, detail=str(e)) 

@app.get("/Routes", tags=["Customer Trip"]) 
def viewRoutes(): 
    try: 
        result = arl.showRoute() 
        return { "data" : result } 
    except (ValueError, KeyError) as e: raise HTTPException(status_code=400, detail=str(e)) 

@app.get("/Route/DepartureStation/{departure_s_name}/ArrivalStation/{arrival_s_name}", tags=["Customer Trip"]) 
def viewRouteByStation(departure_s_name: str, arrival_s_name: str): 
    try: 
        routes = [] 
        for route in arl.getRoutes(): 
            try:
                dep = route.searchStationByName(departure_s_name) 
                arr = route.searchStationByName(arrival_s_name) 
            except KeyError:
                continue
            if route.getStatus() == RouteStatus.DECOMMISSIONED: continue
            if route.getStopIndex(dep) >= route.getStopIndex(arr):
                continue
            times = []
            for trip in arl.getTrips():
                if trip.getRoute().getRouteId() == route.getRouteId():
                    try:
                        dep_time = trip.getArrivalTime(dep, datetime.now().date())
                        arr_time = trip.getArrivalTime(arr, datetime.now().date())
                        if f"Depart Time: {dep_time.strftime('%H:%M')} | Arrive Time: {arr_time.strftime('%H:%M')}" in times:
                            continue
                        times.append(f"Depart Time: {dep_time.strftime('%H:%M')} | Arrive Time: {arr_time.strftime('%H:%M')}")
                    except KeyError: continue 
            if times:
                routes.append(f"Route Id: {route.getRouteId()}, name: {route.getRouteName()}") 
                routes.append(f"Schedule : {times}")
        return { "Route List" : routes } 
    except (ValueError, KeyError) as e: raise HTTPException(status_code=400, detail=str(e)) 

@app.get("/Route/Departure/{departure_s_name}/Arrival/{arrival_s_name}", tags=["Customer Trip"]) 
def viewRouteByTrip(departure_s_name: str, arrival_s_name:str, date_s: str, depart_time: str): 
    try: 
        date = datetime.strptime(date_s, "%Y-%m-%d")
        time = datetime.strptime(depart_time, "%H:%M")
        dep_st = arl.searchStationByName(departure_s_name)
        arr_st = arl.searchStationByName(arrival_s_name)
        schedule = arl.searchSchedule(dep_st, arr_st, time.time())
        route = schedule.getRoute()
        search_trip = f"{route.getRouteId()}-{datetime.strftime(date, '%Y%m%d')}-{datetime.strftime(time, '%H%M')}"
        trip = arl.searchTrip(search_trip)
        start = route.getStopIndex(dep_st) 
        end = route.getStopIndex(arr_st)
        if start >= end: raise HTTPException(status_code=400, detail="Invalid route direction") 
        
        stations = [] 
        distance = route.getStopDistance(dep_st, arr_st) 
        for i in range(start, end + 1): 
            stop = route.getStop()[i] 
            stations.append({ "Station": stop.getStationName(), 
                             "Time": trip.getArrivalTime(stop, date.date()).strftime("%H:%M") 
                             }) 
        seat_data = []
        for seat_view in trip.showSeatInAllCarriage(start, end): 
            seat_data.extend(seat_view.getData())
        return{ "Route Id" : route.getRouteId(), 
               "Route Name" : route.getRouteName(), 
               "Departure" : dep_st.getStationName(), 
               "Arrival" : arr_st.getStationName(), 
               "Stations" : stations, 
               "Price" : distance * arl.getFee() + arl.getStartingFee(), 
               "Train Id" : trip.getTrain().getTrainId(), 
               "Train Class": trip.getTrain().getClass(),
               "Train data" : seat_data 
               } 
    except (ValueError, KeyError) as e: raise HTTPException(status_code=400, detail=str(e)) 

@app.post("/Customer/{customer_id}/Booking", tags=["Customer Trip"]) 
def addABooking(customer_id: str, date_s: str, depart_time: str, carriage_id: str, seat_id: str, departure_station_name:str, arrival_station_name:str): 
    try: 
        customer = arl.searchCustomerByNum(customer_id)
        date = datetime.strptime(date_s, "%Y-%m-%d")
        time = datetime.strptime(depart_time,"%H:%M")
        dep_st = arl.searchStationByName(departure_station_name)
        arr_st = arl.searchStationByName(arrival_station_name)
        schedule = arl.searchSchedule(dep_st, arr_st, time.time())
        route = schedule.getRoute()
        search_trip = f"{route.getRouteId()}-{datetime.strftime(date, '%Y%m%d')}-{datetime.strftime(time, '%H%M')}"
        trip = arl.searchTrip(search_trip)
        train = trip.getTrain()
        carriage = train.searchCarriageByNum(carriage_id) 
        seat = carriage.searchSeatByNum(seat_id) 
        
        booking_time = datetime.combine(date.date(), trip.getTime())
        if booking_time < datetime.now(): raise ValueError("Cannot book past trip") 
        
        booking = Booking(customer, trip, booking_time, dep_st, arr_st, train, carriage, seat, arl) 
        customer.addBooking(booking) 
        return{ "Customer Id" : customer.getUserId(), 
               "Booking Id" : booking.getBookingId(), 
               "Route" : booking.getBookingRoute().getRouteName(), 
               "Departure Station" : booking.getBookingDeparture().getStationName(), 
               "Departure Time" : booking.getBookingTrip().getArrivalTime(dep_st, booking_time.date()).strftime("%d/%m/%Y %H:%M"), 
               "Arrival Station" : booking.getBookingArrival().getStationName(), 
               "Arrival Time" : booking.getBookingTrip().getArrivalTime(arr_st, booking_time.date()).strftime("%d/%m/%Y %H:%M"), 
               "Price" : booking.getBookingPrice() 
               } 
    except (ValueError, KeyError) as e: raise HTTPException(status_code=400, detail=str(e)) 

@app.put("/Customer/{customer_id}/Booking/{booking_id}", tags=["Customer Trip"]) 
def cancelABooking(customer_id: str, booking_id:str): 
    try: 
        customer = arl.searchCustomerByNum(customer_id) 
        booking = customer.searchBookingByNum(booking_id) 
        result = customer.cancelBooking(booking) 
        return{ "Message" : result, "Booking Id" : booking.getBookingId() } 
    except (ValueError, KeyError) as e: raise HTTPException(status_code=400, detail=str(e)) 

@app.post("/Customer/{customer_id}/Booking/{booking_id}/Pay", tags=["Customer Trip"]) 
def payABooking(customer_id: str, booking_id: str, payment_method: str, amount: float, payment_info: str = ""): 
    try: 
        customer = arl.searchCustomerByNum(customer_id) 
        booking = customer.searchBookingByNum(booking_id) 

        # Create Payment Object based on method parameter
        method = payment_method.upper()
        if method == "EWALLET":
            payment = EWalletPayment(amount, payment_info)
        elif method == "CARD":
            payment = CardPayment(amount, payment_info)
        elif method == "BANK":
            payment = BankTransferPayment(amount, payment_info)
        elif method == "CASH":
            payment = CashPayment(amount)
        elif method == "DIRECTDEBIT":
            payment = DirectDebitPayment(amount, payment_info)
        else:
            raise ValueError("Invalid payment method")

        # Process payment via customer & booking
        result = customer.payBooking(booking, payment) 
        ticket = customer.searchTicketByNum(result) 

        return{ "Message" : "Booking has been paid", 
               "Payment Method Processed": payment.process(),
               "Created Date" : ticket.getTicketCreateDate().strftime("%d/%m/%Y %H:%M"), 
               "Ticket Id" : ticket.getTicketId(), 
               "Route" : ticket.getTicketRoute().getRouteName(), 
               "Departure Station" : ticket.getTicketDeparture().getStationName(), 
               "Departure Time" : ticket.getTicketTrip().getArrivalTime(ticket.getTicketDeparture(), ticket.getTicketDate().date()).strftime("%d/%m/%Y %H:%M"), 
               "Arrival Station" : ticket.getTicketArrival().getStationName(), 
               "Arrival Time" : ticket.getTicketTrip().getArrivalTime(ticket.getTicketArrival(), ticket.getTicketDate().date()).strftime("%d/%m/%Y %H:%M"), 
               "Price Paid" : ticket.getTicketPrice() 
               } 
    except (ValueError, KeyError) as e: raise HTTPException(status_code=400, detail=str(e)) 

@app.get("/Staff/{staff_id}", tags=["Staff"]) 
def showStaffUsageHistory(staff_id: str): 
    try: 
        staff = arl.searchStaffByNum(staff_id) 
        return { "data" : staff.getUsageHistories() } 
    except (ValueError, KeyError) as e: raise HTTPException(status_code=400, detail=str(e)) 

@app.put("/StationOfficer/{staff_id}/Customer/{customer_id}/Ticket/{ticket_id}", tags=["StationOfficer"]) 
def verifyATicket(staff_id: str, customer_id: str , ticket_id: str): 
    try: 
        staff = arl.searchStaffByNum(staff_id) 
        if not isinstance(staff, StationOfficer): raise ValueError("Unauthorized") 
        customer = arl.searchCustomerByNum(customer_id) 
        ticket_found = customer.searchTicketByNum(ticket_id) 
        result = staff.verifyTicket(ticket_found, customer) 
        return { "Message" : result, 
                "Ticket Id" : ticket_found.getTicketId(), 
                "Departure Date" : ticket_found.getTicketDate().strftime("%d/%m/%Y %H:%M"), 
                "Ticket Status": ticket_found.getTicketStatus().value 
                } 
    except (ValueError, KeyError) as e: raise HTTPException(status_code=400, detail=str(e)) 

@app.post("/Staff/SystemAdmin/{staff_id}/Add/{position}/register", tags=["System Administrator"]) 
def registerStaff(staff_id: str, position: str, user_name: str, user_email: str, user_phone: str, assign:str): 
    try: 
        admin = arl.searchStaffByNum(staff_id) 
        if not isinstance(admin, SystemAdministrator): raise ValueError("Unauthorized") 
        if position.lower() == "stationofficer": 
            assign_found = None 
            for station in arl.getStations(): 
                if station.getStationId() == assign: 
                    assign_found = station 
                    break 
            if assign_found is None: raise ValueError("Cannot find assign") 
            staff = StationOfficer(user_name, user_email, user_phone, assign_found) 
        elif position.lower() == "systemadministrator": 
            staff = SystemAdministrator(user_name, user_email, user_phone) 
        else: raise ValueError("Invalid position") 
        arl.addStaff(staff) 
        return { "Message" : "created", "user_id" : staff.getUserId() } 
    except (ValueError, KeyError) as e: raise HTTPException(status_code= 400, detail=str(e)) 

@app.post("/Staff/SystemAdmin/{staff_id}/Add/Route", tags=["System Administrator"]) 
def addRoute(staff_id: str, f_station_name: str, f_station_distance: int, l_station_name: str, l_station_distance: int, train_id: str): 
    try: 
        staff = arl.searchStaffByNum(staff_id) 
        if not isinstance(staff, SystemAdministrator): raise ValueError("Unauthorized")  
        route = Route() 
        try: f_station = arl.searchStationByName(f_station_name) 
        except KeyError: 
            f_station = Station(f_station_name) 
            arl.addStation(f_station) 
        try: l_station = arl.searchStationByName(l_station_name) 
        except KeyError: 
            l_station = Station(l_station_name) 
            arl.addStation(l_station) 
        route.addStation(f_station, int(f_station_distance)) 
        route.addStation(l_station, int(l_station_distance)) 
        train = arl.searchTrainByNum(train_id) 
        route.addTrain(train) 
        result = staff.addRoute(arl, route) 
        return { "data" : result } 
    except (ValueError, KeyError) as e: raise HTTPException(status_code= 400, detail=str(e)) 

@app.put("/Staff/SystemAdmin/{staff_id}/Remove/Route/{route_id}", tags=["System Administrator"]) 
def removeRoute(staff_id: str, route_id: str): 
    try: 
        staff = arl.searchStaffByNum(staff_id) 
        if not isinstance(staff, SystemAdministrator): raise ValueError("Unauthorized") 
        route = arl.searchRouteAnyStatus(route_id) 
        result = staff.removeRoute(arl, route) 
        return { "data" : result } 
    except (ValueError, KeyError) as e: raise HTTPException(status_code= 400, detail=str(e)) 

@app.post("/Staff/SystemAdmin/{staff_id}/add/Schedule/Route/{route_id}", tags=["System Administrator"])
def addSchedule(staff_id: str, route_id: str):
    try:
        staff = arl.searchStaffByNum(staff_id) 
        if not isinstance(staff, SystemAdministrator): raise ValueError("Unauthorized") 
        
        result = staff.addSchedule(arl, route_id)
        return { "data" : result } 
    except (ValueError, KeyError) as e: raise HTTPException(status_code= 400, detail=str(e)) 

@app.post("/Staff/SystemAdmin/{staff_id}/add/Schedule/Route/{route_id}/Time", tags=["System Administrator"])
def addScheduleTime(staff_id: str, route_id: str, hour: int, minute: int):
    try:
        staff = arl.searchStaffByNum(staff_id) 
        if not isinstance(staff, SystemAdministrator): raise ValueError("Unauthorized") 

        result = staff.addScheduleTime(arl, route_id, hour, minute)
        return { "data" : result } 
    except (ValueError, KeyError) as e: raise HTTPException(status_code= 400, detail=str(e)) 

@app.post("/Staff/SystemAdmin/{staff_id}/Add/Trip", tags=["System Administrator"])
def addTrip(staff_id: str, route_id: str, train_id: str, travel_date: str, hour: int, minute: int):
    try:
        staff = arl.searchStaffByNum(staff_id)
        if not isinstance(staff, SystemAdministrator): raise ValueError("Unauthorized") 
        route = arl.searchRouteByNum(route_id)
        train = arl.searchTrainByNum(train_id)
        date = datetime.strptime(travel_date, "%Y/%m/%d")
        
        found_schedule = None
        for schedule in arl.getSchedule():
            if schedule.getRoute().getRouteId() == route.getRouteId():
                found_schedule = schedule

        if found_schedule is None:
            raise ValueError("Schedule not found for this route")
        
        depart_time = found_schedule.searchTime(hour, minute)
        travel_time = datetime.combine(date, depart_time)

        trip = Trip(route, train, travel_time, depart_time)

        result = staff.addTrip(arl, trip)

        return { 
            "Message" : result, 
            "Trip ID" : trip.getTripId(),
            "Route" : route.getRouteName(),
            "Date" : travel_time.strftime("%d/%m/%Y"),
            "Departure Time" : depart_time.strftime("%H:%M")
        } 
    except (ValueError, KeyError) as e: 
        raise HTTPException(status_code= 400, detail=str(e))
    
@app.put("/Staff/SystemAdmin/{staff_id}/Cancel/Trip/{trip_id}", tags=["System Administrator"])
def cancelTrip(staff_id: str, trip_id):
    try:
        staff = arl.searchStaffByNum(staff_id)
        if not isinstance(staff, SystemAdministrator): raise ValueError("Unauthorized")

        trip = arl.searchTrip(trip_id)

        if trip.getStatus() == TripStatus.CANCELLED:
            raise ValueError("Trip has been cancelled")
        elif trip.getStatus() == TripStatus.EXPIRED:
            raise ValueError("Trip is expired")
        
        result = staff.cancelTrip(arl, trip)

        return{
            "data": result
        }
    except (ValueError, KeyError) as e: 
        raise HTTPException(status_code= 400, detail=str(e))

@app.post("/Staff/SystemAdmin/{staff_id}/Add/Train", tags=["System Administrator"]) 
def addTrain(staff_id:str, normal_num: str, business_num: str): 
    try: 
        staff = arl.searchStaffByNum(staff_id) 
        if not isinstance(staff, SystemAdministrator): raise ValueError("Unauthorized") 
        train = Train(int(normal_num), int(business_num)) 
        result = staff.addTrain(arl, train) 
        return { "data" : result } 
    except (ValueError, KeyError) as e: raise HTTPException(status_code= 400, detail=str(e)) 

@app.put("/Staff/SystemAdmin/{staff_id}/Remove/Train/{train_id}", tags=["System Administrator"]) 
def removeTrain(staff_id: str, train_id:str): 
    try: 
        staff = arl.searchStaffByNum(staff_id) 
        if not isinstance(staff, SystemAdministrator): raise ValueError("Unauthorized") 
        train = arl.searchTrainAnyStatus(train_id) 
        result = staff.removeTrain(arl, train) 
        return { "data" : result } 
    except (ValueError, KeyError) as e: raise HTTPException(status_code= 400, detail=str(e)) 

@app.put("/Staff/SystemAdmin/{staff_id}/change/fee", tags=["System Administrator"]) 
def changeFee(staff_id:str, starting_fee: int, fee: int): 
    try: 
        staff = arl.searchStaffByNum(staff_id) 
        if not isinstance(staff, SystemAdministrator): raise ValueError("Unauthorized") 
        arl.changeFee(starting_fee, fee) 
        return{ "Starting Fee": arl.getStartingFee(), "Fee": arl.getFee() } 
    except (ValueError, KeyError) as e: raise HTTPException(status_code= 400, detail=str(e)) 

@app.get("/Staff/SystemAdmin/{staff_id}/Routes", tags=["System Administrator"]) 
def showAllRoute(staff_id: str): 
    try: 
        staff = arl.searchStaffByNum(staff_id) 
        if not isinstance(staff, (SystemAdministrator, StationOfficer)): raise ValueError("Unauthorized") 
        return{ "data" : arl.showAdminRoute() } 
    except (ValueError, KeyError) as e: raise HTTPException(status_code= 400, detail=str(e)) 

@app.get("/Staff/SystemAdmin/{staff_id}/Trips", tags=["System Administrator"])
def showAllTrip(staff_id: str):
    try:
        staff = arl.searchStaffByNum(staff_id) 
        if not isinstance(staff, (SystemAdministrator, StationOfficer)): raise ValueError("Unauthorized")
        return{ "data" : arl.showAdminTrip() } 
    except (ValueError, KeyError) as e: raise HTTPException(status_code= 400, detail=str(e)) 

@app.get("/Staff/SystemAdmin/{staff_id}/Trains", tags=["System Administrator"]) 
def showAllTrain(staff_id: str): 
    try: 
        staff = arl.searchStaffByNum(staff_id) 
        if not isinstance(staff, (SystemAdministrator, StationOfficer)): raise ValueError("Unauthorized") 
        return{ "data" : arl.showAdminTrain() } 
    except (ValueError, KeyError) as e: raise HTTPException(status_code= 400, detail=str(e)) 

if __name__ == "__main__": 
    uvicorn.run(app, host="127.0.0.1", port=8000)
from fastmcp import FastMCP
from datetime import datetime 

from models import *
mcp = FastMCP("Railway")

# arl = RailwaySystem()

# ==========================================
# 9. MCP
# ==========================================

@mcp.tool()
def register_customer(customer_name: str, customer_email: str, customer_phone:str): 
    """Register new customer"""
    try: 
        customer = Customer(customer_name, customer_email, customer_phone) 
        arl.add_customer(customer) 
        return { f"Customer Id: {customer.get_user_id()}| Name: {customer.get_user_name()}| E-mail: {customer.get_user_email()}| Phone: {customer.get_user_phone()}"} 
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"  

@mcp.tool() 
def view_customer_profile(customer_id: str): 
    """View Customer Profile (Id, name, email, phone, point)"""
    try: 
        customer = arl.search_customer_by_num(customer_id) 
        return { 
            f"ID : {customer.get_user_id()}", 
            f"Name : {customer.get_user_name()}", 
            f"E-mail : {customer.get_user_email()}", 
            f"Phone : {customer.get_user_phone()}", 
            f"Points : {customer.get_reward_point()}" 
        } 
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}" 

@mcp.tool()
def view_customer_bookings(customer_id: str): 
    """View Customer Bookings"""
    try: 
        customer = arl.search_customer_by_num(customer_id) 
        bookings = customer.get_user_bookings() 
        result = [] 
        for n_booking in bookings: 
            date = n_booking.get_booking_date().strftime("%d/%m/%Y") 
            booking_data = { 
                f"CreateDate: {n_booking.get_booking_create_date().strftime('%d/%m/%Y %H:%M')}", 
                f"BookingId: {n_booking.get_booking_id()}", 
                f"Date: {date}", 
                f"Departure: {n_booking.get_booking_departure().get_station_name()}", 
                f"Departure Time : {n_booking.get_booking_trip().get_arrival_time(n_booking.get_booking_departure(), n_booking.get_booking_date().date()).strftime('%d/%m/%Y %H:%M')}", 
                f"Arrival: {n_booking.get_booking_arrival().get_station_name()}", 
                f"Arrival Time : {n_booking.get_booking_trip().get_arrival_time(n_booking.get_booking_arrival(), n_booking.get_booking_date().date()).strftime('%d/%m/%Y %H:%M')}", 
                f"Train: {n_booking.get_booking_train().get_train_id()} | class: {n_booking.get_booking_train().get_class()}", 
                f"Carriage: {n_booking.get_booking_carriage().get_carriage_id()}", 
                f"Seat: {n_booking.get_booking_seat().get_seat_id()}", 
                f"Price : {n_booking.get_booking_price()}", 
                f"Status: {n_booking.get_booking_status().value}" 
            } 
            if n_booking.get_booking_cancel_date() is not None: 
                f"Cancel Date: {n_booking.get_booking_cancel_date().strftime('%d/%m/%Y %H:%M')}"
            if n_booking.get_booking_confirm_date() is not None: 
                f"Confirm Date: {n_booking.get_booking_confirm_date().strftime('%d/%m/%Y %H:%M')}"
                payment = n_booking.get_payment()
                f"Payment : {type(payment)} | Payment Id: {payment.get_id()}"
            result.append(booking_data) 
        return { "data" : result } 
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"  

@mcp.tool()
def view_customer_tickets(customer_id: str): 
    """View Customer Tickets"""
    try: 
        customer = arl.search_customer_by_num(customer_id) 
        tickets = customer.get_user_tickets() 
        result = [] 
        for n_ticket in tickets: 
            payment = n_ticket.get_payment()
            ticket_data = { 
                f"CreateDate: {n_ticket.get_ticket_create_date().strftime('%d/%m/%Y %H:%M')}", 
                f"TicketId: {n_ticket.get_ticket_id()}", 
                f"Date: {n_ticket.get_ticket_date().strftime('%d/%m/%Y')}", 
                f"Departure: {n_ticket.get_ticket_departure().get_station_name()}", 
                f"Departure Time: {n_ticket.get_ticket_depart_time().strftime('%H:%M')}",
                f"Arrival: {n_ticket.get_ticket_arrival().get_station_name()}",
                f"Arrival Time: {n_ticket.get_ticket_arrive_time().strftime('%H:%M')}",
                f"Train: {n_ticket.get_ticket_train().get_train_id()} | class: {n_ticket.get_ticket_train().get_class()}",
                f"Carriage: {n_ticket.get_ticket_carriage().get_carriage_id()}", 
                f"Seat: {n_ticket.get_ticket_seat().get_seat_id()}", 
                f"Status: {n_ticket.get_ticket_status().value}"
                f"Payment : {type(payment)} | Payment Id: {payment.get_id()}"
            } 
            if n_ticket.get_ticket_validation_date() is not None: 
                f"Validation Date: {n_ticket.get_ticket_validation_date().strftime('%d/%m/%Y %H:%M')}" 
            result.append(ticket_data) 
        return { "data" : result } 
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}" 

@mcp.tool()
def update_customer(customer_id: str, customer_name: str, customer_email: str, customer_phone: str): 
    """Update Customer"""
    try: 
        customer = arl.search_customer_by_num(customer_id) 
        customer.set_user_name(customer_name) 
        customer.set_user_email(customer_email) 
        customer.set_user_phone(customer_phone) 
        return { f"Id : {customer.get_user_id()}| Name : {customer.get_user_name()}| Email : {customer.get_user_email()}| Phone : {customer.get_user_phone()}" } 
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"  

@mcp.tool()
def view_routes(): 
    """View bookable Route"""
    try: 
        result = arl.show_route() 
        return { "data" : result } 
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"  

@mcp.tool() 
def view_route_by_station(departure_s_name: str, arrival_s_name: str): 
    """View route from one station to other station in route"""
    try: 
        routes = [] 
        for route in arl.get_routes(): 
            try:
                dep = route.search_station_by_name(departure_s_name) 
                arr = route.search_station_by_name(arrival_s_name) 
            except KeyError:
                continue
            if route.get_status() == RouteStatus.DECOMMISSIONED: continue
            if route.get_stop_index(dep) >= route.get_stop_index(arr):
                continue
            times = []
            for trip in arl.get_trips():
                if trip.get_route().get_route_id() == route.get_route_id():
                    try:
                        dep_time = trip.get_arrival_time(dep, datetime.now().date())
                        arr_time = trip.get_arrival_time(arr, datetime.now().date())
                        if f"Depart Time: {dep_time.strftime('%H:%M')} | Arrive Time: {arr_time.strftime('%H:%M')}" in times:
                            continue
                        times.append(f"Train id: {trip.get_train().get_train_id()} | Class: {trip.get_train().get_class()} | Depart Time: {dep_time.strftime('%H:%M')} | Arrive Time: {arr_time.strftime('%H:%M')}")
                    except KeyError: continue 
            if times:
                routes.append(f"Route Id: {route.get_route_id()} | name: {route.get_route_name()}") 
                routes.append(f"Schedule : {times}")
        return { "Route List" : routes } 
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"  

@mcp.tool() 
def view_route_by_trip(departure_s_name: str, arrival_s_name:str, date_s: str, depart_time: str): 
    """View route and show seats from one to another station by trip and"""
    try: 
        date = datetime.strptime(date_s, "%Y-%m-%d")
        time = datetime.strptime(depart_time, "%H:%M")
        dep_st = arl.search_station_by_name(departure_s_name)
        arr_st = arl.search_station_by_name(arrival_s_name)
        schedule = arl.search_schedule(dep_st, arr_st, time.time())
        route = schedule.get_route()
        search_t = f"{route.get_route_id()}-{datetime.strftime(date, '%Y%m%d')}-{datetime.strftime(time, '%H%M')}"
        trip = arl.search_trip(search_t)
        if trip.get_train() == None: raise Exception("Invalid no train available") 
        start = route.get_stop_index(dep_st) 
        end = route.get_stop_index(arr_st)
        if start >= end: raise Exception("Invalid route direction") 
        stations = []  
        for i in range(start, end + 1): 
            stop = route.get_stop()[i] 
            stations.append(f"Station: {stop.get_station_name()} | Time: {trip.get_arrival_time(stop, date.date()).strftime('%H:%M')}") 
        carriages = []
        for carriage in trip.get_train().get_train_carriages():
            carriages.append(f"Carriage Id: {carriage.get_carriage_id()} | Capacity: {carriage.count_all_seats()}| Used: {carriage.get_used_seats(trip)}| Remaining: {carriage.get_remaining_seats(trip)}")
        seat_data = []
        for seat_view in trip.show_seat_in_all_carriage(start, end):
            seat_data.extend(seat_view.get_data())
        return{ f"Route Id : {route.get_route_id()}", 
               f"Route Name : {route.get_route_name()}",
               f"Departure : {dep_st.get_station_name()}",
               f"Arrival : {arr_st.get_station_name()}",
               f"Stations : {stations}",
               f"Train Id : {trip.get_train().get_train_id()}",
               f"Train Class: {trip.get_train().get_class()}",
               f"Train full capacity : {trip.get_train().get_total_seats()}",
               f"Train reserved : {trip.count_used_seat()}",
               f"Train remaining seats : {trip.get_remaining_seats()}",
               f"Train data : {seat_data}"
               }
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}" 

@mcp.tool() 
def add_a_booking(customer_id: str, date_s: str, depart_time: str, carriage_id: str, seat_id: str, departure_station_name:str, arrival_station_name:str):
    """Booking for customer""" 
    try: 
        customer = arl.search_customer_by_num(customer_id)
        date = datetime.strptime(date_s, "%Y-%m-%d")
        time = datetime.strptime(depart_time,"%H:%M")
        dep_st = arl.search_station_by_name(departure_station_name)
        arr_st = arl.search_station_by_name(arrival_station_name)
        schedule = arl.search_schedule(dep_st, arr_st, time.time())
        route = schedule.get_route()
        search_t = f"{route.get_route_id()}-{datetime.strftime(date, '%Y%m%d')}-{datetime.strftime(time, '%H%M')}"
        trip = arl.search_trip(search_t)
        train = trip.get_train()
        if train == None: raise Exception("Invalid no train available")
        carriage = train.search_carriage_by_num(carriage_id) 
        seat = carriage.search_seat_by_num(seat_id) 
        
        booking_time = datetime.combine(date.date(), trip.get_time())
        if booking_time < datetime.now(): raise ValueError("Cannot book past trip") 
        
        booking = Booking(customer, trip, booking_time, dep_st, arr_st, train, carriage, seat, arl) 
        customer.add_booking(booking) 
        return{ f"Customer Id : {customer.get_user_id()}",
               f"Booking Id : {booking.get_booking_id()}",
               f"Route : {booking.get_booking_route().get_route_name()}",
               f"Departure Station : {booking.get_booking_departure().get_station_name()}",
               f"Departure Time : {booking.get_booking_trip().get_arrival_time(dep_st, booking_time.date()).strftime('%d/%m/%Y %H:%M')}",
               f"Arrival Station : {booking.get_booking_arrival().get_station_name()}",
               f"Arrival Time : {booking.get_booking_trip().get_arrival_time(arr_st, booking_time.date()).strftime('%d/%m/%Y %H:%M')}",
               f"Price : {booking.get_booking_price()}"
        } 
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}" 

@mcp.tool()
def cancel_a_booking(customer_id: str, booking_id:str): 
    """Cancel Booking"""
    try: 
        customer = arl.search_customer_by_num(customer_id) 
        booking = customer.search_booking_by_num(booking_id) 
        result = customer.cancel_booking(booking) 
        return{ f"Message : {result}, Booking Id : {booking.get_booking_id()}" } 
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"
    
@mcp.tool()
def change_booking(customer_id: str, booking_id: str, date_s: str):
    """Change date in booking"""
    try:
        customer = arl.search_customer_by_num(customer_id) 
        booking = customer.search_booking_by_num(booking_id)

        result = booking.change_trip(date_s, arl)

        return {f"Message : {result}"}
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"


@mcp.tool()
def refund_a_booking(customer_id: str, booking_id: str, payment_code: str):
    """Refund already paid booking"""
    try: 
        customer = arl.search_customer_by_num(customer_id) 
        booking = customer.search_booking_by_num(booking_id) 
        payment = arl.search_payment(payment_code)
        result = customer.refund_booking(booking) 
        return{ f"Message : {result}, Booking Id : {booking.get_booking_id()} | Amount left: {payment.get_amount()}" } 
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"

@mcp.tool() 
def pay_a_booking(customer_id: str, booking_id:str, payment_code: str): 
    """Pay booking with payment"""
    try: 
        customer = arl.search_customer_by_num(customer_id) 
        booking = customer.search_booking_by_num(booking_id) 
        payment = arl.search_payment(payment_code)
        result = customer.pay_booking(booking, payment, payment_code) 
        ticket = customer.search_ticket_by_num(result) 
        return{ f"Message : Booking has been paid",
               f"Created Date : {ticket.get_ticket_create_date().strftime('%d/%m/%Y %H:%M')}",
               f"Ticket Id : {ticket.get_ticket_id()}",
               f"Route : {ticket.get_ticket_route().get_route_name()}",
               f"Departure Station : {ticket.get_ticket_departure().get_station_name()}",
               f"Departure Time : {ticket.get_ticket_trip().get_arrival_time(ticket.get_ticket_departure(), ticket.get_ticket_date().date()).strftime('%d/%m/%Y %H:%M')}",
               f"Arrival Station : {ticket.get_ticket_arrival().get_station_name()}",
               f"Arrival Time : {ticket.get_ticket_trip().get_arrival_time(ticket.get_ticket_arrival(), ticket.get_ticket_date().date()).strftime('%d/%m/%Y %H:%M')}", 
               f"Price : {ticket.get_ticket_price()}"
               f"Amount left : {payment.get_amount()}"
               } 
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}" 
    
@mcp.tool()
def pay_a_booking_with_point(customer_id: str, booking_id: str):
    """Pay booking with point"""
    try:
        customer = arl.search_customer_by_num(customer_id)
        booking = customer.search_booking_by_num(booking_id)

        result = booking.pay_with_points()
        ticket = customer.search_ticket_by_num(result)

        return{f"Message : Booking has been paid",
               f"Created Date : {ticket.get_ticket_create_date().strftime('%d/%m/%Y %H:%M')}",
               f"Ticket Id : {ticket.get_ticket_id()}",
               f"Route : {ticket.get_ticket_route().get_route_name()}",
               f"Departure Station : {ticket.get_ticket_departure().get_station_name()}",
               f"Departure Time : {ticket.get_ticket_trip().get_arrival_time(ticket.get_ticket_departure(), ticket.get_ticket_date().date()).strftime('%d/%m/%Y %H:%M')}",
               f"Arrival Station : {ticket.get_ticket_arrival().get_station_name()}",
               f"Arrival Time : {ticket.get_ticket_trip().get_arrival_time(ticket.get_ticket_arrival(), ticket.get_ticket_date().date()).strftime('%d/%m/%Y %H:%M')}", 
               f"Price : {ticket.get_ticket_price()}"
               f"Amount of point left : {customer.get_reward_point()}"
               } 
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}" 
    

@mcp.tool()
def buy_food(customer_id: str, food_name: str, payment_code: str):
    """buy food"""
    try:
        customer = arl.search_customer_by_num(customer_id)
        food = arl.search_food_by_name(food_name)
        payment = arl.search_payment(payment_code)

        customer.buy_food(arl, food)
        payment.process(food.get_price())

        return {f"{customer_id} bought {food_name} for {food.get_price()}| Amount of money left: {payment.get_amount()}"}
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"

@mcp.tool() 
def show_staff_usage_history(staff_id: str): 
    """show staff usage history """
    try: 
        staff = arl.search_staff_by_num(staff_id) 
        return { f"data : {staff.get_usage_histories()}" } 
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}" 
    
@mcp.tool()
def trip_enter(staff_id: str, trip_id):
    """enter trip to station"""
    try:
        staff = arl.search_staff_by_num(staff_id) 
        if not isinstance(staff, StationOfficer): raise ValueError("Unauthorized") 
        trip = arl.search_trip(trip_id)
        for station in trip.get_route().get_stop():
            station.trip_enter(trip)
        return {
            f"trip entered"
        }
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"
    
@mcp.tool()
def trip_exit(staff_id: str, trip_id):
    """remove trip to station"""
    try:
        staff = arl.search_staff_by_num(staff_id) 
        if not isinstance(staff, StationOfficer): raise ValueError("Unauthorized") 
        trip = arl.search_trip(trip_id)
        for station in trip.get_route().get_stop():
            station.trip_exit(trip)
        return {
            f"trip exited"
        }
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"
        
@mcp.tool() 
def verify_a_ticket(staff_id: str, customer_id: str , ticket_id: str): 
    """verify Ticket"""
    try: 
        staff = arl.search_staff_by_num(staff_id) 
        if not isinstance(staff, StationOfficer): raise ValueError("Unauthorized") 
        customer = arl.search_customer_by_num(customer_id) 
        ticket_found = customer.search_ticket_by_num(ticket_id) 
        result = staff.verify_ticket(ticket_found, customer) 
        return { f"Message : {result}", 
                f"Ticket Id : {ticket_found.get_ticket_id()}", 
                f"Departure Date : {ticket_found.get_ticket_date().strftime('%d/%m/%Y %H:%M')}", 
                f"Ticket Status: {ticket_found.get_ticket_status().value}" 
                } 
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}" 

@mcp.tool()
def register_staff(staff_id: str, position: str, user_name: str, user_email: str, user_phone: str, assign:str): 
    """register staff"""
    try: 
        admin = arl.search_staff_by_num(staff_id) 
        if not isinstance(admin, SystemAdministrator): raise ValueError("Unauthorized") 
        if position.lower() == "stationofficer": 
            assign_found = None 
            for station in arl.get_stations(): 
                if station.get_station_name() == assign: 
                    assign_found = station 
                    break 
            if assign_found is None: raise ValueError("Cannot find assign") 
            staff = StationOfficer(user_name, user_email, user_phone, assign_found) 
        elif position.lower() == "systemadministrator": 
            staff = SystemAdministrator(user_name, user_email, user_phone) 
        else: raise ValueError("Invalid position") 
        arl.add_staff(staff) 
        return { f"Message : created",
                 f"user_id : {staff.get_user_id()}" 
                 } 
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}" 

@mcp.tool() 
def add_route(staff_id: str, f_station_name: str, f_station_distance: int, l_station_name: str, l_station_distance: int): 
    """Add new route"""
    try: 
        staff = arl.search_staff_by_num(staff_id) 
        if not isinstance(staff, SystemAdministrator): raise ValueError("Unauthorized")  
        route = Route() 
        try: f_station = arl.search_station_by_name(f_station_name) 
        except KeyError: 
            f_station = Station(f_station_name) 
            arl.add_station(f_station) 
        try: l_station = arl.search_station_by_name(l_station_name) 
        except KeyError: 
            l_station = Station(l_station_name) 
            arl.add_station(l_station) 
        route.add_station(f_station, int(f_station_distance)) 
        route.add_station(l_station, int(l_station_distance)) 
        result = staff.add_route(arl, route) 
        return { f"data : {result}" } 
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}" 

@mcp.tool()
def remove_route(staff_id: str, route_id: str): 
    """Remove route"""
    try: 
        staff = arl.search_staff_by_num(staff_id) 
        if not isinstance(staff, SystemAdministrator): raise ValueError("Unauthorized") 
        route = arl.search_route_any_status(route_id) 
        for trip in arl.get_trips():
            if trip.get_route().get_route_id() == route.get_route_id():
                staff.cancel_trip(arl, trip)
        result = staff.remove_route(arl, route) 
        return { f"data : {result}" } 
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}" 

@mcp.tool()
def add_schedule(staff_id: str, route_id: str):
    """Add new schedule for route"""
    try:
        staff = arl.search_staff_by_num(staff_id) 
        if not isinstance(staff, SystemAdministrator): raise ValueError("Unauthorized") 
        
        result = staff.add_schedule(arl, route_id)
        return { f"data : {result}" } 
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}" 

@mcp.tool()
def add_schedule_time(staff_id: str, route_id: str, hour: int, minute: int):
    try:
        staff = arl.search_staff_by_num(staff_id) 
        if not isinstance(staff, SystemAdministrator): raise ValueError("Unauthorized") 

        result = staff.add_schedule_time(arl, route_id, hour, minute)
        return { f"data : {result}" } 
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}" 

@mcp.tool()
def add_trip(staff_id: str, route_id: str, train_id: str, travel_date: str, hour: int, minute: int):
    try:
        staff = arl.search_staff_by_num(staff_id)
        if not isinstance(staff, SystemAdministrator): raise ValueError("Unauthorized") 
        route = arl.search_route_by_num(route_id)
        train = arl.search_train_by_num(train_id)
        date = datetime.strptime(travel_date, "%Y/%m/%d")
        
        found_schedule = None
        for schedule in arl.get_schedule():
            if schedule.get_route().get_route_id() == route.get_route_id():
                found_schedule = schedule

        if found_schedule is None:
            raise ValueError("Schedule not found for this route")
        
        depart_time = found_schedule.search_time(hour, minute)
        travel_time = datetime.combine(date, depart_time)

        trip = Trip(route, train, travel_time, depart_time)

        result = staff.add_trip(arl, trip)

        return { 
            f"Message : {result}", 
            f"Trip ID : {trip.get_trip_id()}",
            f"Route : {route.get_route_name()}",
            f"Date : {travel_time.strftime('%d/%m/%Y')}",
            f"Departure Time : {depart_time.strftime('%H:%M')}"
        } 
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}" 
    
@mcp.tool()
def cancel_trip(staff_id: str, trip_id):
    try:
        staff = arl.search_staff_by_num(staff_id)
        if not isinstance(staff, SystemAdministrator): raise ValueError("Unauthorized")

        trip = arl.search_trip(trip_id)

        if trip.get_status() == TripStatus.CANCELLED:
            raise ValueError("Trip has been cancelled")
        elif trip.get_status() == TripStatus.EXPIRED:
            raise ValueError("Trip is expired")
        
        result = staff.cancel_trip(arl, trip)

        return{
            f"data: {result}"
        }
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}" 

@mcp.tool() 
def add_train(staff_id:str, t_class:str,  normal_num: int, business_num: int): 
    try: 
        staff = arl.search_staff_by_num(staff_id) 
        if not isinstance(staff, SystemAdministrator): raise ValueError("Unauthorized") 
        if t_class.lower() == "commuter":
            train = CommuterTrain(normal_num, business_num) 
        elif t_class.lower() == "speeder":
            train = SpeederTrain(normal_num, business_num)
        elif t_class.lower() == "splinter":
            train = SplinterTrain(normal_num, business_num)
        result = staff.add_train(arl, train) 
        return { f"data : {result}" } 
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}" 

@mcp.tool() 
def remove_train(staff_id: str, train_id:str): 
    try: 
        staff = arl.search_staff_by_num(staff_id) 
        if not isinstance(staff, SystemAdministrator): raise ValueError("Unauthorized") 
        train = arl.search_train_any_status(train_id) 
        for n_trip in arl.get_trips():
            if n_trip.get_train().get_train_id() == train.get_train_id():
                staff.cancel_trip(arl, n_trip)
        result = staff.remove_train(arl, train) 
        return { f"data : {result}" } 
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"  

@mcp.tool() 
def change_fee(staff_id:str, starting_fee: int, fee: int, service_fee: int): 
    try: 
        staff = arl.search_staff_by_num(staff_id) 
        if not isinstance(staff, SystemAdministrator): raise ValueError("Unauthorized") 
        arl.change_fee(starting_fee, fee, service_fee) 
        return{ f"Starting Fee: {arl.get_starting_fee()}", 
               f"Fee: {arl.get_fee()}",
                f"Service Fee: {arl.get_service_fee()}" }
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}" 

@mcp.tool() 
def show_all_route(staff_id: str): 
    try: 
        staff = arl.search_staff_by_num(staff_id) 
        if not isinstance(staff, (SystemAdministrator, StationOfficer)): raise ValueError("Unauthorized") 
        return{ f"data : {arl.show_admin_route()}" } 
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"  

@mcp.tool()
def show_all_trip(staff_id: str):
    try:
        staff = arl.search_staff_by_num(staff_id) 
        if not isinstance(staff, (SystemAdministrator, StationOfficer)): raise ValueError("Unauthorized")
        return{ f"data : {arl.show_admin_trip()}" } 
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"  

@mcp.tool()
def show_all_train(staff_id: str): 
    try: 
        staff = arl.search_staff_by_num(staff_id) 
        if not isinstance(staff, (SystemAdministrator, StationOfficer)): raise ValueError("Unauthorized") 
        return{ f"data : {arl.show_admin_train()}" } 
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"  

arl = create_instance()
if __name__ == "__main__":
    mcp.run()
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional
from math import ceil

app = FastAPI(title="Movie Ticket Booking API")

# =========================================================
# DATA & COUNTERS (Tasks 2, 4, 14)
# =========================================================

# Task 2: movies list with at least 6 movies

movies = [
    {"id": 1, "title": "Interstellar", "genre": "Sci-Fi", "language": "English", "duration_mins": 169, "ticket_price": 320, "seats_available": 60},
    {"id": 2, "title": "3 Idiots", "genre": "Comedy", "language": "Hindi", "duration_mins": 170, "ticket_price": 180, "seats_available": 45},
    {"id": 3, "title": "Avengers: Endgame", "genre": "Action", "language": "English", "duration_mins": 181, "ticket_price": 400, "seats_available": 50},
    {"id": 4, "title": "KGF Chapter 2", "genre": "Action", "language": "Kannada", "duration_mins": 168, "ticket_price": 250, "seats_available": 35},
    {"id": 5, "title": "Dangal", "genre": "Drama", "language": "Hindi", "duration_mins": 161, "ticket_price": 200, "seats_available": 40},
    {"id": 6, "title": "Joker", "genre": "Thriller", "language": "English", "duration_mins": 122, "ticket_price": 300, "seats_available": 25},
]
   

# Task 4 & 14: Counters and lists
bookings = []
booking_counter = 1
holds = []
hold_counter = 1

# =========================================================
# PYDANTIC MODELS (Tasks 6, 9, 11, 14)
# =========================================================

class BookingRequest(BaseModel): # Task 6 & 9
    customer_name: str = Field(..., min_length=2)
    movie_id: int = Field(..., gt=0)
    seats: int = Field(..., gt=0, le=10) # Validates seats=0 is rejected
    phone: str = Field(..., min_length=10)
    seat_type: str = "standard"
    promo_code: str = ""

class NewMovie(BaseModel): # Task 11
    title: str = Field(..., min_length=2)
    genre: str = Field(..., min_length=2)
    language: str = Field(..., min_length=2)
    duration_mins: int = Field(..., gt=0)
    ticket_price: int = Field(..., gt=0)
    seats_available: int = Field(..., gt=0)

class SeatHoldRequest(BaseModel): # Task 14 Request Body
    customer_name: str = Field(..., min_length=2)
    movie_id: int = Field(..., gt=0)
    seats: int = Field(..., gt=0)

# =========================================================
# HELPERS (Tasks 7, 9, 10)
# =========================================================

def find_movie(movie_id: int): # Task 7
    return next((m for m in movies if m["id"] == movie_id), None)

def calculate_ticket_cost(base_price: int, seats: int, seat_type: str, promo_code: str = ""): # Task 7 & 9
    multipliers = {"standard": 1.0, "premium": 1.5, "recliner": 2.0}
    price_per_seat = base_price * multipliers.get(seat_type.lower(), 1.0)
    original_cost = price_per_seat * seats
    
    discount = 0.0
    if promo_code == "SAVE10": discount = 0.10
    elif promo_code == "SAVE20": discount = 0.20
    
    discounted_cost = original_cost * (1 - discount)
    return original_cost, discounted_cost

def filter_movies_logic(genre=None, language=None, max_price=None, min_seats=None): # Task 10
    filtered = movies
    if genre is not None:
        filtered = [m for m in filtered if m["genre"].lower() == genre.lower()]
    if language is not None:
        filtered = [m for m in filtered if m["language"].lower() == language.lower()]
    if max_price is not None:
        filtered = [m for m in filtered if m["ticket_price"] <= max_price]
    if min_seats is not None:
        filtered = [m for m in filtered if m["seats_available"] >= min_seats]
    return filtered

# =========================================================
# ROUTES (Tasks 1 - 20)
# =========================================================

# --- FIXED GET ROUTES (Must be above /movies/{movie_id}) ---

@app.get("/") # Task 1
def home():
    return {'message': 'Welcome to Movie Ticket Booking API'    }

@app.get("/movies") # Task 2
def get_all_movies():
    return {
        "movies": movies,
        "total": len(movies),
        "total_seats_available": sum(m["seats_available"] for m in movies)
    }

@app.get("/movies/summary") # Task 5
def get_movie_summary():
    genres = [m["genre"] for m in movies]
    return {
        "total_movies": len(movies),
        "most_expensive_ticket": max(m["ticket_price"] for m in movies),
        "cheapest_ticket": min(m["ticket_price"] for m in movies),
        "total_seats_across_all_movies": sum(m["seats_available"] for m in movies),
        "count_of_movies_by_genre": {g: genres.count(g) for g in set(genres)}
    }

@app.get("/movies/filter") # Task 10
def filter_movies(genre: Optional[str] = None, language: Optional[str] = None, 
                  max_price: Optional[int] = None, min_seats: Optional[int] = None):
    filtered = filter_movies_logic(genre, language, max_price, min_seats)
    return filtered

@app.get("/movies/search") # Task 16
def search_movies(keyword: str):
    kw = keyword.lower()
    matches = [m for m in movies if kw in m["title"].lower() or kw in m["genre"].lower() or kw in m["language"].lower()]
    if not matches:
        return {"message": "No results found matching your keyword."}
    return {"total_found": len(matches), "movies": matches}

@app.get("/movies/sort") # Task 17
def sort_movies(sort_by: str = "ticket_price", order: str = "asc"):
    allowed_sorts = ["ticket_price", "title", "duration_mins", "seats_available"]
    if sort_by not in allowed_sorts:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by. Use one of: {allowed_sorts}")
    return sorted(movies, key=lambda x: x.get(sort_by, 0), reverse=(order == "desc"))

@app.get("/movies/page") # Task 18
def paginate_movies(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    return {"total": len(movies), "total_pages": ceil(len(movies)/limit), "movies": movies[start:start+limit]}

@app.get("/movies/browse") # Task 20
def browse_movies(keyword: Optional[str] = None, genre: Optional[str] = None, 
                  language: Optional[str] = None, sort_by: str = "ticket_price", 
                  order: str = "asc", page: int = 1, limit: int = 3):
    res = movies
    # 1. Keyword filter
    if keyword: res = [m for m in res if keyword.lower() in m["title"].lower()]
    # 2. Genre/Language filter
    if genre: res = [m for m in res if m["genre"].lower() == genre.lower()]
    if language: res = [m for m in res if m["language"].lower() == language.lower()]
    # 3. Sort
    res = sorted(res, key=lambda x: x.get(sort_by, 0), reverse=(order == "desc"))
    # 4. Paginate
    start = (page - 1) * limit
    return res[start:start+limit]

@app.get("/bookings") # Task 4
def get_all_bookings():
    return {"bookings": bookings, "total": len(bookings), "total_revenue": sum(b["total_cost"] for b in bookings)}

@app.get("/bookings/search") # Task 19
def search_bookings(customer_name: str):
    return [b for b in bookings if customer_name.lower() in b["customer_name"].lower()]

@app.get("/bookings/sort") # Task 19
def sort_bookings(sort_by: str = "total_cost"):
    return sorted(bookings, key=lambda x: x.get(sort_by, 0))

@app.get("/bookings/page") # Task 19
def page_bookings(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    return bookings[start:start+limit]

@app.get("/seat-hold") # Task 14
def get_holds():
    return holds

# --- VARIABLE GET ROUTE (Must be below fixed /movies/... routes) ---

@app.get("/movies/{movie_id}") # Task 3
def get_movie_by_id(movie_id: int):
    movie = find_movie(movie_id)
    if not movie: raise HTTPException(status_code=404, detail="Movie not found")
    return movie

# --- POST, PUT, DELETE ROUTES ---

@app.post("/bookings") # Task 8 & 9
def create_booking(req: BookingRequest):
    global booking_counter
    movie = find_movie(req.movie_id)
    if not movie: raise HTTPException(status_code=404, detail="Movie not found")
    if movie["seats_available"] < req.seats: raise HTTPException(status_code=400, detail="Not enough seats")
    
    orig, disc = calculate_ticket_cost(movie["ticket_price"], req.seats, req.seat_type, req.promo_code)
    movie["seats_available"] -= req.seats
    
    booking = {
        "booking_id": booking_counter, "movie_title": movie["title"], "seats": req.seats, 
        "seat_type": req.seat_type, "original_cost": orig, "total_cost": disc, "customer_name": req.customer_name
    }
    bookings.append(booking)
    booking_counter += 1
    return booking

@app.post("/movies", status_code=201) # Task 11
def create_movie(movie: NewMovie):
    if any(m["title"].lower() == movie.title.lower() for m in movies):
        raise HTTPException(status_code=400, detail="Duplicate title")
    new_id = max(m["id"] for m in movies) + 1
    new_m = {"id": new_id, **movie.dict()}
    movies.append(new_m)
    return new_m

@app.put("/movies/{movie_id}") # Task 12
def update_movie(movie_id: int, ticket_price: Optional[int] = None, seats_available: Optional[int] = None):
    movie = find_movie(movie_id)
    if not movie: raise HTTPException(status_code=404, detail="Not found")
    if ticket_price is not None: movie["ticket_price"] = ticket_price
    if seats_available is not None: movie["seats_available"] = seats_available
    return movie

@app.delete("/movies/{movie_id}") # Task 13
def delete_movie(movie_id: int):
    movie = find_movie(movie_id)
    if not movie: raise HTTPException(status_code=404, detail="Not found")
    if any(b["movie_title"] == movie["title"] for b in bookings):
        raise HTTPException(status_code=400, detail="Movie has existing bookings")
    movies.remove(movie)
    return {"message": "Deleted"}

@app.post("/seat-hold") # Task 14
def seat_hold(req: SeatHoldRequest):
    global hold_counter
    movie = find_movie(req.movie_id)
    if not movie or movie["seats_available"] < req.seats: raise HTTPException(status_code=400, detail="Unavailable")
    
    movie["seats_available"] -= req.seats
    hold = {"hold_id": hold_counter, "customer_name": req.customer_name, "movie_id": req.movie_id, "seats": req.seats}
    holds.append(hold)
    hold_counter += 1
    return hold

@app.post("/seat-confirm/{hold_id}") # Task 15
def confirm_hold(hold_id: int):
    global booking_counter
    hold = next((h for h in holds if h["hold_id"] == hold_id), None)
    if not hold: raise HTTPException(status_code=404, detail="Hold not found")
    
    movie = find_movie(hold["movie_id"])
    booking = {
        "booking_id": booking_counter, "customer_name": hold["customer_name"], 
        "movie_title": movie["title"], "seats": hold["seats"], "total_cost": movie["ticket_price"] * hold["seats"]
    }
    bookings.append(booking)
    booking_counter += 1
    holds.remove(hold)
    return booking

@app.delete("/seat-release/{hold_id}") # Task 15
def release_hold(hold_id: int):
    hold = next((h for h in holds if h["hold_id"] == hold_id), None)
    if not hold: raise HTTPException(status_code=404, detail="Hold not found")
    
    movie = find_movie(hold["movie_id"])
    if movie: movie["seats_available"] += hold["seats"]
    holds.remove(hold)
    return {"message": "Released"}
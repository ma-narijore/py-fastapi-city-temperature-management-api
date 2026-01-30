from fastapi import FastAPI

from schemas import City

app = FastAPI()


@app.post("/cities")
def create_city(city: City):
    ...


@app.get("/cities")
def list_cities():
    ...


@app.get("/cities/{city_id}")
def list_detail_city(city_id: int):
    ...


@app.put("/cities/{city_id}")
def update_detail_city(city_id: int, city: City):
    ...


@app.delete("/cities/{city_id}")
def delete_detail_city(city_id: int):
    ...

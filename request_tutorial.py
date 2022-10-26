from fastapi import FastAPI, Query, Path
from pydantic import BaseModel
from enum import Enum

class Platforms(Enum):
    Playstation = 1
    Xbox = 2
    PC = 3

class VideoGame(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    platform: Platforms


api = FastAPI()


@api.post("/items/")
async def create_item(item: VideoGame):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    if item.platform.value == 1:
        item_dict.update({"platform": "Available on Playstation only"})
    if item.platform.value == 2:
        item_dict.update({"platform": "Available on Xbox only"})
    if item.platform.value == 3:
        item_dict.update({"platform": "Available on PC only"})
    return item_dict

@api.put("/items/{item_id}")
async def create_item_with_query(item_id: int, item: VideoGame, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

@api.get("/items/")
async def read_items(q: str | None = Query(default=None, min_length = 3, max_length=50, regex=".*[0-9][0-8][0-4]$", title="Query string",
        description="Query string for the items to search in the database that have a good match", deprecated=True)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@api.get("/items/list/")
async def read_items_with_query_as_list(q: list[str] | None = Query(default=None)):
    query_items = {"q": q}
    return query_items

@api.get("/items/alias/")
async def read_items_with_alias(q: str | None = Query(default=None, alias="item-query")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@api.get("/hidden/")
async def read_items_hidden_query(
    hidden_query: str | None = Query(default=None, include_in_schema=False)
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    else:
        return {"hidden_query": "Not found"}

@api.get("/items/path/{item_id}")
async def read_items_with_path(
    item_id: int = Path(title="The ID of the item to get"),
    q: str | None = Query(default=None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

@api.get("/items/int_validation/{item_id}")
async def read_items_with_id_validation(
    *,
    item_id: int = Path(title="The ID of the item to get", gt=0, le=1000),
    q: str,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
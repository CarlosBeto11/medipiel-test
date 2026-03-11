from pydantic import BaseModel
from typing import List, Literal
from datetime import datetime


class Products(BaseModel):
    id: int
    quantity: int


class OrderCreate(BaseModel):
    customer_id: int
    status: Literal["created", "confirmed", "rejected"]
    products: List[Products]


class OrderUpdateStatus(BaseModel):
    status: Literal["created", "confirmed", "rejected"]


class Customer(BaseModel):
    id: int
    name: str
    last_name: str


class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int


class OrderItems(BaseModel):
    id: int
    product: Product
    quantity: int


class OrderDetail(BaseModel):
    status: str
    customer: Customer
    order_items: List[OrderItems] = [] # Include the related posts

    class Config:
        from_attributes = True


class CreateInventoryMovements(BaseModel):
    product_id : int
    movement_type: Literal["receipt", "sale", "transfer"]
    quantity: int

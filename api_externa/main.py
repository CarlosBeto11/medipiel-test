# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import func, desc
from database import get_db, engine
from sqlalchemy.orm import Session, selectinload
from models import Base, Products, Orders, Customers, OrderItems, InventoryMovements
from schemas import OrderCreate, OrderUpdateStatus, OrderDetail, CreateInventoryMovements
from datetime import datetime

app = FastAPI()

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/products/{product_id}")
def product_detail(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Products).filter(Products.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")    
    return product


@app.get("/products")
def products_list(db: Session = Depends(get_db)):
    return db.query(Products).all()


@app.post("/orders")
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    customer = db.query(Customers).filter(Customers.id == order.customer_id).first()
    if not customer:
        return {"error": "Customer not found"} 
    
    order_to_create = Orders(
        customer_id=order.customer_id, status=order.status
    )
    db.add(order_to_create)
    db.commit()
    db.refresh(order_to_create)

    for product in order.products:
        product_data = db.query(Products).filter(Products.id == product.id).first()

        if not product_data:
            raise HTTPException(status_code=404, detail="Some of the products don't exists")
        
        order_item = OrderItems(
            order_id=order_to_create.id, product_id=product.id, quantity=product.quantity
        )
        db.add(order_item)
        db.commit()
        db.refresh(order_item)

    return order_to_create


@app.get("/orders/{order_id}", response_model=OrderDetail)
def order_detail(order_id: int, db: Session = Depends(get_db)):
    result = db.query(Orders).filter(Orders.id == order_id).options(selectinload(Orders.order_items))
    
    order = result.first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order


@app.put("/orders/{order_id}")
def order_update_status(
    order_status: OrderUpdateStatus, 
    order_id: int, 
    db: Session = Depends(get_db)
):
    order = db.query(Orders).filter(Orders.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="the order does not exists")
    
    order.status = order_status.status
    db.commit()
    return order


@app.get("/inventory-movements")
def inventory_movements(
    product: int = None, 
    date: str = None, 
    movement_type: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(InventoryMovements)

    if product:
        query = query.filter(InventoryMovements.product_id == product)

    if date:
        try:
            datetime_object = datetime.strptime(date, "%Y-%m-%d")
            query = query.filter(func.date(InventoryMovements.movement_date) == datetime_object.date())
        except Exception:
            return {"error": "Invalid date format, must be YYYY-MM-DD"}
        
    if movement_type:
        query = query.filter(InventoryMovements.movement_type == movement_type)
    
    inventory = query.all()
    return inventory


@app.get("/inventory/{product_id}")
def product_inventory(product_id: int, db: Session = Depends(get_db)):
    last_inventory = db.query(InventoryMovements).filter(
        InventoryMovements.product_id == product_id
    ).order_by(desc(InventoryMovements.id)).first()
    
    if not last_inventory:
        raise HTTPException(status_code=404, detail="inventory not found")

    return last_inventory


@app.post("/inventory-movements")
def create_inventory_movements(inventory: CreateInventoryMovements, db: Session = Depends(get_db)):
    product = db.query(Products).filter(Products.id == inventory.product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="the product does not exists")
    
    inventory_to_create = InventoryMovements(
        movement_type=inventory.movement_type, 
        product_id=inventory.product_id, 
        quantity=inventory.quantity
    )

    db.add(inventory_to_create)
    db.commit()
    db.refresh(inventory_to_create)

    product.stock = product.stock - inventory.quantity
    db.commit()

    return inventory_to_create
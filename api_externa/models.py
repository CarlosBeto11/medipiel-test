from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Customers(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    orders = relationship("Orders", back_populates="customer")


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, index=True)
    order_items = relationship("OrderItems", back_populates="product")


class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    # customer: Mapped["Customers"] = relationship(back_populates="customers")
    customer = relationship("Customers", back_populates="orders")
    status = Column(String, nullable=False)
    order_items = relationship("OrderItems", back_populates="order")


class OrderItems(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    order = relationship("Orders", back_populates="order_items")
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    product = relationship("Products", back_populates="order_items")
    quantity = Column(Integer, nullable=False)


class InventoryMovements(Base):
    __tablename__ = "inventory_movements"

    id = Column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    # product: Mapped["Products"] = relationship(back_populates="product")
    movement_date = Column(DateTime(timezone=True), server_default=func.now())
    movement_type = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)

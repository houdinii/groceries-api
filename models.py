import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Table, Float
from sqlalchemy.orm import relationship, backref

db = SQLAlchemy()
Base = db.Model

item_offer = Table("item_offer", Base.metadata,
                   Column("item_id", Integer, ForeignKey("item.id")),
                   Column("offer_id", Integer, ForeignKey("offer.id"))
                   )


class Item(db.Model):
    __tablename__ = "item"  #
    id = Column(Integer, primary_key=True)  #
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)  #
    ean = Column(String(13))  #
    title = Column(String)  #
    upc = Column(String(12), unique=True)  #
    gtin = Column(String(14))  #
    elid = Column(String(12))  #
    description = Column(String(515))  #
    brand = Column(String(64))  #
    model = Column(String(32))  #
    color = Column(String(32))  #
    size = Column(String(32))  #
    dimension = Column(String(32))  #
    weight = Column(String(16))  #
    category = Column(String)  #
    currency = Column(String)  #
    lowest_recorded_price = Column(Float)  #
    highest_recorded_price = Column(Float)  #
    offers = relationship("Offer", backref=backref("item"))  #

    def __repr__(self):
        return f"<Item: {self.title} - {self.upc}>"

    def __str__(self):
        return f'{self.upc}: {self.title}'


class Offer(db.Model):
    __tablename__ = "offer"  #
    id = Column(Integer, primary_key=True)  #
    item_id = Column(Integer, ForeignKey("item.id"))  #
    upc = Column(String)
    merchant = Column(String)  #
    domain = Column(String)  #
    title = Column(String)  #
    currency = Column(String)  #
    list_price = Column(Float)  #
    price = Column(Float)  #
    shipping = Column(String)  #
    condition = Column(String)  #
    availability = Column(String)  #
    link = Column(String)  #
    updated_t = Column(Integer)  #

    def __repr__(self):
        return f"<Offer: {self.title} - {self.merchant} - ${self.price}>"

    def __str__(self):
        return f'{self.merchant}: {self.title}   ${self.price}'


class Error(db.Model):
    __tablename__ = "error"  #
    id = Column(Integer, primary_key=True)  #
    search_url = Column(String)  #
    upc = Column(String)  #
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)  #
    code = Column(String)  #
    message = Column(String)  #

    def __repr__(self):
        return f"<{self.code}: {self.message}>"

    def __str__(self):
        return f'{self.code}: {self.message}'


class Inventory(db.Model):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    item_id = Column(Integer)
    upc = Column(String, unique=True)
    title = Column(String)
    description = Column(String)
    onhand = Column(Float)
    minimum = Column(Float)
    unit = Column(String)
    priority = Column(Integer)

    def __repr__(self):
        return f"<INVENTORY ITEM {self.Title} - On Hand:{self.onhand}  Minimum: {self.minimum}>"

    def __str__(self):
        return f'{self.Title} - On Hand:{self.onhand}  Minimum: {self.minimum}'

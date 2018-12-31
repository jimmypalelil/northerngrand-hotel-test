import uuid

from src.common.database import Database


class InventoryItem(object):
    def __init__(self, item_name, laundry, lock_up, second, third, fourth, fifth, sixth, par_stock, cost_per_item, par_25, type, total_count= None, total_cost=None, cat=None, _id=None):
        self.item_name = item_name
        self.laundry = laundry
        self.lock_up = lock_up
        self.second = second
        self.third = third
        self.fourth = fourth
        self.fifth = fifth
        self.sixth = sixth
        self.par_stock = par_stock
        self.total_count = laundry + lock_up + second + third + fourth + fifth + sixth + par_stock if total_count is None else total_count
        self.cost_per_item = cost_per_item
        self.total_cost = cost_per_item * self.total_count if total_cost is None else total_cost
        self.par_25 = par_25
        self.type = type
        self.cat = "inventory" if cat is None else cat
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "item_name": self.item_name,
            "laundry": self.laundry,
            "lock_up": self.lock_up,
            "second": self.second,
            "third": self.third,
            "fourth": self.fourth,
            "fifth": self.fifth,
            "sixth": self.sixth,
            "par_stock": self.par_stock,
            "total_count": self.total_count,
            "cost_per_item": self.cost_per_item,
            "total_cost": self.total_cost,
            "par_25": self.par_25,
            "type": self.type,
            "cat": self.cat,
            "_id": self._id
        }

    @classmethod
    def update(cls, id, data):
        Database.update('inventory', {"_id": id}, data)

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one('inventory', {"_id": id}))

    def insert(self):
        Database.insert('inventory', self.json())

    @classmethod
    def remove(cls,id):
        Database.remove('inventory', {"_id": id})
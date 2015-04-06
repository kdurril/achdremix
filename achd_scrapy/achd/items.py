# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class AchdItem(Item):
    # define the fields for your item here like:
    r_id = Field()
    name = Field()
    address = Field()
    contact = Field()
    phone = Field()
    inspect = Field()
    r_date = Field()
    r_type = Field()
    r_encounter = Field()

class InspectionItem(Item):
    pass

    

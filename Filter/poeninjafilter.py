import logging
import sys

logger = logging.getLogger(__name__)

class PoENinjaFilter:
    def __init__(self, poeninja):
        self.poeninja = poeninja

    def checkCondition(self, item):
        if 'piece of' in item.get('name'):
            return False

        if 'Tabula' in item.get('name'):
            return True

        if item.get('corrupted') is not None and item.get('corrupted') == True:
            return False

        if item.get('itemType') == 3 or item.get('itemType') == 6:
            if item.get('price') != 'unpriced' and item.get('price') != 'not priced in chaos' and item.get('identified'):
                return True

        return False

    def isWorthBuying(self, item):
        found = False

        if item.get('itemType') == 6:
            divcardprice = self.poeninja.prices['divcard']['0'][item.get('name')]
            found = True

            if self.evaluate(divcardprice, item.get('price')):
                return divcardprice
            
        else:

            for itemType in self.poeninja.prices:

                if itemType == 'divcard':
                    continue
               
                if self.poeninja.prices[itemType][item.get('Links')].get(item.get('name', None)) is not None:
                    found = True
                    price = self.poeninja.prices[itemType][item.get('Links')].get(item.get('name', None))
                    
                    if self.evaluate(price, item.get('price')):
                        return price
                    continue
        if not found:
            logger.warning("Could not find: " + str(item))

        return False

    def evaluate(self, priceNinja, priceItem):
        perc_decrease = ((priceNinja - priceItem) / priceNinja) * 100

        if perc_decrease >= 20 and priceNinja - priceItem > 2:
            return True

    def sendMessage(self, item, price):
        print("item is: " + str(item) + " ninja: " + str(price))

        

#{'name': 'Dusk Ichor', 'itemType': 2, 'price': 'unpriced', 'xLoc': 3, 'yLoc': 1, 'Links': 0, 'mods': [
#    '16% increased Mine Damage', '+8% to all Elemental Resistances', '+15% to Lightning Resistance']}

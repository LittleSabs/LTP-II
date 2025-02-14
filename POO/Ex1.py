class Item:
    def __init__(self,name,value,rarity):
        self.name = name
        self.value = value
        self.rarity = rarity

    def showInfo(self):
        print(f'Nome do item;{self.name}'
              f'\nValor do item;{self.value}'
              f'\nRarity do item;{self}')

item1= Item("Sword", 200, 'common')
print(item1.name)
item1= item1.showInfo()
print(item1._Item_rarity)
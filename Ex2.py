class Player:
    def __init__(self,nome,hp,mana):
        self.__nome = nome
        self.__hp = hp
        self.__mana = mana
        self.__armor = 0

    @property
    def nome(self):
        return self.__nome
    @nome.setter
    def nome(self,novoNome):
        if novoNome != '':
            self.__nome = novoNome
    def getHP(self):
        return self.__hp

    def setHP(self, novoHP):
        if novoHP > 0:
            self.__hp = novoHP

player1= Player("Aragorn",100,10)

player1.nome = "Legolas"
print(player1.nome)
print(player1.getHP())
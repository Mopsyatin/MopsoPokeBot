from random import randint, choice
from datetime import datetime, timedelta
import requests

berries = {"Виноград":"80", "Ежевика":"120","Малина":"180","Клубника":"200", "Арбуз":"500"}

berrys = ["Малина","Клубника","Виноград","Ежевика","Арбуз"]

class Pokemon:
    pokemons = {}
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer   
        self.inventory = []
        self.pokemon_number = randint(1,1000)
        self.img = self.get_img()
        self.name = self.get_name()
        self.type = self.get_type()
        self.level = 1
        self.max_hp = self.get_hp()
        self.hp = self.max_hp
        self.power = self.get_power()
        self.xp = 0 
        self.last_feed_time = datetime.now()
        self.last_attack_time = datetime.now()
        self.last_heal_time = datetime.now()
        self.interval = self.get_speed()

        Pokemon.pokemons[pokemon_trainer] = self

    def get_speed(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['stats'][5]['base_stat']) / 2
        else:
            return 10

    def get_hp(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if isinstance(self, Wizard):
                return (data['stats'][0]['base_stat']) + 10
            else:
                return (data['stats'][0]['base_stat'])
        else:
            return 35

    def get_power(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if isinstance(self, Fighter):
                return (data['stats'][1]['base_stat']) + 5
            else:
                return (data['stats'][1]['base_stat'])
        else:
            return 55

    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['sprites']["other"]['official-artwork']["front_default"])
        else:
            return "https://i.pinimg.com/originals/bf/95/34/bf953419d76bf747cba69b55e6e03957.png"
    
    # Метод для получения имени покемона через API
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"    
    
    def get_type(self):
        list = []
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            for i in range(len(data['types'])):
                list.append(data['types'][i]['type']['name']) 

            string = ", ".join(list)

            return(string)
            
        else:
            return "Electric"

    def evolution(self):
        
        url = f'https://pokeapi.co/api/v2/pokemon-species/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            url1 = data['species']['url']
            response1 = requests.get(url1)

            if response1.status_code == 200:
                data2 = response1.json()
                url2 = data2['evolution_chain']['url']
                response2 = requests.get(url2)

                if response2.status_code == 200:         
                    data3 = response2.json()            

                    if self.name != data3['chain']['evolves_to'][0]['species']['name']:
                        url3 = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number + 1}'
                        response3 = requests.get(url3)

                        if response3.status_code == 200:
                            data4 = response3.json()
                            self.pokemon_number += 1 
                            self.img = self.get_img()
                            self.name = self.get_name()
                            self.type = self.get_type()
                            return f'''
                                    Теперь уровень твоего покемона: {self.level}
                                    Твой покемон еволюционировал!
                                    Теперь его зовут: {self.name}
                                    '''
                        else:
                            return "error"
                    else:
                        return f"Теперь уровень твоего покемона: {self.level}"
                        
                else:
                    return "error"

            else:
                return "error"
                
        else:
            return "error"
        
    def level_up(self, feed_interval = 1):
        current_time = datetime.now()  
        delta_time = timedelta(days = feed_interval)  
        if (current_time - self.last_feed_time) > delta_time:
            self.last_feed_time = current_time
            if self.level < 100:
                self.level += 1
                self.power += 2
                self.max_hp += 4
                if self.level == 16 or self.level == 36:
                    return self.evolution()
            return f"Уровень покемона увеличено. Теперь уровень твоего покемона: {self.level}"
        else:
            return f"Следующее время кормления покемона: {current_time + delta_time}"  
            
    # Метод класса для получения информации     
    def info(self):
        return f'''
        Имя твоего покеомона: {self.name},
        Типы твоего покемона: {self.type}, 
        Уровень твоего покемона: {self.level}, 
        Сила твоего покемона: {self.power},  
        Здоровье твоего покемона: {self.hp}, 
        Инвентарь твоего покемона: {self.inventory}
        '''
    
    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img

    def heal(self, feed_interval = 30):
        current_time = datetime.now()  
        delta_time = timedelta(minutes = feed_interval)  
        if (current_time - self.last_heal_time) > delta_time:
            self.hp = self.max_hp 
            self.last_heal_time = current_time
            return f"Твой покемон отхилен. Текущее здоровье: {self.hp}"
        else:
            return f"Следующее время кормления покемона: {current_time + delta_time}"   
           
    def use(self):
        used = self.inventory.pop(0)
        healed = self.hp + int(berries[used])
        if healed >= self.max_hp:
            self.hp = self.max_hp
        else:
            self.hp = healed
            
    def attack(self, enemy):
        current_time = datetime.now()  
        delta_time = timedelta(seconds = self.interval) 
        if (current_time - self.last_attack_time) > delta_time: 
            self.last_attack_time = current_time
            if isinstance(enemy, Wizard): # Проверка на то, что enemy является типом данных Wizard (является экземпляром класса Волшебник)
                chance = randint(1,5)   
                if chance == 1:
                    return 'Покемон-волшебник применил щит в сражении'
            if enemy.hp > self.power:
                enemy.hp -= self.power
                return f'''Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}
                    Здоровье покемона @{self.pokemon_trainer}: {self.hp}
                    Здоровье покемона: @{enemy.pokemon_trainer} {enemy.hp}'''
            else:
                berry = "нечего"
                enemy.hp = 0
                shance = randint(0, 9)
                if shance == 0:
                    berry = choice(berrys)
                    self.inventory.append(berry)
                if self.level > enemy.level:
                    self.xp += 100
                elif self.level == enemy.level:
                    self.xp += 200
                elif self.level < enemy.level:
                    if enemy.level - self.level == 1:
                        bust = 200
                    else:
                        bust = (enemy.level - self.level) * 100
                    self.xp += bust
                if self.xp >= 1000:
                    self.xp = 0
                    self.level += 1 
                    evo = self.evolution()
                    return f'''
                        Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}!
                        Вы получили:  {berry}
                        {evo}'''
                return f'''
                Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}!
                Вы получили:  {berry}'''
        else:
            return f"Йоу, потише твоему покемону нужен отдых"

class Fighter(Pokemon):
    def attack(self, enemy):
        super = randint(5,15)
        self.power += super
        result = super().attack(enemy)
        self.power -= super
        return result + f'\Покемон боец применил супер удар силой: {super}'

    def info(self):
        return f'''
        Имя твоего покеомона: {self.name},
        Типы твоего покемона: {self.type}, 
        Уровень твоего покемона: {self.level} 
        Сила твоего покемона: {self.power},  
        Здоровье твоего покемона: {self.hp} 
        Твой покемон: боец
        '''

class Wizard(Pokemon):
    def info(self):
        return f'''
        Имя твоего покеомона: {self.name},
        Типы твоего покемона: {self.type}, 
        Уровень твоего покемона: {self.level} 
        Сила твоего покемона: {self.power},  
        Здоровье твоего покемона: {self.hp} 
        Твой покемон: волшебник
        '''
    
                

    



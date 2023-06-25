from collections import UserDict
from collections.abc import Iterator
from datetime import date
import csv
class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value

class Name(Field):
    pass
        
class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if value.isdigit():
            self.value = value 
            

        self.record = None

    def add_to_record(self, record):
        self.record = record
        record.phones.append(self)

class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def save_to_file(self, filename):
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            for record in self.data.values():
                phones = [phone.value for phone in record.phones]
                writer.writerow([record.name.value, *phones]) 

    def load_to_file(self, filename):
        with open(filename, "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                name = Name(row[0])
                phones = [Phone(phone) for phone in row[1:]]
                record = Record(name)
                for phone in phones:
                    phone.add_to_record(record)
                self.add_record(record)

    def search_contact(self, request):
        result = []
        for contact in self.data:
            if request.lower() in self.data[contact].name.value.lower():
                result.append(contact)
        return result


    def __init__(self, phonebook=None, page_size=10):
        super().__init__()
        self.data = phonebook or {}
        self.page_size = page_size
        self.current_page = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        start = self.current_page * self.page_size
        end = start + self.page_size
        if start >= len(self.data):
            raise StopIteration
        page = list(self.data.keys())[start:end]
        self.current_page += 1
        return page   

class Record:
    def __init__(self, name=None, birthday=None):
        self.name = name
        self.birthday = birthday
        self.phones = []
    def days_to_birthday(self):
        today = date.today()
        next_birthday = date(today.year, self.birthday.month, self.birthday.day)

        if next_birthday < today:
            next_birthday = date(today.year + 1, self.birthday.month, self.birthday.day)

        days_left = (next_birthday - today).days
        print(f"До дня народження {self.name.value} залишилось {days_left} днів! ")
        return days_left

if __name__ == "__main__":
    name = Name("Dmytro")
    phone = Phone("+380500100251")

    rec = Record(name)
    phone.add_to_record(rec)

    ab = AddressBook()
    ab.add_record(rec)

    ab.save_to_file('контакти.csv')

    result = ab.search_contact("81")
    for record in result:
        if ab.request.lower() in record.name.value.lower():
            print(f"Знайден контакт: {record.name.value}")
            for phone in record.phones:
                print(f"Номер телефону: {phone.value}")
        else:
            print(f"Збігів намає, контакта з такими цифрами не існує! ")
    # ab["Bill"] = rec

    # assert isinstance(ab['Bill'], Record)
    # assert isinstance(ab['Bill'].name, Name)
    
    # print("All okay")


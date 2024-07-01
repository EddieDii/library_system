# try credit level
import sys
# create three basic classes: Book, Member, and Records
class Book:
    def __init__(self, book_id, name=None, type=None, ncopy=None, maxday=None, lcharge=None):
        # use book_id to store books, because it is unique
        self.id = book_id
        self.name = name
        self.type = type
        self.ncopy = ncopy
        self.maxday = maxday
        self.lcharge = lcharge
        self.borrow_records = {}
        self.num_days = []

    
    def add_borrow_record(self, member_id, days):
        self.borrow_records[member_id] = days

    def set_num_days(self, num_days):
        self.num_days = num_days
    
    def calculate(self):
        # calculate the number of borrow
        n_borrow = len([days for days in self.borrow_records.values() if days != 'R'])
        # calculate the number of reserve
        n_reserve = len([days for days in self.borrow_records.values() if days == 'R'])
        # get all the borrow days except 'R'
        borrow_days = [v for v in self.borrow_records.values() if v != 'R']
        # if borrow_days is true, calculate the range of days
        if borrow_days:
            day_range = f"{min(borrow_days)}-{max(borrow_days)}"
        else:
            day_range = "N/A"
        return n_borrow, n_reserve, day_range

class Member:
    def __init__(self, member_id):
        # use member_id to store members, because it is unique
        self.id = member_id

class Records:
    def __init__(self):
        #create two dicts and one list to store books, memebers and number of borrow days
        self.books = {}
        self.members= {}
        self.num_days = []  

    def read_books(self, book_file_name):
        with open(book_file_name, 'r') as file:
            for line in file:
                lines = line.strip().split(", ")
                book_id, name, type, ncopy, maxday, lcharge = lines
                self.books[book_id] = Book(book_id, name, type, int(ncopy), int(maxday), float(lcharge))

    def read_records(self, record_file_name):
        with open(record_file_name, 'r') as file:
            for line in file:
                lines = line.strip().split(", ")
                # the 0 index is book_id, the rest are member_id and days
                book_id = lines[0]
                # get book_id from books
                if book_id in self.books:
                    book = self.books[book_id]
                else:
                    book = Book(book_id)
                    self.books[book_id] = book
                # book = Book(book_id)
                # self.books[book_id] = book
                for part in lines[1:]:
                    member_id, days = part.split(": ")
                    if member_id not in self.members:
                        self.members[member_id] = Member(member_id)
                    if days != 'R': # if days is not 'R', sotre it as int
                        book.add_borrow_record(member_id, int(days)) 
                        book.set_num_days(self.num_days)
                        self.num_days.append(int(days))
                    else: # if days is 'R', store it as str
                        book.add_borrow_record(member_id, days) 

    def display_records(self): # to display the records by using the format
        print("RECORDS")
        print("-"*64)
        # every book_id gap 7 spaces
        firstline = "       ".join([f"{book.id}" for book in self.books.values()])
        print(f"| Member IDs      {firstline} |") #pirnt the first line ends with "|"
        print("-"*64)
        for member in self.members.values():
            records_line = f"| {member.id: <9}"
            for book in self.books.values():
                # if the id of member is not found, use xx to replace
                num_days = book.borrow_records.get(member.id, 'xx')
                # if num_days is 'R', use -- to replace
                display = '--' if num_days == 'R' else str(num_days)
                records_line += f"{display: >10}"
            print(records_line, "|") # print the records_line ends with "|"
        total_days = sum(self.num_days)
        # if the num_days is true, calculate the average days
        days_avg = total_days / len(self.num_days) if self.num_days else 0
        print("-"*64)
        print("RECORDS SUMMARY")
        print(f"There are {len(self.members)} members and {len(self.books)} books.")
        print(f"The average number of borrow days is {days_avg:.2f} (days).")

    def display_books(self):
        print("BOOK INFORMATION")
        print("-"*103)
        print(f"{'| Book IDs':<14}{'Name':<16}{'Type':<10}{'nCopy':>10}{'Maxday':>10}{'Lcharge':>10}{'Nborrow':>10}{'Nreserve':>11} {'  Range   |':<10}")
        print("-"*103)
        for book in self.books.values():
            n_borrow, n_reserve, day_range = book.calculate()
            if book.type == "T":
                type_name = "Textbook"
            elif book.type == "F":
                type_name = "Fiction"
            print(f"| {book.id: <12}{book.name: <16}{type_name: <10}{book.ncopy: >10}{str(book.maxday): >10}{str(book.lcharge): >10}{str(n_borrow): >10}{(n_reserve): >11}{('   '+str(day_range)): <10} |")
        print("-"*103)

if __name__ == "__main__":
    records = Records()
    if len(sys.argv) == 3:
        records.read_books(sys.argv[2])
        records.read_records(sys.argv[1])
        records.display_records()                                                                                                                                                                                             
        records.display_books()
    elif len(sys.argv) == 2:
        records.read_records(sys.argv[1])
        records.display_records()
    else:
        print("Usage: python my_record.py <your_record_file> [<your_book_file>]")


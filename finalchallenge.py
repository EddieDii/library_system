#pass level: 100%
import sys
# create three basic classes: Book, Member, and Records
class Book:
    def __init__(self, book_id):
        # use book_id to store books, because it is unique
        self.id = book_id
        self.borrow_records = {}
    
    def add_borrow_record(self, member_id, days):
        self.borrow_records[member_id] = days

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

    def read_records(self, record_file_name):
        with open(record_file_name, 'r') as file:
            for line in file:
                lines = line.strip().split(", ")
                # the 0 index is book_id, the rest are member_id and days
                book_id = lines[0]
                # store book_id as a key of books dict
                book = Book(book_id)
                self.books[book_id] = book
                for part in lines[1:]:
                    member_id, days = part.split(": ")
                    if member_id not in self.members:
                        self.members[member_id] = Member(member_id)
                    if days != 'R': # if days is not 'R', sotre it as int
                        book.add_borrow_record(member_id, int(days)) 
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
                if num_days == 'R':
                    records_line += f"{'--': >10}"
                else:
                    records_line += f"{str(num_days): >10}"
            print(records_line, "|") # print the records_line ends with "|"
        total_days = sum(self.num_days)
        # if the num_days is true, calculate the average days
        days_avg = total_days / len(self.num_days) if self.num_days else 0
        print("-"*64)
        print("RECORDS SUMMARY")
        print(f"There are {len(self.members)} members and {len(self.books)} books.")
        print(f"The average number of borrow days is {days_avg:.2f} (days).")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python my_record.py <records.txt>")
    else:
        records = Records()
        records.read_records(sys.argv[1])
        records.display_records()
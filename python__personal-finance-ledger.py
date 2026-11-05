from datetime import datetime ###generate by chatgpt###
from sqlalchemy.orm import sessionmaker ###generate by chatgpt###
from sqlalchemy import create_engine, Column, Integer, String, Date, Numeric, Text, DateTime, func ###generate by chatgpt###
from sqlalchemy.ext.declarative import declarative_base ###generate by chatgpt###
import matplotlib.pyplot as plt
import os

# Database Configuration
class Config: 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///accounting.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
###generate by chatgpt###

# Initialize Database Connection
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
###generate by chatgpt###

# Define Record Model
Base = declarative_base()

class Record(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    type = Column(String(20), nullable=False)  # 'income' or 'expense'
    category = Column(String(50), nullable=False)
    name = Column(String(100), nullable=True)
    note = Column(Text)
    created_at = Column(DateTime, default=func.now())

# Create table in the accounting.db document
Base.metadata.create_all(engine) ###generate by chatgpt###



# Create a 'reports' folder ###generate by AI######
if not os.path.exists('reports'):
    os.makedirs('reports') 
    

# Implementation code for various functions
def add_record():
    print("=== Add Record ===")
    date_str = input("Enter date (YYYY-MM-DD): ")
    amount = float(input("Enter amount: "))
    record_type = input("Enter type (income/expense): ").strip().lower()
    category = input("Enter category: ").strip()
    name = input("Enter name: ").strip()
    note = input("Enter note (optional): ").strip()
    date = datetime.strptime(date_str, '%Y-%m-%d').date() ## BY AI this row####

    record = Record(date=date,
                    amount=amount,
                    type=record_type,
                    category=category,
                    name=name,
                    note=note)
    session.add(record) 
    session.commit() 
    print("Record added: " + str(record))

def delete_record():
    print("=== Delete Record ===")
    record_id = int(input("Enter record ID to delete: "))
    record = session.query(Record).get(record_id) ########generate by AI#########
    if not record:
        print(f"No record found with ID {record_id}")
        return
    session.delete(record)
    session.commit()
    print("Successfully deleted record with ID " + str(record_id) + ".")

def edit_record():
    print("=== Edit Record ===")
    record_id = int(input("Enter record ID to edit: "))
    record = session.query(Record).get(record_id)
    if not record:
        print("No record found with ID " + str(record_id))
        return

    new_date = input("Enter new date (YYYY-MM-DD, current: " + str(record.date) + "): ").strip()
    new_amount = input("Enter new amount (current: " + str(record.amount) + "): ").strip()
    new_type = input("Enter new type (income/expense, current: " + str(record.type) + "): ").strip()
    new_category = input("Enter new category (current: " + str(record.category) + "): ").strip()
    new_name = input("Enter new name (current: " + str(record.name) + "): ").strip()
    new_note = input("Enter new note (current: " + str(record.note) + "): ").strip()

    if new_date:
        record.date = datetime.strptime(new_date, '%Y-%m-%d').date()
    if new_amount:
        record.amount = float(new_amount)
    if new_type:
        record.type = new_type
    if new_category:
        record.category = new_category
    if new_name:
        record.name = new_name
    if new_note:
        record.note = new_note

    session.commit()
    print("Record with ID " + str(record_id) + " updated.")

def view_records():
    print("=== View Records ===")
    records = session.query(Record).order_by(Record.date.desc()).all() ### generate by AI##
    if not records:
        print("No records found.")
        return

    for record in records:
        print("ID: " + str(record.id) +
              ", Date: " + str(record.date) +
              ", Amount: " + str(record.amount) +
              ", Type: " + record.type +
              ", Category: " + record.category +
              ", Name: " + record.name +
              ", Note: " + (record.note if record.note else "None"))
        
def report():
    print("=== Report ===")
    records = session.query(Record).all()
    if not records:
        print("No records found.")
        return

    total_income = 0
    total_expense = 0

    for record in records:
        if record.type == 'income':
            total_income += record.amount
        elif record.type == 'expense':
            total_expense += record.amount

    print("Total Income: " + str(total_income))
    print("Total Expense: " + str(total_expense))
    print("Net Balance: " + str(total_income - total_expense))

    category_stats = {}
    for record in records:
        if record.category not in category_stats:
            category_stats[record.category] = {'income': 0, 'expense': 0}
        if record.type == 'income':
            category_stats[record.category]['income'] += record.amount
        elif record.type == 'expense':
            category_stats[record.category]['expense'] += record.amount
    

    # Draw a bar chart of income and expenses
    categories = list(category_stats.keys())
    incomes = [category_stats[cat]['income'] for cat in categories]
    expenses = [category_stats[cat]['expense'] for cat in categories]
    
    plt.figure(figsize=(10, 6)) ####this row generate by AI###
    bar_width = 0.4
    x = range(len(categories))
    plt.bar(x, incomes, width=bar_width, label='Income', color='green')
    plt.bar([i + bar_width for i in x], expenses, width=bar_width, label='Expense', color='red')
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Amount', fontsize=12)
    plt.title('Category Statistics', fontsize=16)
    plt.xticks([i + bar_width / 2 for i in x], categories, rotation=45)
    plt.legend()
    plt.tight_layout() ####this row generate by AI###

    # Save the image ##### this part generated by AI#####
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    category_plot_path = os.path.join('reports', f'category_report_{timestamp}.png')
    plt.savefig(category_plot_path)
    plt.close()

    print(f"Category statistics saved as {category_plot_path}.")

    # Analyze income and expense trends by date
    date_stats = {}
    for record in records:
        if record.date not in date_stats:
            date_stats[record.date] = {'income': 0, 'expense': 0}
        if record.type == 'income':  
            date_stats[record.date]['income'] += record.amount
        elif record.type == 'expense':
            date_stats[record.date]['expense'] += record.amount
            
    dates = list(date_stats.keys())
    dates.sort() ##this row Generated by AI############

    income_trends = []
    expense_trends = []

    for date in dates:
        income_trends.append(date_stats[date]['income'])
        expense_trends.append(date_stats[date]['expense'])

    plt.figure(figsize=(10, 6))
    plt.plot(dates, income_trends, label='Income', color='green', marker='o')
    plt.plot(dates, expense_trends, label='Expense', color='red', marker='o')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Amount', fontsize=12)
    plt.title('Trends Over Time', fontsize=16)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    # Save the image #####generated by AI this part####    
    trends_plot_path = os.path.join('reports', f'trends_report_{timestamp}.png')
    plt.savefig(trends_plot_path)
    plt.close()

    print(f"Trends report saved as {trends_plot_path}.")

# Main program entry point
def main():
    while True:
        print("\n=== Accounting System ===")
        print("1. Add Record")
        print("2. Delete Record")
        print("3. Edit Record")
        print("4. View Records")
        print("5. Report")
        print("0. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            add_record()
        elif choice == '2':
            delete_record()
        elif choice == '3':
            edit_record()
        elif choice == '4':
            view_records()
        elif choice == '5':
            report()
        elif choice == '0':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()

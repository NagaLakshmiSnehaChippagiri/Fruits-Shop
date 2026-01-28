import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",   # change before running
    database="fruit_shop"
)

cursor = db.cursor()
print("Connected to Fruit Shop Database!")

cursor.execute("INSERT INTO bills (bill_date, total_amount) VALUES (CURDATE(), 0)")
db.commit()
bill_id = cursor.lastrowid

total_bill = 0
bill_items = []

while True:
    cursor.execute(
        "SELECT fruit_id, fruit_name, price_per_kg, stock_kg FROM fruits WHERE stock_kg > 0"
    )
    fruits = cursor.fetchall()

    if not fruits:
        print("No fruits available!")
        break

    print("\nAvailable Fruits")
    print("----------------------")
    for fruit in fruits:
        print(f"ID:{fruit[0]} {fruit[1]} ₹{fruit[2]}/kg Stock:{fruit[3]}kg")

    try:
        fruit_id = int(input("\nEnter Fruit ID to buy: "))
    except ValueError:
        print("Invalid input.")
        continue

    cursor.execute(
        "SELECT fruit_name, price_per_kg, stock_kg FROM fruits WHERE fruit_id=%s",
        (fruit_id,)
    )
    fruit = cursor.fetchone()

    if not fruit:
        print("Invalid Fruit ID!")
        continue

    fruit_name, price, stock = fruit

    try:
        weight = float(input(f"Enter quantity of {fruit_name} (kg): "))
        if weight > stock:
            print("Not enough stock!")
            continue
    except ValueError:
        print("Invalid quantity.")
        continue

    item_total = weight * float(price)
    total_bill += item_total

    bill_items.append((fruit_name, weight, price, item_total))

    cursor.execute("""
        INSERT INTO bill_items (bill_id, fruit_id, weight_kg, price_per_kg, item_total)
        VALUES (%s, %s, %s, %s, %s)
    """, (bill_id, fruit_id, weight, price, item_total))

    cursor.execute(
        "UPDATE fruits SET stock_kg = stock_kg - %s WHERE fruit_id = %s",
        (weight, fruit_id)
    )
    db.commit()

    more = input("Add more fruits? (y/n): ").lower()
    if more != 'y':
        break

cursor.execute(
    "UPDATE bills SET total_amount=%s WHERE bill_id=%s",
    (total_bill, bill_id)
)
db.commit()

print("\n----- FINAL BILL -----")
for i, item in enumerate(bill_items, 1):
    print(f"{i}. {item[0]} - {item[1]}kg x ₹{item[2]} = ₹{item[3]:.2f}")

print("---------------------")
print(f"TOTAL: ₹{total_bill:.2f}")
print("---------------------")

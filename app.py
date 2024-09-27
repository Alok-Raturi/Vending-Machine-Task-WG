import yaml

prompt="""
Press 1 to display available items
Press 2 to select an item
Press 3 to exit
"""

prompt_selection = """
Press 1 buy it
Press 2 to go back 
Press 3 to exit program
"""

prompt_after_update = """
Press 1 for continue shopping
Press 2 for exit
"""

class DBops:
    def __init__(self,file):
        self.file=file

    def read_data(self):
        with open(self.file,"r") as file:
            data = yaml.safe_load(file)
        return data

    def write_data(self,data):
        with open(self.file,"w") as file:
            yaml.dump(data,file)


class VendingMachine:
    def __init__(self,db):
        self.Db = db

    def display_items(self):
        data = self.Db.read_data()
        for d in data:
            print(f"""
            id = {d['id']} --  name = {d['name']} --  price = {d['price']}  --  quantity = {d['quantity']}
            """)

    def select_items(self):
        data = self.Db.read_data()
        sel_id = input("Enter the id of the product you want to buy : ").strip()
        all_ids = [d['id'] for d in  data]
        product = [d for d in data if d['id']==sel_id]

        if sel_id not in all_ids:
            print("--------------------   Id is not valid   --------------------------- ")
            return
        else:
            print(f"""
            id = {product[0]['id']} --  name = {product[0]['name']} --  price = {product[0]['price']}  --  quantity = {product[0]['quantity']}
            """)
            self.selection(product,sel_id,data)

    def selection(self,product,sel_id,data):
        while True:
            print(prompt_selection)
            ch = input("Enter your choice : ")
            if ch == '1':
                money = float(input("Enter the money you want to insert : "))
                if money >= float(product[0]['price']):
                    self.buy_item(sel_id, money, data)
                    return
                else:
                    print("-----------------------------------   Insert more money   --------------------------------")
                    return
            elif ch == '2':
                break
            elif ch == '3':
                exit(0)
            else:
                print("Invalid Choice")

    def buy_item(self,sel_id,money,data):
        product = [d for d in data if d['id']==sel_id]
        if product[0]['quantity'] >= 1:
            self.dispense_item(sel_id,data)
            print(f"Your remaining money ${money - float(product[0]['price'])} will be stored in your wallet")
            return
        else:
            print("-----------------   Sorry,this item is not available in appropriate quantity -----------------------------")

    def dispense_item(self,sel_id,data):
        for d in data:
            if d['id']==sel_id:
                d['quantity']-=1
        self.Db.write_data(data)
        self.update_inventory()

    def update_inventory(self):
        data = self.Db.read_data()
        data = [d for d in data if d['quantity'] != 0]
        self.Db.write_data(data)
        while True:
            print(prompt_after_update)
            ch = input("Enter your choice : ")
            if ch == '1':
                return
            elif ch == '2':
                print("Thank you")
                exit(0)
            else:
                print("Invalid Choice")


if __name__ == "__main__":
    Db = DBops('./data/data.yaml')
    VM = VendingMachine(Db)
    while True:
        print(prompt)
        choice = input("Enter your choice : ")
        if choice=='1':
            VM.display_items()
        elif choice=='2':
            VM.select_items()
        elif choice=='3':
            break
        else:
            print("Invalid choice, try again")
    print("Thank you.")


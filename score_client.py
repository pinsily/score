import json

import requests


class Client:
    # Init function to set required class variables
    def __init__(self):
        self.session = requests.Session()
        # self.base_url = "http://127.0.0.1:8000/"
        self.base_url = "https://1001james.pythonanywhere.com/"
        self.json_headers = {'content-type': 'application/json'}
        self.form_headers = {'content-type': 'application/x-www-form-urlencoded'}
        self.category_list = ['tech', 'pol', 'art', 'trivia']
        self.region_list = ['uk', 'w', 'eu']

    def register(self):
        username = input("username: ").strip()
        email = input("email: ").strip()
        password = input("password: ").strip()

        data = {"username": username, "password": password, "email": email}

        response = self.session.post(f'{self.base_url}api/register/',
                                     data=data, headers=self.form_headers, timeout=10)

        if response.json():
            print(f"register res: {response.json().get('msg')}")

    def login(self):
        """
        login
        """
        username = input("username: ").strip()
        password = input("password: ").strip()
        print("logging In....")
        data = {'username': username, 'password': password}

        response = self.session.post(self.base_url + "api/login/", data=data, headers=self.form_headers, timeout=4)

        if response.json():
            print(f"login res: {response.json().get('msg')}")

    def logout(self):
        """
        logout
        """
        print("\nLoggin out....")

        response = self.session.post(self.base_url + "api/logout/", timeout=10)

        if response.json():
            print(f"login res: {response.json().get('msg')}")

    def list(self):
        """
        list all module
        """
        response = self.session.get(self.base_url + "api/module_list/", data=json.dumps({}), headers=self.form_headers,
                                    timeout=10)

        if response.status_code == 200:
            self.print_module_table(response.json())
        elif response.json():
            print(f"{response.json().get('msg')}")
        else:
            print("--- list nothing!")

    def professor(self):
        """
        list all professor
        """
        response = self.session.get(self.base_url + "api/professor_list/", data=json.dumps({}),
                                    headers=self.form_headers,
                                    timeout=10)

        if response.status_code == 200:
            self.print_professor_table(response.json())
        elif response.json():
            print(f"{response.json().get('msg')}")
        else:
            print("--- list nothing!")

    def view(self):
        """
        list all professor rating
        """
        response = self.session.get(self.base_url + "api/view/", data=json.dumps({}),
                                    headers=self.form_headers,
                                    timeout=10)

        if response.status_code == 200:
            res = response.json()
            for record in res.get("views"):
                print(f"The rating of Professor {record.get('professor_name')} ({record.get('professor_code')}) "
                      f"in {record.get('module_name')} is {record.get('score')}")
        elif response.json():
            print(f"{response.json().get('msg')}")
        else:
            print("--- list nothing!")

    def average(self, command):
        if len(command) != 3:
            print("--- Command missing arguments!")
            return
        professor_code, module_code = command[1:]
        data = {
            "professor_code": professor_code,
            "module_code": module_code,
        }

        response = self.session.get(self.base_url + "api/average/", data=json.dumps(data), headers=self.form_headers,
                                    timeout=10)

        if response.status_code == 200:
            res = response.json()
            print(f"The rating of Professor {res.get('professor_name')} ({res.get('professor_code')}) "
                  f"in module {res.get('module_name')} ({res.get('module_code')}) is {res.get('average')}")
        elif response.json():
            print(f"--- rating res: {response.json().get('msg')}")
        else:
            print("Rating fail, try again!")

    def rate(self, command):
        """
        rate [professor_code] [module_code] [year] [semester] [rating(1-5)]
        """
        # check
        if len(command) != 6:
            print("--- Command missing arguments!")
            return
        professor_code, module_code, year, semester, rating = command[1:]
        if not year.isdigit() or not semester.isdigit() or not rating.isdigit():
            print("--- The year, semester, rating must be int!")
            return
        if int(rating) > 5 or int(rating) < 1:
            print("--- The rating must be between 1 and 5")
            return

        data = {
            "professor_code": professor_code,
            "module_code": module_code,
            "year": year,
            "semester": semester,
            "rating": rating,
        }

        response = self.session.get(self.base_url + "api/rating/", data=json.dumps(data), headers=self.form_headers,
                                    timeout=10)

        if response.json():
            print(f"--- rating res: {response.json().get('msg')}")
        else:
            print("Rating fail, try again!")

    def show(self):
        """
        print command menu
        """
        print("\n\t\t\t\t\t\t\tWelcome To News Sysyem")
        print("-" * 85)
        print("--> register")
        print("--> login")
        print("--> logout")
        print("--> professor")
        print("--> list")
        print("--> view")
        print("--> average [professor_code] [module_code]")
        print("--> rate [professor_code] [module_code] [year] [semester] [rating(1-5)]")
        print("--> exit")
        print("--> show")
        print("-" * 85)

    def exit(self):
        exit(0)

    def run_server(self):
        """
        start service
        """
        self.show()
        while True:
            prompt = ">>>"
            command = input(prompt).strip().split()

            if not command:
                continue

            command_name = command[0]

            try:
                handler = self.__getattribute__(command_name)
            except AttributeError:
                print("the command is invalid, please try again!")
                continue
            if command_name in ["rate", "average"]:
                handler(command)
            else:
                handler()

    def print_module_table(self, modules):
        print("{:<8} {:<15} {:<30} {:<15} {:<15} {:<15}"
              .format('Index', 'Code', 'Name', 'Year', 'Semester', 'Taught by'))

        for module in modules["modules"]:
            print("{:<8} {:<15} {:<30} {:<15} {:<15} {:<15}"
                  .format(module["index"], module["code"], module["name"],
                          module["year"], module["semester"], module["professor"]))

    def print_professor_table(self, professors):
        print("{:<8} {:<8} {:<15}"
              .format('Id', 'Code', 'Name'))

        for professor in professors["professors"]:
            print("{:<8} {:<8} {:<15}".format(professor["index"], professor["code"], professor["name"]))


if __name__ == "__main__":
    """
    start client progress
    """
    Client().run_server()

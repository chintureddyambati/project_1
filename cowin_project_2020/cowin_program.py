import requests
import json
import hashlib
from configparser import ConfigParser


class Cowin:
    def __init__(self):
        self.txnId = ''

    def cowin_config(self, section, option):
        config = ConfigParser()
        config.read('cowin_config_file.txt')
        return config.get(section=section, option=option)

    # proccess of genrate the otp using mobile number
    def gen(self):
        try:
            url = f"{self.cowin_config(section='cowin_url', option='base_url')}{self.cowin_config(section='cowin_url', option='otp_gen_url')}"
            payload = json.dumps({
                "mobile": input("enter your mobile number___ ")
            })
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'PostmanRuntime/7.28.0'
            }
            response = requests.post(url, headers=headers, data=payload)
            print(response.json())
            txnId_json = response.json()
            self.txnId = txnId_json["txnId"]
        except ValueError:
            print('the otp was send by the mobile number and it is valid for 3 minits and next otp come after 3 minits')

    # using the otp and txnId to get the proper authentication
    def confirm(self):
        otp = input("enter your otp__ ")
        result = hashlib.sha256(otp.encode())
        res = (result.hexdigest())
        url = f"{self.cowin_config(section='cowin_url', option='base_url')}{self.cowin_config(section='cowin_url', option='otp_conf_url')}"
        payload = json.dumps({
            "otp": res,
            "txnId": self.txnId
        })
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'PostmanRuntime/7.28.0'
        }
        response = requests.post(url, headers=headers, data=payload)
        print(response.text)
        # output = response.text
        # here the main function starts
        if response.status_code == 200:
            print("success otp is valid")
            self.engine()

        else:
            print('your otp is not valid please provide valid otp')

    # find the states and state_id
    def states_data(self):
        url = f"{self.cowin_config(section='cowin_url', option='base_url')}{self.cowin_config(section='cowin_url', option='states_data_url')}"
        payload = ''
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'PostmanRuntime/7.28.0'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        vale = response.json()
        states = vale["states"]
        for i in states:
            print(i)
            print('\n=============================================\n')

    # find the disrticts and district_id
    def district_data(self):

        state_id = input('enter your state id----- ')
        url = f"{self.cowin_config(section='cowin_url', option='base_url')}{self.cowin_config(section='cowin_url', option='district_data_url').replace('{state_id}', state_id)}"
        payload = ''
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'PostmanRuntime/7.28.0'
        }
        response = requests.get(url, headers=headers, data=payload)
        var = response.json()
        output = var['districts']
        for i in output:
            print(i)
            print('\n==============================================\n')

    # use to pincode data to find the vaccination centers and availability of vaccination
    def pincode_data(self):
        try:
            pincode = input('enter your pincode-- ')
            date = input('enter your date_____ ')
            url = f"{self.cowin_config(section='cowin_url', option='base_url')}{self.cowin_config(section='cowin_url', option='pincode_data_url').replace('{pincode}', pincode).replace('{date}', date)}"
            payload = ''
            headers = {
                'Accept-Language': 'te_IN',
                'User-Agent': 'PostmanRuntime/7.28.0'
            }
            response = requests.get(url, headers=headers, data=payload)
            output = response.json()
            result = output['sessions']
            for i in result:
                print(i)
                print('\n======================================\n')
        except KeyError:
            print('it is not a valid pincode please provide valid pincode')

    # use the district_id to find the vaccination centers and availability of vaccination dates
    def district_id_data(self):
        try:
            district_id = input('enter your district_id ------ ')
            date = input('enter your date to go vaccination-- ')
            url = f"{self.cowin_config(section='cowin_url', option='base_url')}{self.cowin_config(section='cowin_url', option='district_id_url').replace('{district_id}', district_id).replace('{date}', date)}"
            payload = ''
            headers = {
                'Accept-Language': 'te_IN',
                'User-Agent': 'PostmanRuntime/7.28.0'
            }
            response = requests.get(url, headers=headers, data=payload)
            try:
                result = response.json()
                output = result['sessions']
                for i in output:
                    print(i)
                    print('\n======================================================\n')
            except IndexError:
                print('in the given district_id temperarly unavilabule their is no any vaccination proccess')
        except KeyError:
            print('it was not a valid district_id please provide valid district_id')

    # use latitude ang lagitude value to find the vaccination centers
    def lat_long_data(self):
        try:
            lat = input('enetr your latitude value--- ')
            long = input('enter your longitude value--- ')
            url = f"{self.cowin_config(section='cowin_url', option='base_url')}{self.cowin_config(section='cowin_url', option='lat_long_url').replace('{lat}', lat).replace('{long}', long)}"
            payload = {}
            headers = {
                'Accept-Language': 'te_IN',
                'User-Agent': 'PostmanRuntime/7.28.0'
            }
            response = requests.get(url, headers=headers, data=payload)
            try:
                output = response.json()
                result = output['centers']
                for i in result:
                    print(f'center_id = {i["center_id"]}')
                    print(f'name = {i["name"]}')
                    print(f'district_name = {i["district_name"]}')
                    print(f'state_name = {i["state_name"]}')
                    print(f'location = {i["location"]}')
                    print(f'pincode = {i["pincode"]}')
                    print(f'latitude = {i["lat"]}')
                    print(f'longitude = {i["long"]}')
                    print('\n======================================================\n')
            except ValueError:
                print('it is not a valid value or complete value please provide complete lat and long value')
        except KeyError:
            print('it is not a correct lat and long values provide correct lat long values')

    # use calenderbypin method get the which date is vaccination process available
    def calender_by_pin_data(self):
        try:
            pincode = input('enter your pincode-- ')
            date = input('enter your date---- ')
            url = f"{self.cowin_config(section='cowin_url', option='base_url')}{self.cowin_config(section='cowin_url', option='calender_by_pin_url').replace('{pincode}', pincode).replace('{date}', date)}"
            payload = {}
            headers = {
                'Accept-Language': 'te_IN',
                'User-Agent': 'PostmanRuntime/7.28.0'
            }
            response = requests.request("GET", url, headers=headers, data=payload)

            res = response.json()
            output = (res['centers'])
            for i in output:
                print(i)
                print('\n=====================================================\n')
        except KeyError:
            print('provided pincode is invalid (or) it is tempararly unavilabule')

    # get the vaccintation centers using center id
    def calander_by_center_id(self):
        id = input('enter your center_id ___ ')
        date = input('enter your date___ ')
        url = f"{self.cowin_config(section='cowin_url', option='base_url')}{self.cowin_config(section='cowin_url', option='calender_by_center_id_url').replace('{id}', id).replace('{date}', date)}"
        payload = {}
        headers = {
            'Accept-Language': 'hi_IN',
            'User-Agent': 'PostmanRuntime/7.28.0'
        }
        response = requests.get(url, headers=headers, data=payload)
        output = response.json()
        print(output)

    # use district_id get the vacination center details
    def calander_by_district_id(self):
        id = input('enter your district_id--- ')
        date = input('enter your date----- ')
        url = f"{self.cowin_config(section='cowin_url', option='base_url')}{self.cowin_config(section='cowin_url', option='calender_by_district_id_url').replace('{id}', id).replace('{date}', date)}"
        payload = {}
        headers = {
            'Accept-Language': 'hi_IN',
            'User-Agent': 'PostmanRuntime/7.28.0'
        }
        response = requests.get(url, headers=headers, data=payload)
        output = (response.json())
        result = output['centers']
        for i in result:
            data = print(i)
            self.data = data
            print('\n===================================================\n')

    def engine(self):
        while True:
            print('welcome to the cowin_server')
            print('1.states_data', '2.district_data', '3.pincode_data', '4.district_id_data', '5.lat_long_data',
                  '6.calender_by_pin_data', '7.calander_by_center_id', '8.calander_by_district_id', sep='\n')
            choice = input('enter your choice___ ')
            if choice == '1':
                print('in this choice you get the states and state_id')
                self.states_data()
            elif choice == '2':
                print('in this choice you get the district_names and district_ids')
                self.district_data()
            elif choice == '3':
                print('in this choice you get the vaccination_centers')
                self.pincode_data()
            elif choice == '4':
                print('in this session you get the vaccination centers and avilability dates')
                self.district_id_data()
            elif choice == '5':
                print('get the vacination centers addresss')
                self.lat_long_data()
            elif choice == '6':
                print('get the vaccination centers and availbility')
                self.calender_by_pin_data()
            elif choice == '7':
                print('use center id get the vaccination centers ')
                self.calander_by_center_id()
            elif choice == '8':
                print(' in this choice use district_id get the center details ')
                self.calander_by_district_id()
            else:
                print('it is not a valid choice please select valid choice....')
            decision = input('do you want to continue[Y/N]__')
            if decision == 'Y' or decision == 'y':
                continue
            elif decision == 'N' or decision == 'n':
                print('### please wear a mask and maintain social distance ###')
                break
            else:
                print('it is not a valid choice pleace select yes or no ')


c = Cowin()
c.gen()
c.confirm()

from datetime import datetime
import requests
import subprocess
import json
import time
import os


def entrypoint():
    input_file = open('input.json', 'r')
    input_data = json.load(input_file)
    input_file.close()

    today = datetime.today().strftime('%d-%m-%Y')
    get_centres(today, int(input_data["age"]), input_data["state_name"], input_data["district_name"])


def get_centres(date, age, state_name, district_name):
    district_id = get_state_id(state_name, district_name)
    try:
        response = requests.get(
            "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict",
            params={
                'district_id': district_id,
                'date': date
            },
            headers={"User-Agent": "Chrome"}
        )
        total_available_centres = 0
        total_available_slots = 0
        available_centres = list()
        for centre in response.json()["centers"]:
            pin = centre["pincode"]
            for details in centre["sessions"]:
                if details['available_capacity'] > 0 and details["min_age_limit"] <= age:
                    total_available_slots += details['available_capacity']
                    available_centres.append(centre['name']+": ( {} @ {} )".format(details['available_capacity'], pin))
                    total_available_centres += 1
        if total_available_centres > 0:
            current_time = datetime.now().strftime("%H:%M:%S")
            print("At {}, {} slots on {} centres: {}".format(current_time, total_available_slots,
                                                             total_available_centres, available_centres))
            html_head = 'Vaccines are now available in {}, for {} years, in the next 7 days.'.format(district_name, age)
            html_template = "<html><body><h1>{}</h1>" \
                            "<h3>There are {} centres with {} available total slots.</h3>" \
                            "<p><b>Centres:</b> {}</p></body></html>"\
                .format(html_head, total_available_centres, total_available_slots, available_centres)
            open_browser(html_template)
            time.sleep(5)
    except Exception as err:
        log_file = open(error_file, 'w+')
        log_file.write(str(err)+"\n")


def get_state_id(state_name, district_name):
    try:
        unchanged_states = ["Andaman and Nicobar Islands", "Dadra and Nagar Haveli", "Daman and Diu",
                            "Jammu and Kashmir"]
        if state_name not in unchanged_states:
            state_name = state_name.title()
        response = requests.get(
            "https://cdn-api.co-vin.in/api/v2/admin/location/states",
            headers={"User-Agent": "Chrome"}
        )
        states = response.json()['states']
        state_id = next(item for item in states if item["state_name"] == state_name)['state_id']
        district_id = get_district_id(state_id, district_name)
        return district_id
    except Exception as err:
        log_file = open(error_file, 'w+')
        log_file.write(str(err)+"\n")


def get_district_id(state_id, district_name):
    try:
        district_url = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/{0}".format(str(state_id))
        response = requests.get(district_url, headers={"User-Agent": "Chrome"})
        districts = response.json()['districts']
        district_id = next(item for item in districts if item["district_name"] == district_name.capitalize())[
            'district_id']
        return district_id
    except Exception as err:
        log_file = open(error_file, 'w+')
        log_file.write(str(err)+"\n")


def open_browser(html_template):
    f = open(html_file, 'w+')
    f.write(html_template)
    f.close()

    cowin_url = "https://selfregistration.cowin.gov.in/"

    subprocess.call(['open', cowin_url])
    subprocess.call(['open', html_file])


project_dir = "covid-vaccine-notifier-browser"
if project_dir in os.getcwd():
    current_path = os.getcwd()
else:
    current_path = os.path.abspath(project_dir)

error_file = os.path.join(current_path, "errors.txt")
html_file = os.path.join(current_path, "index.html")

entrypoint()

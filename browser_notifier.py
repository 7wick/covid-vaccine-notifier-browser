from datetime import datetime
import requests
import subprocess
import json


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
        for centre in response.json()["centers"]:
            for details in centre["sessions"]:
                if details['available_capacity'] > 0 and details["min_age_limit"] <= age:
                    total_available_centres += 1
        if total_available_centres > 0:
            html_head = 'Vaccines available now in this district, for the given age, in the next 7 days.'
            html_template = "<html><body><h1>{}</h1><h3>Total available centres: {}</h3></body></html>".format(
                html_head, total_available_centres)
            open_browser(html_template)
    except Exception as err:
        log_file = open('/Users/saatwick.chandra/PycharmProjects/covid-vaccine-notifier-browser/errors.txt', 'w+')
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
        log_file = open('/Users/saatwick.chandra/PycharmProjects/covid-vaccine-notifier-browser/errors.txt', 'w+')
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
        log_file = open('/Users/saatwick.chandra/PycharmProjects/covid-vaccine-notifier-browser/errors.txt', 'w+')
        log_file.write(str(err)+"\n")


def open_browser(html_template):
    f = open('/Users/saatwick.chandra/PycharmProjects/covid-vaccine-notifier-browser/index.html', 'w+')
    f.write(html_template)
    f.close()

    html_file = '/Users/saatwick.chandra/PycharmProjects/covid-vaccine-notifier-browser/index.html'
    cowin_url = "https://selfregistration.cowin.gov.in/"

    subprocess.call(['open', cowin_url])
    subprocess.call(['open', html_file])


entrypoint()
import json
# from functools import cache

import requests

with open('./static/location_data.json', 'r', encoding="UTF-8") as base:
    json_data = json.load(base)


# @cache
def get_locations(do="강원"):
    countries = list()
    countries = json_data["do"][do]
    print(countries)
    return countries


# 시명 기준 으로 데이터 가져오기
# @cache
def get_list_by_location(city):
    location_code = json_data['code'][city]
    return find_by_code(location_code)


# 해당 도 하위 시 데이터 모두 가져오기
# @cache
def get_main_list(do="강원"):
    results_main = list()
    base_code = list()

    countries = json_data["do"][do]
    for country in countries:
        codes = json_data["code"][country]
        base_code += codes

    results = find_by_code(base_code)

    return results


# 해변 코드로 기상 정보 가져오기
def find_by_code(location_code):
    results = list()
    for code in location_code:
        params = {
            "ServiceKey": "nB8EIND5cjQ8UsOhFLrjFg==",
            "BeachCode": code,
            "ResultType": json

        }
        response = requests.get(
            "http://www.khoa.go.kr/api/oceangrid/beach/search.do", params=params)
        json_respo = response.json().get("result")
        beach_name = json_respo.get('meta').get('beach_name')
        base_info = json_respo.get("data")[0]

        if 'wind_speed' in base_info and 'water_temp' in base_info:
            base_info['beach'] = beach_name
            results.append(base_info)

    return results


# if __name__ == "__main__":
#     get_locations()

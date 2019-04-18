# import necessary libraries
from bs4 import BeautifulSoup
import requests
import pprint
import json
import pymongo
from sqlalchemy import func
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# create route that renders index.html template
@app.route("/")
def home():
    # print('Default route')
    return render_template("index.html")


# Query the database and send the jsonified results
# @app.route("/send", methods=["GET", "POST"])
# def send():
#     # print('send function')
#     addressline1 = request.args.get("addressLine1")
#     addressline2 = request.args.get("addressLine2")
#     zipcode = request.args.get("zipcode")
#     cuisine = request.args.get("cuisine")
#     geo_list = []    
#     geo_list = api_scrape(addressline1, addressline2, zipcode, cuisine)
#     print(geo_list)
#     return jsonify(geo_list)


# @app.route("/api/hist")
# def hist_search():
#     print('hist_search method')
#     results = db.session.query(Hist.addressline1, Hist.addressline2, Hist.zipcode, Hist.cuisine).all()
    
#     hist_data = [{
#         "addressline1": results[0],
#         "addressline2": results[1],
#         "zipcode": results[2],
#         "cuisine": results[3]    
#     }]

#     return jsonify(hist_data)

@app.route("/apiScrape/<addressline1>/<addressline2>/<zipcode>/<cuisine>")
def api_scrape(addressline1, addressline2, zipcode, cuisine):
    search_result_list = []
    base_url = 'https://www.yelp.com/search?find_desc='
    location= 'find_loc='
    url = base_url + cuisine + '&' + location + str(zipcode) + '&ns=1'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    results_main = soup.find_all('div', class_='largerScrollablePhotos__373c0__3FEIJ')
    counter = 0
    for result in results_main:
        main = result.find('div', class_='mainAttributes__373c0__1r0QA')
    
        if (main):
            main2 = main.find('div', class_= 'lemon--div__373c0__1mboc')
            main3 = main2.find('div', class_= 'lemon--div__373c0__1mboc')
            if (main3.a["href"].find("adredir?") == 1):
                pass
            else:
                counter += 1
                search_result = {}
                href = main2.find('a', class_='lemon--a__373c0__IEZFH')["href"]
                rest = main3.find('a').text
                search_result["resteraunt"] = rest
                search_result["address_url"] = f'https://www.yelp.com{href}'
                search_result_list.append(search_result)
                if (counter >= 10):
                    break

    search_result = []
    counter = 0
    for result in search_result_list:
        results = {}
        response = requests.get(result["address_url"])
        soup = BeautifulSoup(response.text, 'lxml')
        add_main = soup.find_all('div', class_='map-box-address')
        for tag in add_main:
            counter += 1
            results["resteraunt"] = result["resteraunt"]
            results["address_url"] = result["address_url"]
            results["address"] = tag.find('address').get_text().replace(" ","").replace(",","").replace("\n","")
            search_result.append(results)
            if (counter >= 5):
            # if (counter >= 1):
                break

    geo_base_url='https://maps.googleapis.com/maps/api/geocode/json?address='
    api_key = 'AIzaSyDtmsK5ZixHwMLSIf1OzvZGPdddESnJtCc'
    geo_list = []

    source_address = f'{addressline1}{addressline2}{zipcode}'
    geo_url = f'{geo_base_url}{source_address}&key={api_key}'
    response = requests.get(geo_url).json()
    source_lat = response['results'][0]["geometry"]["location"]["lat"]
    source_lng = response['results'][0]["geometry"]["location"]["lng"]

    for result in search_result:
        geo_result = {}
        geo_url = f'{geo_base_url}{result["address"]}&key={api_key}'
        response = requests.get(geo_url).json()
        if (response["status"] != "ZERO_RESULTS"):
            geo_result["resteraunt"] = result["resteraunt"]
            geo_result["address"] = result["address"]
            geo_result["lat"] = response['results'][0]["geometry"]["location"]["lat"]
            geo_result["lng"] = response['results'][0]["geometry"]["location"]["lng"]
            geo_list.append(geo_result)
        else:
            print(f'Excluding results of {result["resteraunt"]} {result["address"]}')

    base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins='
    apikey ='AIzaSyCLhrNPVFMUaFdocknqQeCNOdhAK7TDj4Y'
    r = requests.get(url)

    for result in geo_list:
        dist_url = f'{base_url}{source_lat},{source_lng}&destinations={result["lat"]},{result["lng"]}&key={apikey}'
        r = requests.get(dist_url).json()
        result["distance"] = r["rows"][0]["elements"][0]["distance"]["text"]
        result["duration"] = r["rows"][0]["elements"][0]["duration"]["text"]    

    source_dict = {}
    source_dict["addressline1"] = addressline1
    source_dict["addressline2"] = addressline2
    source_dict["zipcode"] = zipcode
    source_dict["cuisine"] = cuisine
    source_dict["lat"] = source_lat
    source_dict["lng"] = source_lng

    return_list = []
    return_dict = {}
    return_dict["source"] = source_dict
    return_list.append(return_dict)
    return_dict = {}
    return_dict["detail"] = geo_list
    return_list.append(return_dict)
    insert_search(source_dict, return_dict)
    return jsonify(return_list)

def insert_search(source_dict, return_dict):
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    # Define the 'classDB' database in Mongo
    db = client.projDB
    hist = db.hist.find()
    # Insert a document into the 'hist' collection
    db.hist.insert_one(
        {
            'addressline1': source_dict["addressline1"],
            'addressline2': source_dict["addressline2"],
            'zipcode': source_dict["zipcode"],
            'cuisine' : source_dict["cuisine"],
            'result' : return_dict
        }
    )

# @app.route("/apiSource/<addressline1>/<addressline2>/<zipcode>/<cuisine>")
# def api_source(addressline1, addressline2, zipcode, cuisine):
#     geo_base_url='https://maps.googleapis.com/maps/api/geocode/json?address='
#     api_key = 'AIzaSyDtmsK5ZixHwMLSIf1OzvZGPdddESnJtCc'

#     source_address = f'{addressline1}{addressline2}{zipcode}'
#     geo_url = f'{geo_base_url}{source_address}&key={api_key}'
#     response = requests.get(geo_url).json()

#     source_dict = {}
#     source_list = []
#     source_dict["addressline1"] = addressline1
#     source_dict["addressline2"] = addressline2
#     source_dict["zipcode"] = zipcode
#     source_dict["cuisine"] = cuisine
#     source_dict["lat"] = response['results'][0]["geometry"]["location"]["lat"]
#     source_dict["lng"] = response['results'][0]["geometry"]["location"]["lng"]
#     source_list.append(source_dict)

#     return jsonify(source_list)

if __name__ == "__main__":
    app.run()

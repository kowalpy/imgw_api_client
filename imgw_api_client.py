#!/usr/bin/env python

"""
Implementacja klienta API publicznych danych IMGW na licencji LGPL 3.0.

Wersja 1.1 - 24 czerwca 2018.
Autor: [https://github.com/kowalpy|Marcin Kowalczyk]
WWW: https://github.com/kowalpy/imgw_api_client

Komunikat IMGW:
Korzystanie z serwisu oznacza zgode uzytkownika na przestrzeganie postanowien regulaminu,
dlatego tez kazdy uzytkownik zobowiazany jest do zapoznania sie z trescia regulaminu
przed rozpoczeciem korzystania z serwisu. https://danepubliczne.imgw.pl/regulations
"""

import time
import urllib
import sys
import optparse
import ConfigParser

class ImgwApiClient(object):
    def __init__(self):
        self.target_stations = []
        self.contents = []

    def read_remote_data(self):
        myurl_pattern = "https://danepubliczne.imgw.pl/api/data/synop/id/%s/format/%s"
        for i in self.target_stations:
            myurl = myurl_pattern % (i['station'], i['format'])
            response = urllib.urlopen(myurl)
            response_decoded = response.read()
            content = i
            content['data'] = response_decoded
            self.contents.append(content)

    def save_data(self, filepath=""):
        filename = str(time.time()) + ".txt"
        try:
            f = open(filename, 'w')
            f.write(self.convert_contents_to_str())
            f.close()
        except Exception as e:
            print("ERROR: %s" % e)

    def return_data(self):
        return self.contents

    def convert_contents_to_str(self):
        cont_str = ""
        is_first_csv_line = True
        for i in self.contents:
            the_data = i['data']
            if i['format'] == "csv":
                if not is_first_csv_line:
                    the_data = the_data[the_data.find("cisnienie") + 10:]
                else:
                    is_first_csv_line = False
            cont_str += the_data
        return cont_str

    def print_data(self):
        print(self.convert_contents_to_str())

    def read_ini_file(self, filepath="meteo.ini"):
        config = ConfigParser.RawConfigParser()
        config.read(filepath)
        meteoformat = config.get("meteo", "format")
        stations = config.get("meteo", "stations")
        stations = stations.split(";")
        for i in stations:
            new_dict = {"station": i, "format": meteoformat}
            self.target_stations.append(new_dict)

class RunImgwApiClient(ImgwApiClient):
    def __init__(self):
        super(RunImgwApiClient, self).__init__()
        self.warn = "imgw_api_client 1.1 - https://github.com/kowalpy/imgw_api_client\n\n"
        self.warn += "Komunikat IMGW:\n"
        self.warn += "Korzystanie z serwisu oznacza zgode uzytkownika na przestrzeganie"
        self.warn += " postanowien regulaminu, dlatego tez kazdy uzytkownik zobowiazany"
        self.warn += " jest do zapoznania sie z trescia regulaminu przed rozpoczeciem"
        self.warn += " korzystania z serwisu. https://danepubliczne.imgw.pl/regulations\n\n"

    def print_warning(self):
        print(self.warn)

    def run_standalone(self):
        print(self.warn)
        self.parse_args()
        #TBD: futher proceeding based on input args, by default reading default ini file
        self.read_ini_file()
        self.read_remote_data()
        self.print_data()
        self.save_data()

    def parse_args(self):
        #TBD
        pass

def main():
    RunImgwApiClient().run_standalone()

if __name__ == '__main__':
    main()

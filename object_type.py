from __future__ import division, print_function, absolute_import
import logging
from logging import StreamHandler
from requests.auth import HTTPBasicAuth
import logstash
import sys
import random
from calendar import isleap
import time
import requests
import json
import os
import datetime

#Constants
#Defines if the object_type are destined to be logged in elasticsearch
CHECK_ELASTIC_LOGGED = True
#Defines if the object_type are destined to be logged in a .log file
CHECK_FILE_LOGGED = True
#Defines Whether Orit is pregnant or not
CHECK_ORIT_IS_PREGNANT = False

class Child:
    """A Child class"""

    def __init__(self, first_name):
        #Creates a new Child instance
        self.first_name = first_name
        self.last_name = 'Yair'
        #Send out orit's child to the world(wide web) :)
        try:
            if CHECK_ELASTIC_LOGGED:
                #Ship the new child to the elasticsearch db
                logger.info(('A Newborn Child ^_^: '
                    + '{} will be born at {}').format(
                    self.fullname, self.birthdate))
        except:
            print("Error :( " + 
                "Couldn't log out the child to the elasticsearch db...")
            sys.exit("Exiting. Can't log the children to the ES db")

    @property
    def birthdate(self):
        #the child's birth date
        return '{}'.format(birthdate_generator())

    @property
    def fullname(self):
        ##the child's full name
        return '{} {}'.format(self.first_name, self.last_name)

def create_new_elasticsearch_index(
        index_name,
        elastic_username,
        elastic_password,
        elastic_ip_address,
        elastic_port_address):
    """Creates a new elasticsearch index"""
    #Checks if the index exists before creating it
    try:
        r = requests.get(f'http://{elastic_ip_address}:'
            + f'{elastic_port_address}/{index_name}',
            auth = HTTPBasicAuth(elastic_username,
            elastic_password)).json()
        if(list(r.keys())[0] == 'error'):
            r = requests.put(f'http://{elastic_ip_address}:'
                + f'{elastic_port_address}/{index_name}',
            auth = HTTPBasicAuth(elastic_username,
                elastic_password)).json()
    except:
        print("ERROR: " +
            "Couldn't have made a connection to the elasticsearch db.")
        sys.exit("Exiting. Can't log the children to the ES db")

def set_up_elasticsearch_logger(
    logger_host_address,
    logger_port_address):
    """Creates a new elasticsearch logger"""

    #creates a logger
    global logger
    logger = logging.getLogger(__name__)
    #logger = logging.getLogger("orits_children")

    #Configures the logger
    logger.setLevel(logging.INFO)
    logger.addHandler(logstash.TCPLogstashHandler(
        logger_host_address,
        logger_port_address,
        version=1))
    #formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    formatter = logging.Formatter('%(message)s')

    #Optional - stream the output to the terminal
    #stream_handler = logging.StreamHandler()
    #stream_handler.setFormatter(formatter)

    #Adds a stream handler if it writes to the terminal
    #logger.addHandler(stream_handler)

    #Adds a file handler if it writes to a file
    if CHECK_FILE_LOGGED:
        #Log to a .log file as well
        file_handler = logging.FileHandler('children.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

def birthdate_generator():
    """ Returns a birth date for orit's child """

    while True:
        day = random.randint(1, 31)
        month = random.randint(1,12)
        year = random.randint(2021,2037)

        if month == 2:
            if day > 28:
                if not isleap(year):
                    continue
        elif month in [4, 6, 9, 11]:
            if day > 30:
                continue

        #Check if Orit has time to deliver the baby
        if not CHECK_ORIT_IS_PREGNANT:
            if year == datetime.date.today().year:
                if month - datetime.date.today().month < 9:
                    continue
            elif year - datetime.date.today().year == 1:
                if (month + 12) - datetime.date.today().month < 9:
                    continue

        return f'{str(day)} . {str(month)} . {str(year)}'

def name_picker():
    """picks a name out of a names list"""
    try:
        name_index = random.randint(0, len(names_list) - 1)
        name = names_list[name_index]
        names_list.remove(names_list[name_index])
        return name
    except:
        raise IndexError(
            'names list index out of bounds, the list is empty')

def main():

    #a global list of Israeli names
    global names_list
    names_list = ['Adam', 'Aharon', 'Levi', 'Yitzhak', 'Itzik',
    'Omri', 'Ofer', 'Ofek', 'Menny', 'Kobi', 'Ben',
    'Jonathan', 'Efraim', 'Haim', 'Itay', 'Gal', 'Maor',
    'Asher', 'Chanoch', 'Zvi', 'Zion', 'Dan', 'Daniel']

    #the amout of kids
    children_amount = random.randint(2, 10)
    #a list with orit's kids
    children_list = []


    #Creates the logger if the children are logged to elastic
    if CHECK_ELASTIC_LOGGED:
        #Creates an elasticsearch index with the following parameters:
        #index name, 
        #elasticsearch username,
        #elasticsearch password,
        #elasticsearch ip address,
        #elasticsearch port address.
        create_new_elasticsearch_index('orits_children',
            'elastic',
            'plnGh96zNVIj77HNnpsB',
            'localhost',
            '9200')

        #Creates the logger with a logstash ip, port addresses
        set_up_elasticsearch_logger('localhost', 5000)

    #Limit the amount of children because too much is too much...
    if children_amount > 6:
        children_amount = 6
        print("Orit Please... How many do you want... well...")
        
    #The child creation begins
    for x in range(children_amount):
        children_list.append(Child(name_picker()))

    #If you've gotten so far, <3
    print(f'Oritttt <3 congratz for your {children_amount} children!')

if __name__ == '__main__':
    main()
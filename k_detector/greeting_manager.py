import json
import datetime
import paho.mqtt.client as mqtt
from threading import Timer

class GreetingManager:

    def __init__(self, greeting_timeout):
        self.greeting_timeout = greeting_timeout
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect("192.168.0.102", port=1883, keepalive=60, bind_address="")
        self.people_greeted = dict()

    def greet(self, name):
        if name not in self.people_greeted:
            print "New person found!"
            self.people_greeted[name] = False

        if self.people_greeted[name]:
            print name + " has already been greeted! I'll greet you again soon"
        else:
            print "Greeting " + name + "..."
            self.people_greeted[name] = True
            self.mqtt_client.publish("say", self.get_greeting(datetime.datetime.now(), name))
            Timer(self.greeting_timeout, self.reset_greeted, [name]).start()

    def reset_greeted(self, name):
        print "Looks like it's time to greet " + name + " again!"
        self.people_greeted[name] = False

    def get_greeting(self, time, name):
        if time.hour < 12:
            greeting = "Good morning"
        elif 12 <= time.hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"

        return json.dumps({ "message": greeting + name })

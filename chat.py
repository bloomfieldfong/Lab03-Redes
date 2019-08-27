import sys
import logging
import getpass
import sleekxmpp
from optparse import OptionParser
from sleekxmpp.exceptions import IqError, IqTimeout
from opciones import *
from sleekxmpp.stanza import Message, Presence, Iq, StreamError
import json
#from dvr import *
   
class EchoBot(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password, opcion):

        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        #Evento de login y registro
        if (opcion == "1"):
            self.add_event_handler("session_start", self.start)
        elif(opcion == "2"):
            self.add_event_handler("register", self.register)
            self.add_event_handler("session_start", self.start)
        
        self.add_event_handler("message", self.message) 

        self.register_plugin('xep_0047', {
            'auto_accept': True
        })

        #self.add_event_handler("ibb_stream_start", self.stream_opened, threaded=True)
        #self.add_event_handler("ibb_stream_data", self.stream_data)

    #Procesa el evento session_start
    def start(self, event):
        print("Starting session")
        self.send_presence()
        self.get_roster()



    #Procesa los mensajes entrantes 
    def message(self, msg):

        if msg['type'] in ('chat', 'normal'):
            y = msg['body']
            print(y)
            
            contactos = xmpp.client_roster
            contactos = contactos.keys()
            contactos = list(contactos)
            if(y['to'] == y['receiver']):
                for i in range(len(y)) :

                    full_message = {
                    "transmitter": y['to'],
                    "receiver": user,
                    "jumps": str(x),
                    "distance": str(x),
                    "node_list": nodos,
                    "message": message, 
                    "to": contactos[i]
                    }   
                    full_message = str(full_message)
                    ##mto = (y[i])
                    xmpp.send_message(mto= 'michi222@alumchat.xyz', mbody = full_message, mtype = 'chat')
                print("Message sent\n")

            
    def delete(self):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['from'] = self.boundjid.user
        resp['register'] = ' '
        resp['register']['remove'] = ' '
        print(resp)
        try:
            resp.send(now=True)
            logging.info("Account deleted for %s!" % self.boundjid)
        except IqError as e:
            logging.error("Could not register account: %s" %
                          e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            logging.error("No response from server.")
            self.disconnect()

        
    def register(self, iq):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password

        try:
            resp.send(now=True)
            logging.info("You created the account: %s!" % self.boundjid)
        except IqError as e:
            logging.error("Couldnt create the account %s" %
                    e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            logging.error("Server didnt respond")
            self.disconnect()

if __name__ == '__main__':

    initial_menu()
    x = input("What would you like to do? (1 or 2): ")
    optp = OptionParser()

    #Opciones de output
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

    #Opciones de JID y password .
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")

    opts, args = optp.parse_args()

    #Setear el login
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    if opts.jid is None:
        opts.jid = input("Username: ")
    if opts.password is None:
        opts.password = getpass.getpass("Password: ")

    
    #Setup de mi clase EchoBot
    xmpp = EchoBot(opts.jid, opts.password, x)
    
    #plugins de registro
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0004') # Data forms
    xmpp.register_plugin('xep_0066') # Out-of-band Data
    xmpp.register_plugin('xep_0077') # In-band Registration
    xmpp['xep_0077'].force_registration = False

  
            
    #Conexion con el server
    if xmpp.connect():
        
        xmpp.process(block=False) 

        x = 0
        nodos = ''
        
        while(True):
            main_menu()
            main_option = input("What would you like to do?: \n>> ")
            # 1. Add, 2. Show, 3. Send, 4. Log off


            if (main_option == "1"):
                user = input("Who are you trying to add?: ")
                weight = input("How much does it cost to contact the user?: ")
                xmpp.send_presence(pto = user, ptype ='subscribe')
            
            elif (main_option == "2"):
                print("\nContacts:\n")
                contacts = xmpp.client_roster
                print(contacts.keys())

            elif (main_option == "3"):
                algorithm_menu()   
                
                opcion = input("Which algorithm would you like to use?: \n>> ")
                if(opcion == "1"):
                    print("FLOADING")
                
                    x = x + 1
                    nodos = nodos + "-" + opts.jid
                    print(x)
                    # Send message
                    user = input("Who is the message for?: ")
                    message = input("Message:")
                    
                    
                    print("Sending message...\n")
                    y = xmpp.client_roster
                    y = y.keys()
                    y = list(y)

                    for i in range(len(y)) :

                        full_message = {
                        "transmitter": opts.jid,
                        "receiver": user,
                        "jumps": str(x),
                        "distance": str(x),
                        "node_list": nodos,
                        "message": message, 
                        "to": y[i]
                        }   
                        full_message = str(full_message)
                        ##mto = (y[i])
                        xmpp.send_message(mto= 'michi222@alumchat.xyz', mbody = full_message, mtype = 'chat')
                    print("Message sent\n")
                
                    
                if(opcion == "2"):
                    print("Distance vector routing")
                if(opcion == "3"):
                    print("Link state routing")

            elif (main_option == "4"):
                print("Logged Off")
                xmpp.disconnect()
                break  
    else:
        print("Unable to connect.")

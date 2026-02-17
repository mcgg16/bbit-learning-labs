# Attempting consumer
from consumer_interface import mqConsumerInterface # Links to the c_i file to use the class

# Inherit from file at consumer_interface
class mqConsumer(mqConsumerInterface): 
    def __init__(self,  binding_key, exchange_name, queue_name): 
        self.binding_key = binding_key
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.setupRMQConnection() # Attempt to call consumer_interface function
    


# Copyright 2024 Bloomberg Finance L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pika
import os

class mqConsumerInterface:
    def __init__(
        self, binding_key: str, exchange_name: str, queue_name: str
    ) -> None:
        # Save parameters to class variables
        self.binding_key = binding_key
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.channel = None # A ver si empty channel

        # Call setupRMQConnection
        self.setupRMQConnection()

    def on_message_callback(
        self, channel, method_frame, header_frame, body
    ) -> None:
        # Acknowledge message
        self.channel.basic_ack(method_frame.delivery_tag, False)
        #channel.basic_ack(method_frame.delivery_tag, False)

        #Print message (The message is contained in the body parameter variable)
        print(f"Consumer received: {body}")

        ##pass ## TODO Check if pass also dies

    # Moving to try to get it to work w Pika
    def setupRMQConnection(self) -> None:
        # Set-up Connection to RabbitMQ service
        #con_params = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        con_params = pika.URLParameters(os.environ["AMQP_URL"]) # Using the ones provided by the Functions.md
        self.connection = pika.BlockingConnection(parameters=con_params)

        # Establish Channel
        self.channel = self.connection.channel() # Mas yap de self pq no calaba sin eso
        #channel = self.connection.channel() # Mas yap de self pq no calaba sin eso

        # Create Queue if not already present
        self.channel.queue_declare(queue= self.queue_name) # Segun se supone q ya automaticamente lo hace así
        #channel.queue_declare(queue= self.queue_name) # Segun se supone q ya automaticamente lo hace así

        # Create the exchange if not already present
        self.exchange = self.channel.exchange_declare(exchange=self.exchange_name)
        #exchange = channel.exchange_declare(exchange=self.exchange_name)

        # Bind Binding Key to Queue on the exchange
        ## TODO change the routing key and exchange name
        self.channel.queue_bind(
            queue= self.queue_name,
            routing_key= self.binding_key,
            exchange= self.exchange_name,
        )

        # Set-up Callback function for receiving messages
        # Using the on_message_callback funct below
        self.channel.basic_consume(
            self.queue_name, self.on_message_callback, auto_ack=False
        )

        '''channel.basic_consume(
            self.queue_name, on_message_callback, auto_ack=False
        )'''
    
        ## TODO check if I'm supposed to get rid of pass
        ## pass

   

    def startConsuming(self) -> None:
        # Print " [*] Waiting for messages. To exit press CTRL+C"
        " [*] Waiting for messages. To exit press CTRL+C"

        # Start consuming messages
        self.channel.start_consuming()
        #channel.start_consuming()

        ## pass
    
    def __del__(self) -> None:
        # Print "Closing RMQ connection on destruction"
        print("Closing RMQ connection on destruction")
        
        # Close Channel
        self.channel.close()
        #channel.close()

        # Close Connection
        self.connection.close()
        #connection.close()
        
        ##pass

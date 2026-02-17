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
        #self.binding_key = binding_key
        #self.exchange_name = exchange_name
        #self.queue_name = queue_name

        # Call setupRMQConnection
        pass

    # Moving to try to get it to work w Pika
    def setupRMQConnection(self) -> None:
        # Set-up Connection to RabbitMQ service
        ##connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        con_params = pika.URLParameters(os.environ["AMQP_URL"]) # Using the ones provided by the Functions.md
        connection = pika.BlockingConnection(parameters=con_params)


        # Establish Channel
        channel = connection.channel()
        

        # Create Queue if not already present
        channel.queue_declare(queue="Tech Lab Queue") # Segun se supone q ya automaticamente lo hace así

        # Create the exchange if not already present
        exchange = channel.exchange_declare(exchange="Exchange Name")

        # Bind Binding Key to Queue on the exchange
        ## TODO change the routing key and exchange name
        channel.queue_bind(
            queue= "Tech Lab Queue",
            routing_key= "Routing Key",
            exchange="Exchange Name",
        )

        # Set-up Callback function for receiving messages
        # Using the on_message_callback funct below
        channel.basic_consume(
            "Tech Lab Queue", on_message_callback, auto_ack=False
        )
    
        ## TODO check if I'm supposed to get rid of pass
        ## pass

    def on_message_callback(
        self, channel, method_frame, header_frame, body
    ) -> None:
        # Acknowledge message
        channel.basic_ack(method_frame.delivery_tag, False)

        #Print message (The message is contained in the body parameter variable)
        print(f"Consumer received: {body}")

        ##pass ## TODO Check if pass also dies

    def startConsuming(self) -> None:
        # Print " [*] Waiting for messages. To exit press CTRL+C"
        " [*] Waiting for messages. To exit press CTRL+C"

        # Start consuming messages
        channel.start_consuming()

        ## pass
    
    def __del__(self) -> None:
        # Print "Closing RMQ connection on destruction"
        print("Closing RMQ connection on destruction")
        
        # Close Channel
        channel.close()

        # Close Connection
        connection.close()
        
        ##pass

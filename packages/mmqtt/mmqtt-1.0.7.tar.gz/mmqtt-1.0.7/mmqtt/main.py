#!/usr/bin/env python3
"""
Powered by Meshtastic™ https://meshtastic.org/
"""

import time
from mmqtt.load_config import ConfigLoader
from mmqtt.tx_message_handler import send_nodeinfo, send_position, send_device_telemetry, send_text_message
from mmqtt.mqtt_handler import get_mqtt_client
from mmqtt.argument_parser import handle_args, get_args

stay_connected = False

def start():
    _, args = get_args()
    config_file = args.config
    config = ConfigLoader.load_config_file(config_file)
    client = get_mqtt_client()

    if handle_args() == None:

        # send_nodeinfo(config.node.short_name, config.node.long_name, config.node.hw_model)
        # time.sleep(3)

        # send_position(config.node.lat, config.node.lon, config.node.alt, config.node.precision)
        # time.sleep(3)

        # send_device_telemetry(battery_level=99, voltage=4.0, chutil=3, airtxutil=1, uptime=420)
        # time.sleep(3)

        send_text_message("Happy New Year!")
        time.sleep(3)

    client.disconnect()
    
    if not stay_connected:
        client.disconnect()
    else:
        while True:
            time.sleep(1)

if __name__ == "__main__":
    start()
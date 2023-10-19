import os
import platform
from typing import *

class NetworkManager:
    """
    It manages WiFi connection with the system. This helps as verification
    previous to attempt connections and operations on a certain Network
    (in this case Robotat's WiFi Network) by polling the current connection
    and creating a new one if needed.
    """

    def __init__(self):
        self.platform = platform.system()

    def define_network_parameters(self, SSID: str, key: str):
        """
        Define the SSID name and key (password) to refer in the rest of the methods.
        """
        self.SSID = SSID
        self.key = key
    def is_connected_to_network(self):
        """
        It polls the current connection specified with it's SSID (Network's name)

        Returns:
        ---------------
        Current SSID, so the name can be handled in an external script.
        """
        if self.platform == "Windows":
            command = "netsh wlan show interfaces"
        elif self.platform == "Linux":
            command = "iwconfig"

        output = os.popen(command).read()

        return self.SSID in output

    def create_new_connection(self, name: str):
        """
        Method used to create a new WiFi connection.

        Attributes:
        ---------------
        name : str
        SSID : str
            Usually both are the same, it specifies the network the user wants to establish the connection with.
        key : str
            It's the Network's password.

        """
        config = (
            """<?xml version=\"1.0\"?>
        <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
            <name>"""
            + name
            + """</name>
            <SSIDConfig>
                <SSID>
                    <name>"""
            + self.SSID
            + """</name>
                </SSID>
            </SSIDConfig>
            <connectionType>ESS</connectionType>
            <connectionMode>auto</connectionMode>
            <MSM>
                <security>
                    <authEncryption>
                        <authentication>WPA2PSK</authentication>
                        <encryption>AES</encryption>
                        <useOneX>false</useOneX>
                    </authEncryption>
                    <sharedKey>
                        <keyType>passPhrase</keyType>
                        <protected>false</protected>
                        <keyMaterial>"""
            + self.key
            + """</keyMaterial>
                    </sharedKey>
                </security>
            </MSM>
        </WLANProfile>"""
        )
        if self.platform == "Windows":
            command = (
                'netsh wlan add profile filename="'
                + name
                + '.xml"'
                + " interface=Wi-Fi"
            )
            with open(name + ".xml", "w") as file:
                file.write(config)
        elif self.platform == "Linux":
            command = "nmcli dev wifi connect '" + self.SSID + "' password '" + self.key + "'"
        os.system(command)
        if self.platform == "Windows":
            os.remove(name + ".xml")

    def connect(self, name):
        """
        Method used to create a new WiFi connection.

        Attributes:
        ---------------
        name : str
        SSID : str
            Usually both are the same, it specifies the network the user wants to establish the connection with.
        key : str
            It's the Network's password.

        """
        if self.platform == "Windows":
            command = (
                'netsh wlan connect name="'
                + name
                + '" ssid="'
                + self.SSID
                + '" interface=Wi-Fi'
            )
        elif self.platform == "Linux":
            command = "nmcli con up " + self.SSID
        os.system(command)

    def display_available_networks(self):
        """
        Verifies available networks on the operating system.
        """
        if self.platform == "Windows":
            command = "netsh wlan show networks interface=Wi-Fi"
        elif self.platform == "Linux":
            command = "nmcli dev wifi list"
        os.system(command)

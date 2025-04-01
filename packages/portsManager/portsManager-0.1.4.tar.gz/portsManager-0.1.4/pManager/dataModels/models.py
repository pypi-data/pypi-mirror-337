class Port:

    """
    Class for representing a port in .qpmgr file.
    """

    def __init__(self, serviceName, portNum, portProto, openState, portDesc = "No description"):

        # Port stateList
        self.__portOpenState = {"O": True, "C": False}

        # Variables
        self.__serviceName = serviceName
        self.__portNum = int(portNum)
        self.__portProtocol = portProto
        self.__portDescription = portDesc
        if type(openState) == bool: self.__opened = openState
        else: self.__opened = self.__portOpenState[openState]

    def getPortAsJson(self):

        """
        Returns the port details as a JSON-like dictionary.

        Returns:
            dict: A dictionary where the key is the port number, and the value is another dictionary containing:
                - "protocol" (str): The protocol of the port.
                - "description" (str): The description of the port.
                - "opened" (bool): The state of the port, whether it is open or closed.
        """

        return {
            self.__portNum: {
                "protocol": self.__portProtocol,
                "description": self.__portDescription,
                "opened": self.__opened
            }
        }

    def getServiceName(self):

        """
        Returns the name of the service associated with the port.

        Returns:
            str: The name of the service.
        """

        return self.__serviceName


class Service:

    """
    Class for representing a service in .qpmgr file.
    """

    def __init__(self, serviceName, portList=None, serviceDescription ="No description"):

        if portList is None: portList = {
            -1: {
                "protocol": "TCP",
                "description": "PORTLIST NOT SET",
                "opened": False
            }
        }

        self.isPortsAdded = False
        self.__portList = portList
        self.__serviceName = serviceName
        self.__serviceDescription = serviceDescription
        self.__portRecordMask = "$PROTOCOL::$PORT::$STATE::$DESCRIPTION"
        print(f'portList: {self.__portList}\ndescription: {self.__serviceDescription}')

    def addPortToService(self, portJson):

        """
        Adds a port to the service.

        Args:
            portJson (dict): Json of the port to add
        """

        if self.isPortsAdded:
            self.__portList.update(portJson)
        else:
            self.__portList = portJson
            self.isPortsAdded = True


    def getServiceName(self):

        """
        Returns the name of the service.

        Returns:
            str: The name of the service.
        """

        return self.__serviceName

    def getServiceDescription(self):

        """
        Returns the description of the service.

        Returns:
            str: The description of the service.
        """

        return self.__serviceDescription

    def generatePortConfig(self):

        """
        Returns the port configuration of the service.

        Returns:
            str: The port configuration of the service.
        """

        ports = []
        if type(self.__portList) is dict:
            for __p in self.__portList.keys():
                port = self.__portList[__p]
                portConfig = (self.__portRecordMask
                              .replace("$PROTOCOL", port['protocol'], 1)
                              .replace("$PORT", str(__p), 1)
                              .replace("$STATE", "O" if port['opened'] else "C", 1)
                              .replace("$DESCRIPTION", port['description'], 1)
                              )
                ports.append(portConfig)
        else: ports = ["-1::TCP::C::PORTLIST NOT SET"]
        return "; ".join(ports)

    def getServiceAsJson(self):

        """
        Returns the service details as a JSON-like dictionary.

        Returns:
            dict: A dictionary where the key is the service name, and the value is another dictionary containing:
                - "ports" (dict): A dictionary where the key is the port number, and the value is another dictionary containing:
                    - "protocol" (str): The protocol of the port.
                    - "description" (str): The description of the port.
                    - "opened" (bool): The state of the port, whether it is open or closed.
                - "description" (str): The description of the service.
        """

        return {
            self.__serviceName: {
                "ports": self.__portList,
                "description": self.__serviceDescription
            }
        }
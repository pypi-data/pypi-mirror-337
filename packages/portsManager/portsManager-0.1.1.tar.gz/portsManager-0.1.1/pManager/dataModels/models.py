class Port:

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

        return {
            self.__portNum: {
                "protocol": self.__portProtocol,
                "description": self.__portDescription,
                "opened": self.__opened
            }
        }

    def getServiceName(self):

        return self.__serviceName


class Service:

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

    def addPortToService(self, portJson):

        if self.isPortsAdded:
            self.__portList.update(portJson)
        else:
            self.__portList = portJson
            self.isPortsAdded = True


    def getServiceName(self):

        return self.__serviceName

    def getServiceDescription(self):

        return self.__serviceDescription

    def generatePortConfig(self):

        ports = []
        for __p in self.__portList.keys():
            port = self.__portList[__p]
            portConfig = (self.__portRecordMask
                          .replace("$PROTOCOL", port['protocol'], 1)
                          .replace("$PORT", str(__p), 1)
                          .replace("$STATE", "O" if port['opened'] else "C", 1)
                          .replace("$DESCRIPTION", port['description'], 1)
                          )
            ports.append(portConfig)

        return "; ".join(ports)

    def getServiceAsJson(self):

        return {
            self.__serviceName: {
                "ports": self.__portList,
                "description": self.__serviceDescription
            }
        }
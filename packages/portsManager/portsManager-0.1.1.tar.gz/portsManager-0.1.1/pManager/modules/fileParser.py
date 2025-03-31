# Intializing errors

class ParserError(Exception):
    """Base class for exceptions in the parser module."""
    def __init__(self, message, filename=None):
        self.message = message
        self.filename = filename
        super().__init__(message)

class ConfigurationError(ParserError):
    """Exception raised for configuration-related errors during file parsing."""
    pass

class UnknownServiceError(ParserError):
    """Exception raised when an unknown service is encountered during parsing."""
    pass

class UnknownPortError(ParserError):
    """Exception raised when an unknown port is encountered during parsing."""
    pass

class FormatError(ParserError):
    """Exception raised for errors in the file format."""
    pass



class fileParser:

    def __init__(self, filename):

        # Variables
        self.__filename = filename # Shadows filename into class scope
        self.__servicesList = {} # Parsed information from .qpmgr file w/service as key
        self.__portList = {} # Parsed information from .qpmgr file w/port as key, w/o service description
        self.__openedPorts = []
        self.__closedPorts = []
        self.__blankLines = ("\n", "", " ") # What lines parser should skip in file?
        self.__stateTable = {"O": True, "C": False}
        # Port state: O = Opened = True
        #             C = Closed = False

        # Errors declare
        self.__filenameError = ConfigurationError("Filename isn't set. You can get filename from errorObj.filename", self.__filename)
        self.__fileNotFoundError = ParserError(f"File {self.__filename} not found. ", self.__filename)
        self.__unknownServiceError = UnknownServiceError("Unknown service", self.__filename)
        self.__unknownPortError = UnknownPortError("Unknown port", self.__filename)
        self.__formatError = ParserError("File is blank or not formated as .qpmgr", self.__filename)

        # Starting fileParser with configuration above
        self.__parseFile()

    def __parseFile(self):
        if self.__filename is None: raise self.__filenameError

        try:
            with open(self.__filename, 'r') as file:
                for line in file.readlines():

                    if line.startswith("#"): continue
                    if line in self.__blankLines: continue

                    line = line.replace("\n", "")
                    data = line.split(' || ')[0]
                    serviceName = data.split(' -- ')[0]
                    ports = {}

                    for port in data.split(' -- ')[1].split('; '):
                        port = port.split('::')
                        ports[int(port[1])] = {"protocol": port[0], "description": port[3], "opened": self.__stateTable[port[2]]}

                    desc = line.split(' || ')[1]

                    self.__servicesList[serviceName] = {"ports": ports, "description": desc}

                file.close()

        except FileNotFoundError: raise self.__fileNotFoundError
        except IndexError: raise self.__formatError

        for srv in self.__servicesList.keys():
            for port in self.__servicesList[srv]['ports']:
                 self.__portList[port] = {
                     "serviceName": srv,
                     "protocol": self.__servicesList[srv]['ports'][port]['protocol'],
                     "description": self.__servicesList[srv]['ports'][port]['description'],
                     "opened": self.__servicesList[srv]['ports'][port]['opened']
                 }

        self.__fetchPorts()

        if self.__servicesList == {}: raise

    def __fetchPorts(self):
        if self.__servicesList == {}: self.__parseFile()
        for service in self.__servicesList:
            for port in self.__servicesList[service]['ports'].keys():
                if self.__servicesList[service]['ports'][port]['opened']: self.__openedPorts.append(port)
                else: self.__closedPorts.append(port)

    def getOpenedPorts(self) -> list:
        if (self.__openedPorts == {}) or (self.__closedPorts == {}): self.__fetchPorts()
        return self.__openedPorts

    def getClosedPorts(self) -> list:
        if (self.__openedPorts == {}) or (self.__closedPorts == {}): self.__fetchPorts()
        return self.__closedPorts

    def getServicesList(self) -> list:
        if self.__servicesList == {}: self.__parseFile()
        return list(self.__servicesList.keys())

    def getOpenedPortsByService(self, serviceName) -> list:
        if self.__servicesList == {}: self.__parseFile()
        serviceInfo = self.__servicesList.get(serviceName)
        if serviceInfo is None: raise self.__unknownServiceError
        return list(map(str, serviceInfo['ports'].keys()))

    def getDescriptionByService(self, serviceName) -> str:
        if self.__servicesList == {}: self.__parseFile()
        serviceInfo = self.__servicesList.get(serviceName)
        if serviceInfo is None: raise self.__unknownServiceError
        return serviceInfo['description']

    def getBeautifuledInfoByService(self, serviceName) -> str:
        if self.__servicesList == {}: self.__parseFile()
        return \
f'''\
Service name: {serviceName}
Ports in use: {', '.join(self.getOpenedPortsByService(serviceName))}
Description: {self.getDescriptionByService(serviceName)}\
'''

    def getServiceByPort(self, portNum) -> str:
        if self.__portList == {}: self.__parseFile()
        portInfo = self.__portList.get(portNum)
        if portInfo is None: raise self.__unknownPortError
        return portInfo['serviceName']

    def getDescriptionByPort(self, portNum) -> str:
        if self.__servicesList == {}: self.__parseFile()
        portInfo = self.__portList.get(portNum)
        if portInfo is None: raise self.__unknownServiceError
        return portInfo['description']

    def getProtocolByPort(self, portNum) -> str:
        if self.__portList == {}: self.__parseFile()
        portInfo = self.__portList.get(portNum)
        if portInfo is None: raise self.__unknownPortError
        return portInfo['protocol']

    def getPlainServiceList(self) -> dict:
        if self.__servicesList == {}: self.__parseFile()
        return self.__servicesList

    def getPlainPortList(self) -> dict:
        if self.__portList == {}: self.__parseFile()
        return self.__portList
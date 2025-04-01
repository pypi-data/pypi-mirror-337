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

    """
    Class for parsing .qpmgr file
    """

    def __init__(self, filename, ignoreExtension = False):

        """
        Constructor for fileParser class

        Args:
            filename (str): Path to the file
            ignoreExtension (bool): Whether to ignore file extension or not
        """

        # Variables
        if ignoreExtension: self.__filename = filename
        else: self.__filename = filename if filename.endswith(".qpmgr") else f"{filename}.qpmgr"
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

        """
        Returns list of opened ports

        Returns:
            list: List of opened ports
        """

        if (self.__openedPorts == {}) or (self.__closedPorts == {}): self.__fetchPorts()
        return self.__openedPorts

    def getClosedPorts(self) -> list:

        """
        Returns list of closed ports

        Returns:
            list: List of closed ports
        """

        if (self.__openedPorts == {}) or (self.__closedPorts == {}): self.__fetchPorts()
        return self.__closedPorts

    def getServicesList(self) -> list:

        """
        Returns list of services

        Returns:
            list: List of services
        """

        if self.__servicesList == {}: self.__parseFile()
        return list(self.__servicesList.keys())

    def getOpenedPortsByService(self, serviceName) -> list:

        """
        Returns list of opened ports by service

        Args:
            serviceName (str): Name of the service

        Returns:
            list: List of opened ports
        """

        if self.__servicesList == {}: self.__parseFile()
        serviceInfo = self.__servicesList.get(serviceName)
        if serviceInfo is None: raise self.__unknownServiceError
        return list(map(str, serviceInfo['ports'].keys()))

    def getDescriptionByService(self, serviceName) -> str:

        """
        Returns description of the service by it\'s name

        Args:
            serviceName (str): Name of the service

        Returns:
            str: Description of the service
        """

        if self.__servicesList == {}: self.__parseFile()
        serviceInfo = self.__servicesList.get(serviceName)
        if serviceInfo is None: raise self.__unknownServiceError
        return serviceInfo['description']

    def getBeautifuledInfoByService(self, serviceName) -> str:


        """
        Returns string with beautifuled information about the service by it\'s name

        Args:
            serviceName (str): Name of the service

        Returns:
            str: String with beautifuled information about the service
        """

        if self.__servicesList == {}: self.__parseFile()
        return \
f'''\
Service name: {serviceName}
Ports in use: {', '.join(self.getOpenedPortsByService(serviceName))}
Description: {self.getDescriptionByService(serviceName)}\
'''

    def getServiceByPort(self, portNum) -> str:

        """
        Returns service name by port number

        Args:
            portNum (int): Number of the port

        Returns:
            str: Service name
        """

        if self.__portList == {}: self.__parseFile()
        portInfo = self.__portList.get(portNum)
        if portInfo is None: raise self.__unknownPortError
        return portInfo['serviceName']

    def getDescriptionByPort(self, portNum) -> str:

        """
        Returns description of the port by its number

        Args:
            portNum (int): Number of the port

        Returns:
            str: Description of the port
        """

        if self.__servicesList == {}: self.__parseFile()
        portInfo = self.__portList.get(portNum)
        if portInfo is None: raise self.__unknownPortError
        return portInfo['description']

    def getProtocolByPort(self, portNum) -> str:

        """
        Returns protocol of the port by its number

        Args:
            portNum (int): Number of the port

        Returns:
            str: Protocol of the port
        """

        if self.__portList == {}: self.__parseFile()
        portInfo = self.__portList.get(portNum)
        if portInfo is None: raise self.__unknownPortError
        return portInfo['protocol']

    def getPlainServiceList(self) -> dict:

        """
        Returns dictionary with plain service list

        Returns:
            dict: Plain service list
        """

        if self.__servicesList == {}: self.__parseFile()
        return self.__servicesList

    def getPlainPortList(self) -> dict:

        """
        Returns dictionary with plain port list

        Returns:
            dict: Plain port list
        """

        if self.__portList == {}: self.__parseFile()
        return self.__portList
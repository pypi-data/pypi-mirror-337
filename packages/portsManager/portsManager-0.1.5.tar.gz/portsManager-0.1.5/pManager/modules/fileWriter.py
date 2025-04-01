from ..dataModels.models import Port
from ..dataModels.models import Service
from .fileParser import fileParser
import os

class WriterError(Exception):

    """Base class for exceptions in the writer module."""

    def __init__(self, message, filename=None):
        self.message = message
        self.filename = filename
        super().__init__(message)



class fileWriter:

    """
    Class for writing or updating .qpmgr files
    """

    def __init__(self, filename, autoFlush = True, ignoreExtension = False):

        """
        Constructor for fileWriter class

        Args:
            filename (str): Path to the file
            autoFlush (bool): Whether to flush data to file or not
            ignoreExtension (bool): Whether to ignore file extension or not
        """

        self.__portNumError = WriterError('Port should be number', filename)

        # Variables; consts
        self.__autoFlush = autoFlush
        if ignoreExtension: self.__filename = filename
        else: self.__filename = filename if filename.endswith(".qpmgr") else f"{filename}.qpmgr" # Shadows filename into class scope
        self.__servicesList = {} # Parsed information from .qpmgr file w/service as key
        self.__stateTable = {"O" : True, "C" : False}
        self.__serviceRecordMask = "$SERVICE -- $PORTSINFO || $SERVICEDESCRIPTION"
        self.__fileHeader = \
"""\
#====================== firewall allowed ports ======================#
#                                                                    #
#  |--------------------------------------------------------------|  #
#  |                             HINT                             |  #
#  |                                                              |  #
#  |   Use pManager to work with .qpmgr files or follow pattern   |  #
#  |--------------------------------------------------------------|  #
#  |                    ScriptReadable Pattern                    |  #
#  |                                                              |  #
#  | Service -- TCP/UDP::port[1-N]::O/C::PortDescr || ServiceDesc |  #
#  |--------------------------------------------------------------|  #
#                                                                    #
#====================================================================#

"""
        if os.path.exists(self.__filename):
            fp = fileParser(self.__filename)
            existingServicesList = fp.getPlainServiceList()
            for _ in existingServicesList.keys():
                self.constructServiceObj(_, existingServicesList[_]['description'], existingServicesList[_]['ports'])

    def __flushFile(self):

        """
        Flushes data to file
        """

        with open(self.__filename, 'w') as file:

            file.write(self.__fileHeader)

            for srv in self.__servicesList.keys():
                file.write(self.__serviceRecordMask.replace('$SERVICE', srv, 1)
                           .replace('$PORTSINFO', self.__servicesList[srv].generatePortConfig(), 1)
                           .replace('$SERVICEDESCRIPTION', self.__servicesList[srv].getServiceDescription(), 1) + '\n'
                           )

    def constructServiceObj(self, serviceName, serviceDescription ="No description", portList=None) -> Service:

        """
        Creates service object and adds it to the list

        Args:
            serviceName (str): Name of the service
            serviceDescription (str): Description of the service
            portList (dict): Dictionary of ports, where key is port number and value is port object

        Returns:
            Service (pManager.dataModels.models.Service): Created service object
        """

        srv = Service(serviceName=serviceName, serviceDescription=serviceDescription, portList=portList)
        self.addService(srv)
        return srv

    def bindPortToService(self, serviceName, portNum, portProto, openState, portDesc ="No description") -> Port:

        """
        Binds port to existing service

        Args:
            serviceName (str): Name (key) of the service
            portNum (int): Port number
            portProto (str): Protocol of the port
            openState (bool): State of the port
            portDesc (str): Description of the port

        Returns:
            Port (pManager.dataModels.models.Port): Port object that was created
        """

        port = Port(serviceName, portNum, portProto, openState, portDesc)
        self.addPort(port)
        return Port(serviceName, portNum, portProto, openState, portDesc)

    def addService(self, serviceObj: Service):

        """
        Adds service to the list

        Args:
            serviceObj (pManager.dataModels.models.Service): Service object

        Raises:
            WriterError: If the service object is not of type Service
        """

        if type(serviceObj) == Service:
            self.__servicesList[serviceObj.getServiceName()] = serviceObj
        else:
            raise WriterError("Wrong type of object passed to addService method", self.__filename)

    def addPort(self, portObj: Port):

        """
        Adds port to existing service

        Args:
            portObj (pManager.dataModels.models.Port): Port object

        Raises:
            WriterError: If the port object is not of type Port
        """

        if type(portObj) == Port:

            if self.__servicesList[portObj.getServiceName()].isPortsAdded:
                self.__servicesList[portObj.getServiceName()].addPortToService(portObj.getPortAsJson())
            else:
                self.__servicesList[portObj.getServiceName()].addPortToService(portObj.getPortAsJson())

            if self.__autoFlush: self.__flushFile()

        else:

            raise WriterError("Wrong type of object passed to addPort method", self.__filename)

    def getServiceList(self):

        """
        Returns dictionary of services

        Returns:
            dict: Dictionary of services
        """

        return self.__servicesList

    def writeToFile(self):

        """
        Writes service list to file
        """

        self.__flushFile()
from ..dataModels.models import Port
from ..dataModels.models import Service
from .fileParser import fileParser
import os

class WriterError(Exception):

    def __init__(self, message, filename=None):
        self.message = message
        self.filename = filename
        super().__init__(message)



class fileWriter:

    def __init__(self, filename, autoFlush = True):

        self.__portNumError = WriterError('Port should be number', filename)

        # Variables; consts
        self.__autoFlush = autoFlush
        self.__filename = filename # Shadows filename into class scope
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
                self.constructServiceObj(_, existingServicesList[_]['ports'], existingServicesList[_]['description'])

    def __flushFile(self):
        with open(self.__filename, 'w') as file:

            file.write(self.__fileHeader)

            for srv in self.__servicesList.keys():
                file.write(self.__serviceRecordMask.replace('$SERVICE', srv, 1)
                           .replace('$PORTSINFO', self.__servicesList[srv].generatePortConfig(), 1)
                           .replace('$SERVICEDESCRIPTION', self.__servicesList[srv].getServiceDescription(), 1) + '\n'
                           )

    def constructServiceObj(self, serviceName, serviceDescription ="No description", portList=None) -> Service:

        srv = Service(serviceName, portList, serviceDescription)
        self.addService(srv)
        return srv

    def bindPortToService(self, serviceName, portNum, portProto, openState, portDesc ="No description") -> Port:

        port = Port(serviceName, portNum, portProto, openState, portDesc)
        self.addPort(port)
        return Port(serviceName, portNum, portProto, openState, portDesc)

    def addService(self, serviceObj: Service):

        if type(serviceObj) == Service:
            self.__servicesList[serviceObj.getServiceName()] = serviceObj
        else:
            raise WriterError("Wrong type of object passed to addService method", self.__filename)

    def addPort(self, portObj: Port):

        if type(portObj) == Port:

            if self.__servicesList[portObj.getServiceName()].isPortsAdded:
                self.__servicesList[portObj.getServiceName()].addPortToService(portObj.getPortAsJson())
            else:
                self.__servicesList[portObj.getServiceName()].addPortToService(portObj.getPortAsJson())

            if self.__autoFlush: self.__flushFile()

        else:

            raise WriterError("Wrong type of object passed to addPort method", self.__filename)

    def getServiceList(self):

        return self.__servicesList

    def writeToFile(self):

        self.__flushFile()
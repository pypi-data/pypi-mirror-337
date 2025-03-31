from pManager.dataModels.models import Port
from pManager.dataModels.models import Service

class WriterError(Exception):

    def __init__(self, message, filename=None):
        self.message = message
        self.filename = filename
        super().__init__(message)



class fileWriter:

    def __init__(self, filename):

        self.__portNumError = WriterError('Port should be number', filename)

        # Variables; consts
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

    def constructPortObj(self, serviceName, portNum, portProto, openState, portDesc = "No description") -> Port:

        port = Port(serviceName, portNum, portProto, openState, portDesc)
        self.addPort(port)
        return Port(serviceName, portNum, portProto, openState, portDesc)

    def constructServiceObj(self, serviceName, portList=None, serviceDescription ="No description") -> Service:

        srv = Service(serviceName, portList, serviceDescription)
        self.addService(srv)
        return srv

    def addService(self, serviceObj: Service):

        if type(serviceObj) == Service:
            self.__servicesList[serviceObj.getServiceName()] = serviceObj
        else:
            raise WriterError("Wrong type of object passed to addService method", self.__filename)

    def addPort(self, portObj: Port):

        if type(portObj) == Port:
            self.__servicesList[portObj.getServiceName()].addPortToService(portObj.getPortAsJson())
        else:
            raise WriterError("Wrong type of object passed to addPort method", self.__filename)

    def getServiceList(self):

        return self.__servicesList

    def writeToFile(self):

        with open(self.__filename, 'w') as file:

            file.write(self.__fileHeader)

            for srv in self.__servicesList.keys():
                file.write(self.__serviceRecordMask.replace('$SERVICE', srv, 1)
                           .replace('$PORTSINFO', self.__servicesList[srv].generatePortConfig(), 1)
                           .replace('$SERVICEDESCRIPTION', self.__servicesList[srv].getServiceDescription(), 1) + '\n'
                           )
# pManager
Ports manager library. \
Works with .qpmgr files. \
Author: [Qwantman](https://github.com/Qwantman)

You can parse and write .qpmgr files using this library. \
It includes two classes: `fileParser` and `fileWriter`. \
`fileParser` is used for parsing .qpmgr files and extracting information. \
`fileWriter` is used for creating new .qpmgr files or editing existing ones.


## Links
[![PyPI Version](https://img.shields.io/pypi/v/portsManager.svg)](https://pypi.org/project/portsManager/) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/portsManager.svg) ![PyPI - License](https://img.shields.io/pypi/l/portsManager.svg)


## Installation

    pip install portsManager


## Usage

### Parser

    from pManager import fileParser
    parser = fileParser("file.qpmgr")

    # Get opened & closed ports
    openedPorts = parser.getOpenedPorts()
    closedPorts = parser.getClosedPorts()

    # Get list of services
    servicesList = parser.getServicesList()

    # Print beautifully-formated services list
    for _ in servicesList:
        print(f'{parser.getBeautifuledInfoByService(i)}\n')


### Writer

    from pManager import fileWriter

    # Setting up writer
    writer = fileWriter("file.qpmgr", autoFlush = True)

    # Add new service
    # "ServiceName" will be used as a key to bind ports
    writer.constructServiceObj("ServiceName", "ServiceDescription")  

    # Add port to service. 
    # On port adding, file'll be flushed with autoFlush = True
    writer.bindPortToService(
        serviceName = "ServiceName", 
        portNum = 80, 
        portProto = "TCP", 
        openState = True, 
        portDesc = "HTTP server"
    )

    # Or, with autoFlush = False
    writer.writeToFile()

    
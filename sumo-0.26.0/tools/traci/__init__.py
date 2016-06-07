# -*- coding: utf-8 -*-
"""
@file    __init__.py
@author  Michael Behrisch
@author  Lena Kalleske
@author  Mario Krumnow
@author  Daniel Krajzewicz
@author  Jakob Erdmann
@date    2008-10-09
@version $Id: __init__.py 20433 2016-04-13 08:00:14Z behrisch $

Python implementation of the TraCI interface.

SUMO, Simulation of Urban MObility; see http://sumo.dlr.de/
Copyright (C) 2008-2016 DLR (http://www.dlr.de/) and contributors

This file is part of SUMO.
SUMO is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""
from __future__ import print_function
from __future__ import absolute_import
import socket
import time

from .domain import _defaultDomains
from .connection import Connection, _embedded
from .exceptions import TraCIException
from . import _inductionloop, _multientryexit, _trafficlights
from . import _lane, _vehicle, _vehicletype, _person, _route, _areal
from . import _poi, _polygon, _junction, _edge, _simulation, _gui

_connections = {}


def _STEPS2TIME(step):
    """Conversion from time steps in milliseconds to seconds as float"""
    return step / 1000.


def connect(port=8813, numRetries=10, host="localhost"):
    """
    Establish a connection to a TraCI-Server and return the
    connection object. The connection is not saved in the pool and not
    accessible via traci.switch. It should be safe to use different
    connections established by this method in different threads.
    """
    for wait in range(1, numRetries + 2):
        try:
            return Connection(host, port)
        except socket.error:
            time.sleep(wait)


def init(port=8813, numRetries=10, host="localhost", label="default"):
    """
    Establish a connection to a TraCI-Server and store it under the given
    label. This method is not thread-safe. It accesses the connection
    pool concurrently.
    """
    _connections[label] = connect(port, numRetries, host)
    switch(label)
    return getVersion()


def isEmbedded():
    return _embedded


def simulationStep(step=0):
    """
    Make a simulation step and simulate up to the given millisecond in sim time.
    If the given value is 0 or absent, exactly one step is performed.
    Values smaller than or equal to the current sim time result in no action.
    """
    return _connections[""].simulationStep(step)


def getVersion():
    return _connections[""].getVersion()


def close():
    _connections[""].close()


def switch(label):
    _connections[""] = _connections[label]
    for domain in _defaultDomains:
        domain._setConnection(_connections[""])

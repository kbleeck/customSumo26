function returnedValue = getUniversal(varID, polygonID)
%getUniversal An internal function to send the get command and read the 
%variable value.

%   Copyright 2015 Universidad Nacional de Colombia,
%   Politecnico Jaime Isaza Cadavid.
%   Authors: Andres Acosta, Jairo Espinosa, Jorge Espinosa.
%   $Id: getUniversal.m 20 2015-03-02 16:52:32Z afacostag $

import traci.constants
global polygonSubscriptionResults

if isempty(polygonSubscriptionResults)
    returnValueFunc = traci.RETURN_VALUE_FUNC.polygon;
else
    returnValueFunc = polygonSubscriptionResults.valueFunc;
end

% Prepare the outgoing message and read the response. The result variable
% is a traci.Storage object
result = traci.sendReadOneStringCmd(constants.CMD_GET_POLYGON_VARIABLE,varID,polygonID);
handleReturValueFunc = str2func(returnValueFunc(varID));

% Use the proper method to read the variable of interest from the result
returnedValue = handleReturValueFunc(result);
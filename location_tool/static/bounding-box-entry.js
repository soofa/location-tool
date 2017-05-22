var axios = require('axios');

module.exports = (function(axios) {
    var logger = function(string) {
        console.log('BBE: ' + string);
    };

    var payload = function(data) {
        return data;
    };

    var create = function(data) {
        return axios.post('/bounding-boxes', data);
    };

    var handleDrawEvent = function(event) {
        return {
            coordinates: {
                northEast: event._bounds._northEast,
                southWest: event._bounds._southWest,
            }
        }
    };

    return {
        logger: logger,
        handleDrawEvent: handleDrawEvent,
        payload: payload,
        create: create,
    };
}(axios));

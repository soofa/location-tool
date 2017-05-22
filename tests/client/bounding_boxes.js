var assert = require('chai').assert;
var expect = require('chai').expect;
var moxios = require('moxios');

var BBE = require('../../location_tool/static/bounding-box-entry.js');

describe('Create a bounding box', function() {
    describe('payload', function() {
        it('ensures fields are in the right schema', function() {
            data = {
                'name': '',
                'coordinates': {
                    'northwest': { 'lat': 1.0, 'lng': -2.0 }
                }
            };
            expect(BBE.payload(data)).to.equal(data);
        });
    });

    describe('handleDrawEvent', function() {
        it('transforms event data into POST body', function() {
            var fakeEvent = {
                _bounds: {
                    _northEast: { lat: 42.38, lng: -71.10 },
                    _southWest: { lat: 42.37, lng: -71.12 }
                }
            };
            var postData = BBE.handleDrawEvent(fakeEvent);
            expect(JSON.stringify(postData)).to.equal(JSON.stringify({
                coordinates: {
                    northEast: fakeEvent._bounds._northEast,
                    southWest: fakeEvent._bounds._southWest,
                }
            }));
        });
    });

    describe('create', function() {
        beforeEach(function() {
            moxios.install();
        });

        afterEach(function() {
            moxios.uninstall();
        });

        it('issues POST /bounding-boxes', function(done) {
            var data = {
                'name': 'Test',
                'coordinates': {
                    'northwest': { 'lat': 1.0, 'lng': -2.0 }
                }
            };
            BBE.create(data);
            moxios.wait(function () {
                let request = moxios.requests.mostRecent()
                expect(request.config.data).to.equal(JSON.stringify(data));
                done();
            });
        });

        it('handles response data', function() {
            data = {
                'name': 'Test',
                'coordinates': {
                    'northwest': { 'lat': 1.0, 'lng': -2.0 }
                }
            };
            moxios.stubOnce('post', '/bounding-boxes', {
                status: 201,
                responseText: "{ 'name': 'Test' }"
            });

            var result = BBE.create(data);
            return result.then(function(response) {
                expect(response.status).to.equal(201);
                expect(response.data).to.equal("{ 'name': 'Test' }");
            });
        });
    });
});

var path = require('path');

module.exports = {
    entry: './location_tool/static/index.js',
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'location_tool/static')
    }
};

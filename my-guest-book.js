console.log('starting my log book');
const AWS = require('aws-sdk');
const docClient = new AWS.DynamoDB.DocumentClient({region:'us-east-1'});

exports.handler = function(e, ctx, callback) {

    var params = {
        Item : {
            posted : Date.now(),
            post : "A user post"
        },
        TableName : 'MyGuestBookDynDbTable'
    }

    docClient.put(params, function (err, data) {
        if (err) {
            callback(err, null);
        } else {
            callback(null, data);
        }
    });
}

// globals
const AWS = require('aws-sdk');
const SQS = new AWS.SQS({
		"region" : "us-east-1", 
        "apiVersion" : "2012-11-05"
});
const QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/672312526406/MyFifoQueue.fifo";

    //console.log('Received event:', JSON.stringify(event, null, 2));

    // message handling functions

    processMessage = function(msgsObj) {
        console.log(JSON.stringify(msgsObj));
        let msgs = msgsObj.Messages;
        
        if (msgs && msgs.length > 0) {
            console.log("Received " + msgs.length + " messages");
            let msgHandle = msgs[0].ReceiptHandle;
            console.log("Received message with id " + msgs[0].MessageId);
            deleteMessage(msgHandle);
        } else {
            console.log("Received no messages");
        }
    };

    deleteMessage = function(msgHandle) {
        let msgId = {};
        msgId.QueueUrl = QUEUE_URL;
        msgId.ReceiptHandle = msgHandle;
        let myDeletePromise = SQS.deleteMessage(msgId).promise();
        myDeletePromise.then(
            console.log("Removed message OK")
        ).catch(
            err => console.log(err, err.stack)
        )
    };

    processError = function(err) {
        if (!err.includes("The receipt handle has expired."))
        {
            console.log(err, err.stack);
        } else {
            console.log("The message was already gone");
        }
    };

    let msgParams = {};
    msgParams.QueueUrl = QUEUE_URL;
    msgParams.AttributeNames = ["All"];
    let messageAttributeNames = [];
    messageAttributeNames[0] = "emp_id";
    messageAttributeNames[1] = "emp_title";
    msgParams.AttributeNames =messageAttributeNames;

    let myReceivePromise = SQS.receiveMessage(msgParams).promise();
    myReceivePromise.then(
        msgsObj => processMessage(msgsObj)
    ).catch(
        err => processError(err)
    );

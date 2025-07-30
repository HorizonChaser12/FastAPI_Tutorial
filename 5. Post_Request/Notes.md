# Post
- Post is a HTTP Request form which is sent by the client to the server when it wants to send any kind of data to the server. Mostly we send JSON formatted data with a request body to the server.
- While request body is the portion of an HTTP Request that contains data sent by the client to the server. It is typically used in HTTP methods such as POST or PUT to transmit structured data (e.g. JSON, XML) for the purpose of creating or updating resources on the server. The server parses the request body to extract the necessary information and perfom the intended operation.
- The next step is to validate the data using Pydantic.
- Last step would be adding the new record to our database i.e our patient.json file.

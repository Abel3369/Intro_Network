# COSC4705 Spring 2024 Homework 2

Please see the [homework description](https://georgetown.instructure.com/courses/183077/assignments/966043) for a full-write up.

## Starter and sample code

This repository contains the following:

* README.md: this file
* [client.py](client.py): the beginnings of your BasicIM client
* [server.py](server.py): the beginnings of your BasicIM server
* [message.py](message.py): implements an UnencryptedIMMessage object, which is useful for the client
* [samples.py](samples.py): provides some examples of calling methods on the UnencryptedIMMessage object

## Testing your client

The teaching staff is running a BasicIM client at playground.netsecurity.dev.  We'll do our best to keep this service alive.

You can test your client by running:

```
python3 client.py -s playground.netsecurity.dev -n mynickname
```
(please don't actually use "mynickname")

Important caveat: Please keep in mind that multiple students may be testing their clients at once.  That could cause problems.  Suppose John Q. Student has a buggy client implementation and doesn't properly use network-byte ordering for his length.  Then, when he *thinks* he's specifying that the length of the JSON object is 100 bytes, he might accidentally be conveying that it's gigabytes large.  (That's why you should use the `serialize` function defined in [message.py](message.py#L61).)  This might cause your perfectly functioning BasicIM client to wait indefinitely for input.

In short, your client may be affected by others' buggy clients, if they are using the server on playground.netsecurity.dev at the same time you are.  

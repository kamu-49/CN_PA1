CSEE4119 Computer Networks Coding Assignment #1

name: Cameron Coleman
UNI: cc4535

Command Line Instruction Exaample:
SERVER: python3 chatappr.py -s -sport-
CLIENT: python3 chatapp.py -c -username- -IP_addr- -sport- -cport-


 Documentation Information:
 I have simply used the chatapp python file. I was unfortuantely no where close to finishing this homework, which is what I would like to talk to the professor about, which I will talk about in a little bit. There is a "attempts" folder in here as well. I worked really really hard on this and I feel like it's only appreciated (by me) if I were to keep it in the folder, but it is not at all necessary to look at. It's mainly just to make me feel like I didn't give up on this hw.


 Program Features:
 Although incomplete, my program utilized a few features, such as time.sleep in order to slow down the ACK signal. I utilzie test cases as well that help prevent special cases from happening, such as maybe the user input is too small for information to be gathered properly.

 There were a few other features I wanted to implement as well, including the ones that I had to do for homework. I wanted to test to see if there were any unnecessary gaps in between signals that may have slowed down or overloaded the program in a situation where there were multiple users, which is the biggest reason why I chose to implement multithreading. I also wanted to attempt to see if I can limit the amount of signals I sent as well, but I did not have time to go back and fix everything the way I wanted to. I unfortunately could not implement the group chat feature due to my lack of time and lack of ability to get through user input, which will be talked about later.


 Known stuff:
 One of the biggest hurdles that I still cannot get over is the user input. I was having difficulties understanding what the issues I was having in terms of user input. There were certain csituations, specifically from the demo given during recitation, where the user input worked perfectly. I hypothesized that the reason why was either because of the act of receiving the ACK signal from the server or the fact that the client was properly waiting to receive a signal. Those are two different things, especially since the client is able to wait for and receive signals from other clients. I have been working on the user input since Sunday, I tried to go to in person office hours as well as ask peers for help, but I was not able to get enough information for a breakthrough. Therefore, I have been stuck on the registration/de-registration portion of this homework this whole time since I was unable to do proper testing.

 That is the main bug that I am having, which prevents me from testing other bugs. A lot of bugs that I was having were due to the speed of the clashing server and client sockets. They were able to avoid each other by slowing each side down with sleep(). 

 I constructed this file in Python, so I do not have a Makefile to construct.
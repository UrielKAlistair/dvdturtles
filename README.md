# dvdturtles
The first Abhiyaan ROS Task


The first one was accomplished by swapping the sign of the velocity once the position exceeded the wall coordinate, providing the turtle was moving towards the wall.
The second one turned out to be much more intersting. Since I needed to continually spawn new turtles, I had to get rid of all global variables, and ended up making classes.
I made a class called Ears which is an object that has just one function that I use for callback. I can access the parameters of each turtle by giving each turtle an ears object for callback and then getting the attributes of that object.
I also defined a complete turtle object that initiates  its own ears object, spawns itself if it doesnt exist already, and sets up its own publisher to velocity. All these are achieved using attribute objects. 
The tutle object has an update velocity method that calls a summon function every time it hits a wall. The summon function will add a new turtle object to a global list of turtles, and the init of the turtle will be self sufficient to set it up. (I stop summoning after 16 turtles)
All that I need to do is run over the all turtles list in a for loop, and call their update velocity methods. 
The code looks like it ought to work, the only problem is that it doesn't. Two turtles just vibe to some crazy music and spawn a gazillion bois who bounce properly. 
You can find a short video of some almost hilarious glitching and my code in this repository.

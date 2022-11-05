# Microwave-OOD
Python

Using an Objected Oriented approach, design and implement a Microwave Object that 
replicates a modern day microwave.
The below image is simply an example of a microwave and is not indicative that you 
need to implement this exact microwave. Overall, be as creative as you want but try not 
to spend more than 3 hours on this.
Required minimum functionality within the class:
• Timer
• Start Button
• Stop Button 
Please write a main function as well to demonstrate some of the object’s functionality

Example:
    # Create a microwave object
    microwave = Microwave(CloseState())

    EXAMPLE_INTERVAL = 10

    print("1.A basic work flow")
    food_1 = Bread()
    microwave.open_door()
    microwave.put(food_1)
    microwave.close_door()
    microwave.set_time(5)
    microwave.start()
    time.sleep(8)
    microwave.open_door()
    microwave.take_out()
    microwave.close_door()

    time.sleep(EXAMPLE_INTERVAL)
    print()

    print("2.Stop while cooking")
    food_2 = Bread()
    microwave.open_door()
    microwave.put(food_2)
    microwave.close_door()
    microwave.set_time(60)
    microwave.start()
    time.sleep(5)
    microwave.add_30_sec()
    time.sleep(5)
    microwave.stop()
    microwave.open_door()
    microwave.take_out()
    microwave.close_door()

    time.sleep(EXAMPLE_INTERVAL)
    print()

    print("3.Invalid operations")
    food_3 = Bread()
    microwave.open_door()
    microwave.open_door()
    microwave.put(food_3)
    microwave.put(food_2)
    microwave.close_door()
    microwave.set_time(60)
    microwave.start()
    time.sleep(5)
    microwave.open_door()
    microwave.close_door()
    microwave.start()
    time.sleep(5)
    microwave.stop()
    microwave.close_door()
    microwave.open_door()
    microwave.take_out()

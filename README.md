Project Description: An application to build an optimized trip itinerary based on start city, end city and dates provided by the user. Based on the start city, the application will show the nearest tourist cities with distances from the start city. Once the user selects a city, it will show the next list of cities to be added to the itinerary with distances and so on. Based on the user’s selection of cities, the app gives an optimized trip route. 

Data required: A list of tourist cities in the world can be found online. The latitude and longitude for these cities can be generated using a geocoding API and Python library that gives distance based on geolocation and can be used to calculate the distance between these cities. Once the list of cities is created, the optimized route for the selected cities can be generated using the Networkx library. In the end, the user should get an optimized trip itinerary with a list of cities to visit and dates along with the total distance traveled.

Execution Plan
Week 4: Generate an outline of the project workflow and create a list of tourist cities in the world
Week 5: Generate geolocation information (latitude, longitude) and distance between cities for the list of tourist cities
Week 6: Develop the script that calculates the shortest path that covers all selected cities
Week 7: Start building the user interface and finish the part that accepts the start city, end city, and trip dates from the user
Week 8: Finish the part of UI that shows nearby cities for selected cities along with distances and lets the user make a selection
Week 9: Complete building the final UI that shows the optimized itinerary with the start city, end city, and all selected cities with the total distance traveled.



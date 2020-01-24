#Name:      Group Number:
from turtle import *
from itertools import cycle
from tkinter import *
import codecs

#Constants used throughout the program
COLORS = cycle(['yellow', 'green', 'red', 'cyan', 'orange', 'blue', 'mediumpurple'])
RADIUS = 175
LABEL_RADIUS = RADIUS * 1.33
TITLE_RADIUS = RADIUS * 1.5
FONTSIZE = 12
SMALLFONTSIZE = 8
HEADERFONTSIZE = 17
FONT = ("Calibri", FONTSIZE, "bold")
SMALLFONT = ("Calibri", SMALLFONTSIZE, "bold")
HEADERFONT = ("Calibri", HEADERFONTSIZE, "bold")
# Import functions from turtle and codecs
# codecs imported to decode utf-16 encoding used on the text.
# Itertools imported to assist in color selection
# Assumptions made:
# -There is no missing data entry in the dataset
# -The relative format of the dataset does not change
try:
    with codecs.open("Mini Project Text.txt","r",encoding = "utf-16") as f:
        #Data Organisation stage
        data = f.read()
        raw = data.splitlines()
        title = raw.pop(0)
        headers = raw.pop(0).split("; ")
except OSError:
    # 'File not found' error message.
    print("File not Found")
countryNames = []
worldStatistics = {} # Dictionary to store the world statistics
worldStatistics[headers[2]] = 0 # Key-Value Pair tracking 2018 stats
worldStatistics[headers[3]] = 0 #  Key-Value Pair tracking 2019 stats
worldStatistics[headers[5]] = 0 #  Key-Value Pair tracking increase in population stats
worldStatistics[headers[6]] = 0 #  Key-Value Pair tracking percentage of total population stats
worldStatistics[headers[7]] = [] # Key-Value Pair tracking the list of continents
worldStatistics["totalNumber"] = len(raw)
# Data is stored in the program as a Dictionary with key- rank value-> entry in the .txt file representing the data in the table
processableData = {}
for rawString in raw:
    newEntry = rawString.split("; ")
    processedEntry = [int(newEntry[0]),newEntry[1],int(newEntry[2]),int(newEntry[3]),float(newEntry[4]),int(newEntry[5]),float(newEntry[6]),newEntry[7]]
    worldStatistics[headers[2]] += processedEntry[2]
    worldStatistics[headers[3]] += processedEntry[3] 
    worldStatistics[headers[5]] += processedEntry[5]
    countryNames.append(newEntry[1])
    if worldStatistics[headers[7]].count(processedEntry[7]) == 0:
        worldStatistics[headers[7]].append(processedEntry[7])
    processableData[processedEntry[0]] = processedEntry

#Piechart charter
def piechart():
    continentalSum = {}
    for continent in worldStatistics[headers[7]]:
        continentPopulation = sum(map(lambda y: processableData[y][3],filter(lambda x: processableData[x][7] == continent,range(1,worldStatistics["totalNumber"]+1))))
        continentalSum[continent] = continentPopulation
    screen = Screen()
    screen.title('Piechart of World Population by Continent')
    RADIUS = 175
    LABEL_RADIUS = RADIUS * 1.33
    TITLE_RADIUS = RADIUS * 1.5


    # The pie slices
    toFill = list(continentalSum.items())
    total = sum(fraction for _, fraction in continentalSum.items())  # data doesn't sum to 100 so adjustment is required
    piechart = Turtle()
    piechart.penup()
    piechart.sety(-RADIUS)
    piechart.pendown()
    piechart.speed('fastest')
    piechart.hideturtle()
    for _, fraction in toFill:
        piechart.fillcolor(next(COLORS))
        piechart.begin_fill()
        piechart.circle(RADIUS, fraction * 360 / total)
        position = piechart.position()
        piechart.goto(0, 0)
        piechart.end_fill()
        piechart.setposition(position)

    # The labels of each segment

    piechart.penup()
    piechart.sety(-LABEL_RADIUS)

    for label, fraction in toFill:
        piechart.circle(LABEL_RADIUS, fraction * 360 / total / 2)
        piechart.write(label+"\n"+ str((fraction))+"\n"+ str(100*round(fraction/total,2))+"%", align="center", font=FONT)
        piechart.circle(LABEL_RADIUS, fraction * 360 / total / 2)
    piechart.penup()
    piechart.sety(-TITLE_RADIUS)

    # To Caption the Pie Chart
    piechart.circle(TITLE_RADIUS, 0.5 * 360)
    piechart.write("Piechart of World Population by Continent", align="center", font=HEADERFONT)
    piechart.circle(TITLE_RADIUS, 0.5 * 360)
    piechart.circle(1.7, 0)
    piechart.write("Total World Population: "+str(worldStatistics[headers[3]]), align="center", font=HEADERFONT)
    piechart.circle(1.7, 0)
    # Opens a Window to view the Piechart and to initialise the Turtle Drawing

    screen.mainloop()

def queryString(query):
    #Intermediate step to parse the data and flag out if there is a issue
    relevantData = []
    for country in countryNames:
        if country.count(query):
            relevantData.append((country,countryNames.index(country)))
    tableData = list(map(lambda x: processableData[x[1]+1],relevantData))
    if len(relevantData) == 0:
        print(f"Your Query '{query}' has not returned any result")
        return 0
    else:
        return tableData

def barGraphCharter(data,mode):
    #Bar Charter for Both population increase and population decrease
    ### Create and Setup the Window ###
    n = len(data)
    title = f"Top {n} Population Decrease from 2018-2019 by Percentage" if mode == True else f"Top {n} Population Increa" \
                                                                                             f"se from 2018-2019 by Percentage"
    xmax = min(data.values()) if mode ==True else max(data.values())
    window = Screen()
    window.title(title)
    height = ((10 + FONTSIZE/2)*1/n+(30 - FONTSIZE/2)*1/n+5)*2*n + 100
    window.setup(750, height)  # specify window size (width is 750)
    turtle = Turtle()
    turtle.hideturtle()
    turtle.speed('fastest')
    turtle.penup()
    turtle.setpos(-225, -(height / 2) + 50)  # Moves Cursor down to origin point
    turtle.pendown()

     # draw x-axis and ticks
    xtick = 400 / 9

    for i in range(1, 10):
        turtle.forward(xtick)
        xv = float(xmax / 9 * i)
        turtle.right(90)
        turtle.write('%.1f' % xv, move=False, align="center", font=FONT)
        turtle.forward(10)
        turtle.backward(10)
        turtle.left(90)
    turtle.penup()
    turtle.setpos(-225, -(height / 2) + 50)
    turtle.pendown()
    turtle.left(90)
    turtle.forward(10)

    # draw bar and fill color
    pixel = xmax / 400
    recs = []  # bar height
    for value in data.values():
        recs.append(value / pixel)


    for i, rec in enumerate(recs):
        turtle.color('black')
        turtle.forward(5)
        turtle.right(90)
        turtle.begin_fill()
        turtle.forward(rec)
        turtle.left(90)
        turtle.forward(3+(30 - FONTSIZE/2)*1/n)
        turtle.write('  ' + str(round(rec * pixel,2)), move=False, align="left", font=SMALLFONT)
        #Labeling the end of the bar with the value, rounding to 2 dp to prevent floating point error
        turtle.forward(2+(10 + FONTSIZE/2)*1/n)
        turtle.left(90)
        turtle.forward(rec)
        turtle.color(next(COLORS))
        turtle.end_fill()
        turtle.right(90)
    turtle.color('black')
    turtle.forward(30)
    turtle.penup()
    turtle.right(90)
    turtle.forward(300)
    turtle.pendown()
    turtle.write(title,move=False, align="center", font=HEADERFONT)
    turtle.penup()
    turtle.setpos(-225, -(height / 2) + 60)
    turtle.left(90)
    #For alignment of Labels to bar graphs, total width of bargraph is calculated.
    total = (10 + FONTSIZE/2)*1/n+(30 - FONTSIZE/2)*1/n+5
    # draw y-axis and labels
    turtle.pendown()
    #Lable for each graph
    for key in data:
        turtle.forward(5)
        turtle.forward(total/2)
        turtle.write('  ' + key, move=False, align="right", font=SMALLFONT)
        turtle.forward(total/2)

    turtle.forward(40)
    turtle.write('Countries', move=False, align="right", font=FONT)
    turtle.st()

    ### Tell the window to wait for the user to close it ###
    window.mainloop()

def tableMaker(data):
    window = Screen()
    window.title("Table")
    height = 40 + len(data) * 20  # height of 20 per row, hence, 20 for the Title and 20 for the headers of each table
    width = 800
    window.setup(width, height)  # width of each entry is 800
    window.setworldcoordinates(0, 0, width, height)
    turtle = Turtle()
    turtle.clear()
    turtle.speed("fastest")
    turtle.hideturtle()
    turtle.penup()
    turtle.goto(20, height - 20)
    turtle.write(("Query Table"), font=HEADERFONT)
    turtle.goto(0, turtle.ycor() - 20)
    xlocation = []
    ylocation = []
    for label in headers:
        turtle.forward(20)
        xlocation.append(turtle.xcor())
        turtle.write(label, move=True, align='left', font=SMALLFONT)
        if label != headers[1]:
            turtle.forward(30)
        else:
            turtle.forward(120)
    turtle.goto(0, turtle.ycor() - 20)
    # storing data for the drawing of lines on the table
    ylocation.append(height - 20)
    ylocation.append(height - 40)
    #Entering the data into the columns
    for entry in data:
        ylocation.append(turtle.ycor())
        for i in range(len(entry)):
            turtle.setx(xlocation[i])
            turtle.write(entry[i], move=True, align='left', font=SMALLFONT)
        turtle.goto(0, turtle.ycor() - 20)
    #drawing the lines for x axis
    for xcord in xlocation:
        turtle.goto(xcord - 4, height - 20)
        turtle.pendown()
        turtle.goto(xcord - 4, 0)
        turtle.penup()
    turtle.goto(width-4,height-20)
    turtle.pendown()
    turtle.goto(width-4,0)
    turtle.penup()
    #drawing the lines for y axis
    for ycord in ylocation:
        turtle.goto(16, ycord - 2)
        turtle.pendown()
        turtle.goto(width, ycord - 2)
        turtle.penup()

    window.mainloop()
def negativeGrowthByPercentage(topRanking):
    if topRanking == 0 or type(topRanking)!= int:
        print("Invalid Input, please try again")
        return None
    #Will Reject Data that is not negative data
    relevantData = list(processableData.items())
    relevantData.sort(key = lambda x: x[1][6])
    relevantData = relevantData[:topRanking]
    #Graphing data in [(name,percentage decline)]
    graphableData = dict(list(filter(lambda y: y[1] <0,map(lambda x:(x[1][1],round(x[1][6],2)),relevantData))))
    barGraphCharter(graphableData,True)

def positiveGrowthByPercentage(topRanking):
    if topRanking == 0 or type(topRanking)!= int:
        print("Invalid Input, please try again")
        return None
    #Will Reject Data that is not positive data
    relevantData = list(processableData.items())
    relevantData.sort(key = lambda x: x[1][6],reverse=True)
    relevantData = relevantData[:topRanking]
    #Graphing data in [(name,percentage increase)]
    graphableData = dict(list(filter(lambda y: y[1] >0,map(lambda x:(x[1][1],round(x[1][6],2)),relevantData))))
    barGraphCharter(graphableData,False)

def comparisonGraph(country):
    index = countryNames.index(country)
    #Population of largest country  which is China
    largestCountry = processableData[1][3]
    countryPopulation = processableData[index+1][3]
    #computing the scale of the country's Population
    numberOfCountry = 1
    number = countryPopulation
    while number<largestCountry:
        numberOfCountry += 1
        number = countryPopulation*numberOfCountry
    numberOfCountry = numberOfCountry-round((countryPopulation/largestCountry),2)
    scale = 1 if numberOfCountry == 0 else numberOfCountry
    comparator(country,scale)
def comparator(country, scale):
    number = scale if scale < 30 else 30
    label = scale
    largest = processableData[1][1]
    title = f"Comparison Scale of {country} to {largest}"
    window = Screen()
    window.title(title)
    height = 800
    width = 900
    ymax = processableData[1][3]
    window.setup(width, height)  # each bar with a width of 40
    window.setworldcoordinates(0, 0, width, height)
    turtle = Turtle()
    turtle.speed("fastest")
    turtle.hideturtle()
    turtle.penup()
    turtle.goto(80, 20)
    turtle.pendown()
    turtle.goto(840, 20)
    turtle.goto(80, 20)
    turtle.left(90)
    ytick = 700 / 9 #Scaling the y axis to conform to the data
    for i in range(1, 10):
        turtle.forward(ytick)
        yint = float(ymax / 9 * i)

        turtle.right(90)
        turtle.write('%d' % round(yint, -5), move=False, align="right", font=FONT) #rounded to minimum 100000
        turtle.forward(10)

        turtle.backward(10)

        turtle.left(90)
    turtle.forward(40)
    turtle.stamp()
    turtle.write("Population", move=False, align="right", font=FONT)
    #Drawing the representative bar of China's population
    turtle.penup()
    turtle.goto(60 + 155, 20)
    turtle.pendown()
    turtle.begin_fill()
    turtle.forward(700)
    turtle.right(90)
    turtle.forward(40)
    turtle.write(f"{largest}", move=False, align="center", font=FONT)
    turtle.forward(40)
    turtle.right(90)
    turtle.forward(700)
    turtle.color("red")
    turtle.end_fill()
    turtle.color('black')
    turtle.goto(60 + 575, 20)
    turtle.right(180)
    scale = 700 / number
    turtle.pendown()
    while number > 0:
        number -= 1
        if number > 0:#Creates a full box representing the population of the nation as a unit in comparison with China
            turtle.color("black")
            turtle.begin_fill()
            turtle.forward(scale)
            turtle.right(90)
            turtle.forward(80)
            turtle.right(90)
            turtle.forward(scale)
            turtle.right(90)
            turtle.forward(80)
            turtle.color(next(COLORS))
            turtle.end_fill()
            turtle.right(90)
            turtle.color("black")
            turtle.forward(scale)
        else:  # The last box to be scaled to fit the comparison with China
            lastBox = number+1
            turtle.color("black")
            turtle.begin_fill()
            turtle.forward((scale * lastBox))
            turtle.right(90)
            turtle.forward(40)
            if label > 30:
                turtle.write(country + f": {label} bars scaled to 30", move=False, align="center", font=FONT)
            else:
                turtle.write(country + f": {label}", move=False, align="center", font=FONT)
            turtle.forward(40)
            turtle.right(90)
            turtle.forward((scale * lastBox))
            turtle.color(next(COLORS))
            turtle.end_fill()
            turtle.color("black")
            turtle.forward(80)
    turtle.penup()
    turtle.goto(500, 750)
    turtle.write(f"We would need {label} times the population of {country}, \nto equal the population of China",
                 move=False, align="center", font=FONT)

    window.mainloop()

#GUI Function using Tkinter
# Window for main program
def gui():
    window = Tk()
    window.title("My World Population Grapher")
    window.configure(background="white")
    Label(window, text="This is the Turtle Grapher for World Population Data 2019", bg="white", fg='black',
          font="none 20 bold").grid(row=1, column=0, sticky=W)

    Label(window, text="Please select the function you wish to use", bg="white", fg='black', font="none 20 bold").grid(
        row=2, column=0, sticky=W)


    # Functions used for user interaction
    def piechartMaker():
        #When button is pressed, the piechartmaker opens a popup which plots the graph
        try:
            piechart()
        except Terminator:
            piechart()

    def barChartGUI():
        # Each item in the GUI is placed in sequence from top left of window to bottom of window
        newWindow = Tk()
        newWindow.title("Barchart maker")
        newWindow.configure(background="white")
        # Title
        Label(newWindow, text="This is a Barchart plotter for Population Decrease from Year 2018-2019", bg="white",
              fg='black', font="none 20 bold").grid(row=1, column=0, sticky=W)
        # Instructions
        Label(newWindow, text="Please enter a number into the textbox below and click on the submit button", bg="white",
              fg='black', font="none 20 bold").grid(
            row=2, column=0, sticky=W)
        textentry1 = Entry(newWindow, width=20, bg="white")
        textentry1.grid(row=3, column=0, sticky=W)
        # Outputs Error Message if necessary for both positive and negative functions
        errorM = Text(newWindow, width=75, height=4, wrap=WORD, background="white")
        errorM.grid(row=5, column=0, columnspan=2, sticky=W)
        Label(newWindow, text="This is a Barchart plotter for Population Increase from Year 2018-2019", bg="white",
              fg='black', font="none 20 bold").grid(row=6, column=0, sticky=W)
        #Text Box Entry for Graph of Positive Percentage Change in population
        textentry2 = Entry(newWindow, width=20, bg="white")
        textentry2.grid(row=7, column=0, sticky=W)
        #Label for the exiting of the child popup GUI
        Label(newWindow, text="click to exit", bg="white", fg="black", font="none 20 bold").grid(row=10, column=0,
                                                                                                 sticky=W)
        # Interactive Functions for buttons to activate
        def activateNegativeGrapher():
            entered = textentry1.get()
            errorM.delete(0.0, END)
            try:
                entered = int(entered)
            except ValueError:

                errorM.insert(END, f"You have entered a invalid input: {textentry1.get()}")
            except entered > 200:
                errorM.insert(END, f"You have entered too high of a number: {textentry1.get()}")
            else:
                try:
                    negativeGrowthByPercentage(entered)
                except Terminator:
                    negativeGrowthByPercentage(entered)

        def activatePositiveGrapher():
            entered = textentry2.get()
            errorM.delete(0.0, END)
            try:
                entered = int(entered)

            except ValueError:

                errorM.insert(END, f"You have entered a invalid input: {textentry2.get()}")
            else:
                try:
                    positiveGrowthByPercentage(entered)
                except Terminator:
                    positiveGrowthByPercentage(entered)

        def close_window():
            newWindow.destroy()

        Button(newWindow, text='Submit',bg="white", fg='black', font="none 20 bold", width=6, command=activateNegativeGrapher).grid(row=4, column=0, sticky=W)
        Button(newWindow, text='Submit',bg="white", fg='black', font="none 20 bold", width=6, command=activatePositiveGrapher).grid(row=8, column=0, sticky=W)

        Button(newWindow, text="Exit",bg="white", fg='black', font="none 20 bold", width=14, command=close_window).grid(row=10, column=0, sticky=E)

        # Internal close window function with a button

        newWindow.mainloop()

    def close_window():
        window.destroy()
        exit()


    def findMatches():
        entered = query.get()
        errorM.delete(0.0, END)
        #To do Exception Handling of Queries
        if not entered.isalpha():
            errorM.insert(END, f"Query Function:\nYou have entered a invalid input: {query.get()}\nPlease enter a alphabetical string")
        else:
            data = queryString(str(entered))
            if data == 0:
                errorM.insert(END, f"Query Function:\nYou have entered a invalid query: {query.get()}\nPlease enter a valid query string")
            else:
                try:
                    tableMaker(data)
                except Terminator:
                    tableMaker(data)
    def comparisonGraphMaker():
        entered = compareMe.get()
        errorM.delete(0.0, END)
        if entered not in countryNames:
            errorM.insert(END, f"Comparison Graph:\nYou have entered a invalid country: {query.get()}\nPlease check your spelling,"
                               f" or use the Query Function to find a matching country")
        else:
            try:
                comparisonGraph(entered)
            except Terminator:
                comparisonGraph(entered)

    #User Interactions
    Button(window, text="Piechart of Population by Continent",bg="white", fg='black', font="none 20 bold", width=35, command=piechartMaker).grid(row=4, column=0,
                                                                                                     sticky=W)
    Button(window, text="Make a Barchart of Population Increase/Decrease by Percentage",bg="white", fg='black', font="none 20 bold", width=52,
           command=barChartGUI).grid(row=6, column=0, sticky=W)
    Label(window, text="Please enter a alphabetical string in the text box to query by Country", bg="white",
          fg='black', font="none 20 bold").grid(row=7, column=0, sticky=W)
    #Text Box for Querying the string.
    query = Entry(window, width=20, bg="white")
    query.grid(row=8, column=0, sticky=W)
    #Button for Querying the Country Names matching a certain string.
    Button(window, text="Make a Table of Countries with a query",bg="white", fg='black', font="none 20 bold", width=40, command=findMatches).grid(row=9, column=0,
                                                                                            sticky=W)
    # Textbox output for any errors encountered when inputing values in the
    errorM = Text(window, width=75, height=4, wrap=WORD, background="white")
    errorM.grid(row=10, column=0, columnspan=2, sticky=W)
    # Comparison Grapher
    Label(window, text="Please enter a Country to compare with China's Population", bg="white",
          fg='black', font="none 20 bold").grid(row=11, column=0, sticky=W)
    compareMe = Entry(window, width=20, bg="white")
    compareMe.grid(row=12, column=0, sticky=W)
    Button(window, text="Comparison Between Population of a Country and China",bg="white", fg='black', font="none 20 bold", width=53,
           command=comparisonGraphMaker).grid(row=13, column=0, sticky=W)

    # Exit Label
    Label(window, text="click to exit", bg="white", fg="black", font="none 20 bold").grid(row=14, column=0, sticky=W)
    Button(window, text="Exit",bg="white", fg='black', font="none 20 bold", width=14, command=close_window).grid(row=14, column=1, sticky=E)
    # Window remains open until it is closed
    window.mainloop()
if __name__ == '__main__':
    gui()


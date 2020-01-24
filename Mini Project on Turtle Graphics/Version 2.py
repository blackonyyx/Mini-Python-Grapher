#Name:      Group Number:
from turtle import *
from itertools import cycle
from tkinter import *
import codecs
from statistics import *
from math import *

#Globals Declared for usage throughout the program
COLORS = cycle(['#CC9933', '#6699CC', '#CC3399', '#996633', '#336699', '#0099CC', '#FF9999', '#CC0066', '#99CC00', '#CC3399', '#009933'])
# Import functions from turtle and codecs
# codecs imported to decode utf-16 encoding used on the text.
# Itertools imported to assist in color selection
# statistics and math imported to assist in data transformation to assist in graphing

try:
    with codecs.open("Mini Project Text.txt","r",encoding = "utf-16") as file:
        #Data Organisation stage
        # reads in as a large string file
        data = file.read()
        # splits by line
        raw = data.splitlines()
        #removes the title
        title = raw.pop(0)
        #seperates the title tablelabels
        tablelabels = raw.pop(0).split("; ")
        countryNames = []
        worldStats = {}  # Dictionary to store the world statistics
        worldStats[tablelabels[2]] = 0  # Key-Value Pair to cache 2018 stats
        worldStats[tablelabels[3]] = 0  # Key-Value Pair to cache 2019 stats
        worldStats[tablelabels[5]] = 0  # Key-Value Pair to cache increase in population stats
        worldStats[tablelabels[6]] = 0  # Key-Value Pair to cache percentage of total population stats
        worldStats[tablelabels[7]] = []  # Key-Value Pair to cache the list of continents
        worldStats["totalNumber"] = len(raw)
        # Data is stored in the program as a Dictionary with key rank of country value as entry in the txt file representing data in the table
        parsedData = {}
        for rawString in raw:
            # Parses data
            dataEntry = rawString.split("; ")
            processedEntry = [int(dataEntry[0]), dataEntry[1], int(dataEntry[2]), int(dataEntry[3]),
                              float(dataEntry[4]), int(dataEntry[5]), float(dataEntry[6]), dataEntry[7]]
            worldStats[tablelabels[2]] += processedEntry[2]
            worldStats[tablelabels[3]] += processedEntry[3]
            worldStats[tablelabels[5]] += processedEntry[5]
            countryNames.append(dataEntry[1])
            if worldStats[tablelabels[7]].count(processedEntry[7]) == 0:
                worldStats[tablelabels[7]].append(processedEntry[7])
            parsedData[processedEntry[0]] = processedEntry
except OSError:
    # 'File not found' error message.
    print("File not Found")


#Piechart charter
def piechart():
    continentPopulation = []
    for continent in worldStats[tablelabels[7]]:
        matchingCountry = []
        for i in range(1,worldStats["totalNumber"]+1):
            if parsedData[i][7] == continent:
                matchingCountry.append(parsedData[i][3])
        continentPopulation.append((continent,sum(matchingCountry)))

    screen = Screen()
    screen.title('Piechart of World Population by Continent')
    RADIUS = 200
    LABEL_RADIUS = RADIUS * 1.33
    TITLE_RADIUS = RADIUS * 1.5


    # The pie slices
    toFill = continentPopulation
    totalPop = worldStats[tablelabels[3]]  # data doesn't sum to total
    pen = Turtle()
    pen.penup()
    pen.sety(-RADIUS)
    pen.pendown()
    pen.width(3)
    pen.speed('fastest')
    pen.hideturtle()
    for _, proportion in toFill:
        pen.fillcolor(next(COLORS))
        pen.begin_fill()
        pen.circle(RADIUS, proportion * 360 / totalPop)
        position = pen.position()
        pen.goto(0, 0)
        pen.end_fill()
        pen.setposition(position)
    #PieChat Lables
    pen.penup()
    pen.sety(-LABEL_RADIUS)

    for label, proportion in toFill:
        pen.circle(LABEL_RADIUS, proportion * 360 / totalPop / 2)
        pen.write(label+"\n"+ str((proportion))+"\n"+ str(100*round(proportion/totalPop,2))+"%", align="center", font=("Arial", 11, "bold"))
        pen.circle(LABEL_RADIUS, proportion * 360 / totalPop / 2)
    pen.penup()
    pen.sety(-TITLE_RADIUS)

    # Caption for the Pie Chart
    pen.circle(TITLE_RADIUS, 0.5 * 360)
    pen.write("Chart of World Population by Continent", align="center", font=("Arial", 20, "bold"))
    pen.circle(TITLE_RADIUS, 0.5 * 360)
    pen.circle(1.7, 0)
    pen.write("Total World Population: "+str(worldStats[tablelabels[3]]), align="center", font=("Arial", 20, "bold"))
    pen.circle(1.7, 0)
    # Opens a Window to view the Piechart and to open the turtle window

    screen.exitonclick()

def dataParser(query):
    #Intermediate step to parse the data and flag out if there is a error input
    relevantEntries = []
    for country in countryNames:
        if country.count(query):
            relevantEntries.append((country,countryNames.index(country)))
    if len(relevantEntries) == 0:
        #Flags out that there is no matching entry
        return 0
    else:
        tableData = []
        for ent in relevantEntries:
            tableData.append(parsedData[ent[1] + 1])
        return tableData





def barGraphCharter(data,mode):
    #Bar Charter for Both population increase and population decrease
    #Changing the title according to the mode

    fontsize = 11
    n = len(data)
    if mode == True:
        title = f"Top {n} Population Decrease 2018-2019 by %"
    else:
        title = f"Top {n} Population Increase 2018-2019 by %"
    xmax = min(data.values()) if mode ==True else max(data.values())
    #Window Setup
    window = Screen()
    window.title(title)
    height = ((10 + fontsize/2)*1/n+(30 - fontsize/2)*1/n+5)*2*n + 100
    window.setup(750, height)
    pen = Turtle()
    pen.hideturtle()
    pen.speed('fastest')
    pen.penup()
    pen.setpos(-225, -(height / 2) + 50)  # Moves Cursor down to start point of graph
    pen.pendown()

     # draw x-axis and ticks
    xinterval = 500 / 9

    for i in range(1, 10):
        pen.forward(xinterval)
        dx = float(xmax / 9 * i)
        pen.right(90)
        pen.write(f'{round(dx,1)}', move=False, align="center", font=("Arial", 11, "bold"))
        pen.forward(10)
        pen.backward(10)
        pen.left(90)
    pen.penup()
    pen.setpos(-225, -(height / 2) + 50)
    pen.pendown()
    pen.left(90)
    pen.forward(10)

    # drawing bar and fill
    scale = xmax / 400
    widths = []  # bar height
    for value in data.values():
        widths.append(value / scale)
    for width in widths:
        pen.color('black')
        pen.forward(5)
        pen.right(90)
        pen.begin_fill()
        pen.forward(width)
        pen.left(90)
        pen.forward(3+(30 - fontsize/2)*1/n)
        pen.write('  ' + str(round(width * scale,2)), move=False, align="left", font=("Arial", 8, "bold"))
        #Labeling the end of the bar with the value, rounding to 2 dp to prevent floating point error
        pen.forward(2+(10 + fontsize/2)*1/n)
        pen.left(90)
        pen.forward(width)
        pen.color(next(COLORS))
        pen.right(90)
        pen.backward((3 + (30 - fontsize / 2) * 1 / n) + 2 + (10 + fontsize / 2) * 1 / n)
        pen.end_fill()
        pen.forward((3 + (30 - fontsize / 2) * 1 / n) + 2 + (10 + fontsize / 2) * 1 / n)

    pen.color('black')
    pen.forward(30)
    pen.penup()
    pen.right(90)
    pen.forward(300)
    pen.pendown()
    pen.write(title,move=False, align="center", font=("Arial", 20, "bold"))
    pen.penup()
    pen.setpos(-225, -(height / 2) + 60)
    pen.left(90)
    #For alignment of Labels to bar graphs, total width of bargraph is calculated.
    total = (10 + fontsize/2)*1/n+(30 - fontsize/2)*1/n+5
    # draw y-axis and labels
    pen.pendown()
    #Lable for each graph
    for key in data:
        pen.forward(5)
        pen.forward(total/2)
        pen.write('  ' + key, move=False, align="right", font=("Arial", 8, "bold"))
        pen.forward(total/2)

    pen.forward(40)
    pen.write('Countries', move=False, align="right", font=("Arial", 11, "bold"))
    pen.st()
    #Leaves the window open until the user closes it
    window.exitonclick()


def tableMaker(table):
    window = Screen()
    window.title("Search Results")
    height = 1000
    width = 600
    window.setup(width, height)
    window.setworldcoordinates(0, 0, width, height)
    pen = Turtle()
    pen.clear()
    pen.speed("fastest")
    pen.hideturtle()
    pen.penup()
    pen.goto( width/2, height - 60)
    pen.write(("Matching String Search Results"),align="center", font=("Arial", 20, "bold"))
    pen.goto(0, pen.ycor() - 20)
    xcoord = []
    #to store the x coordinates used
    for label in tablelabels:
        pen.forward(10)
        xcoord.append(pen.xcor())
        pen.write(label, move=True, align='left', font=("Arial", 8, "bold"))
        if label != tablelabels[1]:
            pen.forward(30)
        else:
            pen.forward(100)
    pen.goto(0, pen.ycor() - 25)
    #Entering the data into the columns row by row
    for row in table:
        for i in range(len(row)):
            pen.setx(xcoord[i])
            pen.write(row[i], move=True, align='left', font=("Arial", 8, "bold"))
        pen.goto(0, pen.ycor() - 25)

    window.exitonclick()

def negativeGrowthByPercentage(topRanking):
    if topRanking == 0 or type(topRanking)!= int:
        return None
    #Will Reject Data that is non negative data
    usefulData = list(parsedData.items())
    usefulData.sort(key = lambda x: x[1][6])
    usefulData = usefulData[:topRanking]
    #Graphing data in [(name,percentage decline)]
    dictionary = {}
    for data in usefulData:
        key = data[1][1]
        value = round(data[1][6],2)
        if value<0:
            dictionary[key]=value
    try:
        barGraphCharter(dictionary,True)
    except Terminator:
        barGraphCharter(dictionary, True)

def positiveGrowthByPercentage(topRanking):
    if topRanking == 0 or type(topRanking)!= int:
        print("Invalid Input, please try again")
        return None
    #Will Reject Data that is not positive data
    usefulData = list(parsedData.items())
    usefulData.sort(key = lambda x: x[1][6],reverse=True)
    usefulData = usefulData[:topRanking]
    #Graphing data in [(name,percentage increase)]
    dictionary = {}
    for data in usefulData:
        key = data[1][1]
        value = round(data[1][6], 2)
        if value > 0:
            dictionary[key] = value
    try:
        barGraphCharter(dictionary,False)
    except Terminator:
        barGraphCharter(dictionary, False)
def boxWhisker(header):

    indx = header
    title = f"Box-Whiskers Plot of log10 transformation of Population {tablelabels[indx]}."
    data = []
    # Log Transformation is applied on the data as the difference between the smallest and largest point in the data set is very large.
    for item in list(parsedData.values()):
        data.append(log10(item[indx]))
    # Cacheing and capturing the required entries for the graph.
    maximum = max(data)
    minimum = min(data)
    mid = median_high(data)
    q1 = median_high(list(filter(lambda x: x<mid,data)))
    q3 = median_high(list(filter(lambda x: x>=mid,data)))
    labelMid = countryNames[data.index(mid)]
    labelMn = countryNames[data.index(minimum)]
    labelMx = countryNames[data.index(maximum)]
    labelQ1 = countryNames[data.index(q1)]
    labelQ3 = countryNames[data.index(q3)]
    scalar = (maximum-minimum) #scaling factor
    medianX = 800*(mid-minimum)/scalar
    q1X = 800*(q1-minimum)/scalar
    q3X = 800*(q3-minimum)/scalar
    window = Screen()
    window.title(title)
    height = 500
    width = 1100
    window.setup(width, height)
    window.setworldcoordinates(-200,0,width,height)
    pen = Turtle()
    #pen.speed("fastest")
    pen.hideturtle()
    pen.penup()
    #drawing and labeling the minimum and maximum values
    pen.goto(50,250)
    pen.write(f"Minimum: {labelMn}- {round(minimum,2)}",move=False, align="right", font=("Arial", 11, "bold"))
    pen.pendown()
    pen.goto(850,250)
    pen.stamp()
    pen.write(f"Maximum {labelMx}: {round(maximum,2)}",move=False, align="left", font=("Arial", 11, "bold"))
    pen.penup()
    #to Draw the Box
    pen.goto(medianX+50,200)
    pen.pendown()
    pen.color("black")
    pen.right(180)
    pen.fillcolor(next(COLORS))
    pen.begin_fill()
    pen.forward(medianX-q1X)
    pen.right(90)
    pen.forward(100)# box of height 100
    pen.write(f"Q1: {labelQ1}- {round(q1,2)}",move=False, align="right", font=("Arial", 11, "bold"))
    pen.right(90)
    pen.forward(medianX-q1X)
    pen.end_fill()
    continuation = pen.ycor()
    pen.penup()
    pen.sety(continuation+15)
    pen.write(f"Median: {labelMid}- {round(mid,2)}",move=False, align="right", font=("Arial", 11, "bold"))
    pen.sety(continuation)
    pen.pendown()
    pen.fillcolor(next(COLORS))
    pen.begin_fill()
    pen.forward(q3X-medianX)
    pen.write(f"Q3: {labelQ3}- {round(q3,2)}",move=False, align="left", font=("Arial", 11, "bold"))
    pen.right(90)
    pen.forward(100)# box of height 100
    pen.right(90)
    pen.forward(q3X-medianX)
    pen.end_fill()
    pen.penup()
    pen.goto(450,400)
    pen.write(title,move = False,align = "center",font = ("Arial", 20, "bold"))
    pen.goto(100, 175)
    pen.write("Standard Deviation: " + str(round(stdev(data), 2))+"\nVariance: "+str(round(variance(data),2)), move=False, align="center", font=("Arial", 11, "bold"))

    window.exitonclick()

#GUI Function using Tkinter
# Window for main program
def gui():
    mainWindow = Tk()
    mainWindow.title("World Population Grapher")
    mainWindow.configure(background="black")
    Label(mainWindow, text="Data Processing Program for World Population Data 2019", bg="black", fg='white',
          font=("Arial", 20, "bold")).grid(row=1, column=0, sticky=W)

    Label(mainWindow, text="Please select a function you wish to use", bg="black", fg='white', font=("Arial", 11, "bold")).grid(
        row=2, column=0, sticky=W)


    # Functions used for user interaction
    def piecharter():
        #When button is pressed, the piechartmaker opens a popup which plots the graph
        try:
            piechart()
        except Terminator:
            pass





        # Interactive Functions for buttons to activate
    def activateNegativeGrapher():
        entered = negativeGraphEntry.get()
        errorHandler.delete(0.0, END)
        try:
            entered = int(entered)
        except ValueError:
            errorHandler.insert(END, f"Negative BarGraph Function: You have entered a Non Numeric input: {negativeGraphEntry.get()}\nPlease enter a numeric input")
        else:
            if entered > 31:
                errorHandler.insert(END,f"Negative BarGraph Function: Warning! You have entered a value above 31 there are not enough negative entries to display")
            negativeGrowthByPercentage(entered)

    def activatePositiveGrapher():
        entered = positiveGraphEntry.get()
        errorHandler.delete(0.0, END)
        try:
            entered = int(entered)

        except ValueError:
            errorHandler.insert(END, f"Positive BarGraph Function: You have entered a Non Numeric input: {positiveGraphEntry.get()}\nPlease enter a numeric input")

        else:
            if entered >70:
                errorHandler.insert(END, f"Positive BarGraph Function: Warning! You have entered a value above 70 the graph may not display the bargraph properly")
            positiveGrowthByPercentage(entered)

    def close_window():
        mainWindow.destroy()
        exit()


    def findMatches():
        entered = query.get()
        errorHandler.delete(0.0, END)
        #To filter out invalid inputs of Queries
        if not entered.isalpha():
            errorHandler.insert(END, f"TableMaker Function:\nYou have entered a invalid input: {query.get()}\nPlease enter a alphabetical string")
        else:
            data = dataParser(entered)
            if data == 0:
                errorHandler.insert(END, f"TableMaker Function:\nYou have entered a invalid search term: {query.get()}\nPlease enter a valid search term string")
            else:
                try:
                    tableMaker(data)
                except Terminator:
                    tableMaker(data)
    def boxWhiskerMaker():
        # to handle invalid inputs.
        entered = whisker.get()
        errorHandler.delete(0.0, END)
        if entered not in tablelabels[2:4]:
            errorHandler.insert(END, f"BoxWhisker Function: Please enter one of the following into the textbox: {' '.join(tablelabels[2:4])}")
        else:
            try:
                boxWhisker(tablelabels.index(entered))
            except Terminator:
                boxWhisker(tablelabels.index(entered))


    #User Interactions
    Button(mainWindow, text="Piechart of Population by Continent",bg="black", fg='white', font=("Arial", 11, "bold"), width=35, command=piecharter).grid(row=4, column=0,
                                                                                                     sticky=W)
    Label(mainWindow, text=" Barchart Graph of Population Decrease, Year 2018-2019", bg="black",
          fg='white', font=("Arial", 11, "bold")).grid(row=5, column=0, sticky=W)
    # Instructions
    Label(mainWindow, text="Enter a number into the textbox below", bg="black",
          fg='white', font=("Arial", 11, "bold")).grid(
        row=6, column=0, sticky=W)
    negativeGraphEntry = Entry(mainWindow, width=20, bg="black", fg='white')
    negativeGraphEntry.grid(row=7, column=0, sticky=W)
    Label(mainWindow, text="Barchart Graph of Population Increase, Year 2018-2019", bg="black",
          fg='white', font=("Arial", 11, "bold")).grid(row=9, column=0, sticky=W)

    # User Entry Positive Percentage Change in population
    positiveGraphEntry = Entry(mainWindow, width=20, bg="black", fg='white')
    positiveGraphEntry.grid(row=10, column=0, sticky=W)
    Button(mainWindow, text='Graph it!', bg="black", fg="white", font=("Arial", 11, "bold"), width=9,
           command=activateNegativeGrapher).grid(row=8, column=0, sticky=W)
    Button(mainWindow, text='Graph it!', bg="black", fg="white", font=("Arial", 11, "bold"), width=9,
           command=activatePositiveGrapher).grid(row=11, column=0, sticky=W)
    Label(mainWindow, text="Please enter a alphabetical string in the text box to find matching countries", bg="black",
          fg='white', font=("Arial", 11, "bold")).grid(row=12, column=0, sticky=W)
    #Text Box for Querying the string.
    query = Entry(mainWindow, width=20, bg="black", fg='white')
    query.grid(row=13, column=0, sticky=W)
    #Button for Querying the Country Names matching a certain string.

    Button(mainWindow, text="Make a Table of Countries with a search term",bg="black", fg='white', font=("Arial", 11, "bold"), width=40, command=findMatches).grid(row=14, column=0,
                                                                                            sticky=W)
    # Textbox output for any errors encountered when inputing values in the
    errorHandler = Text(mainWindow, width=75, height=4, wrap=WORD, background="black",fg = "white")
    errorHandler.grid(row=15, column=0, columnspan=2, sticky=W)
    # Comparison Grapher

    Label(mainWindow, text="Please enter a valid year to see the Box-Whisker Plot for the year", bg="black", fg="white", font=("Arial", 11, "bold")).grid(row=16, column=0, sticky=W)
    whisker = Entry(mainWindow, width=20, bg="black", fg='white')
    whisker.grid(row=17, column=0, sticky=W)
    Button(mainWindow, text="Box Whisker Plot of Population",bg="black", fg='white', font=("Arial", 11, "bold"), width=33,
           command=boxWhiskerMaker).grid(row=18, column=0, sticky=W)

    # Exit Label
    Label(mainWindow, text="click to exit", bg="black", fg="white", font=("Arial", 11, "bold")).grid(row=19, column=0, sticky=W)
    Button(mainWindow, text="Esc",bg="black", fg="white", font=("Arial", 11, "bold"), width=14, command=close_window).grid(row=19, column=1, sticky=E)
    # Window remains open until it is closed
    mainWindow.mainloop()




if __name__ == '__main__':
    gui()


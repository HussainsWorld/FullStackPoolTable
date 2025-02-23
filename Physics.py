import phylib;
import os;
import sqlite3;
import math;

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH
SIM_RATE = phylib.PHYLIB_SIM_RATE 
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON
DRAG = phylib.PHYLIB_DRAG 
MAX_TIME = phylib.PHYLIB_MAX_TIME 
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS
FRAME_RATE = 0.01

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
                        "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="350" height="687.5" viewBox="-25 -25 1400 2750"
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink">
    <rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";
FOOTER = """</svg>\n""";

# add more here

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    def svg(self):
        """
        Generate SVG
        """
        # Get position and ball number
        cx, cy = self.obj.still_ball.pos.x, self.obj.still_ball.pos.y
        r = BALL_RADIUS
        fill = BALL_COLOURS[self.obj.still_ball.number]

        svg_string = """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (cx, cy, r, fill)
        return svg_string


################################################################################

################################################################################
class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__( self, number, pos, vel, acc ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a RollingBall class
        self.__class__ = RollingBall;


    def svg(self):
        """
        Generate SVG
        """
        cx, cy = self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y
        r = BALL_RADIUS
        fill = BALL_COLOURS[self.obj.rolling_ball.number]

        # Construct SVG string
        svg_string = """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (cx, cy, r, fill)
        return svg_string


################################################################################

################################################################################
class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__( self, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a Hole class
        self.__class__ = Hole;


    def svg(self):
        """
        Generate SVG
        """
        # Get position and ball number
        cx, cy = self.obj.hole.pos.x, self.obj.hole.pos.y
        r = HOLE_RADIUS

        # Construct SVG string
        svg_string = """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (cx, cy, r)
        return svg_string


################################################################################

################################################################################
class HCushion( phylib.phylib_object ):
    """
    Python HCushion class.
    """

    def __init__( self, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a HCushion class
        self.__class__ = HCushion;


    def svg(self):
        """
        Generate SVG
        """
        # Get y position
        y = -25 if self.obj.hcushion.y == 0 else 2700

        # Construct SVG string
        svg_string = """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (y)
        return svg_string


################################################################################

################################################################################
class VCushion( phylib.phylib_object ):
    """
    Python VCushion class.
    """

    def __init__( self, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a VCushion class
        self.__class__ = VCushion;


    def svg(self):
        """
        Generate SVG
        """
        # Get x position
        x = -25 if self.obj.vcushion.x == 0 else 1350

        # Construct SVG string
        svg_string = """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (x)
        return svg_string

###############################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        self.current = -1
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    def svg(self):
        svg_String = HEADER
        for obj in self:
            if obj is not None:
                if isinstance(obj, StillBall) and obj.obj.still_ball.number == 0:
                    svg_String += f'<circle id="cue-ball" cx="{obj.obj.still_ball.pos.x}" cy="{obj.obj.still_ball.pos.y}" r="{BALL_RADIUS}" fill="white" />\n'
                else:
                    svg_String += obj.svg()
        svg_String += FOOTER
        return svg_String
    
    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );

                # add ball to table
                new += new_ball;

            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                      Coordinate( ball.obj.still_ball.pos.x,
                                      ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
        # return table
        return new;
    def cueBall(self):
        for ball in self:
            if isinstance(ball, RollingBall) and ball.obj.rolling_ball.number == 0:
                return (ball, ball.obj.rolling_ball.pos.x, ball.obj.rolling_ball.pos.y)
            elif isinstance(ball, StillBall) and ball.obj.still_ball.number == 0:
                return (ball, ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y)
        return None


class Database():

    def __init__(self, reset=False):
        # Set the database name
        db_file = "phylib.db"
        
        if reset and os.path.exists(db_file):
            os.remove(db_file)
        
        # Open connection
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        if reset:
            self.createDB()

    def createDB(self):
        cursor = self.conn.cursor()
        # SQL statements to create tables
        BALL = '''CREATE TABLE IF NOT EXISTS Ball (
                            BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            BALLNO INTEGER NOT NULL,
                            XPOS FLOAT NOT NULL,
                            YPOS FLOAT NOT NULL,
                            XVEL FLOAT,
                            YVEL FLOAT
                        )'''
        TABLE = '''CREATE TABLE IF NOT EXISTS TTable (
                           TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            TIME FLOAT NOT NULL
                        )'''
        BALLTABLE = '''CREATE TABLE IF NOT EXISTS BallTable (
                            BALLID INTEGER NOT NULL,
                            TABLEID INTEGER NOT NULL,
                            FOREIGN KEY (BALLID) REFERENCES Ball(BALLID),
                            FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID),
                            PRIMARY KEY (BALLID, TABLEID)
                        )'''
        SHOT = '''CREATE TABLE IF NOT EXISTS Shot (
                            SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            PLAYERID INTEGER NOT NULL,
                            GAMEID INTEGER NOT NULL,
                            FOREIGN KEY (PLAYERID) REFERENCES Player(PLAYERID),
                            FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)
                        )'''
        TABLESHOT = '''CREATE TABLE IF NOT EXISTS TableShot (
                            TABLEID INTEGER NOT NULL,
                            SHOTID INTEGER NOT NULL,
                            FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID),
                            FOREIGN KEY (SHOTID) REFERENCES Shot(SHOTID),
                            PRIMARY KEY (TABLEID, SHOTID)
                        )'''
        GAME = '''CREATE TABLE IF NOT EXISTS Game (
                            GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            GAMENAME VARCHAR(64) NOT NULL
                        )'''
        PLAYER = '''CREATE TABLE IF NOT EXISTS Player (
                            PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            GAMEID INTEGER NOT NULL,
                            PLAYERNAME VARCHAR(64) NOT NULL,
                            FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)
                        )'''

        # Execute SQL statements to create tables
        cursor.execute(BALL)
        cursor.execute(TABLE)
        cursor.execute(BALLTABLE)
        cursor.execute(SHOT)
        cursor.execute(TABLESHOT)
        cursor.execute(GAME)
        cursor.execute(PLAYER)

        # Commit changes
        self.conn.commit()

        # Close cursor
        cursor.close()


    def readTable(self, tableID):
        cursor = self.conn.cursor()
        #incrementing tableID
        cursor.execute("SELECT * FROM TTable WHERE TABLEID = ?", (tableID + 1,))
        time = cursor.fetchone()
        if not time: 
            return None

        table = Table()

        table.time = time[1] 

        cursor.execute("""
            SELECT Ball.BALLID, Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL
            FROM Ball
            INNER JOIN BallTable ON Ball.BALLID = BallTable.BALLID
            WHERE BallTable.TABLEID = ?""", (tableID + 1,))
        rows = cursor.fetchall()

        for time in rows:
            ballNo = time[1]
            ballPosition = Coordinate(time[2], time[3])
            if time[4] is not None:
                ballVelocity = Coordinate(time[4], time[5])
                speed = (ballVelocity.x**2 + ballVelocity.y**2)**0.5
                xAcc = 0
                yAcc = 0
                if speed > VEL_EPSILON: 
                    #calculate acc
                    xAcc = (-ballVelocity.x / speed) * DRAG
                    yAcc = (-ballVelocity.y / speed) * DRAG
                acceleration = Coordinate(xAcc, yAcc)
                ball = RollingBall(ballNo, ballPosition, ballVelocity, acceleration)
            else:
                ball = StillBall(ballNo, ballPosition)

            table += ball
        self.conn.commit()
        cursor.close()
        return table


    def writeTable(self, table):
        cursor = self.conn.cursor()
        #put time in table
        query = "INSERT INTO TTable (TIME) VALUES (?)"
        cursor.execute(query, (table.time,))
        table_id = cursor.lastrowid  # Get the autoincremented TABLEID value

        for ball in table:
            if isinstance(ball, StillBall):
                query = '''INSERT INTO Ball (BALLNO, XPOS, YPOS)
                           VALUES (?, ?, ?)'''
                cursor.execute(query, (ball.obj.still_ball.number, ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y))
                ball_id = cursor.lastrowid
                query = "INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)"
                cursor.execute(query, (ball_id, table_id))
            elif isinstance(ball, RollingBall):
                query = '''INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL)
                           VALUES (?, ?, ?, ?, ?)'''
                cursor.execute(query, (ball.obj.rolling_ball.number, ball.obj.rolling_ball.pos.x, ball.obj.rolling_ball.pos.y, ball.obj.rolling_ball.vel.x, ball.obj.rolling_ball.vel.y))
                ball_id = cursor.lastrowid
                query = "INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)"
                cursor.execute(query, (ball_id, table_id))
            
        self.conn.commit()
        cursor.close()
        return table_id - 1
    
    def getGame(self, gameID):
        cursor = self.conn.cursor()
        query = '''SELECT Game.GAMENAME, Player1.PLAYERNAME, Player2.PLAYERNAME
                   FROM Game
                   JOIN Player AS Player1 ON Game.GAMEID = Player1.GAMEID
                   JOIN Player AS Player2 ON Game.GAMEID = Player2.GAMEID AND Player1.PLAYERID < Player2.PlayerID
                   WHERE Game.GAMEID = ?'''
        cursor.execute(query, (gameID,))
        game_details = cursor.fetchone()
        cursor.close()
        return game_details

    def setGame(self, gameName, player1Name, player2Name):
        cursor = self.conn.cursor()
        # game details into Game table
        query = "INSERT INTO Game (GAMENAME) VALUES (?)"
        cursor.execute(query, (gameName,))
        self.conn.commit()
        cursor.execute("SELECT GAMEID FROM Game WHERE GAMENAME=?", (gameName,))
        result = cursor.fetchone()
        if result is None:
            gameID = 1
        gameID = result[0]

        cursor.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (gameID, player1Name))
        cursor.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (gameID, player2Name))

        self.conn.commit()
        cursor.close()
        #adjust for SQL
        return gameID - 1

    def newShot(self, gameName, playerName):
        cursor = self.conn.cursor()
        cursor.execute("SELECT GAMEID FROM Game WHERE GAMENAME=?", (gameName,))
        result = cursor.fetchone()
        if result is None:
            return None
        gameID = result[0]

        query = "SELECT PLAYERID FROM Player WHERE PLAYERNAME=? AND GAMEID = ?"
        cursor.execute(query, (playerName, gameID))
        result = cursor.fetchone()
        
        if result is None:
            return None
        
        playerID = result[0]

        cursor.execute("INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, ?)", (playerID, gameID))
        shotID = cursor.lastrowid
        self.conn.commit()
        cursor.close()
        return shotID + 1
    
    def setTableShot(self, tableID, shotID):
        cursor = self.conn.cursor()
        # entry into TableShot
        query = "INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?)"
        cursor.execute(query, (tableID, shotID))
        self.conn.commit()
        cursor.close()
    def getLastTableID(self):
        # Query to find the highest TABLEID
        self.cursor.execute("SELECT MAX(TABLEID) FROM TTable")
        result = self.cursor.fetchone()
        if result and result[0] is not None:
            return result[0]
        else:
            # If no table has been created yet, return a default value or handle it appropriately
            return 0  #
    def close(self):
        self.conn.commit()
        self.conn.close()
        
class Game():
    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        self.db = Database()
        self.db.createDB()
        # valid constructor usage
        if gameID is not None and (gameName is not None or player1Name is not None or player2Name is not None):
            raise TypeError("Invalid")

        # member variables
        self.gameID = None
        self.gameName = None
        self.player1Name = None
        self.player2Name = None

        # get game details from database
        if gameID is not None and (gameName is None and player1Name is None and player2Name is None):
            game_details = self.db.getGame(gameID)
            # assign to member variables
            if game_details:
                self.gameID = gameID
                self.gameName = game_details[0]
                self.player1Name = game_details[1]
                self.player2Name = game_details[2]
            else:
                raise ValueError("Game with ID {} not found.".format(gameID))
        # add to the database
        elif gameName is not None and player1Name is not None and player2Name is not None and (gameID is None):
            self.gameID = self.db.setGame(gameName, player1Name, player2Name)
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name
        else:
            raise TypeError("Invalid")


    def shoot( self, gameName, playerName, table, xvel, yvel ):
        db = Database()
        cursor = db.conn.cursor()
        shotID = db.newShot(gameName, playerName)
        #Cue ball calculations
        cue_Ball, xpos, ypos = table.cueBall()
        if not cue_Ball:
            return None
        cue_Ball.type = phylib.PHYLIB_ROLLING_BALL
        cue_Ball.obj.number = 0
        cue_Ball.obj.rolling_ball.pos.x = xpos
        cue_Ball.obj.rolling_ball.pos.y = ypos
        cue_Ball.obj.rolling_ball.vel.x = xvel
        cue_Ball.obj.rolling_ball.vel.y = yvel

        #calculate acc like was done in A2
        speed = (xvel**2 + yvel**2)**0.5

        if speed <= VEL_EPSILON:
            cue_Ball.obj.rollingball.acc.x = 0
            cue_Ball.obj.rollingball.acc.y = 0
        else:
            cue_Ball.obj.rolling_ball.acc.x = -xvel / speed * DRAG
            cue_Ball.obj.rolling_ball.acc.y = -yvel / speed * DRAG
        initialTime = 0.0
        maxFrames = 500
        while table:
            initialTime = table.time
            table = table.segment()
            if table is None:
                break
            segmentTime = table.time - initialTime
            frameCount = int(segmentTime / FRAME_RATE)

            for i in range(frameCount):
                frameTime = i * FRAME_RATE
                newT = table.roll(frameTime)
                newT.time = initialTime + frameTime
                maxFrames -= 1
                tableID = self.db.writeTable(newT)
                self.db.setTableShot(tableID, shotID)
                if (maxFrames == 0):
                    return tableID
        # self.conn.commit()
        return tableID
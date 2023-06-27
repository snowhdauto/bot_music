import sqlite3
class SQLighter:
    def __init__(self, database="MusicTestBot.db"):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def getListQuestions(self):
        with self.connection:
            return self.cursor.execute("SELECT id,question,correct,wrong FROM questions").fetchall()
                         
    def delall(self):
        with self.connection:
            self.cursor.execute("DELETE FROM questions")
            self.cursor.execute("UPDATE sqlite_sequence SET seq=0 WHERE name='questions'")
            self.connection.commit()

    def AddQuest(self,value):
        with self.connection:
            self.cursor.execute("INSERT INTO questions (question,correct,wrong) VALUES (?,?,?)",[value['Quest'],value['CAnsw'],value['WAnsw']])
            self.connection.commit()
    def DelQuest(self,questid):
        with self.connection:
            self.cursor.execute("DELETE FROM questions WHERE id=?",[questid])
            self.connection.commit()
    def AddMember(self,userID,username):
        self.cursor.execute("INSERT INTO Members (MemberID,MemberName) VALUES (?,?)",[userID,username])
        self.connection.commit()
    def GetMemberList(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM Members").fetchall()
    def DelMember(self,memid):
        with self.connection:
            self.cursor.execute("DELETE FROM Members WHERE MemberID=?",[memid])
            self.connection.commit()
    def __del__(self):
        self.connection.close()
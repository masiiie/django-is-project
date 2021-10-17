import sqlite3 as sql

#conn=sql.connect('./aadb.mbtiles')

class Map:
    def __init__(self,dbPath):
        self.conn=sql.connect(dbPath)
        self.cursor=self.conn.cursor()

    def get_Image(self,zoom,col,row):
        image=self.cursor.execute("SELECT tile_data FROM images INNER JOIN map ON images.tile_id=map.tile_id WHERE map.zoom=%s AND map.col=%s  AND map.row=%s " %(zoom,col,row) )
        a=image.fetchone()
        return a[0]
            
       
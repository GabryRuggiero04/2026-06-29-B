from database.DB_connect import DBConnect
from model.album import Album


class DAO():

    @staticmethod
    def getAllNodes():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT a.AlbumId, a.Title, a.ArtistId
                    FROM Album a 
                    join Track t on t.AlbumId = a.AlbumId """

        cursor.execute(query)

        for row in cursor:
            results.append(Album(AlbumId=row["AlbumId"], Title=row["Title"], ArtistId=row["ArtistId"], ListaBrani=[]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getTracksByAlbum(album):
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t.Name 
                    FROM Album a 
                    join Track t on t.AlbumId = a.AlbumId 
                    where a.AlbumId = %s"""

        cursor.execute(query, (album.AlbumId,))

        for row in cursor:
            album.ListaBrani.append(row["Name"])

        cursor.close()
        conn.close()

    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT v1.AlbumId as IdAlbum1, v2.AlbumId as IdAlbum2
                        FROM (select a.AlbumId, t.GenreId
                                from Album a
                                join Track t on a.AlbumId=t.AlbumID) v1
                        join (select a2.AlbumId, t2.GenreId
                                from Album a2
                                join Track t2 on a2.AlbumId=t2.AlbumID) v2
                        on v1.GenreId= v2.GenreId
                        WHERE  v1.AlbumId<v2.AlbumId
                        GROUP BY IdAlbum1, IdAlbum2 """

        cursor.execute(query)

        for row in cursor:
            results.append((row["IdAlbum1"], row["IdAlbum2"]))

        cursor.close()
        conn.close()
        return results



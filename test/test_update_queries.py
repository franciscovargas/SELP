from numpy import arange, pi
import unittest
from app.map_graph import distance
import sqlite3


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):

        self.con = sqlite3.connect("app.db")
        self.con2 = sqlite3.connect("app2.db")

    def test_update_queries_count(self):
        """
        The following tests checks that the 
        queries and procedure utilized in
        counting paths users have submitted
        does indeed update the database.
        """
        query_rank = """SELECT user.path_count
                            FROM user
                            WHERE user.user = ?;
                         """
        cur = self.con.cursor()
        user = 'vargfran@gmail.com'
        cur.execute(query_rank, (user,))
        cur.execute(""" UPDATE  user
                        SET path_count=?
                        WHERE user=?;
                    """, (0, user))
        self.con.commit()
        cur.execute("""SELECT path_count
                       FROM user
                       WHERE user=?
                    """, (user,))
        assert cur.fetchall()[0][0] == 0
        for i in range(100):
            user = 'vargfran@gmail.com'
            cur.execute(query_rank, (user,))
            user_rank = cur.fetchall()[0][0]
            cur.execute(""" UPDATE  user
                        SET path_count=?
                        WHERE user=?;
                    """, (user_rank + 1, user))
            self.con.commit()
            cur.execute("""SELECT path_count
                           FROM user
                           WHERE user=?
                        """, (user,))
            new_count = cur.fetchall()[0][0]
            self.assertTrue(new_count == i + 1)

    def test_update_queries_average(self):
        """
        This test checks that the procedure and
        queries used in updating the ranks via
        averaging new inputs indeed works.
        """
        query_rank = """SELECT user.path_count
                            FROM user
                            WHERE user.user = ?;
                         """
        cur = self.con.cursor()
        user = 'vargfran@gmail.com'
        cur.execute(query_rank, (user,))
        cur.execute(""" UPDATE  user
                        SET path_count=?
                        WHERE user=?;
                    """, (0, user))
        self.con.commit()
        cur.execute("""SELECT path_count
                       FROM user
                       WHERE user=?
                    """, (user,))
        assert cur.fetchall()[0][0] == 0
        for i in range(100):
            user = 'vargfran@gmail.com'
            cur.execute(query_rank, (user,))
            user_rank = cur.fetchall()[0][0]
            cur.execute(""" UPDATE  user
                        SET path_count=?
                        WHERE user=?;
                    """, ((float(user_rank) + float(i)) / 2.0, user))
            self.con.commit()
            cur.execute("""SELECT path_count
                           FROM user
                           WHERE user=?
                        """, (user,))
            new_count = cur.fetchall()[0][0]
            self.assertTrue(new_count == (float(user_rank) + float(i)) / 2.0)


    def test_data_consistency(self):
        """
        This test checks that the procedure and
        queries used in updating the ranks via
        averaging new inputs indeed works.
        """
        query_count = """SELECT user.path_count
                            FROM user
                            WHERE user.user = ?;
                         """
	query_user = """SELECT user from user;"""
        cur = self.con2.cursor()
	cur.execute(query_user)
	users = [x[0] for x in cur.fetchall()]
        count = []
	for user in users:
	    cur.execute(query_count, (user,))
            count += [cur.fetchall()[0][0]]
	count1 = sum(count)
        cur.execute("select count(*) from edges;")
        count2 = cur.fetchall()[0][0]
        self.assertTrue(count1 == count2)

if __name__ == '__main__':
    unittest.main()

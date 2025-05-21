from database.DB_connect import DBConnect
from model.retailer import Retailer
class DAO():

    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()
        cursor = conn.cursor()

        result = []

        query = """select distinct country
            from go_retailers"""

        cursor.execute(query, )

        for row in cursor:
            result.append(row[0])

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getAllNodes(nazione):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        query = """select *
        from go_retailers
        where country = %s"""

        cursor.execute(query, (nazione,))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(anno, nazione, u: Retailer, v: Retailer):
        conn = DBConnect.get_connection()
        cursor = conn.cursor()

        result = []

        query = """select count(distinct(gds.Product_number))
from go_daily_sales gds, go_daily_sales gds2, go_retailers gr 
where YEAR(gds.`Date`) = YEAR(gds2.`Date`) and YEAR(gds.`Date`)= %s and Country = %s
and gds.Product_number = gds2.Product_number
and gds.Retailer_code = %s AND gds2.Retailer_code = %s
and gr.Retailer_code = gds.Retailer_code """

        cursor.execute(query, (anno, nazione, u.Retailer_code, v.Retailer_code))

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result[0][0]




if __name__ == "__main__":
    print(DAO.getAllCountries())
    print(DAO.getAllNodes("Italy"))

    print(DAO.getAllEdges(2015, "France", Retailer(1225, "La bonne Forme","Sports Store","France"), Retailer(1135, "Camping Sauvage","Outdoors Shop","France")))
import config_service as config
import psycopg2

def insert(dictionary):
    connect = None
    response = {"success": True}
    try:
        params = config.config('database.ini', 'postgresql')
        connect = psycopg2.connect(**params)

        # connect = psycopg2.connect(
        #     user="qr_user",
        #     password="password",
        #     host="81.163.29.127",
        #     port="5432",
        #     database="postgres"
        # )
        cursor = connect.cursor()

        query = """INSERT INTO qr_table (телефон, отзыв) VALUES (%s,%s,%s)"""
        data = (
            dictionary["phone"],
            dictionary["review"]
        )

        cursor.execute(query, data)
        connect.commit()
    except (Exception, psycopg2.Error) as error:
        response["success"] = False
        response["error"] = error

    finally:
        # closing database connection.
        if connect:
            cursor.close()
            connect.close()

        return response
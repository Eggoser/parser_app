# from app.app import app as application
# application.secret_key = 'kj43h2hdiushf243iurhakjdsfhKJDSFHIU3r4h23rhaksdjlfyl234019DSFlas'

from app.app import data, my_background_task

# if __name__ == "__main__":
# 	application.run(host="0.0.0.0")


my_background_task(data)

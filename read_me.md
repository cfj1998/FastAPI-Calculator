This app is a work-in-progress calculator app made using FastAPI
in Python. To test this app you will need to provide 
your own database connection, I have used PostgresSQL
but you are welcome to choose what you want
as long as it is supported by SQLAlchemy.

This Calculator also has support for complex numbers.

Using trigonometric functions:
- If you want to find sin/cos of for example pi/2 make sure mode is "radians", set multiply_with_pi to "yes" and a = 0.5. Pi will then be added automatically by the function.
Complex functions:
- The complex functions return str due to FastAPI not accepting Python´s complex type.
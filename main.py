import cmath
import math
import statistics
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette import status

import auth
import models
from database import get_db

user_dependency = Annotated[dict, Depends(auth.get_current_user)]


def set_mode(a: float, mode: str = "radians", multiply_with_pi: str = "no"):
    if mode.lower() == "degrees":
        return (a * math.pi) / 180
    elif mode.lower() == "radians" and multiply_with_pi.lower() == "yes":
        return a * math.pi
    else:
        return a


def check_for_probability_error(p: float):
    if p < 0 or p > 1:
        raise HTTPException(
            status_code=409,
            detail="Probability is a number between 0 and 1, inclusive.",
        )


app = FastAPI(
    title="Calculator",
    description="This is a calculator FastAPI app with" "support for complex numbers.",
)
app.include_router(auth.router)


@app.get("/")
def home():
    return f"Welcome to my FastAPICalculator"


# Function is from https://www.youtube.com/watch?v=0A_GCXBCNUQ by coding with Roby
@app.get("/get_user", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return {"User": user}


@app.get("/number", tags=["Number"])
def get_number(a: float):
    return a


@app.get("/addition", tags=["Basic Operations"])
def addition(a: float, b: float):
    return a + b


@app.get("/subtraction", tags=["Basic Operations"])
def subtraction(a: float, b: float):
    return a - b


@app.get("/multiplication", tags=["Basic Operations"])
def multiplication(a: float, b: float):
    return a * b


@app.get("/division", tags=["Basic Operations"])
def division(a: float, b: float):
    if b == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by 0")
    return a / b


@app.get("/square_root", tags=["Basic Operations"])
def sqrt(a: float):
    return math.sqrt(a)


@app.get("/power", tags=["Basic Operations"])
def power(exponent: float, a: float):
    return a**exponent


@app.get("/sin", tags=["Trigonometric Functions"])
def sin(a: float, mode="radians", multiply_with_pi="no"):
    a = set_mode(a, mode, multiply_with_pi)
    return math.sin(a)


@app.get("/asin", tags=["Trigonometric Functions"])
def asin(a: float):
    return math.asin(a)


@app.get("/cos", tags=["Trigonometric Functions"])
def cos(a: float, mode="radians", multiply_with_pi="no"):
    a = set_mode(a, mode, multiply_with_pi)
    return math.cos(a)


@app.get("/acos", tags=["Trigonometric Functions"])
def acos(a: float):
    return math.acos(a)


@app.get("/tan", tags=["Trigonometric Functions"])
def tan(a: float, mode: str = "radians", multiply_with_pi: str = "no"):
    a = set_mode(a, mode, multiply_with_pi)
    if a > 1 * 10**16:
        raise HTTPException(status_code=400, detail="Tangent is undefined for n*(pi/2)")
    return math.tan(a)


@app.get("/atan", tags=["Trigonometric Functions"])
def atan(a: float):
    try:
        return math.atan(a)
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Dividing by 0")


@app.get("/sinh", tags=["Hyperbolic Functions"])
def sinh(a: float):
    return math.sinh(a)


@app.get("/asinh", tags=["Hyperbolic Functions"])
def asinh(a: float):
    return math.asinh(a)


@app.get("/cosh", tags=["Hyperbolic Functions"])
def cosh(a: float):
    return math.cosh(a)


@app.get("/acosh", tags=["Hyperbolic Functions"])
def acosh(a: float):
    return math.acosh(a)


@app.get("/tanh", tags=["Hyperbolic Functions"])
def tanh(a: float):
    return math.tanh(a)


@app.get("/atanh", tags=["Hyperbolic Functions"])
def atanh(a: float):
    return math.atan(a)


@app.get("/logarithm", tags=["Logarithm"])
def log(a: float):
    try:
        return math.log(a)
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Trying to take logarithm of a negative number."
        )


@app.get("/exponential", tags=["Exponential"])
def exponential(a: float):
    return math.exp(a)


@app.get("/complex_number", tags=["Complex Number"])
def get_complex_number(z_real, z_imag):
    z = complex(z_real, z_imag)
    return str(z)


@app.get("/complex_addition", tags=["Basic Complex Operations"])
def complex_addition(z1_real: float, z1_imag: float, z2_real: float, z2_imag: float):
    z1 = complex(z1_real, z1_imag)
    z2 = complex(z2_real, z2_imag)
    return str(z1 + z2)


@app.get("/complex_subtraction", tags=["Basic Complex Operations"])
def complex_subtraction(z1_real: float, z1_imag: float, z2_real: float, z2_imag: float):
    z1 = complex(z1_real, z1_imag)
    z2 = complex(z2_real, z2_imag)
    return str(z1 - z2)


@app.get("/complex_multiplication", tags=["Basic Complex Operations"])
def complex_multiplication(
    z1_real: float, z1_imag: float, z2_real: float, z2_imag: float
):
    z1 = complex(z1_real, z1_imag)
    z2 = complex(z2_real, z2_imag)
    return str(z1 * z2)


@app.get("/complex_division", tags=["Basic Complex Operations"])
def complex_division(z1_real: float, z1_imag: float, z2_real: float, z2_imag: float):
    z1 = complex(z1_real, z1_imag)
    z2 = complex(z2_real, z2_imag)
    if z2 == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by 0")
    return str(z1 / z2)


@app.get("/complex_length", tags=["Basic Complex Operations"])
def complex_length(z_real: float, z_imag: float):
    return math.sqrt(z_real**2 + z_imag**2)


@app.get("/complex_argument", tags=["Basic Complex Operations"])
def complex_argument(z_real: float, z_imag: float):
    z = complex(z_real, z_imag)
    return cmath.phase(z)


@app.get("/complex_polar_form", tags=["Basic Complex Operations"])
def complex_polar_form(z_real: float, z_imag: float):
    z = complex(z_real, z_imag)
    return cmath.polar(z)


@app.get("/complex_roots", tags=["Basic Complex Operations"])
def get_complex_roots(z_real: float, z_imag: float, n: int):
    if n <= 0:
        return []
    z = complex(z_real, z_imag)
    z_arg = cmath.phase(z)
    z_length = complex_length(z_real, z_imag)
    roots = []
    root_length = z_length ** (1 / n)
    for i in range(n):
        root_arg = (z_arg + 2 * math.pi * i) / n
        root_real = root_length * math.cos(root_arg)
        if abs(root_real) < 10e-15:
            root_real = round(root_real)
        root_imag = root_length * math.sin(root_arg)
        if abs(root_imag) < 10e-15:
            root_imag = round(root_imag)
        roots.append(complex(root_real, root_imag))
    return str(roots)


@app.get("/complex_power", tags=["Basic Complex Operations"])
def complex_to_the_power_int(
    z_real: float, z_imag: float, a_real: float, a_imag: float
):
    z = complex(z_real, z_imag)
    a = complex(a_real, a_imag)
    return str(z**a)


@app.get("/complex_sin", tags=["Complex Trigonometric Functions"])
def complex_sin(z_real: float, z_imag: float):
    z = complex(z_real, z_imag)
    return str(cmath.sin(z))


@app.get("/complex_asin", tags=["Complex Trigonometric Functions"])
def complex_asin(z_real: float, z_imag: float):
    z = complex(z_real, z_imag)
    return str(cmath.asin(z))


@app.get("/complex_cos", tags=["Complex Trigonometric Functions"])
def complex_cos(z_real: float, z_imag: float):
    z = complex(z_real, z_imag)
    return str(cmath.cos(z))


@app.get("/complex_acos", tags=["Complex Trigonometric Functions"])
def complex_acos(z_real: float, z_imag: float):
    z = complex(z_real, z_imag)
    return str(cmath.acos(z))


@app.get("/complex_tan", tags=["Complex Trigonometric Functions"])
def complex_tan(z_real: float, z_imag: float):
    z = complex(z_real, z_imag)
    return str(cmath.tan(z))


@app.get("/complex_atan", tags=["Complex Trigonometric Functions"])
def complex_atan(z_real: float, z_imag: float):
    z = complex(z_real, z_imag)
    return str(cmath.atan(z))


@app.get("/complex_sinh", tags=["Complex Hyperbolic Functions"])
def complex_sinh(z_real: float, z_imag: float):
    z = complex(z_real, z_imag)
    return str(cmath.sinh(z))


@app.get("/complex_asinh", tags=["Complex Hyperbolic Functions"])
def complex_asinh(z_real: float, z_imag: float):
    z = complex(z_real, z_imag)
    return str(cmath.asinh(z))


@app.get("/complex_cosh", tags=["Complex Hyperbolic Functions"])
def complex_cosh(z_real: float, z_imag: float):
    z = complex(z_real, z_imag)
    return str(cmath.cosh(z))


@app.get("/complex_acosh", tags=["Complex Hyperbolic Functions"])
def complex_acosh(z_real: float, z_imag: float):
    z = complex(z_real, z_imag)
    return str(cmath.acosh(z))


@app.get("/complex_tanh", tags=["Complex Hyperbolic Functions"])
def complex_tanh(z_real: float, z_imag: float):
    z = complex(z_real, z_imag)
    return str(cmath.tanh(z))


@app.get("/complex_atanh", tags=["Complex Hyperbolic Functions"])
def complex_atanh(z_real: float, z_imag: float):
    z = complex(z_real, z_imag)
    return str(cmath.atanh(z))


@app.get("/fibonacci_calculator", tags=["Fibonacci"])
def fibonacci(n: int, all_numbers="no"):
    if n == 0:
        return n
    if n == 1:
        return n
    fibos = [0, 1]
    for i in range(2, n + 1):
        fibos.append(fibos[i - 2] + fibos[i - 1])
    if all_numbers.lower() == "yes":
        return fibos
    return fibos[n]


@app.get("/mean", tags=["Statistics"])
def get_mean(measurements: list[float]):
    return statistics.mean(measurements)


@app.get("/median", tags=["Statistics"])
def get_median(measurements: list[float]):
    return statistics.median(measurements)


@app.get("/mode", tags=["Statistics"])
def get_mode(measurements: list[float]):
    return statistics.mode(measurements)


@app.get("/binomial_distribution", tags=["Discrete Probability Distributions"])
def get_binomial_prob(n: int, p: float, x: int):
    if x > n:
        raise HTTPException(status_code=409, detail="n has to be larger or equal to x.")
    if n < 0 or x < 0:
        raise HTTPException(status_code=409, detail="Both n and x has to be positive.")
    check_for_probability_error(p)
    return math.comb(n, x) * (p**x) * (1 - p) ** (n - x)


@app.get("/geometric_distribution", tags=["Discrete Probability Distributions"])
def get_geometric_prob(p: float, x: int):
    check_for_probability_error(p)
    if x < 0:
        raise HTTPException(
            status_code=409,
            detail="Number of failures  x until first success must be positive",
        )
    return p * ((1 - p) ** x)


@app.get("/negative_binomial_distribution", tags=["Discrete Probability Distributions"])
def get_neg_binom_prob(p: float, x: int, r: int):
    check_for_probability_error(p)
    if r < 0:
        raise HTTPException(
            status_code=409, detail="The number of successes r must be positive."
        )
    if x < 0:
        raise HTTPException(
            status_code=409, detail="The number of failures must be positive."
        )
    return math.comb(x + r - 1, r - 1) * (p**r) * ((1 - p) ** x)


@app.get("/poisson_distribution", tags=["Discrete Probability Distributions"])
def get_poisson_prob(x: int, _lambda: float):
    if x < 0 or _lambda < 0:
        raise HTTPException(
            status_code=409, detail="Both x and lambda has to be positive."
        )
    return ((math.e ** (-_lambda)) * (_lambda**x)) / math.factorial(x)


@app.get("/Normal_distribution_pdf", tags=["Continuous Probability Density Functions"])
def normal_distribution_pdf(x: float, my: float, sigma: float):
    return (1 / (math.sqrt(math.pi) * sigma)) * math.exp(
        -0.5 * (((x - my) / sigma) ** 2)
    )


@app.get(
    "/Lognormal_distribution_pdf", tags=["Continuous Probability Density Functions"]
)
def lognormal_distribution_pdf(x: float, my: float, sigma: float):
    if x < 0:
        raise HTTPException(status_code=409, detail="x has to be positive.")
    return (1 / (x * math.sqrt(2 * math.pi) * sigma)) * math.exp(
        -((math.log(x) - my) ** 2) / (2 * sigma**2)
    )


@app.get(
    "/Exponential_distribution_pdf", tags=["Continuous Probability Density Functions"]
)
def exponential_distribution_pdf(x: float, _lambda: float):
    if x < 0:
        raise HTTPException(status_code=409, detail="x must be positive.")
    return _lambda * math.exp(-_lambda * x)


@app.get("/is_prime", tags=["Prime Numbers"])
def is_prime(n: int):
    if n <= 1:
        return False
    if n == 2:
        return True
    for i in range(2, n):
        if i > math.sqrt(n):
            break
        if i != 2 and i % 2 == 0:
            continue
        if n % i == 0:
            return False
    return True


@app.get("/prime_factors", tags=["Prime Numbers"])
def get_prime_factors(n: int):
    if n <= 1:
        return [n]
    if is_prime(n):
        return [n]
    else:
        prime_factors = []
        while not is_prime(n):
            for i in range(2, n):
                if is_prime(i) and n % i == 0:
                    prime_factors.append(i)
                    n = n // i
                    break
        prime_factors.append(n)
        return prime_factors


@app.get("/factorial", tags=["Factorial"])
def factorial(n: int):
    if n < 0:
        raise HTTPException(status_code=409, detail="n must be positive")
    return math.factorial(n)


@app.get("/gamma_function_for_integers", tags=["Functions"])
def gamma_function_for_positive_integers(n: int):
    if n < 0:
        raise HTTPException(status_code=409, detail="n must be positive")
    return math.factorial(n - 1)


@app.get("/get_saved_numbers", tags=["Memory"])
def get_memory(db: Session = Depends(get_db)):
    numbers = db.query(models.Memory).all()
    return numbers


@app.post("/add_to_memory_db", tags=["Memory"])
def add_to_memory(a: float, db: Session = Depends(get_db)):
    number_model = models.Memory()
    number_model.number_saved = a

    db.add(number_model)
    db.commit()
    return f"Number {a} was added to memory with id {number_model.id}."


@app.delete("/delete_from_memory_db", tags=["Memory"])
def delete_from_memory(id: int, db: Session = Depends(get_db)):
    number_model = db.query(models.Memory).filter(models.Memory.id == id).first()  # type: ignore
    if number_model is None:
        raise HTTPException(status_code=404, detail="Number not found")
    db.query(models.Memory).filter(models.Memory.id == id).delete()  # type: ignore
    db.commit()
    return f"Number with id {id} was deleted."


@app.get("/add_two_numbers_from_memory", tags=["Memory"])
def add_from_memory(id_1: int, id_2: int, db: Session = Depends(get_db)):
    number_model1 = db.query(models.Memory).filter(models.Memory.id == id_1).first()  # type: ignore
    number_model2 = db.query(models.Memory).filter(models.Memory.id == id_2).first()  # type: ignore
    if number_model1 is None or number_model2 is None:
        raise HTTPException(status_code=404, detail="Number could not be found")
    return addition(number_model1.number_saved, number_model2.number_saved)


@app.get("/subtract_two_numbers_from_memory", tags=["Memory"])
def subtract_from_memory(id_1: int, id_2: int, db: Session = Depends(get_db)):
    number_model1 = db.query(models.Memory).filter(models.Memory.id == id_1).first()  # type: ignore
    number_model2 = db.query(models.Memory).filter(models.Memory.id == id_2).first()  # type: ignore
    if number_model1 is None or number_model2 is None:
        raise HTTPException(status_code=404, detail="Number not found")
    return subtraction(number_model1.number_saved, number_model2.number_saved)


@app.get("/get_complex_memory", tags=["Complex Memory"])
def get_complex_memory(db: Session = Depends(get_db)):
    complex_memory = db.query(models.ComplexMemory).all()
    return complex_memory


@app.post("/save_to_complex_memory", tags=["Complex Memory"])
def save_to_complex_memory(z_real: float, z_imag: float, db: Session = Depends(get_db)):
    z = complex(z_real, z_imag)
    complex_model = models.ComplexMemory()
    complex_model.cartesian = str(z)
    complex_model.real = z_real
    complex_model.imaginary = z_imag
    complex_model.length = complex_length(z_real, z_imag)
    db.add(complex_model)
    db.commit()
    return f"The complex number {complex_model.cartesian} was added to memory and given id {complex_model.id}."


@app.delete("/delete_from_complex_memory", tags=["Complex Memory"])
def delete_from_from_complex_memory(id: int, db: Session = Depends(get_db)):
    complex_model = db.query(models.ComplexMemory).filter(models.ComplexMemory.id == id).first()  # type: ignore
    if complex_model is None:
        raise HTTPException(
            status_code=404, detail=f"Complex Number with id {id} not found."
        )
    db.query(models.ComplexMemory).filter(models.ComplexMemory.id == id).delete()  # type: ignore
    db.commit()
    return f"The complex number with id {id} was deleted from memory."

# DATE DAY PREDICTOR

`date_day_estimator` is a Python package that calculates the day of the week for a given date using **Zeller's Congruence**.

## Installation

```bash
pip install date-day-estimator
```

## Usage

from date_day_estimator.date_day_estimator import zellers_congruence

# Example: Find the day of the week for 5th July 1995
day_number, day_name = zellers_congruence(5, 7, 1995)

print(day_number)  # 4
print(day_name)    # 'Wednesday'


## FORMULA

**Zeller's Congruence**, which is an algorithm used to calculate the day of the week for any given date. It typically takes the following form:

\[
h = \left(q + \left\lfloor \frac{13(m+1)}{5} \right\rfloor + K + \left\lfloor \frac{K}{4} \right\rfloor + \left\lfloor \frac{J}{4} \right\rfloor - 2J\right) \mod 7
\]

Where:
- \( h \) is the day of the week (0 = Saturday, 1 = Sunday, 2 = Monday, etc.),
- \( q \) is the day of the month,
- \( m \) is the month (March = 3, April = 4, ..., February = 14),
- \( K \) is the year of the century (i.e., year % 100),
- \( J \) is the zero-based century (i.e., year // 100).

The specific formula you've shared is not a complete Zeller's congruence, but it appears to be a variation or part of it, focusing on some constants related to the month and year, potentially for a specific date range or calculation method.


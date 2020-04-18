
from numpy.polynomial import Polynomial
import pprint

from jdcal import gcal2jd, jd2gcal
# Subroutine to convert a Julian Day Number to its equivalent Gregorian date.
month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
               "Aug", "Sep", "Oct", "Nov", "Dec"] 
def greg (JDN, separator):
  ymdf = jd2gcal (float(JDN), 0.5)
  year_no = ymdf [0]
  month_no = ymdf [1]
  day_no = ymdf [2]
  month_name = month_names [month_no-1]
  return (str(day_no) + separator + month_name + separator + str(year_no))

# Subroutine to convert a Gregorian date to its equivalnet Julian day number.
def Julian (the_year, the_month, the_day):
  float_1, float_2 = gcal2jd (the_year, the_month, the_day)
  Julian_day_number = int(float_1 + float_2 - 0.5)
  return (Julian_day_number)

# Subroutine to convert a Julian day number to a datetime.date
def to_date (JDN):
    ymdf = jd2gcal (float(JDN), 0.5)
    return (datetime.date (ymdf[0], ymdf[1], ymdf[2]))

def calc_parabola_vertex(x1, y1, x2, y2, x3, y3):
    '''
    Adapted and modifed to get the unknowns for defining a parabola:
    http://stackoverflow.com/questions/717762/how-to-calculate-the-vertex-of-a-parabola-given-three-points
    '''
    denom = (x1-x2) * (x1-x3) * (x2-x3);
    A     = (x3 * (y2-y1) + x2 * (y1-y3) + x1 * (y3-y2)) / denom;
    B     = (x3*x3 * (y1-y2) + x2*x2 * (y3-y1) + x1*x1 * (y2-y3)) / denom;
    C     = (x2 * x3 * (x2-x3) * y1+x3 * x1 * (x3-x1) * y2+x1 * x2 * (x1-x2) * y3) / denom;
    return A,B,C

# Define the known points
x_vals = [Julian(1895,1,1), Julian(1958,1,1),
          Julian(2000,1,1), Julian(2020,4,9), Julian(2021,4,17),
          Julian(2030,1,1), Julian(2040,1,1), Julian(2050,1,1),
          Julian(2100,1,1), Julian(2200,1,1),
          Julian(2300,1,1), Julian(2400,1,1), Julian(2500,1,1)]
y_vals = [-4.866, 32.184,
          63.8285221, 69.4172, 69.50391,
          70.154, 72.154, 75.154,
          93.154, 163.154,
          297.154, 521.154, 855.154]
weights = [1.0, 1.0,
           1000.0, 1000.0, 1000.0,
           100.0, 50.0, 25.0,
           10.0, 5.0,
           1.0, 1.0, 1.0]

# Calculate the unknowns of the equation y=ax^2+bx+c
a,b,c=calc_parabola_vertex(x_vals[0], y_vals[0], x_vals[3], y_vals[3],
                           x_vals[5], y_vals[5])

print (str(a) + ", " + str(b) + ", " + str(c) + ".")

# Do it again, using numpy and with all the points.

p = Polynomial.fit(x_vals, y_vals, 2, w=weights)
pnormal = p.convert(domain=(-1, 1))

pprint.pprint (pnormal)

a=pnormal.coef[2]
b=pnormal.coef[1]
c=pnormal.coef[0]

print (str(a) + ", " + str(b) + ", " + str(c) + ".")

# Define x range for which to calc parabola
import numpy as np

x_pos=np.arange(Julian(2000,1,1),Julian(2500,1,1),1)
y_pos=[]

# Calculate y values.
for x in range(len(x_pos)):
    x_val=x_pos[x]
    y=(a*(x_val**2))+(b*x_val)+c
    y_pos.append(y)

print (str(len(y_pos)))

# Convert the JDNs in x_pos to dates.
import datetime

x_date = list()
for pos_index in range (len(x_pos)):
    x_date.append (to_date(x_pos[pos_index]))

# Plot the parabola (+ the known points)
import matplotlib.pyplot as plt

plt.plot(x_date, y_pos, linestyle='-.', color='black') # parabola line
plt.scatter(x_date, y_pos, color='gray') # parabola points
for pos_index in range(len(x_vals)):
  plt.scatter(to_date(x_vals[pos_index]),y_vals[pos_index],color='r',
              marker="D",s=50)
plt.show()

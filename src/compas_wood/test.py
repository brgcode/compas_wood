
print("Hello")
from compas.geometry import Point
"""

#https://www.youtube.com/watch?v=-eIkUnCLMFc
#https://www.youtube.com/watch?v=-R5sgnHuTFs

#ToDo
#Reference Boost
#Reference Eigen
#Reference CGAL
#Create CGAL polyline https://doc.cgal.org/latest/Nef_3/Nef_3_2polyline_construction_8cpp-example.html
#Follow compas instructions
#Create separately C++ / C# Wrapper and C++/CPython Wraclpper
import sys
#folder = "C:/IBOIS57/_Code/Software/Python/cpp/build/Release/"
folder = "C:/IBOIS57/_Code/Software/Python/Pybind11Example/vsstudio/Release/"
if folder not in sys.path:
    sys.path.append(folder)

print('hello world')
import pybind11module

pybind11module.say_hello()
pybind11module.boostTest()
mydata = pybind11module.MyData(5,3)
print(mydata.x)

import kf_cpp

addition = kf_cpp.add(10, 2)
print(addition)
"""


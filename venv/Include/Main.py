from Point import Point
from Shape import Circle
from Shape import Rectangle
from Shape import Line
from Center import Center
from Kohonen import  Kohonen
from NeuralGas import NeuralGas
import matplotlib.pyplot as plt




def main():
    print("How many shapes do you want: ")
    shapesNumber = int(input())
    points = []
    neurals = []
    j = 0
    while j < shapesNumber:
        print("Choose Shape:\n"
              "1. Circle\n"
              "2. Rectangle\n"
              "3. Line\n")
        choosedShape = int(input())
        shape = 0
        if choosedShape == 1:
            print("Input center of the circle: \n"
                  "x: ")
            x0 = float(input())
            print("\ny: ")
            y0 = float(input())
            print("\nInput radius: ")
            r = float(input())
            shape = Circle(Point(x0,y0),r)
            print("How many points do you want to generate: ")
            pointsNumber = int(input())
            i = 0
            while i < pointsNumber:
                points.append(shape.randPoint())
                i += 1
        if choosedShape == 2:
            print("Input begin of rectangle: \n"
                  "x: ")
            x0 = float(input())
            print("\ny: ")
            y0 = float(input())
            print("\nInput end point\n"
                  "x: ")
            x1 = float(input())
            print("\ny: ")
            y1 = float(input())
            shape = Rectangle(Point(x0,y0), Point(x1,y1))
            print("How many points do you want to generate: ")
            pointsNumber = int(input())
            i = 0
            while i < pointsNumber:
                points.append(shape.randPoint())
                i += 1
        if choosedShape == 3:
            print("Input begin of line: \n"
                  "x: ")
            x0 = float(input())
            print("\ny: ")
            y0 = float(input())
            print("\nInput end point\n"
                  "x: ")
            x1 = float(input())
            print("\ny: ")
            y1 = float(input())
            shape = Line(Point(x0, y0), Point(x1, y1))
            print("How many points do you want to generate: ")
            pointsNumber = int(input())
            i = 0
            while i < pointsNumber:
                points.append(shape.randPoint())
                i += 1
        j += 1
    print("Choose Algorithm: \n"
          "1. Kohonen\n"
          "2. Neural Gas\n")
    choosedAlg = int(input())
    # print("Input: \n"
    #       "Neurals number: ")
    # neuralsNumber = int(input())
    # k = 0
    # while k < neuralsNumber:
    #     neurals.append(Center(random.uniform(-10,10), random.uniform(-10,10),k))
    #     k += 1
    print("Learning rate value: ")
    learningRate = float(input())
    print("Lambda Factor value: ")
    lambdaFactor = float(input())
    # print("Error: ")
    # epsilon = float(input())
    neuralsNumber = 2
    proba = 0
    plt.title("Błąd kwantyzacji dla 200 punktów wpisanych w okrąg i 100 w prostokąt,\n współczynnika nauczania = 0.8, współczynnika lambda = 2 ")
    plt.xlabel("Epoka")
    plt.ylabel("Błąd kwantyzacji")
    plt.xlim(0, 70)
    plt.ylim(0,2)
    plt.grid()
    # file = open("nGas_lr1_lf1_it600_p300_2f_bez_zmeczenia.txt",'w')
    while neuralsNumber <= 20:
        neurals = []
        i = 0
        while i < neuralsNumber:
            neurals.append(Center(random.uniform(-10,10),random.uniform(-10,10),i))
            i += 1
        if choosedAlg == 1:
            kohonen = Kohonen(points, neurals, learningRate, lambdaFactor, 1)
            kohonen.algorithm()
            # file.write(str(kohonen.countMeanError()) + " " + str(kohonen.countDeadCenters()) + "\n")
            kohonen.plotError()
        if choosedAlg == 2:
            ng = NeuralGas(points, neurals, learningRate, lambdaFactor, 1)
            ng.algorithm()
            # file.write(str(ng.countMeanError()) + "  " + str(ng.countDeadCenters()) + "\n")
            ng.plotError()
        neuralsNumber += 2
    # file.close()
    plt.legend()
    plt.savefig("blad_kwantyzacji_ngas_new.png")
    plt.close()



if __name__ == "__main__":
    main()
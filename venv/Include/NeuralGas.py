import math
import matplotlib.pyplot as plt
import numpy as np
import random
import os

class NeuralGas:

    def __init__(self, points, centers, learningRate, lambdaRate, epsilon):
        self.points = points
        self.centers = centers
        self.learningRate = learningRate
        self.lambdaRate = lambdaRate
        self.epsilon = epsilon
        self.meanErrors = []
        self.queue = []
        self.currLearningRate = learningRate
        self.currLambdaFactor = lambdaRate
        self.exhaustedIteration = len(self.centers)
        try:
            os.mkdir("NeuralGas" + str(len(self.centers)))
        except FileExistsError:
            print(" ")
            
    def algorithm(self):
        generation = 1
        while generation <= 70:
            iteration = 0
            random.shuffle(self.points)
            # self.plot(-10,10,-10,10,generation,iteration)
            for point in self.points:
                self.sortByWinner(point)
                # self.centers[0].countError(point)
                self.adaptCenter(point)
                point.group = self.centers[0].group
                # if generation != 1:
                #     if self.epsilon > self.countMeanError():
                #         break
                self.currLearningRate = self.currLearningRate * 0.999
                self.currLambdaFactor = self.currLambdaFactor * 0.99
                iteration += 1
                # self.meanErrors.append(self.countMeanError())
                # self.plot(-10, 10, -10, 10, generation, iteration)
            # if self.epsilon > self.countMeanError():
            #     break
            # else:
            generation += 1
            self.meanErrors.append(self.countMeanError())
            print("Epoka" + str(generation))
            self.exhaustedIteration = int(self.exhaustedIteration * 0.5)

    def plot(self, minxlim, maxxlim, minylim, maxylim, generation, iteration):
        x = []
        y = []
        for point in self.points:
            x.append(point.x)
            y.append(point.y)
        cX = []
        cY = []
        for center in self.centers:
            cX.append(center.x)
            cY.append(center.y)
        plt.plot(x, y, 'k.')
        plt.plot(cX, cY, 'r.')
        plt.title("Generation " + str(generation) + " iteration " + str(iteration))
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.xlim(minxlim, maxxlim)
        plt.ylim(minylim, maxylim)
        plt.savefig(
            "k" + str(len(self.centers)) + "\k" + str(len(self.centers)) + "_gen_" + str(generation) + "_it_" + str(
                iteration) + ".png")
        plt.close()
        print("Generation " + str(generation) + " iteration " + str(iteration) + "error " + str(self.countMeanError()))

    def plotError(self):
        x = np.linspace(0, len(self.meanErrors), len(self.meanErrors))
        # factors = np.polyfit(x, self.meanErrors, 9)
        plt.plot(x, self.meanErrors, '-', label=str(len(self.centers)))
        # plt.title("Błąd kwantyzacji dla " + str(len(self.centers)) + " centrów")
        # plt.xlabel("Iteracja")
        # plt.ylabel("Błąd kwantyzacji")
        # plt.xlim(0, len(self.meanErrors))
        # plt.grid()
        # plt.savefig("blad_kwantyzacji_k" + str(len(self.centers)) + ".png")
        # plt.close()

    def redefineGroups(self):
        for point in self.points:
            point.setGroup(-1)

    def countMeanError(self):
        # i = 0
        # result = 0
        # for center in self.centers:
        #     result += center.meanError()
        #     i += 1
        # result /= len(self.centers)
        # return result
        result = 0
        for point in self.points:
            try:
                result += next(center for center in self.centers if center.group == point.group).countDistance(point.x, point.y)
            except StopIteration:
                result += self.centers[0].countDistance(point.x, point.y)
        result /= len(self.points)
        return result

    def countDeadCenters(self):
        result = 0;
        for center in self.centers:
            try:
                next(point for point in self.points if point.group == center.group)
            except StopIteration:
                result += 1
        return result

    def neighbourFactor(self, index):
        result = math.exp(-index / self.currLambdaFactor)
        return result

    def sortByWinner(self, point):
        for center in self.centers:
            center.relax()
            if center.energy != 0:
                center.setDistance(1000000)
            else:
                center.setDistance(center.countDistance(point.x, point.y))
        self.centers.sort(key=lambda center: center.distance, reverse=False)
        self.centers[0].setEnergy(self.exhaustedIteration)

    def adaptCenter(self,point):
        i = 0
        while i < len(self.centers):
            subVecX = self.centers[i].x - point.x
            subVecY = self.centers[i].y - point.y
            self.centers[i].x = self.centers[i].x - self.currLearningRate * \
                                          self.neighbourFactor(i) * subVecX
            self.centers[i].y = self.centers[i].y - self.currLearningRate * \
                                          self.neighbourFactor(i) * subVecY
            i += 1

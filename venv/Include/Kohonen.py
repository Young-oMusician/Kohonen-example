import math
import matplotlib.pyplot as plt
import numpy as np
import random
import os


class Kohonen:

    def __init__(self, points, centers, learningRate, lambdaFactor, epsilon):
        self.points = points
        self.centers = centers
        self.learningRate = learningRate
        self.lambdaFactor = lambdaFactor
        self.epsilon = epsilon
        self.meanErrors = []
        self.currLambdaFactor = lambdaFactor
        self.currLearningRate = learningRate
        self.exhaustedIteration = len(self.centers)
        try:
            os.mkdir("Kohonen" + str(len(self.centers)))
        except FileExistsError:
            print(" ")
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
            "Kohonen" + str(len(self.centers)) + "\k" + str(len(self.centers)) + "_gen_" + str(generation) + "_it_" + str(
                iteration) + ".png")
        plt.close()
        print("Generation " + str(generation) + " iteration " + str(iteration))

    def plotError(self):
        x = np.linspace(0, len(self.meanErrors), len(self.meanErrors))
        # factors = np.polyfit(x, self.meanErrors, 9)
        plt.plot(x, self.meanErrors, '-', label=str(len(self.centers)))

        # plt.title("Błąd kwantyzacji dla " + str(len(self.centers)) + " centrów")
        # plt.xlabel("Iteracja")
        # plt.ylabel("Błąd kwantyzacji")
        # plt.xlim(0, len(self.meanErrors))
        # plt.grid()
        # plt.savefig("blad_kwantyzacji_kohonen" + str(len(self.centers)) + ".png")
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
            result += self.centers[point.group].countDistance(point.x, point.y)
        result /= len(self.points)
        return result

    def neighbourFactor(self, winnerIndex, neighbourIndex):
        result = math.exp(-(abs(winnerIndex - neighbourIndex) ** 2) / (2 * self.currLambdaFactor ** 2))
        return result

    def findWinner(self, point):
        distances = []
        for center in self.centers:
            center.relax()
            distances.append(center.countDistance(point.x, point.y))
        min = 0
        itDistances = 1
        while itDistances < len(distances):
            if distances[min] > distances[itDistances] and self.centers[itDistances].energy == 0:
                min = itDistances
            itDistances += 1
        self.centers[min].setEnergy(self.exhaustedIteration)
        return min

    def adaptCenter(self, centerIndex, point, winner):
        subVecX = self.centers[centerIndex].x - point.x
        subVecY = self.centers[centerIndex].y - point.y
        self.centers[centerIndex].x = self.centers[centerIndex].x - self.currLearningRate * \
                                      self.neighbourFactor(winner, centerIndex) * subVecX
        self.centers[centerIndex].y = self.centers[centerIndex].y - self.currLearningRate * \
                                      self.neighbourFactor(winner, centerIndex) * subVecY

    def countDeadCenters(self):
        result = 0;
        for center in self.centers:
            try:
                next(point for point in self.points if point.group == center.group)
            except StopIteration:
                result += 1
        return result
                
    def algorithm(self):
        generation = 1
        while generation <= 70:
            iteration = 0
            random.shuffle(self.points)
            # self.plot(-10, 10, -10, 10, generation, iteration)
            for point in self.points:
                winner = self.findWinner(point)
                self.centers[winner].countError(point)
                self.adaptCenter(winner, point, winner)
                point.group = winner
                itNeighbour = winner - 1
                while itNeighbour >= 0:
                    self.adaptCenter(itNeighbour, point, winner)
                    itNeighbour -= 1
                itNeighbour = winner + 1
                while itNeighbour < len(self.centers):
                    self.adaptCenter(itNeighbour, point, winner)
                    itNeighbour += 1
                # if generation != 1:
                    # if self.epsilon > self.countMeanError():
                    #     break
                self.currLearningRate = self.currLearningRate * 0.999
                self.currLambdaFactor = self.currLambdaFactor * 0.99
                iteration += 1
                # self.plot(-10, 10, -10, 10, generation, iteration)
            # if self.epsilon > self.countMeanError():
            #     break
            # else:
                for center in self.centers:
                    center.clearErrors()
            generation += 1
            self.meanErrors.append(self.countMeanError())
            print("Epoka" + str(generation))
            self.exhaustedIteration = int(self.exhaustedIteration * 0.75)


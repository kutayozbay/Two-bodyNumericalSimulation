import math


class TwoBodyController:
    # Constructor
    def __init__(self, q, eccentricity, T):
        self.T = T
        self.model1 = TwoBodyModel(mass=1, position={"x": 0, "y": 0})  # sun
        self.model2 = TwoBodyModel(mass=q, position={"x": 0, "y": 0})  # earth
        self.massRatio = q
        self.massm1m2 = q + 1
        self.eccentricity = eccentricity
        self.u = [1, 0, 0, self.calculateVelocity(q, eccentricity)]

    # Velocity Calculator
    def calculateVelocity(self, q, eccentricity):
        return math.sqrt((1 + q) * (1 + eccentricity))

    # Derivative
    def derivative(self):
        du = [None for i in range(len(self.u))]

        r = self.u[0:2]

        rr = math.sqrt(math.pow(r[0], 2) + math.pow(r[1], 2))

        for i in range(2):
            du[i] = self.u[i + 2]
            du[i + 2] = -(1 + self.massRatio) * r[i] / (math.pow(rr, 3))

        return du

    # New position calculator
    def calculateNewPosition(self):
        r = 1
        # Distance between two bodies
        # m12 is the sum of two massses
        a1 = (self.model2.mass / self.massm1m2) * r
        a2 = (self.model1.mass / self.massm1m2) * r
        self.model1.position["x"] = -a2 * self.u[0]
        self.model1.position["y"] = -a2 * self.u[1]
        self.model2.position["x"] = a1 * self.u[0]
        self.model2.position["y"] = a1 * self.u[1]

    def rungeKutta(self, h):
        # h: timestep
        a = [h / 2, h / 2, h, 0]
        b = [h / 6, h / 3, h / 3, h / 6]
        u0 = []
        ut = []
        dimension = len(self.u)

        for i in range(dimension):
            u0.append(self.u[i])
            ut.append(0)

        for j in range(4):
            du = self.derivative()

            for i in range(dimension):
                self.u[i] = u0[i] + a[j] * du[i]
                ut[i] = ut[i] + b[j] * du[i]

        for i in range(dimension):
            self.u[i] = u0[i] + ut[i]

    def euler(self, h):
        # h: timestep
        for i in range(4):
            self.u[i] = self.u[i] + self.derivative()[i] * h

    # Euler position calculator caller
    def calculatePositionEuler(self, timestep):
        self.euler(timestep)
        self.calculateNewPosition()

    # Runge Kutta position calculator caller
    def calculatePositionRungeKutta(self, timestep):
        self.rungeKutta(timestep)
        self.calculateNewPosition()

    # Helper method to make things look nicer
    def addPositions(self, positions):
        positions.append(
            {
                "x1": self.model1.position["x"],
                "y1": self.model1.position["y"],
                "x2": self.model2.position["x"],
                "y2": self.model2.position["y"],
            }
        )

    def coordinatesEuler(self, h):
        positions = []
        for i in range(self.T):
            self.calculatePositionEuler(h)
            self.addPositions(positions)
        return positions

    def coordinatesRungeKutta(self, h):
        positions = []
        for i in range(self.T):
            self.calculatePositionRungeKutta(h)
            self.addPositions(positions)
        return positions


class TwoBodyModel:
    def __init__(self, mass=0, position={"x": 0, "y": 0}):
        self.position = position
        self.mass = mass


class TwoBodyApp:
    def get_input(self):
        t = int(input("T = "))
        delta_t = float(input("\u03B4t = "))
        mass_ratio = float(input("mass ratio = "))
        eccentricity = float(input("eccentricity = "))
        method = int(input("1. Euler's method \n2. Runge-Kutta method"))
        calculator = TwoBodyController(mass_ratio, eccentricity, t)
        if method == 1:
            return calculator.coordinatesEuler(delta_t)
        elif method == 2:
            return calculator.coordinatesRungeKutta(delta_t)

    def run(self):
        output = self.get_input()
        stringToWrite = ""
        for i in output:
            stringToWrite += (
                str(i["x1"])
                + "\n"
                + str(i["y1"])
                + "\n"
                + str(i["x2"])
                + "\n"
                + str(i["y2"])
                + "\n"
            )
        f = open("coordinates.txt", "w")
        f.write(stringToWrite)
        f.close()


if __name__ == "__main__":
    app = TwoBodyApp()
    app.run()

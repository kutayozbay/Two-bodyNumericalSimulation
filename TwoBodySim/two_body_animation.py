import pygame


class TwoBodyView:
    # File I/O
    def readFile(self, fileName):
        file = open(fileName, "r")
        lines = []
        for line in file:
            lines.append(line)

        return lines

    # Displaying Planets
    def planet(self, screen, planetImg, planet2Img, x, y, x2, y2):
        screen.blit(planetImg, (x, y))
        screen.blit(planet2Img, (x2, y2))

    def animation(self, fname):
        # Initialize the pygame
        pygame.init()

        # Create the screen
        screen = pygame.display.set_mode((1400, 1100))

        # Title
        pygame.display.set_caption("TwoBodyProblem")

        # Background
        background = pygame.image.load("background.jpg")

        # Planet1
        planetImg = pygame.image.load("planet.png")
        planetX = 700
        planetY = 550
        planetXInitial = 700
        planetYInitial = 550

        # Coefficient
        coefficient = 100

        # Center of objects
        center = 32

        # Planet2
        planet2Img = pygame.image.load("neptune.png")
        planet2X = 700
        planet2Y = 550
        planet2XInitial = 700
        planet2YInitial = 550

        # Simulation Loop

        paused = False

        x1_array = []
        y1_array = []
        x2_array = []
        y2_array = []
        x1_array_orbit = []
        y1_array_orbit = []
        x2_array_orbit = []
        y2_array_orbit = []
        for i in range(len(fname)):
            if (i + 1) % 4 == 0:
                y2_array.append(fname[i])
            elif (i + 1) % 4 == 1:
                x1_array.append(fname[i])
            elif (i + 1) % 4 == 2:
                y1_array.append(fname[i])
            elif (i + 1) % 4 == 3:
                x2_array.append(fname[i])
        index = 0
        running = True
        rewind = False
        while running:

            # RGB = Red, Green, Blue
            # screen.fill((0, 0, 0))

            # Background
            screen.blit(background, (0, 0))

            # Quit / Pause/Unpause  / Rewind
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Pausing
                        paused = True
                    elif event.key == pygame.K_u:  # Unpausing
                        paused = False
                    elif event.key == pygame.K_r:  # Rewind/Unrewind
                        rewind = not rewind

            if not paused:
                x1_array[index] = float(x1_array[index])
                y1_array[index] = float(y1_array[index])
                x2_array[index] = float(x2_array[index])
                y2_array[index] = float(y2_array[index])
                planetX = (x1_array[index] * coefficient) + planetXInitial - center
                planetY = (y1_array[index] * coefficient) + planetYInitial - center
                planet2X = (x2_array[index] * coefficient) + planet2XInitial - center
                planet2Y = (y2_array[index] * coefficient) + planet2YInitial - center

                # Orbits Calculation
                planetX = round(planetX, 0)
                x1_array_orbit.append(planetX)
                planetY = round(planetY, 0)
                y1_array_orbit.append(planetY)
                planet2X = round(planet2X, 0)
                x2_array_orbit.append(planet2X)
                planet2Y = round(planet2Y, 0)
                y2_array_orbit.append(planet2Y)

                # Drawing Orbits
                for k in range(len(x1_array_orbit)):
                    screen.set_at(
                        (
                            int(x1_array_orbit[k]) + center,
                            int(y1_array_orbit[k]) + center,
                        ),
                        (200, 0, 0),
                    )
                    screen.set_at(
                        (
                            int(x2_array_orbit[k]) + center,
                            int(y2_array_orbit[k]) + center,
                        ),
                        (0, 0, 128),
                    )

                if not rewind:
                    if index < (len(x1_array) - 1):
                        index += 1
                    elif index == (len(x1_array) - 1):
                        index = 0
                else:
                    if index >= 0:
                        index -= 1
                    else:
                        index = len(x1_array) - 1

                self.planet(
                    screen, planetImg, planet2Img, planetX, planetY, planet2X, planet2Y
                )

                pygame.display.update()


if __name__ == "__main__":
    app = TwoBodyView()
    fname = app.readFile("coordinates.txt")
    app.animation(fname)

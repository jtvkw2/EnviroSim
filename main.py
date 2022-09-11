# Libraries
import organism
import plants
import numpy as np
import arcade
from opensimplex import OpenSimplex

# Constants
screen_title = "Genetic Evolution Simulator"
screen_sidebar_width = 400
screen_width = 1200 + screen_sidebar_width
screen_height = 800
plant_start_amount = 50
organism_start_amount = 50
scaling = 0.5
block_size = 2


class Environment(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.season_list = ['Spring', 'Summer', 'Fall', 'Winter']
        # Set Background Color
        arcade.set_background_color(arcade.color.AMAZON)

        # Set Variables
        self.playable_width = width - screen_sidebar_width
        self.playable_height = height
        self.seed = 12345
        self.year = 0
        self.season = 1
        self.day = 1
        self.time = 0
        self.hour = 0
        self.min = 0
        self.number_of_plants = 0
        self.number_of_organisms = 0

        # Test Player
        self.shape = (self.playable_width, self.playable_height)
        self.curr_state = np.zeros(self.shape)
        self.curr_state_shape_list = None
        self.plant_list = []
        self.organism_list = []

    def generate_world(self, seed):
        tmp = OpenSimplex(seed)
        for x in range(0, self.playable_width):
            for y in range(0, self.playable_height):
                z = tmp.noise2(x=x * 0.01, y=y * 0.01)
                self.curr_state[x][y] = self.z_to_id(z)

    @staticmethod
    def z_to_id(z):
        if z >= 0.9:
            state_id = 1  # Peak of Mountain
        elif z >= 0.8:
            state_id = 2  # Mid Mountain
        elif z >= 0.7:
            state_id = 3  # Low Mountain
        elif z >= 0.6:
            state_id = 4  # Dirt
        elif z >= 0.5:
            state_id = 5  # High Grass Plains
        elif z >= 0.4:
            state_id = 6  # Grassland
        elif z >= 0.3:
            state_id = 7  # Low Grass
        elif z >= 0.2:
            state_id = 8  # Beach
        elif z >= 0.1:
            state_id = 9  # Shallow Water
        else:
            state_id = 10  # Water
        return state_id

    @staticmethod
    def get_color(state_id):
        if state_id == 1:
            color = arcade.color.ALICE_BLUE
        elif state_id == 2:
            color = arcade.color.DARK_GRAY
        elif state_id == 3:
            color = arcade.color.BATTLESHIP_GREY
        elif state_id == 4:
            color = arcade.color.BISTRE_BROWN
        elif state_id == 5:
            color = arcade.color.CADMIUM_GREEN
        elif state_id == 6:
            color = arcade.color.CELADON
        elif state_id == 7:
            color = arcade.color.BUD_GREEN
        elif state_id == 8:
            color = arcade.color.BLOND
        elif state_id == 9:
            color = arcade.color.BLIZZARD_BLUE
        else:
            color = arcade.color.BLUE
        return color

    def generate_weather(self):
        return

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # World Generation
        self.generate_world(self.seed)
        self.curr_state_shape_list = arcade.ShapeElementList()
        for x in range(0, self.playable_width, 2):
            for y in range(0, self.playable_height, 2):
                shape = arcade.create_rectangle_filled(x, y, 2, 2, self.get_color(self.curr_state[x][y]))
                self.curr_state_shape_list.append(shape)
        # self.generate_weather()

        # Spawn Creatures
        # for i in range(plant_start_amount):
        #    tmp_plant = arcade.Sprite(,)
        #    self.all_sprites.append(plants.Plant())
        # organism.Organism()

    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()
        self.curr_state_shape_list.draw()
        # self.all_sprites.draw()

        # Draw time info
        arcade.draw_text('Time: ' + "{:02d}".format(int(self.hour)) + ':' + "{:02d}".format(int(self.min)),
                         self.playable_width + 10, self.height - 50,
                         arcade.color.BLACK, 25, 80, 'left')
        arcade.draw_text('Day: ' + str(self.day), self.playable_width + 10, self.height - 150, arcade.color.BLACK, 25,
                         80, 'left')
        arcade.draw_text('Season: ' + self.season_list[self.season - 1], self.playable_width + 10, self.height - 250,
                         arcade.color.BLACK, 25, 80, 'left')
        arcade.draw_text('Year: ' + str(self.year), self.playable_width + 10, self.height - 350,
                         arcade.color.BLACK, 25, 80, 'left')
        arcade.draw_text('# of Plants: ' + str(self.number_of_plants), self.playable_width + 10, self.height - 450,
                         arcade.color.BLACK, 25, 80, 'left')
        arcade.draw_text('# of Animals: ' + str(self.number_of_organisms), self.playable_width + 10, self.height - 550,
                         arcade.color.BLACK, 25, 80, 'left')

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.min += delta_time * 10
        if self.min >= 60:
            self.min = 0
            self.hour += 1
            if self.hour >= 24:
                self.min = 0
                self.hour = 0
                self.day += 1
            if self.day % 90 == 0:
                self.season += 1
                if self.season == 5:
                    self.season = 0
                    self.year += 1
            self.number_of_plants = len(self.plant_list)
            self.number_of_organisms = len(self.organism_list)


def main():
    """ Main function """
    game = Environment(screen_width, screen_height, screen_title)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()

# %%

import tkinter as tk
import random
from a3_support import *
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from PIL import Image, ImageTk

__author__ = "Harold Shaw, 47020665"
__email__ = "s4702066@student.uq.edu.au"

class Entity(object):
    """An abstract class representing an Entity within Hacker."""
    def display(self) -> str:
        """(str) Returns character representing Entity."""
        raise NotImplementedError

    def __repr__(self) -> str:
        """(str) Returns representation of Entity."""
        return f'{self.__class__.__name__}()'


class Player(Entity):
    """A class representing a Player Entity within Hacker."""
    def display(self) -> str:
        return PLAYER


class Destroyable(Entity):
    """A class representing a Destroyable Entity within Hacker."""
    def display(self) -> str:
        return DESTROYABLE


class Collectable(Entity):
    """A class representing a Collectable Entity within Hacker."""
    def display(self) -> str:
        return COLLECTABLE


class Blocker(Entity):
    """A class representing a Blocker Entity within Hacker."""
    def display(self) -> str:
        return BLOCKER


class Grid(object):
    """A class representing a Grid of Entities in Hacker."""
    def __init__(self, size: int) -> None:
        """Constructs a Grid.

        Parameters:
            size (int): Number of rows (and cols) in Grid.

        Returns:
            (None)
        """
        self._size = size
        self._entities = {}

    def get_size(self) -> int:
        """(int) Returns Grid size."""
        return self._size

    def add_entity(self, position: Position, entity: Entity) -> None:
        """Adds an Entity to Grid at Position.

        Parameters:
            position (Position): A Position on the Grid.
            entity (Entity): A Player, Destroyable, Collectable or Blocker.

        Returns:
            (None)
        """
        position_col = position.get_x()
        position_row = position.get_y()

        # Checks that iff entity is Player, it is in the correct position
        if (isinstance(entity, Player)) and \
           (position_col == ((self._size - 1) // 2) and not position_row):
            self._entities[position] = entity
        # Checks that iff entity is not a Player, it is in bounds
        if (not isinstance(entity, Player)) and \
           (position_row == (self._size - 1)) and (self.in_bounds(position)):
            self._entities[position] = entity
        return None

    def get_entities(self) -> Dict[Position, Entity]:
        """(Dict[Position, Entity]) Returns all Entities on Grid."""
        return self._entities.copy()

    def get_entity(self, position: Position) -> Optional[Entity]:
        """Returns Entity at Position.

        Parameters:
            position (Position): A Position on the Grid.

        Returns:
            (Optional[Entity]): A Player, Destroyable, Collectable or Blocker.
        """
        return self.get_entities().get(position)

    def remove_entity(self, position: Position) -> None:
        """Removes an Entity from Grid at Position.

        Parameters:
            position (Position): A Position on the Grid.

        Returns:
            (None)
        """
        self._entities.pop(position)
        return None

    def serialise(self) -> Dict[Tuple[int, int], str]:
        """(Dict[Tuple[int, int], str]) Returns serialised mapping of Grid."""
        serialised = {}
        for entity in self.get_entities():
            position_col = entity.get_x()
            position_row = entity.get_y()
            serialised_position = (position_col, position_row)
            serialised_entity = self.get_entities().get(entity).display()
            serialised[serialised_position] = serialised_entity
        return serialised

    def in_bounds(self, position: Position) -> bool:
        """Determines whether Position is valid for Grid.

        Parameters:
            position (Position): A Position on the Grid.

        Returns:
            (bool): True iff (x >= 0 and x < GRID_SIZE) and
                        (y >= 1 and y < GRID_SIZE).
        """
        position_col = position.get_x()
        position_row = position.get_y()

        if not (position_col >= 0 and position_col < self.get_size()):
            return False
        if not (position_row >= 1 and position_row < self.get_size()):
            return False
        return True

    def __repr__(self) -> str:
        """(str) Returns representation of Grid."""
        return f'Grid({self._size})'


class Game(object):
    """A class representing a Game of Hacker."""
    def __init__(self, size: int) -> None:
        """Constructs a Game.

        Parameters:
            size (int): Number of rows (and cols) in Game Grid.

        Returns:
            (None)
        """
        self._flag = None
        self._grid = Grid(size)
        self._collectables_collected = 0
        self._destroyables_destroyed = 0
        self._total_shots = 0

        # Adds Player Entity to Game Entities
        self.get_grid().add_entity(self.get_player_position(), Player())

    def get_grid(self) -> Grid:
        """(Grid) Returns Game Grid."""
        return self._grid

    def get_player_position(self) -> Position:
        """(Position) Returns Position of Player on Grid."""
        median_col = (self.get_grid().get_size() - 1) // 2
        return Position(median_col, 0)

    def get_num_collected(self) -> int:
        """(int) Returns total Collectables collected."""
        return self._collectables_collected

    def get_num_destroyed(self) -> int:
        """(int) Returns total Destroyables destroyed."""
        return self._destroyables_destroyed

    def get_total_shots(self) -> int:
        """(int) Returns total number of shots taken in Game."""
        return self._total_shots

    def rotate_grid(self, direction: str) -> None:
        """Rotates Grid in Direction.

        Parameters:
            direction (str): Direction of Rotation.

        Returns:
            (None)
        """
        # Specifies rotational offset
        if direction == LEFT:
            offset = -1
        else:
            offset = 1

        to_be_rotated_grid = self.get_grid().get_entities()
        rotated_grid = {}

        for position in to_be_rotated_grid:
            position_col = position.get_x()
            position_row = position.get_y()

            # Keeps Player Position constant
            if position_row == 0:
                rotated_grid[position] = to_be_rotated_grid.get(position)
                continue

            # Checks special cases
            end_col = self.get_grid().get_size() - 1
            new_position = Position(position_col + offset, position_row)
            if (position_col == end_col) and (direction == RIGHT):
                new_position = Position(0, position_row)
            if (not position_col) and (direction == LEFT):
                new_position = Position(end_col, position_row)

            # Updates position with new position
            rotated_grid[new_position] = to_be_rotated_grid.get(position)

        # Updates grid entities
        self.get_grid()._entities = rotated_grid
        return None

    def _create_entity(self, display: str) -> Entity:
        """(Entity) Creates an Entity for Game."""
        all_entity_types = [Player(), Collectable(), Destroyable(), Blocker()]
        for entity in all_entity_types:
            if entity.display() == display:
                return entity
        raise NotImplementedError

    def generate_entities(self) -> None:
        """
        Method given to the students to generate a random amount of entities to
        add into the game after each step
        """
        # Generate amount
        entity_count = random.randint(0, self.get_grid().get_size() - 3)
        entities = random.choices(ENTITY_TYPES, k=entity_count)

        # Blocker in a 1 in 4 chance
        blocker = random.randint(1, 4) % 4 == 0

        # UNCOMMENT THIS FOR TASK 3 (CSSE7030)
        # bomb = False
        # if not blocker:
        #     bomb = random.randint(1, 4) % 4 == 0

        total_count = entity_count
        if blocker:
            total_count += 1
            entities.append(BLOCKER)

        # UNCOMMENT THIS FOR TASK 3 (CSSE7030)
        # if bomb:
        #     total_count += 1
        #     entities.append(BOMB)

        entity_index = random.sample(range(self.get_grid().get_size()),
                                     total_count)

        # Add entities into grid
        for pos, entity in zip(entity_index, entities):
            position = Position(pos, self.get_grid().get_size() - 1)
            new_entity = self._create_entity(entity)
            self.get_grid().add_entity(position, new_entity)

    def step(self) -> None:
        """Performs Game's 'step event'.

        A 'step event' is when all entities on a Game's Grid shift by an offset
        of (0, -1) in the direction of the Player Entity. The only entity which
        doesn't move during a 'step event' is the Player, as their position
        is fixed.

        Returns:
            (None)
        """
        offset = -1

        to_be_stepped_grid = self.get_grid().get_entities()
        stepped_grid = {}

        for position in to_be_stepped_grid:
            position_col = position.get_x()
            position_row = position.get_y()
            position_display = to_be_stepped_grid.get(position).display()

            # Keeps Player Position constant
            if position_row == 0:
                stepped_grid[position] = to_be_stepped_grid.get(position)
                continue

            # Checks if Game is lost
            if (position_row == 1) and (position_display == DESTROYABLE):
                self._flag = False

            # Checks special cases
            new_position = Position(position_col, position_row + offset)
            if not self.get_grid().in_bounds(new_position):
                continue

            # Updates Position with new Position
            stepped_grid[new_position] = to_be_stepped_grid.get(position)

        # Updates Grid Entities
        self.get_grid()._entities = stepped_grid
        self.generate_entities()
        return None

    def fire(self, shot_type: str) -> None:
        """Performs Player's 'fire' action.

        When a Player 'fires', they shoot either a 'collect' or 'destroy' shot
        iteratively down the Grid. If the first entity hit is compatible with
        the type of shot fired, relevant action will be taken.

        Parameters:
            shot_type (str): Type of shot fired - either COLLECT or DESTROY.

        Returns:
            (None)
        """
        player_position = self.get_player_position()
        player_col = player_position.get_x()
        entities = self.get_grid().get_entities()

        # Finds Position and type of Entity shot
        entity_shot = None
        for entity_row in range(1, self.get_grid().get_size()):
            test_position = Position(player_col, entity_row)
            if entities.get(test_position) is not None:
                position_shot = test_position
                entity_shot = entities.get(test_position).display()
                break

        # Handles Entity cases
        self._total_shots += 1
        if (entity_shot == DESTROYABLE) and (shot_type == DESTROY):
            self._destroyables_destroyed += 1
            self.get_grid()._entities.pop(position_shot)
        if (entity_shot == COLLECTABLE) and (shot_type == COLLECT):
            self._collectables_collected += 1
            self.get_grid()._entities.pop(position_shot)

        # Checks if Game is won
        if self.get_num_collected() == COLLECTION_TARGET:
            self._flag = True

        return None

    def has_won(self) -> bool:
        """(bool) True iff Player has won Game."""
        if self._flag:
            return self._flag
        return False

    def has_lost(self) -> bool:
        """(bool) True iff Player has lost Game."""
        if (not self._flag) and (self._flag is not None):
            return not self._flag
        return False


class AbstractField(tk.Canvas):
    """An abstract class inheriting from tk.Canvas."""
    def __init__(
        self,
        master: tk.Tk,
        rows: int,
        cols: int,
        width: int,
        height: int,
        **kwargs) -> None:
        """Constructs an AbstractField.

        Parameters:
            master (tk.Tk): The parent Tkinter object of AbstractField.
            rows (int): The number of rows in Grid of AbstractField.
            cols (int): The number of columns in Grid of AbstractField.
            width (int): The width of AbstractField in pixels.
            height (int): The height of AbstractField in pixels.
            **kwargs: Keyword arguments supported by tk.Canvas and
                        AbstractField.

        Returns:
            (None)
        """
        super().__init__(master, width=width, height=height, **kwargs)
        self._rows = rows
        self._cols = cols
        self._width = width
        self._height = height
        self._cell_width = self._width / self._cols
        self._cell_height = self._height / self._rows

    def get_bbox(self, position: Position) -> Tuple[int, int, int, int]:
        """Returns bounding box of Position on AbstractField's Grid.

        Parameters:
            position (Position): A Position in AbstractField.

        Returns:
            (Tuple[int, int, int, int]): The bounding box of Position in form
                (x_min, y_min, x_max, y_max).
        """
        position_col = position.get_x()
        position_row = position.get_y()
        x_min = position_col * self._cell_width
        y_min = position_row * self._cell_height
        x_max = x_min + self._cell_width
        y_max = y_min + self._cell_height
        bbox = (x_min, y_min, x_max, y_max)
        return bbox

    def pixel_to_position(self, pixel: Tuple[int, int]) -> Position:
        """Converts Pixel to Position.

        Parameters:
            pixel (Tuple[int, int]): Pixel in AbstractField.

        Returns:
            (Position): Returns Position of pixel in AbstractField.
        """
        pixel_col, pixel_row = pixel
        position_col = int(pixel_col // self._cell_width)
        position_row = int(pixel_row // self._cell_height)
        return Position(position_col, position_row)

    def get_position_center(self, position: Position) -> Tuple[int, int]:
        """Returns pixel at center of Position.

        Parameters:
            position (Position): A Position in AbstractField.

        Returns:
            (Tuple[int, int]): The pixel coordinates of Position's center.
        """
        x_min, y_min, x_max, y_max = self.get_bbox(position)
        x = (x_min + x_max) / 2
        y = (y_min + y_max) / 2
        position_center = (x, y)
        return position_center

    def annotate_position(self, position: Position, text: str) -> None:
        """Annotates Position center with Text.

        Parameters:
            position (Position): A Position in AbstractField.
            text (str): Annotation.

        Returns:
            (None)
        """
        position_center = self.get_position_center(position)
        x, y = position_center
        self.create_text(x, y, text=text)
        return None


class GameField(AbstractField):
    """A class visually representing Hacker Game Grid."""
    def __init__(
        self,
        master: tk.Tk,
        size: int,
        width: int,
        height: int,
        **kwargs) -> None:
        """Constructs a GameField.

        Parameters:
            master (tk.Tk): The parent Tkinter object of GameField.
            size (int): The number of rows (and cols) in Game Grid.
            width (int): The width in pixels of the GameField.
            height (int): The height in pixels of the GameField.
            **kwargs (int): Keyword arguments.

        Returns:
            (None)
        """
        super().__init__(
            master,
            rows=size,
            cols=size,
            width=width,
            height=height,
            bg=FIELD_COLOUR,
            **kwargs)
        self._size = size

    def draw_grid(self, entities: Dict[Position, Entity]) -> None:
        """Draws Grid of Entities.

        Parameters:
            entities (Dict[Position, Entity]): Entites of Game.

        Returns:
            (None)
        """
        for position in entities:
            bbox = self.get_bbox(position)
            text = entities.get(position).display()
            colour = COLOURS.get(text)
            self.create_rectangle(bbox, fill=colour)
            self.annotate_position(position, text)
        return None

    def draw_player_area(self) -> None:
        """Draws Player Area of Grid.

        This covers the row of the Game Grid in which the Player sits.

        Returns:
            (None)
        """
        x_max = self._size * self._cell_width
        y_max = self._cell_height
        bbox = (0, 0, x_max, y_max)
        self.create_rectangle(bbox, fill=PLAYER_AREA)
        return None


class ScoreBar(AbstractField):
    """A class visually representing Player Shot Statistics."""
    def __init__(self, master: tk.Tk, rows: int, **kwargs) -> None:
        """Constructs a ScoreBar.

        Parameters:
            master (tk.Tk): The parent Tkinter object of ScoreBar.
            rows (int): The number of rows in Score Bar.
            **kwargs (int): Keyword arguments.

        Returns:
            (None)
        """
        super().__init__(
            master,
            rows=rows,
            cols=2,
            width=SCORE_WIDTH,
            height=MAP_HEIGHT,
            bg=SCORE_COLOUR,
            **kwargs)

    def draw(self, game: Game) -> None:
        """Visually displays Game's ScoreBar.

        Parameters:
            game (Game): Current instance of Game.

        Returns:
            (None)
        """
        num_collected = str(game.get_num_collected())
        num_destroyed = str(game.get_num_destroyed())
        x = SCORE_WIDTH / 2
        y = self._cell_height / 2
        self.create_text(x, y, text="Score", font=('Arial', 35))
        self.annotate_position(Position(0, 1), "Collected:")
        self.annotate_position(Position(0, 2), "Destroyed:")
        self.annotate_position(Position(1, 1), num_collected)
        self.annotate_position(Position(1, 2), num_destroyed)


class HackerController(object):
    """A class representing the Game Controller for Hacker."""
    def __init__(self, master: tk.Tk, size: int) -> None:
        """Constructs a HackerController.

        Parameters:
            master (tk.Tk): The parent Tkinter object of HackerController.
            size (int): The number of rows (and cols) in Game's Grid/Field.

        Returns:
            (None)
        """
        self._master = master
        self._size = size

        # Constructs Title
        self._title = tk.Label(
            text=TITLE,
            bg=TITLE_BG,
            font=TITLE_FONT
        )
        self._title.pack(fill=tk.X)

        # Constructs Game Model
        self._game = Game(self._size)

        # Constructs Game Field
        self._game_field = GameField(
            self._master,
            self._size,
            width=MAP_WIDTH,
            height=MAP_HEIGHT
        )
        self._game_field.pack(side=tk.LEFT)

        # Constructs Score Bar
        self._score_bar = ScoreBar(
            self._master,
            self._size
        )
        self._score_bar.pack(side=tk.LEFT)

        # Handles any key pressed by user
        self._master.bind("<Key>", self.handle_keypress)

        # Visually displays initial game view
        self._game_field.draw_player_area()
        self._game_field.draw_grid(self._game.get_grid().get_entities())
        self._score_bar.draw(self._game)

        # Initiates Game's 'step event'
        self._step_after = self._master.after(2000, self.step)

    def handle_keypress(self, event) -> None:
        """Handles User KeyPresses.

        Parameters:
            event (KeyPress): The KeyPress inputted by user.

        Returns:
            (None)
        """
        # Handles rotating
        if event.char == LEFT or event.char == LEFT.lower():
            self.handle_rotate(LEFT)
        if event.char == RIGHT or event.char == RIGHT.lower():
            self.handle_rotate(RIGHT)

        # Handles firing
        if event.keysym == "return" or event.keysym == "Return":
            self.handle_fire(COLLECT)
        if event.keysym == DESTROY.lower():
            self.handle_fire(DESTROY)
        return None

    def check_game_over(self) -> None:
        """(None) Destroys Game iff it is over."""
        if self._game.has_won():
            mb.showinfo(message='You win!')
            self._master.destroy()
        if self._game.has_lost():
            mb.showinfo(message='You lost!')
            self._master.destroy()

    def draw(self, game: Game) -> None:
        """Clears and Redraws View from Model.

        Parameters:
            game (Game): Current instance of Game.

        Returns:
            (None)
        """
        # Clear canvases
        self._score_bar.delete(tk.ALL)
        self._game_field.delete(tk.ALL)

        # Redraws GameField and ScoreBar
        self._game_field.draw_player_area()
        self._game_field.draw_grid(game.get_grid().get_entities())
        self._score_bar.draw(game)

        # Handles game won or lost
        self.check_game_over()
        return None

    def handle_rotate(self, direction: str) -> None:
        """Rotates Grid of Entities in direction specified by user before
        updating the Game View to reflect these changes.

        Parameters:
            direction (str): Direction of Rotation.

        Returns:
            (None)
        """
        self._game.rotate_grid(direction)
        self.draw(self._game)
        return None

    def handle_fire(self, shot_type: str) -> None:
        """Fires shot of shot type specified by user before updating the
        Game View to reflect any changes.

        Parameters:
            shot_type (str): Type of shot fired - either COLLECT or DESTROY.

        Returns:
            (None)
        """
        self._game.fire(shot_type)
        self.draw(self._game)
        return None

    def step(self) -> None:
        """Performs Game's 'step event' before updating the Game's View to
        reflect updated Entity Grid.

        Returns:
            (None)
        """
        self._game.step()
        self.draw(self._game)

        # Inititates recursive 'step event' loop
        self._step_after = self._master.after(2000, self.step)
        return None


class ImageGameField(GameField):
    """A class visually representing Hacker Game Grid using Images."""
    def draw_grid(self, entities: Dict[Position, Entity]) -> None:
        for position in entities:
            bbox = self.get_bbox(position)
            x_min, y_min, x_max, y_max = bbox

            # Calculates new dimensions for Entity Image
            x_resize = int(x_max - x_min)
            y_resize = int(y_max - y_min)

            # Gets Image for respective Entity
            text = entities.get(position).display()
            image_file_name = IMAGES.get(text)

            # Gets Image and converts to appropriate size
            entity_image = Image.open('images/' + image_file_name).resize(
                (x_resize, y_resize)
            )

            # Adds Image to Game Field
            photo = ImageTk.PhotoImage(entity_image)
            label = tk.Label(image=photo)
            label.image = photo
            x, y = self.get_position_center(position)
            self.create_image(x, y, image=photo)
        return None


class StatusBar(tk.Frame):
    """A class representing the Status of a Hacker Game."""
    def __init__(
        self,
        master: tk.Tk,
        width: int,
        height: int,
        **kwargs) -> None:
        """Constructs a StatusBar.

        Parameters:
            master (tk.Tk): The parent Tkinter object of StatusBar.
            width (int): The width of the StatusBar in pixels.
            height (int): The height of the StatusBar in pixels.
            **kwargs: Keyword arguments supported by both tk.Frame and
                        StatusBar.

        Returns:
            (None)
        """
        super().__init__(
            master,
            width=width,
            height=height,
            bg='white',
            **kwargs)


class AdvancedHackerController(HackerController):
    """A class representing an advanced Game Controller for Hacker."""
    def __init__(self, master: tk.Tk, size: int) -> None:
        self._master = master
        self._size = size
        self._minute = 0
        self._second = 0
        self._status_bar_bg = 'white'
        self._status_bar_fg = 'black'

        # Constructs Menubar
        self._hacker_menubar = tk.Menu(self._master)
        self._master.config(menu=self._hacker_menubar)

        # Constructs File Menu
        self._file_menu = tk.Menu(self._hacker_menubar)
        self._hacker_menubar.add_cascade(label="File", menu=self._file_menu)
        self._file_menu.add_command(label="New game", command=self.new)
        self._file_menu.add_command(label="Save game", command=self.save)
        self._file_menu.add_command(label="Load game", command=self.load)
        self._file_menu.add_command(label="Quit", command=self.quit)

        # Constructs Title
        self._title = tk.Label(
            text=TITLE,
            bg=TITLE_BG,
            font=TITLE_FONT
        )
        self._title.pack(fill=tk.X)

        # Constructs Game Model
        self._game = Game(self._size)

        # Constructs Middle Frame (for Image Game Field and Score Bar)
        self._middle_frame = tk.Frame(
            self._master
        )
        self._middle_frame.pack()

        # Constructs Image Game Field
        self._game_field = ImageGameField(
            self._middle_frame,
            self._size,
            width=MAP_WIDTH,
            height=MAP_HEIGHT
        )
        self._game_field.pack(side=tk.LEFT)

        # Constructs Score Bar
        self._score_bar = ScoreBar(
            self._middle_frame,
            self._size
        )
        self._score_bar.pack(side=tk.LEFT)

        # Constructs Status Bar
        self._status_bar_width = MAP_WIDTH + SCORE_WIDTH
        self._status_bar = StatusBar(
            self._master,
            width=self._status_bar_width,
            height=50 # sort this out
        )
        self._status_bar.pack(
            fill=tk.X,
            expand=tk.TRUE
        )

        # Constructs Shots Frame (for Shot Counter)
        self._shots_frame = tk.Frame(
            self._status_bar,
            bg=self._status_bar_bg
        )
        self._shots_frame.pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=tk.TRUE
        )

        # Constructs Shots Frame Labels
        self._shot_counter_header = tk.Label(
            self._shots_frame,
            text="Total Shots",
            bg=self._status_bar_bg,
            fg=self._status_bar_fg
        )
        self._shot_counter_header.pack()
        self._shot_counter_value = tk.Label(
            self._shots_frame,
            text=str(self._game.get_total_shots()),
            bg=self._status_bar_bg,
            fg=self._status_bar_fg
        )
        self._shot_counter_value.pack()

        # Constructs Timer Frame (for Game Timer)
        self._timer_frame = tk.Frame(
            self._status_bar,
            bg=self._status_bar_bg
        )
        self._timer_frame.pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=tk.TRUE
        )

        # Constructs Timer Frame Labels
        self._game_timer_header = tk.Label(
            self._timer_frame,
            text="Timer",
            bg=self._status_bar_bg,
            fg=self._status_bar_fg
        )
        self._game_timer_header.pack()
        self._game_timer_text = f'{self._minute}m {self._second}s'
        self._game_timer_value = tk.Label(
            self._timer_frame,
            text=self._game_timer_text,
            bg=self._status_bar_bg,
            fg=self._status_bar_fg
        )
        self._game_timer_value.pack()

        # Constructs PausePlay Frame (for 'Pause/Play' Button)
        self._pauseplay_frame = tk.Frame(
            self._status_bar,
            bg=self._status_bar_bg
        )
        self._pauseplay_frame.pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=tk.TRUE
        )

        # Constructs PausePlay Frame Button
        self._pause_play_text = "Pause"
        self._pause_play_value = tk.Button(
            self._pauseplay_frame,
            text="Pause",
            command=self.toggle_pause_play,
            highlightbackground=self._status_bar_bg,
            fg=self._status_bar_fg
        )
        self._pause_play_value.pack()

        # Handles any key pressed by user
        self._master.bind("<Key>", self.handle_keypress)

        # Visually displays initial Game view
        self.draw(self._game)

        # Initiaites Game 'step event' and timer
        self._step_after = self._master.after(2000, self.step)
        self._timer_after = self._master.after(1000, self.increment_game_timer)

    def draw(self, game: Game) -> None:
        # Clear canvases
        self._score_bar.delete(tk.ALL)
        self._game_field.delete(tk.ALL)

        # Configures Shot Counter and Gamer Timer Labels
        self._shot_counter_value.config(text=str(game.get_total_shots()))
        self._game_timer_value.config(text=f'{self._minute}m {self._second}s')

        # Redraws ImageGameField and ScoreBar
        self._game_field.draw_player_area()
        self._game_field.draw_grid(game.get_grid().get_entities())
        self._score_bar.draw(game)

        # Handles game won or lost
        self.check_game_over()
        return None

    def increment_game_timer(self) -> None:
        """(None) Increments the Game timer by 1 second."""
        if self._second == 59:
            self._minute += 1
            self._second = 0
        else:
            self._second += 1
        self._game_timer_value.config(text=f'{self._minute}m {self._second}s')
        self._timer_after = self._master.after(1000, self.increment_game_timer)

    def get_pause_play_text(self) -> str:
        """(str) Returns current text of Pause/Play Button."""
        return self._pause_play_text

    def toggle_pause_play(self) -> None:
        """(None) Toggles Pause/Play Button."""
        if self.get_pause_play_text() == "Pause":
            self._pause_play_text = "Play"
            self._pause_play_value.config(text="Play")
            self._master.after_cancel(self._step_after)
            self._master.after_cancel(self._timer_after)
        else:
            self._pause_play_text = "Pause"
            self._pause_play_value.config(text="Pause")
            self._step_after = self._master.after(2000, self.step)
            self._timer_after = self._master.after(
                1000,
                self.increment_game_timer
            )

    def new(self) -> None:
        """(None) Creates a new Hacker Game."""
        # Cancels recursive step and timer loops
        self._master.after_cancel(self._step_after)
        self._master.after_cancel(self._timer_after)

        # Resets Game timer
        self._minute = 0
        self._second = 0
        self._game_timer_value.config(text=self._game_timer_text)

        # Resets Gam shots
        self._game._total_shots = 0
        self._shot_counter_value.config(text=str(self._game.get_total_shots()))
        self._game._collectables_collected = 0
        self._game._destroyables_destroyed = 0

        # Resets Game Grid
        self._game._grid._entities = {Position(3, 0): Player()}
        self.draw(self._game)

        # Recommences recursive step and timer loops
        self._step_after = self._master.after(2000, self.step)
        self._timer_after = self._master.after(1000, self.increment_game_timer)

    def save(self) -> None:
        """(None) Saves current Hacker Game to user-specified directory."""
        saved_file = fd.asksaveasfile(mode="w", defaultextension=".txt")
        saved_file = saved_file.name
        with open(saved_file, "w") as file:
            # Line 1 - minute
            file.write(str(self._minute) + '\n')
            # Line 2 - second
            file.write(str(self._second) + '\n')
            # Line 3 - total shots
            file.write(str(self._game.get_total_shots()) + '\n')
            # Line 4 - collectables
            file.write(str(self._game.get_num_collected()) + '\n')
            # Line 5 - destroyables
            file.write(str(self._game.get_num_destroyed()) + '\n')
            # Line 6 - entities
            file.write(str(self._game.get_grid().get_entities()))
        return None

    def load(self) -> None:
        """(None) Loads saved Hacker Game from user-specified directory."""
        file_name = fd.askopenfilename(
            title="Load game",
            initialdir='/',
        )
        with open(file_name, "r") as file:
            self._minute = int(file.readline())
            self._second = int(file.readline())
            self._game._total_shots = int(file.readline())
            self._game._collectables_collected = int(file.readline())
            self._game._destroyables_destroyed = int(file.readline())
            self._game._grid._entities = eval(file.readline())
            self._game._grid.add_entity(Position(3, 0), Player())
            self.draw(self._game)
        return None

    def quit(self) -> None:
        """(None) Ends current Hacker Game."""
        quit_confirmation = mb.askyesno(
            message="Are you sure you would like to quit?"
        )
        if quit_confirmation == tk.YES:
            self._master.destroy()

def start_game(root, TASK=TASK):
    """Starts a Game of Hacker."""
    controller = HackerController

    if TASK != 1:
        controller = AdvancedHackerController

    app = controller(root, GRID_SIZE)
    return app

def main():
    """Runs Hacker Game."""
    root = tk.Tk()
    root.title(TITLE)
    root.resizable(width=False, height=False)
    app = start_game(root)
    root.mainloop()

if __name__ == '__main__':
    main()

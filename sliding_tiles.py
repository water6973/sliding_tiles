import pygame
import sys
import random
from pygame.locals import *

class SlidingPuzzle:
    def __init__(self, image_path, rows=3, cols=4):
        pygame.init()
        
        # Game settings
        self.rows = rows
        self.cols = cols
        self.tile_size = 100
        self.width = cols * self.tile_size
        self.height = rows * self.tile_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Sliding Puzzle Game')
        
        # Load and process the image
        self.load_image(image_path)
        
        # Game state
        self.empty_pos = (self.cols - 1, self.rows - 1)  # Bottom right tile starts empty
        self.reset_game()

    def load_image(self, image_path):
        try:
            # Load the full image
            original_img = pygame.image.load(image_path)
            
            # Scale to fit the game window
            scaled_img = pygame.transform.scale(original_img, (self.width, self.height))
            
            # Create tiles by splitting the image
            self.tiles = []
            for row in range(self.rows):
                for col in range(self.cols):
                    # Create a new surface for the tile
                    tile = pygame.Surface((self.tile_size, self.tile_size))
                    # Set the clipping area to copy from the original image
                    tile.blit(scaled_img, (0, 0), 
                             (col * self.tile_size, row * self.tile_size, 
                              self.tile_size, self.tile_size))
                    # Store the tile
                    self.tiles.append(tile)
            
            # Last tile is empty (black)
            self.tiles[-1] = pygame.Surface((self.tile_size, self.tile_size))
            self.tiles[-1].fill((0, 0, 0))
        except pygame.error as e:
            print(f"Error loading image: {e}")
            sys.exit()

    def reset_game(self):
        # Create the solved state
        self.board = [[col + row * self.cols for col in range(self.cols)] for row in range(self.rows)]
        
        # Shuffle the board (make sure it's solvable)
        self.shuffle()

    def shuffle(self):
        # Start from solved state
        self.board = [[col + row * self.cols for col in range(self.cols)] for row in range(self.rows)]
        self.empty_pos = (self.cols - 1, self.rows - 1)
        
        # Apply random moves (ensures solvability)
        moves = 1000  # Number of random moves
        for _ in range(moves):
            possible_moves = []
            ex, ey = self.empty_pos
            
            # Check all four directions
            if ex > 0:                    # Left
                possible_moves.append((ex-1, ey))
            if ex < self.cols - 1:        # Right
                possible_moves.append((ex+1, ey))
            if ey > 0:                    # Up
                possible_moves.append((ex, ey-1))
            if ey < self.rows - 1:        # Down
                possible_moves.append((ex, ey+1))
            
            # Choose a random direction
            new_empty = random.choice(possible_moves)
            
            # Swap tiles
            self.swap_tiles(new_empty, self.empty_pos)
            self.empty_pos = new_empty

    def swap_tiles(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        self.board[y1][x1], self.board[y2][x2] = self.board[y2][x2], self.board[y1][x1]

    def is_solved(self):
        # Check if board is in solved state
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != col + row * self.cols:
                    return False
        return True

    def handle_click(self, mouse_pos):
        # Convert mouse position to grid position
        col = mouse_pos[0] // self.tile_size
        row = mouse_pos[1] // self.tile_size
        
        # Check if clicked position is adjacent to empty tile
        ex, ey = self.empty_pos
        
        if (col == ex and abs(row - ey) == 1) or (row == ey and abs(col - ex) == 1):
            # Swap the tiles
            self.swap_tiles((col, row), self.empty_pos)
            self.empty_pos = (col, row)
            
            # Check if puzzle is solved
            if self.is_solved():
                print("Congratulations! Puzzle solved!")
                pygame.time.delay(1000)  # Delay 1 second
                self.reset_game()

    def draw(self):
        # Clear the screen
        self.screen.fill((0, 0, 0))
        
        # Draw each tile
        for row in range(self.rows):
            for col in range(self.cols):
                tile_idx = self.board[row][col]
                tile_img = self.tiles[tile_idx]
                self.screen.blit(tile_img, (col * self.tile_size, row * self.tile_size))
        
        # Update display
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == KEYDOWN:
                    if event.key == K_r:  # Reset the game with 'R' key
                        self.reset_game()
                    elif event.key == K_q:  # Quit with 'Q' key
                        running = False
            
            # Draw the board
            self.draw()
            
            # Cap at 30 FPS
            clock.tick(30)
        
        pygame.quit()
        sys.exit()

def main():
    # Get image path from command line or use default
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        print("Please provide an image path as a command line argument.")
        print("Example: python sliding_puzzle.py your_image.jpg")
        sys.exit()
    
    # Create and run the game
    game = SlidingPuzzle(image_path)
    game.run()

if __name__ == "__main__":
    main()
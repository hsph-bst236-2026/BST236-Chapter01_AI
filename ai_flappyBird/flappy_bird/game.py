"""
Flappy Bird Game - PyScript Implementation
A browser-based Flappy Bird clone written in Python using PyScript.
"""

from pyscript import document, window
import random

# =============================================================================
# GAME CONSTANTS
# =============================================================================
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 600

# Bird settings
BIRD_X = 80
BIRD_WIDTH = 40
BIRD_HEIGHT = 30
GRAVITY = 0.5
FLAP_STRENGTH = -9
MAX_VELOCITY = 12

# Pipe settings
PIPE_WIDTH = 60
PIPE_GAP = 150
PIPE_SPEED = 3
PIPE_SPAWN_INTERVAL = 90  # frames

# Colors
SKY_COLOR = "#70c5ce"
GROUND_COLOR = "#ded895"
BIRD_COLOR = "#f7dc6f"
BIRD_OUTLINE = "#e67e22"
PIPE_COLOR = "#2ecc71"
PIPE_OUTLINE = "#27ae60"
TEXT_COLOR = "#fff"
SHADOW_COLOR = "rgba(0,0,0,0.3)"


# =============================================================================
# GAME CLASSES
# =============================================================================
class Bird:
    """Represents the player-controlled bird."""
    
    def __init__(self):
        self.x = BIRD_X
        self.y = CANVAS_HEIGHT // 2
        self.velocity = 0
        self.width = BIRD_WIDTH
        self.height = BIRD_HEIGHT
        self.rotation = 0
    
    def flap(self):
        """Make the bird jump upward."""
        self.velocity = FLAP_STRENGTH
    
    def update(self):
        """Update bird physics each frame."""
        # Apply gravity
        self.velocity += GRAVITY
        
        # Limit max falling speed
        if self.velocity > MAX_VELOCITY:
            self.velocity = MAX_VELOCITY
        
        # Update position
        self.y += self.velocity
        
        # Calculate rotation based on velocity
        self.rotation = min(max(self.velocity * 3, -30), 90)
    
    def draw(self, ctx):
        """Draw the bird on the canvas."""
        ctx.save()
        ctx.translate(self.x + self.width / 2, self.y + self.height / 2)
        ctx.rotate(self.rotation * 3.14159 / 180)
        
        # Bird body (ellipse)
        ctx.fillStyle = BIRD_COLOR
        ctx.beginPath()
        ctx.ellipse(0, 0, self.width / 2, self.height / 2, 0, 0, 2 * 3.14159)
        ctx.fill()
        ctx.strokeStyle = BIRD_OUTLINE
        ctx.lineWidth = 2
        ctx.stroke()
        
        # Wing
        ctx.fillStyle = BIRD_OUTLINE
        ctx.beginPath()
        ctx.ellipse(-5, 5, 12, 8, -0.3, 0, 2 * 3.14159)
        ctx.fill()
        
        # Eye
        ctx.fillStyle = "#fff"
        ctx.beginPath()
        ctx.arc(10, -5, 8, 0, 2 * 3.14159)
        ctx.fill()
        
        # Pupil
        ctx.fillStyle = "#000"
        ctx.beginPath()
        ctx.arc(12, -5, 4, 0, 2 * 3.14159)
        ctx.fill()
        
        # Beak
        ctx.fillStyle = "#e74c3c"
        ctx.beginPath()
        ctx.moveTo(15, 2)
        ctx.lineTo(28, 5)
        ctx.lineTo(15, 10)
        ctx.closePath()
        ctx.fill()
        
        ctx.restore()
    
    def get_rect(self):
        """Return collision rectangle (slightly smaller for fair gameplay)."""
        margin = 5
        return {
            'x': self.x + margin,
            'y': self.y + margin,
            'width': self.width - margin * 2,
            'height': self.height - margin * 2
        }


class Pipe:
    """Represents a pair of pipes (top and bottom)."""
    
    def __init__(self, x):
        self.x = x
        self.width = PIPE_WIDTH
        self.gap = PIPE_GAP
        
        # Random gap position (with margins from top/bottom)
        min_top = 80
        max_top = CANVAS_HEIGHT - self.gap - 120  # Leave room for ground
        self.top_height = random.randint(min_top, max_top)
        self.bottom_y = self.top_height + self.gap
        
        self.passed = False  # Track if bird passed this pipe
    
    def update(self):
        """Move the pipe leftward."""
        self.x -= PIPE_SPEED
    
    def draw(self, ctx):
        """Draw both top and bottom pipes."""
        # Top pipe
        self._draw_pipe(ctx, self.x, 0, self.width, self.top_height, True)
        
        # Bottom pipe
        bottom_height = CANVAS_HEIGHT - self.bottom_y - 50  # Account for ground
        self._draw_pipe(ctx, self.x, self.bottom_y, self.width, bottom_height, False)
    
    def _draw_pipe(self, ctx, x, y, width, height, is_top):
        """Draw a single pipe with cap."""
        cap_height = 30
        cap_width = width + 10
        cap_x = x - 5
        
        # Main pipe body
        ctx.fillStyle = PIPE_COLOR
        ctx.fillRect(x, y, width, height)
        ctx.strokeStyle = PIPE_OUTLINE
        ctx.lineWidth = 3
        ctx.strokeRect(x, y, width, height)
        
        # Pipe cap
        if is_top:
            cap_y = y + height - cap_height
        else:
            cap_y = y
        
        ctx.fillStyle = PIPE_COLOR
        ctx.fillRect(cap_x, cap_y, cap_width, cap_height)
        ctx.strokeStyle = PIPE_OUTLINE
        ctx.strokeRect(cap_x, cap_y, cap_width, cap_height)
        
        # Highlight effect
        ctx.fillStyle = "rgba(255,255,255,0.2)"
        ctx.fillRect(x + 5, y, 8, height)
    
    def is_off_screen(self):
        """Check if pipe has moved off the left side of screen."""
        return self.x + self.width < 0
    
    def get_rects(self):
        """Return collision rectangles for both pipes."""
        return [
            # Top pipe
            {'x': self.x, 'y': 0, 'width': self.width, 'height': self.top_height},
            # Bottom pipe
            {'x': self.x, 'y': self.bottom_y, 'width': self.width, 
             'height': CANVAS_HEIGHT - self.bottom_y}
        ]


# =============================================================================
# GAME STATE
# =============================================================================
class Game:
    """Main game controller."""
    
    def __init__(self):
        # Get canvas and context
        self.canvas = document.getElementById("gameCanvas")
        self.ctx = self.canvas.getContext("2d")
        
        # Game state
        self.state = "start"  # start, playing, gameover
        self.score = 0
        self.best_score = 0
        self.frame_count = 0
        
        # Game objects
        self.bird = Bird()
        self.pipes = []
        
        # Ground animation
        self.ground_x = 0
        
        # Hide loading message
        loading = document.getElementById("loading")
        loading.style.display = "none"
        
        # Set up event listeners
        self._setup_events()
        
        # Start game loop
        self._game_loop()
    
    def _setup_events(self):
        """Set up keyboard and mouse event handlers."""
        # Keyboard events
        def on_keydown(event):
            if event.code == "Space":
                event.preventDefault()
                self._handle_input()
        
        document.addEventListener("keydown", on_keydown)
        
        # Mouse/touch events on canvas
        def on_click(event):
            self._handle_input()
        
        self.canvas.addEventListener("click", on_click)
        self.canvas.addEventListener("touchstart", on_click)
    
    def _handle_input(self):
        """Handle player input (flap/restart)."""
        if self.state == "start":
            self.state = "playing"
            self.bird.flap()
        elif self.state == "playing":
            self.bird.flap()
        elif self.state == "gameover":
            self._reset_game()
    
    def _reset_game(self):
        """Reset game to initial state."""
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.frame_count = 0
        self.state = "start"
        self._update_score_display()
    
    def _update(self):
        """Update game state each frame."""
        if self.state != "playing":
            return
        
        self.frame_count += 1
        
        # Update bird
        self.bird.update()
        
        # Spawn new pipes
        if self.frame_count % PIPE_SPAWN_INTERVAL == 0:
            self.pipes.append(Pipe(CANVAS_WIDTH))
        
        # Update pipes
        for pipe in self.pipes:
            pipe.update()
            
            # Check if bird passed pipe
            if not pipe.passed and pipe.x + pipe.width < self.bird.x:
                pipe.passed = True
                self.score += 1
                self._update_score_display()
        
        # Remove off-screen pipes
        self.pipes = [p for p in self.pipes if not p.is_off_screen()]
        
        # Check collisions
        self._check_collisions()
        
        # Animate ground
        self.ground_x -= PIPE_SPEED
        if self.ground_x <= -50:
            self.ground_x = 0
    
    def _check_collisions(self):
        """Check for collisions with pipes, ground, and ceiling."""
        bird_rect = self.bird.get_rect()
        
        # Ground collision
        if self.bird.y + self.bird.height > CANVAS_HEIGHT - 50:
            self._game_over()
            return
        
        # Ceiling collision
        if self.bird.y < 0:
            self._game_over()
            return
        
        # Pipe collisions
        for pipe in self.pipes:
            for pipe_rect in pipe.get_rects():
                if self._rects_collide(bird_rect, pipe_rect):
                    self._game_over()
                    return
    
    def _rects_collide(self, r1, r2):
        """Check if two rectangles overlap."""
        return (r1['x'] < r2['x'] + r2['width'] and
                r1['x'] + r1['width'] > r2['x'] and
                r1['y'] < r2['y'] + r2['height'] and
                r1['y'] + r1['height'] > r2['y'])
    
    def _game_over(self):
        """Handle game over state."""
        self.state = "gameover"
        if self.score > self.best_score:
            self.best_score = self.score
            self._update_score_display()
    
    def _update_score_display(self):
        """Update the score display below the canvas."""
        display = document.getElementById("score-display")
        display.textContent = f"Score: {self.score} | Best: {self.best_score}"
    
    def _draw(self):
        """Render the game each frame."""
        ctx = self.ctx
        
        # Draw sky background
        ctx.fillStyle = SKY_COLOR
        ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)
        
        # Draw clouds (decorative)
        self._draw_clouds(ctx)
        
        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(ctx)
        
        # Draw ground
        self._draw_ground(ctx)
        
        # Draw bird
        self.bird.draw(ctx)
        
        # Draw score (large, in-game)
        if self.state == "playing":
            self._draw_score(ctx)
        
        # Draw start screen
        if self.state == "start":
            self._draw_start_screen(ctx)
        
        # Draw game over screen
        if self.state == "gameover":
            self._draw_game_over(ctx)
    
    def _draw_clouds(self, ctx):
        """Draw decorative clouds in background."""
        ctx.fillStyle = "rgba(255,255,255,0.8)"
        
        # Static cloud positions
        clouds = [(50, 80), (200, 120), (320, 60), (100, 200), (280, 180)]
        for x, y in clouds:
            ctx.beginPath()
            ctx.arc(x, y, 25, 0, 2 * 3.14159)
            ctx.arc(x + 25, y - 10, 20, 0, 2 * 3.14159)
            ctx.arc(x + 45, y, 25, 0, 2 * 3.14159)
            ctx.fill()
    
    def _draw_ground(self, ctx):
        """Draw the ground at bottom of screen."""
        ground_height = 50
        ground_y = CANVAS_HEIGHT - ground_height
        
        # Ground base
        ctx.fillStyle = GROUND_COLOR
        ctx.fillRect(0, ground_y, CANVAS_WIDTH, ground_height)
        
        # Ground pattern (stripes)
        ctx.fillStyle = "#c4a35a"
        for i in range(-1, 10):
            x = self.ground_x + i * 50
            ctx.fillRect(x, ground_y, 25, 10)
        
        # Ground top line
        ctx.fillStyle = "#5d8c2a"
        ctx.fillRect(0, ground_y, CANVAS_WIDTH, 10)
    
    def _draw_score(self, ctx):
        """Draw the current score in the center-top of screen."""
        ctx.fillStyle = TEXT_COLOR
        ctx.font = "bold 48px Arial"
        ctx.textAlign = "center"
        
        # Shadow
        ctx.fillStyle = SHADOW_COLOR
        ctx.fillText(str(self.score), CANVAS_WIDTH // 2 + 2, 72)
        
        # Main text
        ctx.fillStyle = TEXT_COLOR
        ctx.fillText(str(self.score), CANVAS_WIDTH // 2, 70)
    
    def _draw_start_screen(self, ctx):
        """Draw the start screen overlay."""
        # Semi-transparent overlay
        ctx.fillStyle = "rgba(0,0,0,0.3)"
        ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)
        
        # Title
        ctx.fillStyle = TEXT_COLOR
        ctx.font = "bold 48px Arial"
        ctx.textAlign = "center"
        ctx.fillText("Flappy Bird", CANVAS_WIDTH // 2, 200)
        
        # Instructions
        ctx.font = "24px Arial"
        ctx.fillText("Press SPACE or CLICK", CANVAS_WIDTH // 2, 300)
        ctx.fillText("to start!", CANVAS_WIDTH // 2, 340)
        
        # Bird animation hint
        ctx.font = "18px Arial"
        ctx.fillStyle = "#ffd700"
        ctx.fillText("🐦 Avoid the pipes! 🐦", CANVAS_WIDTH // 2, 420)
    
    def _draw_game_over(self, ctx):
        """Draw the game over screen overlay."""
        # Semi-transparent overlay
        ctx.fillStyle = "rgba(0,0,0,0.6)"
        ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)
        
        # Game Over text
        ctx.fillStyle = "#e74c3c"
        ctx.font = "bold 48px Arial"
        ctx.textAlign = "center"
        ctx.fillText("Game Over!", CANVAS_WIDTH // 2, 180)
        
        # Score
        ctx.fillStyle = TEXT_COLOR
        ctx.font = "32px Arial"
        ctx.fillText(f"Score: {self.score}", CANVAS_WIDTH // 2, 260)
        
        # Best score
        ctx.fillStyle = "#ffd700"
        ctx.fillText(f"Best: {self.best_score}", CANVAS_WIDTH // 2, 310)
        
        # Restart instruction
        ctx.fillStyle = TEXT_COLOR
        ctx.font = "24px Arial"
        ctx.fillText("Press SPACE or CLICK", CANVAS_WIDTH // 2, 400)
        ctx.fillText("to play again!", CANVAS_WIDTH // 2, 440)
    
    def _game_loop(self):
        """Main game loop using requestAnimationFrame."""
        self._update()
        self._draw()
        
        # Schedule next frame
        window.requestAnimationFrame(lambda dt: self._game_loop())


# =============================================================================
# START THE GAME
# =============================================================================
game = Game()

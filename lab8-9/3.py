import pygame
import math

pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Paint")

white = (255, 255, 255)
black = (0, 0, 0)
colors = [(0, 0, 0), (255, 0, 0), (0, 200, 0), (0, 0, 255), (255, 255, 0)]
current_color = black
tools = ['PEN', 'RECT', 'CIRCLE', 'ERASER', 'SQUARE', 'RIGHT\nTRI', 'EQUI\nTRI','RHOMBUS']
current_tool = 'PEN'
font = pygame.font.SysFont("docker", 12)
color_rectangles = []
tool_rectangles = []
drawing = False
start_pos = None
last_pos = None
canvas = pygame.Surface((1000, 700 - 110))
canvas.fill(white)
def toolbar():
    pygame.draw.rect(screen, (0, 0, 0), (420, 0, 1000, 3))
    pygame.draw.rect(screen, (0, 0, 0), (420, 100, 1000, 3))
    pygame.draw.rect(screen, (0, 0, 0), (420, 0, 3, 100))
    color_rectangles.clear()
    for i, col in enumerate(colors):
        rect = pygame.Rect(800 + i * 40, 10, 35, 35)
        pygame.draw.rect(screen, col, rect)
        pygame.draw.rect(screen, black, rect, 1)
        color_rectangles.append(rect)

    tool_rectangles.clear()
    for i, tool_name in enumerate(tools):
        rect = pygame.Rect(440 + i * 70, 55, 65, 40)
        pygame.draw.rect(screen, (180, 180, 180), rect)
        pygame.draw.rect(screen, black, rect, 1)
        
        if '\n' in tool_name:
            lines = tool_name.split('\n')
            for j, line in enumerate(lines):
                label = font.render(line, True, black)
                text_rect = label.get_rect(center=(rect.centerx, rect.centery - 8 + j * 16))
                screen.blit(label, text_rect)
        else:
            label = font.render(tool_name, True, black)
            text_rect = label.get_rect(center=rect.center)
            screen.blit(label, text_rect)
            
        tool_rectangles.append((rect, tool_name.replace('\n', '')))

def draw_square(start, end):
    width = end[0] - start[0]
    height = end[1] - start[1]
    size = min(abs(width), abs(height))
    if width < 0: size = -size
    if height < 0: size = -size
    rect = pygame.Rect(start[0], start[1], size, size)
    pygame.draw.rect(canvas, current_color, rect, 2)

def draw_right_triangle(start, end):
    points = [start, (start[0], end[1]), end]
    pygame.draw.polygon(canvas, current_color, points, 2)

def draw_equilateral_triangle(start, end):
    width = end[0] - start[0]
    height = start[1] - end[1]
    side_length = math.sqrt(width**2 + height**2)
    triangle_height = (math.sqrt(3)/2 * side_length)
    points = [
        start,
        (end[0], end[1]),
        (start[0] + width/2, start[1] - triangle_height)
    ]
    pygame.draw.polygon(canvas, current_color, points, 2)

def draw_rhombus(start, end):
    center_x = (start[0] + end[0]) / 2
    center_y = (start[1] + end[1]) / 2
    width = abs(end[0] - start[0])
    height = abs(end[1] - start[1])
    points = [
        (center_x, start[1]),
        (end[0], center_y),
        (center_x, end[1]),
        (start[0], center_y)
    ]
    pygame.draw.polygon(canvas, current_color, points, 2)

running = True
while running:
    screen.fill(white)
    screen.blit(canvas, (0, 110))
    toolbar()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos    
            if y <= 110:
                if y < 50:
                    for i, rect in enumerate(color_rectangles):
                        if rect.collidepoint(x, y):
                            current_color = colors[i]
                else:
                    for rect, tool_name in tool_rectangles:
                        if rect.collidepoint(x, y):
                            current_tool = tool_name
                            print(f"Selected tool: {current_tool}")
            else:
                drawing = True
                start_pos = (x, y - 110)
                last_pos = start_pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing and start_pos:
                end_pos = (event.pos[0], event.pos[1] - 110)
                if current_tool == 'RECT':
                    rect = pygame.Rect(start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
                    pygame.draw.rect(canvas, current_color, rect, 2)
                elif current_tool == 'CIRCLE':
                    radius = int(((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2)**0.5)
                    pygame.draw.circle(canvas, current_color, start_pos, radius, 2)               
                elif current_tool == 'SQUARE':
                    draw_square(start_pos, end_pos)               
                elif current_tool == 'RIGHTTRI':
                    draw_right_triangle(start_pos, end_pos)
                elif current_tool == 'EQUITRI':
                    draw_equilateral_triangle(start_pos, end_pos)  
                elif current_tool == 'RHOMBUS':
                    draw_rhombus(start_pos, end_pos)

            drawing = False
            start_pos = None
            last_pos = None

        elif event.type == pygame.MOUSEMOTION:
            if drawing and current_tool in ['PEN', 'ERASER']:
                mouse_x, mouse_y = event.pos
                mouse_y -= 110
                if last_pos:
                    color_to_use = white if current_tool == 'ERASER' else current_color
                    pygame.draw.line(canvas, color_to_use, last_pos, (mouse_x, mouse_y), 4)

                last_pos = (mouse_x, mouse_y)

    pygame.display.flip()
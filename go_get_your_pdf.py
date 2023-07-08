import re
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.markers import MarkerStyle
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from fpdf import FPDF
import numpy as np

# Function to extract moves, comments, and alternative moves from the SGF content
def extract_moves_comments_and_alternatives(sgf_content):
    pattern = re.compile(r';(?P<color>[B|W])\[(?P<pos>[a-z][a-z])\](?:C\[(?P<comment>.*?)\])?')
    matches = pattern.findall(sgf_content)

    moves = []
    comments = {}
    alternatives = []
    for i, match in enumerate(matches):
        color, pos, comment = match
        moves.append((color, (ord(pos[0]) - 96, ord(pos[1]) - 96)))
        if comment:
            comments[i] = comment.replace('\n', ' ')
            # Check for alternative moves in comment
            alt_moves = re.findall(r'\((?P<color>[B|W])\[(?P<pos>[a-z][a-z])\]\)', comment)
            for alt_move in alt_moves:
                alt_color, alt_pos = alt_move
                alternatives.append((i, (alt_color, (ord(alt_pos[0]) - 96, ord(alt_pos[1]) - 96))))
    return moves, comments, alternatives

# Function to create an image of the Go board with the given moves
def create_board_image(board, moves):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.add_patch(patches.Rectangle((-1, -1), 20, 20, facecolor='burlywood'))
    for i in range(19):
        ax.plot([i, i], [0, 18], color='black')
        ax.plot([0, 18], [i, i], color='black')
    star_points = [(3, 3), (3, 9), (3, 15), (9, 3), (9, 9), (9, 15), (15, 3), (15, 9), (15, 15)]
    for x, y in star_points:
        ax.plot(x, y, marker='o', markersize=10, color='black')
    for i in range(len(moves)):
        color, (x, y) = moves[i]
        stone_color = 'white' if color == 'W' else 'black'
        text_color = 'black' if color == 'W' else 'white'
        marker = MarkerStyle('o', fillstyle='full')
        ax.plot(x-1, 19-y, marker=marker, markersize=20, color=stone_color, markeredgecolor='black')
        ax.text(x-1, 19-y, str(i+1), fontsize=10, ha='center', va='center', color=text_color)
    ax.set_aspect('equal', 'box')
    ax.set_xlim(-1, 19)
    ax.set_ylim(-1, 19)
    ax.axis('off')
    ax.invert_yaxis()
    return fig, ax

# Read the SGF file
with open("game1.sgf", "r") as file:
    sgf_content = file.read()

# Extract moves, comments, and alternative moves from the SGF content
moves, comments, alternatives = extract_moves_comments_and_alternatives(sgf_content)

# Generate high-resolution images for all the moves
for i in range(len(moves)):
    fig, ax = create_board_image(np.full((19, 19), '.'), moves[:i+1])
    canvas = FigureCanvas(fig)
    canvas.print_figure(f"high_res_board_state_{i+1}.png", dpi=100)
    plt.close(fig)

# Generate high-resolution images for all alternative moves
for i, (color, (x, y)) in alternatives:
    fig, ax = create_board_image(np.full((19, 19), '.'), moves[:i+1] + [(color, (x, y))])
    canvas = FigureCanvas(fig)
    canvas.print_figure(f"high_res_alternative_{i+1}.png", dpi=100)
    plt.close(fig)

pdf = FPDF()
pdf.set_font("Arial", size=12)

# Add the introductory message to the first page
pdf.add_page()
pdf.cell(0, 10, "This document was made using 'GoGetYourPDF', by Pedro Medeiros. Please, visit my GitHub: https://github.com/pedrohdemedeiros/go_get_your_pdf", ln=True)

for i in range(len(moves)):
    pdf.add_page()
    # Add the turn number at the top of the page
    pdf.cell(0, 10, f"Turn {i+1}", ln=True)
    pdf.image(f"high_res_board_state_{i+1}.png", x=10, y=30, w=180)
    if i in comments:
        pdf.set_xy(10, 210)
        pdf.multi_cell(0, 10, comments[i])

# Add alternative moves to the end of the document
for i, (color, (x, y)) in alternatives:
    pdf.add_page()
    pdf.cell(0, 10, f"Alternative for turn {i+1}", ln=True)
    pdf.image(f"high_res_alternative_{i+1}.png", x=10, y=30, w=180)

pdf_filename = "go_game_with_high_res_images.pdf"
pdf.output(pdf_filename)

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

BG = "#02050a"
PANEL = "#050b13"
BLUE = "#30a7ff"
CYAN = "#78d4ff"
WHITE = "#eaf6ff"
MUTED = "#66829c"
GREEN = "#4ef2a2"
LINE = "#153552"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else MONO, size)

def terminal(w, h, title):
    im = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(im)
    for y in range(0, h, 4):
        d.line((0, y, w, y), fill="#050b12")
    for x in range(0, w, 24):
        for y in range(58, h, 24):
            d.point((x, y), fill="#0e2539")
    d.rounded_rectangle((2, 2, w - 3, h - 3), 12, fill=PANEL, outline="#1e6599", width=2)
    d.rectangle((3, 3, w - 4, 48), fill="#071522")
    for i, color in enumerate(("#1b557d", "#2589c7", "#52bfff")):
        d.rectangle((20 + i * 22, 20, 30 + i * 22, 30), fill=color)
    d.text((104, 14), title, font=font(15), fill=MUTED)
    d.text((w - 154, 14), "● ONLINE", font=font(13), fill=GREEN)
    return im

def cursor(d, x, y, frame, size=18):
    if (frame // 7) % 2 == 0:
        d.rectangle((x, y, x + 10, y + size), fill=CYAN)

def type_text(text, progress):
    return text[:max(0, min(len(text), int(progress)))]

def save_gif(frames, path, duration=75):
    palette = frames[0].quantize(colors=64)
    frames = [im.quantize(palette=palette, dither=Image.Dither.NONE) for im in frames]
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=duration, loop=0, optimize=True)

# Main boot sequence: commands appear one by one and loop.
frames = []
lines = [
    ("$ ./start-profile", BLUE),
    ("[ OK ] identity........ Barış", GREEN),
    ("[ OK ] current_path.... C# fundamentals", GREEN),
    ("[ OK ] toolset......... Python", GREEN),
    ("[ OK ] creative_mode... Blender", GREEN),
]
for frame in range(108):
    im = terminal(1200, 650, "barismsi@github  /  profile.exe")
    d = ImageDraw.Draw(im)
    y = 78
    budget = frame * 2.15
    for text, color in lines:
        shown = type_text(text, budget)
        if shown:
            d.text((42, y), shown, font=font(18), fill=color)
        budget -= len(text) + 6
        y += 34
    reveal = max(0, frame - 60)
    if reveal:
        d.line((42, 270, 1156, 270), fill=LINE, width=2)
        d.text((42, 304), type_text("HELLO, I'M", reveal * 1.4), font=font(28, True), fill=CYAN)
        name = type_text("BARIS.", max(0, reveal - 12) * 1.5)
        d.text((37, 346), name, font=font(78, True), fill=WHITE)
        sub = type_text("LEARNING CODE. BUILDING TOOLS. CREATING MOTION.", max(0, reveal - 25) * 1.7)
        d.text((43, 450), sub, font=font(19), fill=BLUE)
        prompt = type_text("READY > explore_the_workspace", max(0, reveal - 42) * 1.5)
        d.text((43, 524), prompt, font=font(17), fill=MUTED)
        box = d.textbbox((43, 524), prompt, font=font(17))
        cursor(d, box[2] + 5, 524, frame)
    # Pixel signal on the right edge.
    for i in range(17):
        height = int(8 + 25 * (math.sin(frame * .16 + i * .7) + 1) / 2)
        d.rectangle((880 + i * 16, 592 - height, 887 + i * 16, 592), fill=(20, 90 + i * 5, 160 + i * 5))
    frames.append(im)
frames[90].save(ASSETS / "terminal-hero.png")
save_gif(frames, ASSETS / "terminal-hero.gif", 72)

# Current focus terminal.
frames = []
focus_lines = [
    "> focus.current = C# fundamentals;",
    "> tools.active  = Python;",
    "> canvas.mode   = Blender;",
    "> mindset       = learn + build + improve;",
]
for frame in range(72):
    im = terminal(1200, 330, "focus.log")
    d = ImageDraw.Draw(im)
    d.text((35, 72), "$ cat current_focus.log", font=font(17), fill=BLUE)
    budget = max(0, frame - 7) * 2.1
    y = 118
    for i, line in enumerate(focus_lines):
        shown = type_text(line, budget)
        if shown:
            d.text((48, y), f"{i + 1:02}", font=font(14), fill="#31536f")
            d.text((87, y), shown, font=font(17), fill=WHITE if i != 3 else CYAN)
        budget -= len(line) + 5
        y += 43
    cursor(d, 88 + min(max(budget, 0), 30) * 10, min(y, 283), frame, 16)
    frames.append(im)
frames[60].save(ASSETS / "focus-console.png")
save_gif(frames, ASSETS / "focus-console.gif", 78)

# Two independently clickable project terminals.
projects = [
    ("project-mineshader.gif", "01", "MineShader Enhancer", "Python / Blender", "material workflow tool", "open --repo mineshader"),
    ("project-color-reveal.gif", "02", "Color Reveal", "Python / Blender", "selective color add-on", "open --repo color-reveal"),
]
for filename, number, name, stack, desc, command in projects:
    frames = []
    for frame in range(58):
        im = terminal(760, 330, f"project_{number}.sh")
        d = ImageDraw.Draw(im)
        typed = type_text(f"$ {command}", frame * 1.15)
        d.text((28, 73), typed, font=font(15), fill=BLUE)
        if frame > 14:
            d.text((28, 117), name, font=font(29, True), fill=WHITE)
        if frame > 23:
            d.text((29, 165), f"[{stack}]", font=font(14), fill=GREEN)
            d.text((29, 198), desc, font=font(16), fill=MUTED)
        if frame > 33:
            d.rectangle((28, 250, 731, 252), fill=LINE)
            scan = int(28 + ((frame - 33) % 24) / 23 * 703)
            d.rectangle((28, 249, scan, 253), fill=BLUE)
            d.text((28, 278), "CLICK TO EXECUTE  >", font=font(13), fill=CYAN)
        for j in range(7):
            x = 600 + ((frame * 5 + j * 21) % 110)
            y = 113 + ((frame * 3 + j * 27) % 100)
            d.rectangle((x, y, x + 4, y + 4), fill=(32, 110 + j * 12, 180 + j * 9))
        frames.append(im)
    save_gif(frames, ASSETS / filename, 85)

# Footer command prompt.
frames = []
commands = ["$ connect --with barismsi", "Opening LinkedIn · Instagram · Repositories", "Connection ready."]
for frame in range(66):
    im = terminal(1200, 220, "connect.cmd")
    d = ImageDraw.Draw(im)
    budget = frame * 2.1
    y = 76
    for i, text in enumerate(commands):
        shown = type_text(text, budget)
        d.text((38, y), shown, font=font(16, i == 2), fill=BLUE if i == 0 else GREEN if i == 2 else WHITE)
        budget -= len(text) + 8
        y += 38
    for j in range(27):
        x = 738 + j * 15
        wave = int(8 * math.sin(frame * .18 + j * .5))
        d.rectangle((x, 172 + wave, x + 6, 178 + wave), fill=["#155989", "#2b9eeb", "#81d5ff"][j % 3])
    frames.append(im)
frames[54].save(ASSETS / "connect-console.png")
save_gif(frames, ASSETS / "connect-console.gif", 80)
print("Generated complete pixel terminal profile")

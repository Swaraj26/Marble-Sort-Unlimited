import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

colors_old = """val GameColors = listOf(
    Color(0xFFE6194B), // Red
    Color(0xFF3CB44B), // Green
    Color(0xFFFFE119), // Yellow
    Color(0xFF4363D8), // Blue
    Color(0xFFF58231), // Orange
    Color(0xFF911EB4), // Purple
    Color(0xFF42D4F4), // Cyan
    Color(0xFFF032E6), // Magenta
    Color(0xFFBFEF45), // Lime
    Color(0xFF9A6324)  // Brown
)"""

colors_new = """val GameColors = listOf(
    Color(0xFFE6194B), // Red
    Color(0xFF3CB44B), // Green
    Color(0xFFFFE119), // Yellow
    Color(0xFF4363D8), // Blue
    Color(0xFFF58231), // Orange
    Color(0xFF911EB4), // Purple
    Color(0xFF42D4F4), // Cyan
    Color(0xFFF032E6), // Magenta
    Color(0xFFBFEF45), // Lime
    Color(0xFF9A6324), // Brown
    Color(0xFF000000)  // Black
)"""

if colors_old in content:
    content = content.replace(colors_old, colors_new)
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(content)
    print("Patched GameColors")
else:
    print("GameColors not found!")

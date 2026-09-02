import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

tubegrid_old = """        val heightScale = if (rows > 0) (screenHeight / (baseTubeHeight * rows)) * 0.9f else 1f
        
        // Final scale factor ensures it fits vertically and horizontally
        val scaleFactor = minOf(widthScale, heightScale).coerceIn(0.4f, 1.5f)"""

tubegrid_new = """        val heightScale = if (rows > 0) (screenHeight / (baseTubeHeight * rows)) * 0.95f else 1f
        
        // Final scale factor ensures it fits vertically and horizontally
        val scaleFactor = minOf(widthScale, heightScale).coerceIn(0.4f, 2.0f)"""

if tubegrid_old in content:
    content = content.replace(tubegrid_old, tubegrid_new)
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(content)
    print("Patched TubeGrid")
else:
    print("TubeGrid not found!")

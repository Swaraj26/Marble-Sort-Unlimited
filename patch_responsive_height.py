import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

tube_grid_old = """        // Dynamically compute columns based on screen width. 
        // 4 tubes on a small screen is fine if we scale them down.
        // For larger screens (like S25 Ultra or tablets), we can show more or scale them up.
        val columns = maxOf(4, (screenWidth / 75).toInt()).coerceAtMost(7)
        val chunks = tubes.chunked(columns)
        
        // Base screen width for scaling is ~360dp
        val scaleFactor = (screenWidth / 360f).coerceIn(0.85f, 1.4f)"""

tube_grid_new = """        // Dynamically compute columns based on screen width. 
        val columns = maxOf(4, (screenWidth / 75).toInt()).coerceAtMost(8)
        val chunks = tubes.chunked(columns)
        
        // Calculate required rows
        val rows = chunks.size
        
        // Base dimensions for a tube + vertical spacing
        val baseTubeHeight = 176f + 48f // Tube height + spacing
        
        // We calculate a width-based scale and a height-based scale, and pick the smaller one to fit!
        val widthScale = (screenWidth / 360f)
        val heightScale = if (rows > 0) (screenHeight / (baseTubeHeight * rows)) * 0.9f else 1f
        
        // Final scale factor ensures it fits vertically and horizontally
        val scaleFactor = minOf(widthScale, heightScale).coerceIn(0.6f, 1.5f)"""

content = content.replace(tube_grid_old, tube_grid_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

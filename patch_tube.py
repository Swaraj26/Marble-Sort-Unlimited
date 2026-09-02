import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

tube_old = """        // Tube Container (Glass effect)
        Box(
            modifier = Modifier
                .width(tubeWidth)
                .height(tubeHeight)
                .align(Alignment.BottomCenter)
                .background(
                    brush = Brush.horizontalGradient(
                        colors = listOf(
                            Color.White.copy(alpha = 0.1f),
                            Color.White.copy(alpha = 0.3f),
                            Color.White.copy(alpha = 0.1f)
                        )
                    ),
                    shape = RoundedCornerShape(bottomStart = tubeWidth / 2, bottomEnd = tubeWidth / 2)
                )"""

tube_new = """        // Tube Container (Glass effect)
        Box(
            modifier = Modifier
                .width(tubeWidth)
                .height(tubeHeight)
                .align(Alignment.BottomCenter)
                .shadow(
                    elevation = 12.dp,
                    shape = RoundedCornerShape(bottomStart = tubeWidth / 2, bottomEnd = tubeWidth / 2),
                    spotColor = Color.Black.copy(alpha = 0.3f),
                    ambientColor = Color.Black.copy(alpha = 0.3f)
                )
                .background(
                    brush = Brush.horizontalGradient(
                        colors = listOf(
                            Color.White.copy(alpha = 0.1f),
                            Color.White.copy(alpha = 0.3f),
                            Color.White.copy(alpha = 0.1f)
                        )
                    ),
                    shape = RoundedCornerShape(bottomStart = tubeWidth / 2, bottomEnd = tubeWidth / 2)
                )"""

if tube_old in content:
    content = content.replace(tube_old, tube_new)
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(content)
    print("Patched TubeView")
else:
    print("TubeView not found!")

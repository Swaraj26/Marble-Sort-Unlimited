import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

tube_view_old = """        // Tube Container
        Box(
            modifier = Modifier
                .width(tubeWidth)
                .height(tubeHeight)
                .align(Alignment.BottomCenter)
                .background(
                    color = Color.White.copy(alpha = 0.05f),
                    shape = RoundedCornerShape(bottomStart = tubeWidth / 2, bottomEnd = tubeWidth / 2)
                )
                .border(
                    width = if (isSelected) (4 * (tubeWidth.value / 48f)).dp else 0.dp,
                    color = ringColor,
                    shape = RoundedCornerShape(bottomStart = tubeWidth / 2, bottomEnd = tubeWidth / 2)
                )
                .border(
                    width = (2 * (tubeWidth.value / 48f)).dp,
                    color = borderColor,
                    shape = RoundedCornerShape(bottomStart = tubeWidth / 2, bottomEnd = tubeWidth / 2)
                )
        )"""

tube_view_new = """        // Tube Container (Glass effect)
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
                )
                .border(
                    width = (3 * (tubeWidth.value / 48f)).dp,
                    color = Color.White.copy(alpha = 0.5f),
                    shape = RoundedCornerShape(bottomStart = tubeWidth / 2, bottomEnd = tubeWidth / 2)
                )
                .border(
                    width = if (isSelected) (4 * (tubeWidth.value / 48f)).dp else 0.dp,
                    color = ringColor,
                    shape = RoundedCornerShape(bottomStart = tubeWidth / 2, bottomEnd = tubeWidth / 2)
                )
        ) {
            // Inner shadow / rim highlight
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .border(
                        width = (1 * (tubeWidth.value / 48f)).dp,
                        color = Color.Black.copy(alpha = 0.05f),
                        shape = RoundedCornerShape(bottomStart = tubeWidth / 2, bottomEnd = tubeWidth / 2)
                    )
            )
        }"""

content = content.replace(tube_view_old, tube_view_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

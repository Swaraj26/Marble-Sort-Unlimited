import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

if "import androidx.compose.foundation.layout.BoxWithConstraints" not in content:
    content = content.replace("import androidx.compose.foundation.layout.*", "import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.layout.BoxWithConstraints")

tube_grid_old = """@Composable
fun TubeGrid(
    tubes: List<Tube>,
    selectedTubeIndex: Int?,
    activeTheme: String,
    onTubeSelect: (Int) -> Unit
) {
    val chunks = tubes.chunked(4)
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(48.dp)
    ) {
        for (chunk in chunks) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                for (tube in chunk) {
                    val index = tubes.indexOf(tube)
                    TubeView(
                        tube = tube,
                        isSelected = selectedTubeIndex == index,
                        activeTheme = activeTheme,
                        onTubeClick = { onTubeSelect(index) }
                    )
                }
            }
        }
    }
}"""

tube_grid_new = """@Composable
fun TubeGrid(
    tubes: List<Tube>,
    selectedTubeIndex: Int?,
    activeTheme: String,
    onTubeSelect: (Int) -> Unit
) {
    BoxWithConstraints(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp),
        contentAlignment = Alignment.Center
    ) {
        val screenWidth = maxWidth.value
        val screenHeight = maxHeight.value
        
        // Dynamically compute columns based on screen width. 
        // 4 tubes on a small screen is fine if we scale them down.
        // For larger screens (like S25 Ultra or tablets), we can show more or scale them up.
        val columns = maxOf(4, (screenWidth / 75).toInt()).coerceAtMost(7)
        val chunks = tubes.chunked(columns)
        
        // Base screen width for scaling is ~360dp
        val scaleFactor = (screenWidth / 360f).coerceIn(0.85f, 1.4f)
        
        val tubeWidth = (48 * scaleFactor).dp
        val tubeHeight = (176 * scaleFactor).dp
        val ballSize = (36 * scaleFactor).dp
        val ballSpacing = (38 * scaleFactor).dp
        val liftOffset = (48 * scaleFactor).dp
        val bottomPadding = (6 * scaleFactor).dp
        
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy((48 * scaleFactor).dp)
        ) {
            for (chunk in chunks) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceEvenly
                ) {
                    for (tube in chunk) {
                        val index = tubes.indexOf(tube)
                        TubeView(
                            tube = tube,
                            isSelected = selectedTubeIndex == index,
                            activeTheme = activeTheme,
                            tubeWidth = tubeWidth,
                            tubeHeight = tubeHeight,
                            ballSize = ballSize,
                            ballSpacing = ballSpacing,
                            liftOffset = liftOffset,
                            bottomPadding = bottomPadding,
                            onTubeClick = { onTubeSelect(index) }
                        )
                    }
                }
            }
        }
    }
}"""

content = content.replace(tube_grid_old, tube_grid_new)

tube_view_old = """@Composable
fun TubeView(
    tube: Tube,
    isSelected: Boolean,
    activeTheme: String,
    onTubeClick: () -> Unit
) {
    val borderColor = if (isSelected) Color.White.copy(alpha = 0.4f) else Color.White.copy(alpha = 0.2f)
    val ringColor = if (isSelected) Color(0xFF6366F1).copy(alpha = 0.3f) else Color.Transparent

    Box(
        contentAlignment = Alignment.BottomCenter,
        modifier = Modifier
            .width(48.dp)
            .height(190.dp)
            .clickable(
                interactionSource = remember { MutableInteractionSource() },
                indication = null,
                onClick = onTubeClick
            )
    ) {
        // Tube Container
        Box(
            modifier = Modifier
                .width(48.dp)
                .height(176.dp)
                .align(Alignment.BottomCenter)
                .background(
                    color = Color.White.copy(alpha = 0.05f),
                    shape = RoundedCornerShape(bottomStart = 24.dp, bottomEnd = 24.dp)
                )
                .border(
                    width = if (isSelected) 4.dp else 0.dp,
                    color = ringColor,
                    shape = RoundedCornerShape(bottomStart = 24.dp, bottomEnd = 24.dp)
                )
                .border(
                    width = 2.dp,
                    color = borderColor,
                    shape = RoundedCornerShape(bottomStart = 24.dp, bottomEnd = 24.dp)
                )
        )

        // Balls
        tube.balls.forEachIndexed { index, ball ->
            val isTop = index == tube.balls.size - 1
            val isLifting = isSelected && isTop
            val targetY = -(index * 38 + 6).dp - if (isLifting) 48.dp else 0.dp
            val yOffset by animateDpAsState(
                targetValue = targetY,
                animationSpec = tween(durationMillis = 300),
                label = "ball_lift"
            )

            BallView(
                ball = ball,
                isSelectedLifting = isLifting,
                activeTheme = activeTheme,
                modifier = Modifier
                    .offset(y = yOffset)
                    .size(36.dp)
            )
        }
    }
}"""

tube_view_new = """@Composable
fun TubeView(
    tube: Tube,
    isSelected: Boolean,
    activeTheme: String,
    tubeWidth: androidx.compose.ui.unit.Dp = 48.dp,
    tubeHeight: androidx.compose.ui.unit.Dp = 176.dp,
    ballSize: androidx.compose.ui.unit.Dp = 36.dp,
    ballSpacing: androidx.compose.ui.unit.Dp = 38.dp,
    liftOffset: androidx.compose.ui.unit.Dp = 48.dp,
    bottomPadding: androidx.compose.ui.unit.Dp = 6.dp,
    onTubeClick: () -> Unit
) {
    val borderColor = if (isSelected) Color.White.copy(alpha = 0.4f) else Color.White.copy(alpha = 0.2f)
    val ringColor = if (isSelected) Color(0xFF6366F1).copy(alpha = 0.3f) else Color.Transparent
    
    val totalHeight = tubeHeight + liftOffset

    Box(
        contentAlignment = Alignment.BottomCenter,
        modifier = Modifier
            .width(tubeWidth)
            .height(totalHeight)
            .clickable(
                interactionSource = remember { MutableInteractionSource() },
                indication = null,
                onClick = onTubeClick
            )
    ) {
        // Tube Container
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
        )

        // Balls
        tube.balls.forEachIndexed { index, ball ->
            val isTop = index == tube.balls.size - 1
            val isLifting = isSelected && isTop
            val targetY = -(index * ballSpacing.value + bottomPadding.value).dp - if (isLifting) liftOffset else 0.dp
            val yOffset by animateDpAsState(
                targetValue = targetY,
                animationSpec = tween(durationMillis = 300),
                label = "ball_lift"
            )

            BallView(
                ball = ball,
                isSelectedLifting = isLifting,
                activeTheme = activeTheme,
                modifier = Modifier
                    .offset(y = yOffset)
                    .size(ballSize)
            )
        }
    }
}"""

content = content.replace(tube_view_old, tube_view_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

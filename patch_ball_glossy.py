import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

ball_view_old = """@Composable
fun BallView(ball: Ball, isSelectedLifting: Boolean, activeTheme: String, modifier: Modifier = Modifier) {
    val isLiftingBorder = if (isSelectedLifting) Color.White.copy(alpha = 0.5f) else Color.Transparent
    Canvas(modifier = modifier) {
        val lightColor = ball.color.copy(alpha = 0.6f)
        val linear = Brush.linearGradient(
            colors = listOf(lightColor, ball.color),
            start = Offset(size.width, 0f),
            end = Offset(0f, size.height)
        )
        drawCircle(brush = linear)
        
        if (isSelectedLifting) {
            drawCircle(
                color = isLiftingBorder,
                style = Stroke(width = 2.dp.toPx())
            )
        }
        // highlight
        drawCircle(
            color = Color.White.copy(alpha = 0.3f),
            radius = size.width * 0.15f,
            center = Offset(size.width * 0.25f, size.height * 0.25f)
        )
    }
}"""

ball_view_new = """@Composable
fun BallView(ball: Ball, isSelectedLifting: Boolean, activeTheme: String, modifier: Modifier = Modifier) {
    val isLiftingBorder = if (isSelectedLifting) Color.White.copy(alpha = 0.5f) else Color.Transparent
    Canvas(modifier = modifier) {
        val radius = size.width / 2f
        
        if (activeTheme == "NEON") {
            // Neon Theme
            drawCircle(color = Color.Black)
            drawCircle(
                color = ball.color,
                style = Stroke(width = 4.dp.toPx())
            )
            drawCircle(
                color = ball.color.copy(alpha = 0.5f),
                style = Stroke(width = 8.dp.toPx())
            )
        } else if (activeTheme == "PASTEL") {
            // Pastel Theme
            val pastelColor = ball.color.copy(alpha = 0.4f)
            drawCircle(color = pastelColor)
            drawCircle(
                color = Color.White.copy(alpha = 0.5f),
                radius = size.width * 0.2f,
                center = Offset(size.width * 0.3f, size.height * 0.3f)
            )
        } else {
            // CLASSIC / GLOSSY Theme
            
            // Base shadow
            drawCircle(
                color = Color.Black.copy(alpha = 0.15f),
                radius = radius,
                center = Offset(radius, radius + 2.dp.toPx())
            )

            // Base color with radial gradient
            val radial = Brush.radialGradient(
                colors = listOf(ball.color.copy(alpha = 0.5f), ball.color.copy(alpha = 0.95f), ball.color.copy(alpha = 0.7f)),
                center = Offset(radius, radius),
                radius = radius
            )
            drawCircle(brush = radial)
            
            // Rim light bottom
            val bottomRim = Brush.verticalGradient(
                colors = listOf(Color.Transparent, Color.White.copy(alpha = 0.6f)),
                startY = radius,
                endY = size.height
            )
            drawCircle(brush = bottomRim, style = Stroke(width = 1.dp.toPx()))

            // Specular highlight top
            drawCircle(
                color = Color.White.copy(alpha = 0.5f),
                radius = radius * 0.4f,
                center = Offset(radius * 0.6f, radius * 0.4f)
            )
            drawCircle(
                color = Color.White.copy(alpha = 0.8f),
                radius = radius * 0.1f,
                center = Offset(radius * 0.7f, radius * 0.3f)
            )
        }

        if (isSelectedLifting) {
            drawCircle(
                color = isLiftingBorder,
                style = Stroke(width = 2.dp.toPx())
            )
        }
    }
}"""

content = content.replace(ball_view_old, ball_view_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

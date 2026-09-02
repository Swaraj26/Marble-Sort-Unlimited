import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

stat_box_old = """@Composable
fun RowScope.StatBox(label: String, value: String, valueColor: Color = Color(0xFF1E293B)) {
    Box(
        modifier = Modifier
            .weight(1f)
            .background(Color.White.copy(alpha = 0.35f), RoundedCornerShape(16.dp))
            .border(1.dp, Color.White.copy(alpha = 0.6f), RoundedCornerShape(16.dp))
            .padding(16.dp)
    )"""

stat_box_new = """@Composable
fun RowScope.StatBox(label: String, value: String, valueColor: Color = Color(0xFF1E293B)) {
    Box(
        modifier = Modifier
            .weight(1f)
            .shadow(4.dp, RoundedCornerShape(16.dp), spotColor = Color.Black.copy(alpha = 0.05f))
            .background(Color.White.copy(alpha = 0.35f), RoundedCornerShape(16.dp))
            .border(1.dp, Color.White.copy(alpha = 0.6f), RoundedCornerShape(16.dp))
            .padding(16.dp)
    )"""
content = content.replace(stat_box_old, stat_box_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

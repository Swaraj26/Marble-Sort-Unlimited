import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

statbox_old = """@Composable
fun RowScope.StatBox(label: String, value: String, valueColor: Color = Color(0xFF1E293B)) {
    Box(
        modifier = Modifier
            .weight(1f)
            .shadow(4.dp, RoundedCornerShape(16.dp), spotColor = Color.Black.copy(alpha = 0.05f))
            .background(Color.White.copy(alpha = 0.5f), RoundedCornerShape(16.dp))
            .border(1.dp, Color.White.copy(alpha = 0.8f), RoundedCornerShape(16.dp))
            .padding(16.dp)
    ) {
        Column {
            Text(label, fontSize = 10.sp, color = Color(0xFF1E293B).copy(alpha = 0.8f), fontWeight = FontWeight.ExtraBold, letterSpacing = 1.sp)
            Text(value, fontSize = 20.sp, color = valueColor, fontWeight = FontWeight.ExtraBold)
        }
    }
}"""

statbox_new = """@Composable
fun RowScope.StatBox(label: String, value: String, valueColor: Color = Color(0xFF1E293B)) {
    Box(
        modifier = Modifier
            .weight(1f)
            .shadow(2.dp, RoundedCornerShape(12.dp), spotColor = Color.Black.copy(alpha = 0.05f))
            .background(Color.White.copy(alpha = 0.5f), RoundedCornerShape(12.dp))
            .border(1.dp, Color.White.copy(alpha = 0.8f), RoundedCornerShape(12.dp))
            .padding(8.dp)
    ) {
        Column {
            Text(label, fontSize = 8.sp, color = Color(0xFF1E293B).copy(alpha = 0.8f), fontWeight = FontWeight.ExtraBold, letterSpacing = 1.sp)
            Text(value, fontSize = 16.sp, color = valueColor, fontWeight = FontWeight.ExtraBold)
        }
    }
}"""

if statbox_old in content:
    content = content.replace(statbox_old, statbox_new)
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(content)
    print("Patched StatBox")
else:
    print("StatBox not found!")

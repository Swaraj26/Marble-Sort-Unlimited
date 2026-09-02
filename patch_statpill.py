import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

statpill_old = """@Composable
fun StatPill(icon: androidx.compose.ui.graphics.vector.ImageVector, tint: Color, text: String, label: String) {
    Row(
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier
            .shadow(4.dp, CircleShape, spotColor = Color.Black.copy(alpha = 0.05f))
            .background(Color.White.copy(alpha = 0.35f), CircleShape)
            .border(1.dp, Color.White.copy(alpha = 0.6f), CircleShape)
            .padding(horizontal = 16.dp, vertical = 8.dp)
    ) {
        Icon(icon, contentDescription = null, tint = tint, modifier = Modifier.size(24.dp))
        Spacer(Modifier.width(8.dp))
        Text(text, color = Color(0xFF1E293B), fontWeight = FontWeight.ExtraBold, fontSize = 18.sp)
        if (label.isNotEmpty()) {
            Spacer(Modifier.width(4.dp))
            Text(label, color = Color(0xFF64748B), fontSize = 12.sp, fontWeight = FontWeight.Bold)
        }
    }
}"""

statpill_new = """@Composable
fun StatPill(icon: androidx.compose.ui.graphics.vector.ImageVector, tint: Color, text: String, label: String) {
    Row(
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier
            .shadow(2.dp, CircleShape, spotColor = Color.Black.copy(alpha = 0.05f))
            .background(Color.White.copy(alpha = 0.35f), CircleShape)
            .border(1.dp, Color.White.copy(alpha = 0.6f), CircleShape)
            .padding(horizontal = 8.dp, vertical = 4.dp)
    ) {
        Icon(icon, contentDescription = null, tint = tint, modifier = Modifier.size(16.dp))
        Spacer(Modifier.width(6.dp))
        Text(text, color = Color(0xFF1E293B), fontWeight = FontWeight.ExtraBold, fontSize = 14.sp)
        if (label.isNotEmpty()) {
            Spacer(Modifier.width(4.dp))
            Text(label, color = Color(0xFF64748B), fontSize = 10.sp, fontWeight = FontWeight.Bold)
        }
    }
}"""

if statpill_old in content:
    content = content.replace(statpill_old, statpill_new)
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(content)
    print("Patched StatPill")
else:
    print("StatPill not found!")

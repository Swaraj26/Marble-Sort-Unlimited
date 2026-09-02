import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

tab_old = """@Composable
fun TabItem(icon: androidx.compose.ui.graphics.vector.ImageVector, label: String, isSelected: Boolean, onClick: () -> Unit) {
    val color = if (isSelected) Color(0xFF1E293B) else Color(0xFF94A3B8)
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier.clickable(onClick = onClick).padding(8.dp)
    ) {
        Icon(icon, contentDescription = label, tint = color, modifier = Modifier.size(28.dp))
        Spacer(Modifier.height(4.dp))
        Text(label, color = color, fontSize = 12.sp, fontWeight = FontWeight.Bold)
    }
}"""
tab_new = """@Composable
fun TabItem(icon: androidx.compose.ui.graphics.vector.ImageVector, label: String, isSelected: Boolean, onClick: () -> Unit) {
    val color = if (isSelected) Color(0xFF1E293B) else Color(0xFF475569)
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier.clickable(onClick = onClick).padding(8.dp)
    ) {
        Icon(icon, contentDescription = label, tint = color, modifier = Modifier.size(28.dp))
        Spacer(Modifier.height(4.dp))
        Text(label, color = color, fontSize = 12.sp, fontWeight = FontWeight.ExtraBold)
    }
}"""
content = content.replace(tab_old, tab_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

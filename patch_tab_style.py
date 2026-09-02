import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# 1. Update StatPill
stat_pill_old = """@Composable
fun StatPill(icon: androidx.compose.ui.graphics.vector.ImageVector, tint: Color, text: String, label: String) {
    Row(
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier
            .background(Color.White.copy(alpha = 0.1f), CircleShape)
            .border(1.dp, Color.White.copy(alpha = 0.2f), CircleShape)
            .padding(horizontal = 12.dp, vertical = 6.dp)
    ) {
        Icon(icon, contentDescription = null, tint = tint, modifier = Modifier.size(24.dp))
        Spacer(Modifier.width(8.dp))
        Text(text, color = Color.White, fontWeight = FontWeight.Bold, fontSize = 18.sp)
        if (label.isNotEmpty()) {
            Spacer(Modifier.width(4.dp))
            Text(label, color = Color.White.copy(alpha = 0.7f), fontSize = 12.sp, fontWeight = FontWeight.Bold)
        }
    }
}"""
stat_pill_new = """@Composable
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
content = content.replace(stat_pill_old, stat_pill_new)

# 2. Update LevelNode
level_node_old = """@Composable
fun LevelNode(level: Int, isCompleted: Boolean, isCurrent: Boolean, isLocked: Boolean, isHardLevel: Boolean = false) {
    val size = if (isCurrent) 90.dp else 70.dp
    val color = if (isCompleted) {
        Color(0xFF10B981)
    } else if (isCurrent) {
        if (isHardLevel) Color(0xFFEF4444) else Color(0xFFF59E0B)
    } else {
        if (isHardLevel) Color(0xFF7F1D1D) else Color(0xFF374151)
    }
    val contentColor = if (isLocked) Color.LightGray else Color.White

    Box(
        modifier = Modifier.height(140.dp).width(120.dp),
        contentAlignment = Alignment.Center
    ) {
        Box(modifier = Modifier.width(8.dp).fillMaxHeight().background(Color.White.copy(alpha = 0.2f)))

        Box(
            modifier = Modifier
                .size(size)
                .background(color, CircleShape)
                .border(4.dp, Color.White.copy(alpha = if (isCurrent) 1f else 0.5f), CircleShape),
            contentAlignment = Alignment.Center
        ) {
            Text("$level", color = contentColor, fontSize = 28.sp, fontWeight = FontWeight.ExtraBold)
        }
    }
}"""
level_node_new = """@Composable
fun LevelNode(level: Int, isCompleted: Boolean, isCurrent: Boolean, isLocked: Boolean, isHardLevel: Boolean = false) {
    val size = if (isCurrent) 90.dp else 70.dp
    val color = if (isCompleted) {
        Color(0xFF82A6F1) // completed - blue
    } else if (isCurrent) {
        Color(0xFF90E4AD) // current - green
    } else {
        Color.White.copy(alpha = 0.35f) // locked - glass
    }
    val contentColor = if (isLocked) Color(0xFF94A3B8) else Color.White

    Box(
        modifier = Modifier.height(140.dp).width(120.dp),
        contentAlignment = Alignment.Center
    ) {
        Box(modifier = Modifier.width(8.dp).fillMaxHeight().background(Color.White.copy(alpha = 0.4f)))

        Box(
            modifier = Modifier
                .size(size)
                .shadow(if (isCurrent) 8.dp else 4.dp, CircleShape, spotColor = if (isCurrent) Color(0xFF76DB9E) else Color.Black.copy(alpha = 0.05f))
                .background(color, CircleShape)
                .border(2.dp, Color.White.copy(alpha = 0.8f), CircleShape),
            contentAlignment = Alignment.Center
        ) {
            Text("$level", color = contentColor, fontSize = 28.sp, fontWeight = FontWeight.ExtraBold)
        }
    }
}"""
content = content.replace(level_node_old, level_node_new)

# 3. Update TabItem
tab_item_old = """@Composable
fun TabItem(icon: androidx.compose.ui.graphics.vector.ImageVector, label: String, isSelected: Boolean, onClick: () -> Unit) {
    val color = if (isSelected) Color(0xFF4F46E5) else Color.White.copy(alpha = 0.5f)
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier.clickable(onClick = onClick).padding(8.dp)
    ) {
        Icon(icon, contentDescription = label, tint = color, modifier = Modifier.size(28.dp))
        Spacer(Modifier.height(4.dp))
        Text(label, color = color, fontSize = 12.sp, fontWeight = FontWeight.Bold)
    }
}"""
tab_item_new = """@Composable
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
content = content.replace(tab_item_old, tab_item_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

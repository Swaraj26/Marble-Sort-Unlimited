import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

statpill_old = """@Composable
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

statpill_new = """@Composable
fun StatPill(icon: androidx.compose.ui.graphics.vector.ImageVector, tint: Color, text: String, label: String, isLarge: Boolean = false) {
    Row(
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier
            .shadow(if (isLarge) 4.dp else 2.dp, CircleShape, spotColor = Color.Black.copy(alpha = 0.05f))
            .background(Color.White.copy(alpha = 0.35f), CircleShape)
            .border(1.dp, Color.White.copy(alpha = 0.6f), CircleShape)
            .padding(horizontal = if (isLarge) 16.dp else 8.dp, vertical = if (isLarge) 8.dp else 4.dp)
    ) {
        Icon(icon, contentDescription = null, tint = tint, modifier = Modifier.size(if (isLarge) 24.dp else 16.dp))
        Spacer(Modifier.width(if (isLarge) 8.dp else 6.dp))
        Text(text, color = Color(0xFF1E293B), fontWeight = FontWeight.ExtraBold, fontSize = if (isLarge) 18.sp else 14.sp)
        if (label.isNotEmpty()) {
            Spacer(Modifier.width(4.dp))
            Text(label, color = Color(0xFF64748B), fontSize = if (isLarge) 12.sp else 10.sp, fontWeight = FontWeight.Bold)
        }
    }
}"""

main_menu_old = """                            } else {
                                timerText = "00:00"
                            }
                            kotlinx.coroutines.delay(1000)
                        }
                    }
                }
                
                StatPill(icon = Icons.Default.Favorite, tint = Color(0xFFEF4444), text = "${appState.lives}", label = timerText)
                StatPill(icon = Icons.Default.Star, tint = Color(0xFFFBBF24), text = "${appState.coins}", label = "")
            }

            Box(modifier = Modifier.weight(1f).fillMaxWidth()) {
                when (screen) {"""

main_menu_new = """                            } else {
                                timerText = "00:00"
                            }
                            kotlinx.coroutines.delay(1000)
                        }
                    }
                }
                
                StatPill(icon = Icons.Default.Favorite, tint = Color(0xFFEF4444), text = "${appState.lives}", label = timerText, isLarge = true)
                StatPill(icon = Icons.Default.Star, tint = Color(0xFFFBBF24), text = "${appState.coins}", label = "", isLarge = true)
            }

            Box(modifier = Modifier.weight(1f).fillMaxWidth()) {
                when (screen) {"""

if statpill_old in content:
    content = content.replace(statpill_old, statpill_new)
    if main_menu_old in content:
        content = content.replace(main_menu_old, main_menu_new)
        with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
            f.write(content)
        print("Patched Both Successfully")
    else:
        print("Menu old not found")
else:
    print("StatPill not found")

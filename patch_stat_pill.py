import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

home_old = """        Column(modifier = Modifier.fillMaxSize()) {
            Row(modifier = Modifier.fillMaxWidth().padding(24.dp).zIndex(1f), horizontalArrangement = Arrangement.SpaceBetween) {
                StatPill(icon = Icons.Default.Favorite, tint = Color(0xFFEF4444), text = "${appState.lives}", label = "MAX")
                StatPill(icon = Icons.Default.Star, tint = Color(0xFFFBBF24), text = "${appState.coins}", label = "")
            }"""

home_new = """        Column(modifier = Modifier.fillMaxSize()) {
            Row(modifier = Modifier.fillMaxWidth().padding(24.dp).zIndex(1f), horizontalArrangement = Arrangement.SpaceBetween) {
                var timerText by remember { mutableStateOf(if (appState.lives >= 5) "MAX" else "") }
                
                LaunchedEffect(appState.lives, appState.nextLifeTime) {
                    if (appState.lives >= 5) {
                        timerText = "MAX"
                    } else {
                        while (true) {
                            val remaining = appState.nextLifeTime - System.currentTimeMillis()
                            if (remaining > 0) {
                                val mins = (remaining / 60000).toInt()
                                val secs = ((remaining % 60000) / 1000).toInt()
                                timerText = String.format("%02d:%02d", mins, secs)
                            } else {
                                timerText = "00:00"
                            }
                            kotlinx.coroutines.delay(1000)
                        }
                    }
                }
            
                StatPill(icon = Icons.Default.Favorite, tint = Color(0xFFEF4444), text = "${appState.lives}", label = timerText)
                StatPill(icon = Icons.Default.Star, tint = Color(0xFFFBBF24), text = "${appState.coins}", label = "")
            }"""
content = content.replace(home_old, home_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

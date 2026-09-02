import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

header_old = """            // Header
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 16.dp, start = 16.dp, end = 16.dp, bottom = 12.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    IconButton(
                        onClick = { viewModel.goHome() },
                        modifier = Modifier
                            .size(40.dp)
                            .shadow(4.dp, RoundedCornerShape(10.dp), spotColor = Color(0xFF6B8CE0))
                            .background(Color(0xFF82A6F1), RoundedCornerShape(10.dp))
                    ) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Home", tint = Color(0xFF1E293B), modifier = Modifier.size(20.dp))
                    }
                    Column {
                        Text(
                            text = "PUZZLE SOLVER",
                            color = Color(0xFF1E293B),
                            fontSize = 10.sp,
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 1.sp
                        )
                        Text(
                            text = "Level ${state.level}",
                            color = Color(0xFF172554),
                            style = MaterialTheme.typography.titleLarge,
                            fontWeight = FontWeight.ExtraBold
                        )
                    }
                }
                Column(horizontalAlignment = Alignment.End, verticalArrangement = Arrangement.spacedBy(8.dp)) {
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
                }
            }"""

header_new = """            // Header
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 16.dp, start = 16.dp, end = 16.dp, bottom = 8.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    IconButton(
                        onClick = { viewModel.goHome() },
                        modifier = Modifier
                            .size(40.dp)
                            .shadow(4.dp, RoundedCornerShape(10.dp), spotColor = Color(0xFF6B8CE0))
                            .background(Color(0xFF82A6F1), RoundedCornerShape(10.dp))
                    ) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Home", tint = Color(0xFF1E293B), modifier = Modifier.size(20.dp))
                    }
                    Text(
                        text = "Level ${state.level}",
                        color = Color(0xFF172554),
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.ExtraBold
                    )
                }
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
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
                }
            }"""

if header_old in content:
    content = content.replace(header_old, header_new)
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(content)
    print("Patched Header2")
else:
    print("Header2 not found!")

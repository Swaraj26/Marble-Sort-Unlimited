import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

game_old = """                    Column {
                        Text(
                            text = "PUZZLE SOLVER",
                            color = Color(0xFF1E293B),
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 1.sp
                        )
                        Text(
                            text = "Level ${state.level}",
                            color = Color(0xFF172554),
                            style = MaterialTheme.typography.headlineMedium,
                            fontWeight = FontWeight.ExtraBold
                        )
                    }
                }
                StatPill(icon = Icons.Default.Star, tint = Color(0xFFFBBF24), text = "${appState.coins}", label = "")
            }"""

game_new = """                    Column {
                        Text(
                            text = "PUZZLE SOLVER",
                            color = Color(0xFF1E293B),
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 1.sp
                        )
                        Text(
                            text = "Level ${state.level}",
                            color = Color(0xFF172554),
                            style = MaterialTheme.typography.headlineMedium,
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
content = content.replace(game_old, game_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

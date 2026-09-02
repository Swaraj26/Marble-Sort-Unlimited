import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

win_dialog = """        // Win Overlay
        if (state.isWon) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(Color.Black.copy(alpha = 0.7f)),
                contentAlignment = Alignment.Center
            ) {
                Card(
                    shape = RoundedCornerShape(24.dp),
                    colors = CardDefaults.cardColors(containerColor = Color(0xFF1E1E1E))
                ) {
                    Column(
                        modifier = Modifier.padding(32.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Text(
                            text = "Level Complete!",
                            style = MaterialTheme.typography.headlineLarge,
                            color = Color(0xFFFFB300),
                            fontWeight = FontWeight.Bold
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        Text(
                            text = "Moves: ${state.moveCount}",
                            style = MaterialTheme.typography.bodyLarge,
                            color = Color.White
                        )
                        Spacer(modifier = Modifier.height(24.dp))
                        Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                            Button(
                                onClick = { viewModel.goHome() },
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF374151))
                            ) {
                                Text("Home", fontSize = 18.sp, modifier = Modifier.padding(8.dp))
                            }
                            val adManager = LocalAdManager.current
                            val activity = LocalContext.current as Activity
                            Button(
                                onClick = {
                                    val levelsCompleted = viewModel.appState.value.highestUnlockedLevel - 1
                                    if (levelsCompleted % 2 == 0) {
                                        adManager.showInterstitialAd(activity) {
                                            viewModel.nextLevel()
                                        }
                                    } else {
                                        viewModel.nextLevel()
                                    }
                                },
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF43A047))
                            ) {
                                Text("Next", fontSize = 18.sp, modifier = Modifier.padding(8.dp))
                            }
                        }
                    }
                }
            }
        }"""

lost_dialog = win_dialog + """
        if (state.isLost && !state.isWon) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(Color.Black.copy(alpha = 0.7f)),
                contentAlignment = Alignment.Center
            ) {
                Card(
                    shape = RoundedCornerShape(24.dp),
                    colors = CardDefaults.cardColors(containerColor = Color(0xFF1E1E1E))
                ) {
                    Column(
                        modifier = Modifier.padding(32.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Text(
                            text = "Out of Moves!",
                            style = MaterialTheme.typography.headlineLarge,
                            color = Color(0xFFEF4444),
                            fontWeight = FontWeight.Bold
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        Text(
                            text = "You lost a life.",
                            style = MaterialTheme.typography.bodyLarge,
                            color = Color.White
                        )
                        Spacer(modifier = Modifier.height(24.dp))
                        Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                            Button(
                                onClick = { viewModel.goHome() },
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF374151))
                            ) {
                                Text("Home", fontSize = 18.sp, modifier = Modifier.padding(8.dp))
                            }
                            val adManager = LocalAdManager.current
                            val activity = LocalContext.current as Activity
                            Button(
                                onClick = {
                                    adManager.showRewardedAd(activity, {
                                        viewModel.undo()
                                    }, {
                                        viewModel.undo() // Fallback if ad fails to load
                                    })
                                },
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF82A6F1))
                            ) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(Icons.AutoMirrored.Filled.Undo, contentDescription = null, tint = Color.White)
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Text("Undo (Ad)", fontSize = 16.sp, modifier = Modifier.padding(vertical = 8.dp))
                                }
                            }
                        }
                    }
                }
            }
        }"""

content = content.replace(win_dialog, lost_dialog)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

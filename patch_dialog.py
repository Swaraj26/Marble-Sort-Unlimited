import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

dialog_old = """    if (showGiveUpDialog) {
        AlertDialog(
            onDismissRequest = { showGiveUpDialog = false },
            containerColor = Color.White.copy(alpha = 0.95f),
            titleContentColor = Color(0xFFEF4444),
            textContentColor = Color(0xFF64748B),
            title = { Text("Are you stuck?", fontWeight = FontWeight.ExtraBold) },
            text = { Text("Give up and lose a life to restart, or watch an ad to reverse your last move for free!", fontWeight = FontWeight.Medium) },
            confirmButton = {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(
                        onClick = {
                            showGiveUpDialog = false
                            viewModel.restartLevel()
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFEF4444))
                    ) {
                        Text("Give Up", color = Color.White)
                    }
                    Button(
                        onClick = {
                            showGiveUpDialog = false
                            adManager.showRewardedAd(activity) {
                                viewModel.undo()
                            }
                        }
                    ) {
                        Text("Watch Ad (Undo)")
                    }
                }
            },
            dismissButton = {
                TextButton(onClick = { showGiveUpDialog = false }) { Text("Cancel") }
            }
        )
    }"""

dialog_new = """    if (showGiveUpDialog) {
        AlertDialog(
            onDismissRequest = { showGiveUpDialog = false },
            containerColor = Color.White,
            titleContentColor = Color(0xFFB91C1C), // Red 700
            textContentColor = Color(0xFF1E293B), // Slate 800
            title = { Text("Are you stuck?", fontWeight = FontWeight.ExtraBold) },
            text = { Text("Give up and lose a life to restart, or watch an ad to reverse your last move for free!", fontWeight = FontWeight.Medium) },
            confirmButton = {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(
                        onClick = {
                            showGiveUpDialog = false
                            viewModel.restartLevel()
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFDC2626)) // Red 600
                    ) {
                        Text("Give Up", color = Color.White, fontWeight = FontWeight.Bold)
                    }
                    Button(
                        onClick = {
                            showGiveUpDialog = false
                            adManager.showRewardedAd(activity) {
                                viewModel.undo()
                            }
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2563EB)) // Blue 600
                    ) {
                        Text("Watch Ad (Undo)", color = Color.White, fontWeight = FontWeight.Bold)
                    }
                }
            },
            dismissButton = {
                TextButton(onClick = { showGiveUpDialog = false }) { 
                    Text("Cancel", color = Color(0xFF475569), fontWeight = FontWeight.Bold) 
                }
            }
        )
    }"""

if dialog_old in content:
    content = content.replace(dialog_old, dialog_new)
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(content)
    print("Patched dialog successfully!")
else:
    print("Dialog not found!")

import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

powerup_old = """        AlertDialog(
            onDismissRequest = { showPowerUpDialog = PowerUpType.NONE },
            containerColor = Color.White.copy(alpha = 0.95f),
            titleContentColor = Color(0xFF1E293B),
            textContentColor = Color(0xFF64748B),
            title = { Text(title, fontWeight = FontWeight.ExtraBold) },
            text = { Text("$desc\n\nCost: 1000 Coins or Watch an Ad", fontWeight = FontWeight.Medium) },
            confirmButton = {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(
                        onClick = {
                            if (viewModel.spendCoins(1000)) {
                                showPowerUpDialog = PowerUpType.NONE
                                if (isUndo) viewModel.undo() else viewModel.addTube()
                            }
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFF59E0B)),
                        enabled = appState.coins >= 1000
                    ) {
                        Text("1000 Coins", color = Color.Black)
                    }
                    Button(
                        onClick = {
                            showPowerUpDialog = PowerUpType.NONE
                            adManager.showRewardedAd(activity) {
                                if (isUndo) viewModel.undo() else viewModel.addTube()
                            }
                        }
                    ) {
                        Text("Watch Ad")
                    }
                }
            },
            dismissButton = {
                TextButton(onClick = { showPowerUpDialog = PowerUpType.NONE }) { Text("Cancel") }
            }
        )"""

powerup_new = """        AlertDialog(
            onDismissRequest = { showPowerUpDialog = PowerUpType.NONE },
            containerColor = Color.White,
            titleContentColor = Color(0xFF1E293B),
            textContentColor = Color(0xFF1E293B),
            title = { Text(title, fontWeight = FontWeight.ExtraBold) },
            text = { Text("$desc\n\nCost: 1000 Coins or Watch an Ad", fontWeight = FontWeight.Medium) },
            confirmButton = {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(
                        onClick = {
                            if (viewModel.spendCoins(1000)) {
                                showPowerUpDialog = PowerUpType.NONE
                                if (isUndo) viewModel.undo() else viewModel.addTube()
                            }
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFF59E0B)),
                        enabled = appState.coins >= 1000
                    ) {
                        Text("1000 Coins", color = Color.Black, fontWeight = FontWeight.Bold)
                    }
                    Button(
                        onClick = {
                            showPowerUpDialog = PowerUpType.NONE
                            adManager.showRewardedAd(activity) {
                                if (isUndo) viewModel.undo() else viewModel.addTube()
                            }
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2563EB))
                    ) {
                        Text("Watch Ad", color = Color.White, fontWeight = FontWeight.Bold)
                    }
                }
            },
            dismissButton = {
                TextButton(onClick = { showPowerUpDialog = PowerUpType.NONE }) { 
                    Text("Cancel", color = Color(0xFF475569), fontWeight = FontWeight.Bold) 
                }
            }
        )"""

if powerup_old in content:
    content = content.replace(powerup_old, powerup_new)
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(content)
    print("Patched powerup dialog successfully!")
else:
    print("PowerUp dialog not found!")

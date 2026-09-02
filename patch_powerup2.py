import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Replace colors
content = content.replace(
    'containerColor = Color.White.copy(alpha = 0.95f),\n            titleContentColor = Color(0xFF1E293B),\n            textContentColor = Color(0xFF64748B),',
    'containerColor = Color.White,\n            titleContentColor = Color(0xFF1E293B),\n            textContentColor = Color(0xFF1E293B),'
)

# Replace 1000 Coins text
content = content.replace(
    'Text("1000 Coins", color = Color.Black)',
    'Text("1000 Coins", color = Color.Black, fontWeight = FontWeight.Bold)'
)

# Replace Watch Ad button in PowerUp Dialog
content = content.replace(
    '''Button(
                        onClick = {
                            showPowerUpDialog = PowerUpType.NONE
                            adManager.showRewardedAd(activity) {
                                if (isUndo) viewModel.undo() else viewModel.addTube()
                            }
                        }
                    ) {
                        Text("Watch Ad")
                    }''',
    '''Button(
                        onClick = {
                            showPowerUpDialog = PowerUpType.NONE
                            adManager.showRewardedAd(activity) {
                                if (isUndo) viewModel.undo() else viewModel.addTube()
                            }
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2563EB))
                    ) {
                        Text("Watch Ad", color = Color.White, fontWeight = FontWeight.Bold)
                    }'''
)

# Replace Cancel button in PowerUp Dialog
content = content.replace(
    'TextButton(onClick = { showPowerUpDialog = PowerUpType.NONE }) { Text("Cancel") }',
    'TextButton(onClick = { showPowerUpDialog = PowerUpType.NONE }) { Text("Cancel", color = Color(0xFF475569), fontWeight = FontWeight.Bold) }'
)


with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
print("Patched PowerUp")

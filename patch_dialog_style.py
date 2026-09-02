import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# 1. PowerUp Dialog
powerup_dialog_old = """    if (showPowerUpDialog != PowerUpType.NONE) {
        val isUndo = showPowerUpDialog == PowerUpType.UNDO
        val title = if (isUndo) "Undo Move" else "Add Extra Tube"
        val desc = if (isUndo) "Reverse your last move!" else "Add an empty tube to help you sort!"
        AlertDialog(
            onDismissRequest = { showPowerUpDialog = PowerUpType.NONE },
            title = { Text(title) },
            text = { Text("$desc\\n\\nCost: 1000 Coins or Watch an Ad") },"""
powerup_dialog_new = """    if (showPowerUpDialog != PowerUpType.NONE) {
        val isUndo = showPowerUpDialog == PowerUpType.UNDO
        val title = if (isUndo) "Undo Move" else "Add Extra Tube"
        val desc = if (isUndo) "Reverse your last move!" else "Add an empty tube to help you sort!"
        AlertDialog(
            onDismissRequest = { showPowerUpDialog = PowerUpType.NONE },
            containerColor = Color.White.copy(alpha = 0.95f),
            titleContentColor = Color(0xFF1E293B),
            textContentColor = Color(0xFF64748B),
            title = { Text(title, fontWeight = FontWeight.ExtraBold) },
            text = { Text("$desc\\n\\nCost: 1000 Coins or Watch an Ad", fontWeight = FontWeight.Medium) },"""
content = content.replace(powerup_dialog_old, powerup_dialog_new)

# 2. GiveUp Dialog
giveup_dialog_old = """    if (showGiveUpDialog) {
        AlertDialog(
            onDismissRequest = { showGiveUpDialog = false },
            title = { Text("Are you stuck?", color = Color(0xFFEF4444)) },
            text = { Text("Give up and lose a life to restart, or watch an ad to reverse your last move for free!") },"""
giveup_dialog_new = """    if (showGiveUpDialog) {
        AlertDialog(
            onDismissRequest = { showGiveUpDialog = false },
            containerColor = Color.White.copy(alpha = 0.95f),
            titleContentColor = Color(0xFFEF4444),
            textContentColor = Color(0xFF64748B),
            title = { Text("Are you stuck?", fontWeight = FontWeight.ExtraBold) },
            text = { Text("Give up and lose a life to restart, or watch an ad to reverse your last move for free!", fontWeight = FontWeight.Medium) },"""
content = content.replace(giveup_dialog_old, giveup_dialog_new)

# 3. Daily Bonus Dialog
daily_bonus_old = """    if (appState.showDailyBonusDialog) {
        AlertDialog(
            onDismissRequest = { viewModel.dismissDailyBonus() },
            title = { Text("Daily Bonus!") },
            text = { Text("Welcome back! Here are your 50 daily coins.") },"""
daily_bonus_new = """    if (appState.showDailyBonusDialog) {
        AlertDialog(
            onDismissRequest = { viewModel.dismissDailyBonus() },
            containerColor = Color.White.copy(alpha = 0.95f),
            titleContentColor = Color(0xFF1E293B),
            textContentColor = Color(0xFF64748B),
            title = { Text("Daily Bonus!", fontWeight = FontWeight.ExtraBold) },
            text = { Text("Welcome back! Here are your 50 daily coins.", fontWeight = FontWeight.Medium) },"""
content = content.replace(daily_bonus_old, daily_bonus_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

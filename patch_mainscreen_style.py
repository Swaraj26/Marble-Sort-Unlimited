import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# 1. Main background
bg_old = """    Box(modifier = Modifier.fillMaxSize().background(Color(0xFF0F1115))) {
        Canvas(modifier = Modifier.fillMaxSize()) {
            drawCircle(
                brush = Brush.radialGradient(
                    colors = listOf(Color(0x334F46E5), Color.Transparent),
                    center = Offset(0f, 0f),
                    radius = size.width * 0.8f
                )
            )
            drawCircle(
                brush = Brush.radialGradient(
                    colors = listOf(Color(0x33059669), Color.Transparent),
                    center = Offset(size.width, size.height),
                    radius = size.width * 0.8f
                )
            )
        }"""
bg_new = """    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(
                brush = Brush.linearGradient(
                    colors = listOf(
                        Color(0xFFFCD5CE), // Soft peach
                        Color(0xFFD8E2DC), // Light grey/green
                        Color(0xFFB5E4CB)  // Soft mint/cyan
                    ),
                    start = Offset(0f, 0f),
                    end = Offset.Infinite
                )
            )
    ) {"""
content = content.replace(bg_old, bg_new)

# 2. Play Button
play_btn_old = """                            // Play Button positioned inside the content area (above ads and tabs)
                            Box(modifier = Modifier.align(Alignment.BottomCenter).fillMaxWidth().padding(start = 32.dp, end = 32.dp, bottom = 24.dp)) {
                                Button(
                                    onClick = { if (appState.lives > 0) viewModel.startLevel(appState.highestUnlockedLevel) },
                                    colors = ButtonDefaults.buttonColors(
                                        containerColor = if (appState.lives > 0) Color(0xFF4F46E5) else Color.Gray
                                    ),
                                    shape = CircleShape,
                                    modifier = Modifier.fillMaxWidth().height(64.dp)
                                ) {
                                    Text(
                                        if (appState.lives > 0) "PLAY LEVEL ${appState.highestUnlockedLevel}" else "OUT OF LIVES",
                                        fontSize = 20.sp,
                                        fontWeight = FontWeight.Bold,
                                        letterSpacing = 1.sp
                                    )
                                }
                            }"""
play_btn_new = """                            // Play Button positioned inside the content area (above ads and tabs)
                            Box(modifier = Modifier.align(Alignment.BottomCenter).fillMaxWidth().padding(start = 32.dp, end = 32.dp, bottom = 24.dp)) {
                                Button(
                                    onClick = { if (appState.lives > 0) viewModel.startLevel(appState.highestUnlockedLevel) },
                                    colors = ButtonDefaults.buttonColors(
                                        containerColor = if (appState.lives > 0) Color(0xFF90E4AD) else Color.LightGray
                                    ),
                                    shape = CircleShape,
                                    elevation = ButtonDefaults.buttonElevation(defaultElevation = 6.dp),
                                    modifier = Modifier.fillMaxWidth().height(64.dp)
                                ) {
                                    Text(
                                        if (appState.lives > 0) "PLAY LEVEL ${appState.highestUnlockedLevel}" else "OUT OF LIVES",
                                        fontSize = 20.sp,
                                        color = Color.White,
                                        fontWeight = FontWeight.Bold,
                                        letterSpacing = 1.sp
                                    )
                                }
                            }"""
content = content.replace(play_btn_old, play_btn_new)

# 3. Bottom Tabs Bar background
tabs_bar_old = """            // Bottom Tabs Bar (pushed to bottom of column)
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color(0xFF1E1E2E).copy(alpha = 0.95f))
                    .border(1.dp, Color.White.copy(alpha = 0.1f))
                    .padding(vertical = 12.dp, horizontal = 24.dp),"""
tabs_bar_new = """            // Bottom Tabs Bar (pushed to bottom of column)
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .shadow(16.dp, RoundedCornerShape(topStart = 24.dp, topEnd = 24.dp), spotColor = Color.Black.copy(alpha = 0.1f))
                    .background(Color.White.copy(alpha = 0.7f), RoundedCornerShape(topStart = 24.dp, topEnd = 24.dp))
                    .border(1.dp, Color.White, RoundedCornerShape(topStart = 24.dp, topEnd = 24.dp))
                    .padding(vertical = 12.dp, horizontal = 24.dp),"""
content = content.replace(tabs_bar_old, tabs_bar_new)

# 4. Settings tab UI
settings_old = """                    Screen.SETTINGS -> {
                        Column(
                            modifier = Modifier.fillMaxSize().padding(32.dp),
                            verticalArrangement = Arrangement.spacedBy(24.dp)
                        ) {
                            Text("Settings", color = Color.White, fontSize = 32.sp, fontWeight = FontWeight.Bold)
                            
                            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                Text("Sound", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Medium)
                                Switch(
                                    checked = appState.soundEnabled,
                                    onCheckedChange = { viewModel.toggleSound() },
                                    colors = SwitchDefaults.colors(checkedThumbColor = Color(0xFF4F46E5), checkedTrackColor = Color(0xFF4F46E5).copy(alpha=0.5f))
                                )
                            }
                            
                            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                Text("Haptic Feedback", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Medium)
                                Switch(
                                    checked = appState.hapticEnabled,
                                    onCheckedChange = { viewModel.toggleHaptics() },
                                    colors = SwitchDefaults.colors(checkedThumbColor = Color(0xFF4F46E5), checkedTrackColor = Color(0xFF4F46E5).copy(alpha=0.5f))
                                )
                            }
                        }
                    }"""
settings_new = """                    Screen.SETTINGS -> {
                        Column(
                            modifier = Modifier.fillMaxSize().padding(32.dp),
                            verticalArrangement = Arrangement.spacedBy(24.dp)
                        ) {
                            Text("Settings", color = Color(0xFF1E293B), fontSize = 32.sp, fontWeight = FontWeight.ExtraBold)
                            
                            Row(modifier = Modifier.fillMaxWidth().shadow(4.dp, RoundedCornerShape(16.dp), spotColor = Color.Black.copy(alpha = 0.05f)).background(Color.White.copy(alpha = 0.35f), RoundedCornerShape(16.dp)).border(1.dp, Color.White.copy(alpha = 0.6f), RoundedCornerShape(16.dp)).padding(16.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                Text("Sound", color = Color(0xFF1E293B), fontSize = 20.sp, fontWeight = FontWeight.Bold)
                                Switch(
                                    checked = appState.soundEnabled,
                                    onCheckedChange = { viewModel.toggleSound() },
                                    colors = SwitchDefaults.colors(checkedThumbColor = Color(0xFF82A6F1), checkedTrackColor = Color(0xFF82A6F1).copy(alpha=0.5f))
                                )
                            }
                            
                            Row(modifier = Modifier.fillMaxWidth().shadow(4.dp, RoundedCornerShape(16.dp), spotColor = Color.Black.copy(alpha = 0.05f)).background(Color.White.copy(alpha = 0.35f), RoundedCornerShape(16.dp)).border(1.dp, Color.White.copy(alpha = 0.6f), RoundedCornerShape(16.dp)).padding(16.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                Text("Haptic Feedback", color = Color(0xFF1E293B), fontSize = 20.sp, fontWeight = FontWeight.Bold)
                                Switch(
                                    checked = appState.hapticEnabled,
                                    onCheckedChange = { viewModel.toggleHaptics() },
                                    colors = SwitchDefaults.colors(checkedThumbColor = Color(0xFF82A6F1), checkedTrackColor = Color(0xFF82A6F1).copy(alpha=0.5f))
                                )
                            }
                        }
                    }"""
content = content.replace(settings_old, settings_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

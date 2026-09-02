import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# 1. Update StatBox
stat_box_old = """@Composable
fun RowScope.StatBox(label: String, value: String, valueColor: Color = Color.White) {
    Box(
        modifier = Modifier
            .weight(1f)
            .background(Color.White.copy(alpha = 0.05f), RoundedCornerShape(16.dp))
            .border(1.dp, Color.White.copy(alpha = 0.05f), RoundedCornerShape(16.dp))
            .padding(12.dp)
    ) {
        Column {
            Text(label, fontSize = 10.sp, color = Color(0xFF94A3B8), fontWeight = FontWeight.Bold, letterSpacing = 1.sp)
            Text(value, fontSize = 20.sp, color = valueColor, fontWeight = FontWeight.Bold)
        }
    }
}"""
stat_box_new = """@Composable
fun RowScope.StatBox(label: String, value: String, valueColor: Color = Color(0xFF1E293B)) {
    Box(
        modifier = Modifier
            .weight(1f)
            .background(Color.White.copy(alpha = 0.35f), RoundedCornerShape(16.dp))
            .border(1.dp, Color.White.copy(alpha = 0.6f), RoundedCornerShape(16.dp))
            .padding(16.dp)
    ) {
        Column {
            Text(label, fontSize = 10.sp, color = Color(0xFF64748B), fontWeight = FontWeight.Bold, letterSpacing = 1.sp)
            Text(value, fontSize = 20.sp, color = valueColor, fontWeight = FontWeight.ExtraBold)
        }
    }
}"""
content = content.replace(stat_box_old, stat_box_new)

# 2. Update the background in MarbleSortScreen
bg_old = """    Box(
        modifier = modifier
            .fillMaxSize()
            .background(Color(0xFF0F1115))
    ) {
        // Background Glows
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
        modifier = modifier
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

# 3. Header colors and Back Button
header_old = """                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                    IconButton(
                        onClick = { viewModel.goHome() },
                        modifier = Modifier
                            .size(44.dp)
                            .background(Color.White.copy(alpha = 0.05f), androidx.compose.foundation.shape.RoundedCornerShape(12.dp))
                            .border(1.dp, Color.White.copy(alpha = 0.1f), androidx.compose.foundation.shape.RoundedCornerShape(12.dp))
                    ) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Home", tint = Color.White)
                    }
                    Column {
                        Text(
                            text = "PUZZLE SOLVER",
                            color = Color(0xFF818CF8),
                            fontSize = 10.sp,
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 2.sp
                        )
                        Text(
                            text = "Level ${state.level}",
                            color = Color.White,
                            style = MaterialTheme.typography.headlineMedium,
                            fontWeight = FontWeight.ExtraBold
                        )
                    }
                }"""
header_new = """                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                    IconButton(
                        onClick = { viewModel.goHome() },
                        modifier = Modifier
                            .size(52.dp)
                            .shadow(8.dp, RoundedCornerShape(14.dp), spotColor = Color(0xFF6B8CE0))
                            .background(Color(0xFF82A6F1), RoundedCornerShape(14.dp))
                    ) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Home", tint = Color.White, modifier = Modifier.size(28.dp))
                    }
                    Column {
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
                }"""
content = content.replace(header_old, header_new)

# 4. Fix StatBox call in MarbleSortScreen to not pass colors
stats_old = """            // Stats
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 24.dp),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                StatBox(label = "MOVES", value = state.moveCount.toString().padStart(3, '0'))
                StatBox(label = "BEST", value = "009", valueColor = Color(0xFFA5B4FC))
            }"""
stats_new = """            // Stats
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 24.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                StatBox(label = "MOVES", value = state.moveCount.toString().padStart(3, '0'))
                StatBox(label = "BEST", value = "009")
            }"""
content = content.replace(stats_old, stats_new)

# 5. Fix Bottom Power up Buttons
power_ups_old = """            // Footer - Power Ups
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 24.dp, vertical = 16.dp)
                    .padding(bottom = 56.dp), // Padding to keep above banner ad
                horizontalArrangement = Arrangement.SpaceEvenly,
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Add Tube Power Up
                IconButton(
                    onClick = { showPowerUpDialog = PowerUpType.ADD_TUBE },
                    modifier = Modifier
                        .size(64.dp)
                        .background(Color.White.copy(alpha = 0.05f), RoundedCornerShape(16.dp))
                        .border(1.dp, Color.White.copy(alpha = 0.1f), RoundedCornerShape(16.dp)),
                    enabled = !state.isWon
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.Center) {
                        Icon(Icons.Default.Add, contentDescription = "Add Tube", tint = Color.White, modifier = Modifier.size(28.dp))
                        Spacer(modifier = Modifier.height(2.dp))
                        Text("Tube", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Medium)
                    }
                }
                
                // Undo Power Up
                IconButton(
                    onClick = { showPowerUpDialog = PowerUpType.UNDO },
                    modifier = Modifier
                        .size(64.dp)
                        .background(Color.White.copy(alpha = 0.05f), RoundedCornerShape(16.dp))
                        .border(1.dp, Color.White.copy(alpha = 0.1f), RoundedCornerShape(16.dp)),
                    enabled = state.undoStack.isNotEmpty() && !state.isWon
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.Center) {
                        Icon(Icons.AutoMirrored.Filled.Undo, contentDescription = "Undo", tint = if (state.undoStack.isNotEmpty()) Color.White else Color.White.copy(alpha = 0.3f), modifier = Modifier.size(28.dp))
                        Spacer(modifier = Modifier.height(2.dp))
                        Text("Undo", color = if (state.undoStack.isNotEmpty()) Color.White else Color.White.copy(alpha = 0.3f), fontSize = 10.sp, fontWeight = FontWeight.Medium)
                    }
                }
                
                // Restart / Give Up
                IconButton(
                    onClick = { showGiveUpDialog = true },
                    modifier = Modifier
                        .size(64.dp)
                        .background(Color.White.copy(alpha = 0.05f), RoundedCornerShape(16.dp))
                        .border(1.dp, Color.White.copy(alpha = 0.1f), RoundedCornerShape(16.dp))
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.Center) {
                        Icon(Icons.Default.Refresh, contentDescription = "Restart", tint = Color.White, modifier = Modifier.size(28.dp))
                        Spacer(modifier = Modifier.height(2.dp))
                        Text("Restart", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Medium)
                    }
                }
            }"""

power_ups_new = """            // Footer - Power Ups
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 24.dp, vertical = 16.dp)
                    .padding(bottom = 56.dp), // Padding to keep above banner ad
                horizontalArrangement = Arrangement.SpaceEvenly,
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Add Tube Power Up
                Box(modifier = Modifier.background(Color.White.copy(alpha = 0.3f), RoundedCornerShape(20.dp)).padding(12.dp)) {
                    IconButton(
                        onClick = { showPowerUpDialog = PowerUpType.ADD_TUBE },
                        modifier = Modifier
                            .size(72.dp)
                            .shadow(6.dp, RoundedCornerShape(16.dp), spotColor = Color(0xFF76DB9E))
                            .background(Color(0xFF90E4AD), RoundedCornerShape(16.dp)),
                        enabled = !state.isWon
                    ) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.Center) {
                            Icon(Icons.Default.Add, contentDescription = "Add Tube", tint = Color.White, modifier = Modifier.size(32.dp))
                            Spacer(modifier = Modifier.height(2.dp))
                            Text("Tube", color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Medium)
                        }
                    }
                }
                
                // Undo Power Up
                Box(modifier = Modifier.background(Color.White.copy(alpha = 0.3f), RoundedCornerShape(20.dp)).padding(12.dp)) {
                    IconButton(
                        onClick = { showPowerUpDialog = PowerUpType.UNDO },
                        modifier = Modifier
                            .size(72.dp)
                            .shadow(6.dp, RoundedCornerShape(16.dp), spotColor = Color(0xFF6B8CE0))
                            .background(Color(0xFF82A6F1), RoundedCornerShape(16.dp)),
                        enabled = state.undoStack.isNotEmpty() && !state.isWon
                    ) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.Center) {
                            Icon(Icons.AutoMirrored.Filled.Undo, contentDescription = "Undo", tint = if (state.undoStack.isNotEmpty()) Color.White else Color.White.copy(alpha = 0.5f), modifier = Modifier.size(32.dp))
                            Spacer(modifier = Modifier.height(2.dp))
                            Text("Undo", color = if (state.undoStack.isNotEmpty()) Color.White else Color.White.copy(alpha = 0.5f), fontSize = 12.sp, fontWeight = FontWeight.Medium)
                        }
                    }
                }
                
                // Restart / Give Up
                Box(modifier = Modifier.background(Color.White.copy(alpha = 0.3f), RoundedCornerShape(20.dp)).padding(12.dp)) {
                    IconButton(
                        onClick = { showGiveUpDialog = true },
                        modifier = Modifier
                            .size(72.dp)
                            .shadow(6.dp, RoundedCornerShape(16.dp), spotColor = Color(0xFFE59C69))
                            .background(Color(0xFFFCB682), RoundedCornerShape(16.dp))
                    ) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.Center) {
                            Icon(Icons.Default.Refresh, contentDescription = "Restart", tint = Color.White, modifier = Modifier.size(32.dp))
                            Spacer(modifier = Modifier.height(2.dp))
                            Text("Restart", color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Medium)
                        }
                    }
                }
            }"""
content = content.replace(power_ups_old, power_ups_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

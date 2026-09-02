import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

footer_old = """            // Footer - Power Ups
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
footer_new = """            // Footer - Power Ups
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
                        .size(84.dp)
                        .shadow(6.dp, RoundedCornerShape(24.dp), spotColor = Color(0xFF76DB9E))
                        .background(if (!state.isWon) Color(0xFF90E4AD) else Color.White.copy(alpha = 0.5f), RoundedCornerShape(24.dp)),
                    enabled = !state.isWon
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.Center) {
                        Icon(Icons.Default.Add, contentDescription = "Add Tube", tint = if (!state.isWon) Color(0xFF1E293B) else Color(0xFF1E293B).copy(alpha = 0.5f), modifier = Modifier.size(32.dp))
                        Spacer(modifier = Modifier.height(2.dp))
                        Text("Tube", color = if (!state.isWon) Color(0xFF1E293B) else Color(0xFF1E293B).copy(alpha = 0.5f), fontSize = 14.sp, fontWeight = FontWeight.ExtraBold)
                    }
                }
                
                // Undo Power Up
                val isUndoEnabled = state.undoStack.isNotEmpty() && !state.isWon
                IconButton(
                    onClick = { showPowerUpDialog = PowerUpType.UNDO },
                    modifier = Modifier
                        .size(84.dp)
                        .shadow(6.dp, RoundedCornerShape(24.dp), spotColor = Color(0xFF6B8CE0))
                        .background(if (isUndoEnabled) Color(0xFF82A6F1) else Color.White.copy(alpha = 0.5f), RoundedCornerShape(24.dp)),
                    enabled = isUndoEnabled
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.Center) {
                        Icon(Icons.AutoMirrored.Filled.Undo, contentDescription = "Undo", tint = if (isUndoEnabled) Color(0xFF1E293B) else Color(0xFF1E293B).copy(alpha = 0.5f), modifier = Modifier.size(32.dp))
                        Spacer(modifier = Modifier.height(2.dp))
                        Text("Undo", color = if (isUndoEnabled) Color(0xFF1E293B) else Color(0xFF1E293B).copy(alpha = 0.5f), fontSize = 14.sp, fontWeight = FontWeight.ExtraBold)
                    }
                }
                
                // Restart / Give Up
                IconButton(
                    onClick = { showGiveUpDialog = true },
                    modifier = Modifier
                        .size(84.dp)
                        .shadow(6.dp, RoundedCornerShape(24.dp), spotColor = Color(0xFFE59C69))
                        .background(Color(0xFFFCB682), RoundedCornerShape(24.dp))
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.Center) {
                        Icon(Icons.Default.Refresh, contentDescription = "Restart", tint = Color(0xFF1E293B), modifier = Modifier.size(32.dp))
                        Spacer(modifier = Modifier.height(2.dp))
                        Text("Restart", color = Color(0xFF1E293B), fontSize = 14.sp, fontWeight = FontWeight.ExtraBold)
                    }
                }
            }"""
content = content.replace(footer_old, footer_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

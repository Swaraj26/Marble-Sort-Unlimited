import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

shop_old = """                    Screen.SHOP -> {
                        val billingManager = LocalBillingManager.current
                        val activity = LocalContext.current as Activity
                        
                        LazyColumn(
                            modifier = Modifier.fillMaxSize().padding(horizontal = 24.dp),
                            verticalArrangement = Arrangement.spacedBy(24.dp),
                            contentPadding = PaddingValues(top = 160.dp, bottom = 170.dp)
                        ) {
                            item {
                                Text("Themes", color = Color(0xFF1E293B), fontSize = 28.sp, fontWeight = FontWeight.ExtraBold)
                                Spacer(modifier = Modifier.height(16.dp))
                            }
                            
                            val themes = listOf(
                                Triple("CLASSIC", "Classic", 0),
                                Triple("NEON", "Neon Glow", 5000),
                                Triple("PASTEL", "Pastel Dream", 10000),
                                Triple("COSMIC", "Cosmic", 25000),
                                Triple("FANTASY", "Fantasy", 50000)
                            )
                            
                            items(themes.size) { index ->
                                val theme = themes[index]
                                val themeId = theme.first
                                val isUnlocked = appState.unlockedThemes.contains(themeId)
                                val isActive = appState.activeTheme == themeId
                                
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .shadow(4.dp, RoundedCornerShape(16.dp), spotColor = Color.Black.copy(alpha = 0.05f))
                                        .background(if (isActive) Color.White.copy(alpha = 0.6f) else Color.White.copy(alpha = 0.35f), RoundedCornerShape(16.dp))
                                        .border(
                                            width = if (isActive) 2.dp else 1.dp,
                                            color = if (isActive) Color(0xFF82A6F1) else Color.White.copy(alpha = 0.6f),
                                            shape = RoundedCornerShape(16.dp)
                                        )
                                        .padding(16.dp),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text(theme.second, color = Color(0xFF1E293B), fontSize = 20.sp, fontWeight = FontWeight.Bold)
                                    if (isActive) {
                                        Text("Equipped", color = Color(0xFF82A6F1), fontWeight = FontWeight.ExtraBold)
                                    } else if (isUnlocked) {
                                        Button(
                                            onClick = { viewModel.setTheme(themeId) },
                                            shape = CircleShape,
                                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF82A6F1), contentColor = Color(0xFF1E293B))
                                        ) { Text("Equip", fontWeight = FontWeight.ExtraBold) }
                                    } else {
                                        Button(
                                            onClick = { viewModel.buyTheme(themeId, theme.third) },
                                            enabled = appState.coins >= theme.third,
                                            shape = CircleShape,
                                            colors = ButtonDefaults.buttonColors(
                                                containerColor = Color(0xFFFBBF24),
                                                contentColor = Color(0xFF1E293B),
                                                disabledContainerColor = Color.White.copy(alpha = 0.4f),
                                                disabledContentColor = Color(0xFF1E293B).copy(alpha = 0.5f)
                                            )
                                        ) {
                                            Text("${theme.third} Coins", fontWeight = FontWeight.ExtraBold)
                                        }
                                    }
                                }
                            }
                            
                            item {
                                Spacer(modifier = Modifier.height(24.dp))
                                Text("Buy Coins", color = Color(0xFF1E293B), fontSize = 28.sp, fontWeight = FontWeight.ExtraBold)
                                Spacer(modifier = Modifier.height(16.dp))
                            }
                            
                            val coinPacks = listOf(
                                Pair(1000, "coin_pack_1000"),
                                Pair(5000, "coin_pack_5000"),
                                Pair(12000, "coin_pack_12000")
                            )
                            
                            items(coinPacks.size) { index ->
                                val pack = coinPacks[index]
                                val amount = pack.first
                                val price = if (amount == 1000) "$0.99" else if (amount == 5000) "$3.99" else "$7.99"
                                
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .shadow(4.dp, RoundedCornerShape(16.dp), spotColor = Color.Black.copy(alpha = 0.05f))
                                        .background(Color.White.copy(alpha = 0.35f), RoundedCornerShape(16.dp))
                                        .border(1.dp, Color.White.copy(alpha = 0.6f), RoundedCornerShape(16.dp))
                                        .padding(16.dp),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                        Icon(Icons.Default.Star, contentDescription = "Coins", tint = Color(0xFFFBBF24))
                                        Text("$amount Coins", color = Color(0xFF1E293B), fontSize = 20.sp, fontWeight = FontWeight.Bold)
                                    }
                                    Button(
                                        onClick = {
                                            billingManager.initiatePurchaseFlow(activity, pack.second) {
                                                viewModel.addCoins(amount)
                                            }
                                        },
                                        shape = CircleShape,
                                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF90E4AD), contentColor = Color(0xFF1E293B))
                                    ) {
                                        Text(price, fontWeight = FontWeight.ExtraBold)
                                    }
                                }
                            }
                        }
                    }"""

shop_new = """                    Screen.SHOP -> {
                        val billingManager = LocalBillingManager.current
                        val activity = LocalContext.current as Activity
                        
                        LazyColumn(
                            modifier = Modifier.fillMaxSize().padding(horizontal = 24.dp),
                            verticalArrangement = Arrangement.spacedBy(24.dp),
                            contentPadding = PaddingValues(top = 16.dp, bottom = 170.dp)
                        ) {
                            item {
                                Text("Buy Coins", color = Color(0xFF1E293B), fontSize = 28.sp, fontWeight = FontWeight.ExtraBold)
                                Spacer(modifier = Modifier.height(16.dp))
                            }
                            
                            val coinPacks = listOf(
                                Pair(1000, "coin_pack_1000"),
                                Pair(5000, "coin_pack_5000"),
                                Pair(12000, "coin_pack_12000")
                            )
                            
                            items(coinPacks.size) { index ->
                                val pack = coinPacks[index]
                                val amount = pack.first
                                val price = if (amount == 1000) "$0.99" else if (amount == 5000) "$3.99" else "$7.99"
                                
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .shadow(4.dp, RoundedCornerShape(16.dp), spotColor = Color.Black.copy(alpha = 0.05f))
                                        .background(Color.White.copy(alpha = 0.35f), RoundedCornerShape(16.dp))
                                        .border(1.dp, Color.White.copy(alpha = 0.6f), RoundedCornerShape(16.dp))
                                        .padding(16.dp),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                        Icon(Icons.Default.Star, contentDescription = "Coins", tint = Color(0xFFFBBF24))
                                        Text("$amount Coins", color = Color(0xFF1E293B), fontSize = 20.sp, fontWeight = FontWeight.Bold)
                                    }
                                    Button(
                                        onClick = {
                                            billingManager.initiatePurchaseFlow(activity, pack.second) {
                                                viewModel.addCoins(amount)
                                            }
                                        },
                                        shape = CircleShape,
                                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF90E4AD), contentColor = Color(0xFF1E293B))
                                    ) {
                                        Text(price, fontWeight = FontWeight.ExtraBold)
                                    }
                                }
                            }
                            
                            item {
                                Spacer(modifier = Modifier.height(32.dp))
                                Text("Themes", color = Color(0xFF1E293B), fontSize = 28.sp, fontWeight = FontWeight.ExtraBold)
                                Spacer(modifier = Modifier.height(16.dp))
                            }
                            
                            val themes = listOf(
                                Triple("CLASSIC", "Classic", 0),
                                Triple("NEON", "Neon Glow", 5000),
                                Triple("PASTEL", "Pastel Dream", 10000),
                                Triple("COSMIC", "Cosmic", 25000),
                                Triple("FANTASY", "Fantasy", 50000)
                            )
                            
                            items(themes.size) { index ->
                                val theme = themes[index]
                                val themeId = theme.first
                                val isUnlocked = appState.unlockedThemes.contains(themeId)
                                val isActive = appState.activeTheme == themeId
                                
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .shadow(4.dp, RoundedCornerShape(16.dp), spotColor = Color.Black.copy(alpha = 0.05f))
                                        .background(if (isActive) Color.White.copy(alpha = 0.6f) else Color.White.copy(alpha = 0.35f), RoundedCornerShape(16.dp))
                                        .border(
                                            width = if (isActive) 2.dp else 1.dp,
                                            color = if (isActive) Color(0xFF82A6F1) else Color.White.copy(alpha = 0.6f),
                                            shape = RoundedCornerShape(16.dp)
                                        )
                                        .padding(16.dp),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text(theme.second, color = Color(0xFF1E293B), fontSize = 20.sp, fontWeight = FontWeight.Bold)
                                    if (isActive) {
                                        Text("Equipped", color = Color(0xFF82A6F1), fontWeight = FontWeight.ExtraBold)
                                    } else if (isUnlocked) {
                                        Button(
                                            onClick = { viewModel.setTheme(themeId) },
                                            shape = CircleShape,
                                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF82A6F1), contentColor = Color(0xFF1E293B))
                                        ) { Text("Equip", fontWeight = FontWeight.ExtraBold) }
                                    } else {
                                        Button(
                                            onClick = { viewModel.buyTheme(themeId, theme.third) },
                                            enabled = appState.coins >= theme.third,
                                            shape = CircleShape,
                                            colors = ButtonDefaults.buttonColors(
                                                containerColor = Color(0xFFFBBF24),
                                                contentColor = Color(0xFF1E293B),
                                                disabledContainerColor = Color.White.copy(alpha = 0.4f),
                                                disabledContentColor = Color(0xFF1E293B).copy(alpha = 0.5f)
                                            )
                                        ) {
                                            Text("${theme.third} Coins", fontWeight = FontWeight.ExtraBold)
                                        }
                                    }
                                }
                            }
                        }
                    }"""
content = content.replace(shop_old, shop_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

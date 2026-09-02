import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# 1. Shop Buy Theme Button
shop_theme_old = """                                    if (isActive) {
                                        Text("Equipped", color = Color(0xFF82A6F1), fontWeight = FontWeight.ExtraBold)
                                    } else if (isUnlocked) {
                                        Button(onClick = { viewModel.setTheme(themeId) }, colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF82A6F1))) { Text("Equip") }
                                    } else {
                                        Button(
                                            onClick = { viewModel.buyTheme(themeId, theme.third) },
                                            enabled = appState.coins >= theme.third,
                                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFFBBF24))
                                        ) {
                                            Text("${theme.third} Coins", color = Color.White, fontWeight = FontWeight.Bold)
                                        }
                                    }"""
shop_theme_new = """                                    if (isActive) {
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
                                    }"""
content = content.replace(shop_theme_old, shop_theme_new)

# 2. Shop Buy Coins Button
shop_coins_old = """                                    Button(
                                        onClick = {
                                            billingManager.initiatePurchaseFlow(activity, pack.second) {
                                                viewModel.addCoins(amount)
                                            }
                                        },
                                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF90E4AD))
                                    ) {
                                        Text(price, color = Color.White, fontWeight = FontWeight.ExtraBold)
                                    }"""
shop_coins_new = """                                    Button(
                                        onClick = {
                                            billingManager.initiatePurchaseFlow(activity, pack.second) {
                                                viewModel.addCoins(amount)
                                            }
                                        },
                                        shape = CircleShape,
                                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF90E4AD), contentColor = Color(0xFF1E293B))
                                    ) {
                                        Text(price, fontWeight = FontWeight.ExtraBold)
                                    }"""
content = content.replace(shop_coins_old, shop_coins_new)

# 3. Home Play Button
home_play_old = """                            // Play Button positioned inside the content area (above ads and tabs)
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
home_play_new = """                            // Play Button positioned inside the content area (above ads and tabs)
                            Box(modifier = Modifier.align(Alignment.BottomCenter).fillMaxWidth().padding(start = 32.dp, end = 32.dp, bottom = 24.dp)) {
                                Button(
                                    onClick = { if (appState.lives > 0) viewModel.startLevel(appState.highestUnlockedLevel) },
                                    colors = ButtonDefaults.buttonColors(
                                        containerColor = if (appState.lives > 0) Color(0xFF90E4AD) else Color.White.copy(alpha = 0.5f),
                                        contentColor = Color(0xFF1E293B),
                                        disabledContainerColor = Color.White.copy(alpha = 0.5f),
                                        disabledContentColor = Color(0xFF1E293B).copy(alpha = 0.5f)
                                    ),
                                    shape = CircleShape,
                                    elevation = ButtonDefaults.buttonElevation(defaultElevation = 6.dp),
                                    modifier = Modifier.fillMaxWidth().height(64.dp)
                                ) {
                                    Text(
                                        if (appState.lives > 0) "PLAY LEVEL ${appState.highestUnlockedLevel}" else "OUT OF LIVES",
                                        fontSize = 20.sp,
                                        fontWeight = FontWeight.ExtraBold,
                                        letterSpacing = 1.sp
                                    )
                                }
                            }"""
content = content.replace(home_play_old, home_play_new)

# 4. Tab Bar and Ad Layout
tab_ad_old = """            // Banner Ad
            AdmobBanner()
            
            // Bottom Tabs Bar (pushed to bottom of column)
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .shadow(16.dp, RoundedCornerShape(topStart = 24.dp, topEnd = 24.dp), spotColor = Color.Black.copy(alpha = 0.1f))
                    .background(Color.White.copy(alpha = 0.7f), RoundedCornerShape(topStart = 24.dp, topEnd = 24.dp))
                    .border(1.dp, Color.White, RoundedCornerShape(topStart = 24.dp, topEnd = 24.dp))
                    .padding(vertical = 12.dp, horizontal = 24.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                TabItem(Icons.Default.ShoppingCart, "Shop", screen == Screen.SHOP) { viewModel.navigate(Screen.SHOP) }
                TabItem(Icons.Default.Home, "Home", screen == Screen.HOME) { viewModel.navigate(Screen.HOME) }
                TabItem(Icons.Default.Settings, "Settings", screen == Screen.SETTINGS) { viewModel.navigate(Screen.SETTINGS) }
            }"""
tab_ad_new = """            // Bottom Tabs Island
            Row(
                modifier = Modifier
                    .padding(horizontal = 32.dp, vertical = 12.dp)
                    .fillMaxWidth()
                    .shadow(16.dp, CircleShape, spotColor = Color.Black.copy(alpha = 0.1f))
                    .background(Color.White.copy(alpha = 0.8f), CircleShape)
                    .border(1.dp, Color.White, CircleShape)
                    .padding(vertical = 8.dp, horizontal = 24.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                TabItem(Icons.Default.ShoppingCart, "Shop", screen == Screen.SHOP) { viewModel.navigate(Screen.SHOP) }
                TabItem(Icons.Default.Home, "Home", screen == Screen.HOME) { viewModel.navigate(Screen.HOME) }
                TabItem(Icons.Default.Settings, "Settings", screen == Screen.SETTINGS) { viewModel.navigate(Screen.SETTINGS) }
            }
            
            // Banner Ad at the very bottom
            Box(modifier = Modifier.fillMaxWidth(), contentAlignment = Alignment.Center) {
                AdmobBanner()
            }"""
content = content.replace(tab_ad_old, tab_ad_new)

# 5. Shop Padding Update
shop_padding_old = """                        LazyColumn(
                            modifier = Modifier.fillMaxSize().padding(horizontal = 24.dp),
                            verticalArrangement = Arrangement.spacedBy(24.dp),
                            contentPadding = PaddingValues(top = 160.dp, bottom = 120.dp)
                        ) {"""
shop_padding_new = """                        LazyColumn(
                            modifier = Modifier.fillMaxSize().padding(horizontal = 24.dp),
                            verticalArrangement = Arrangement.spacedBy(24.dp),
                            contentPadding = PaddingValues(top = 160.dp, bottom = 170.dp)
                        ) {"""
content = content.replace(shop_padding_old, shop_padding_new)

# 6. Home Padding Update
home_padding_old = """                            LazyColumn(
                                state = listState,
                                userScrollEnabled = false,
                                reverseLayout = true,
                                contentPadding = PaddingValues(top = 160.dp, bottom = 160.dp),
                                horizontalAlignment = Alignment.CenterHorizontally,
                                modifier = Modifier.fillMaxWidth().fillMaxHeight()
                            ) {"""
home_padding_new = """                            LazyColumn(
                                state = listState,
                                userScrollEnabled = false,
                                reverseLayout = true,
                                contentPadding = PaddingValues(top = 160.dp, bottom = 210.dp),
                                horizontalAlignment = Alignment.CenterHorizontally,
                                modifier = Modifier.fillMaxWidth().fillMaxHeight()
                            ) {"""
content = content.replace(home_padding_old, home_padding_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

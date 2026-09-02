import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

mapping_old = """                    it.copy(
                        coins = entity.coins,
                        lives = entity.lives,
                        highestUnlockedLevel = entity.highestUnlockedLevel,
                        soundEnabled = entity.soundEnabled,
                        hapticEnabled = entity.hapticEnabled,
                        lastClaimedDate = entity.lastClaimedDate,
                        unlockedThemes = entity.unlockedThemes.split(",").filter { it.isNotBlank() },
                        activeTheme = entity.activeTheme
                    )"""

mapping_new = """                    it.copy(
                        coins = entity.coins,
                        lives = entity.lives,
                        highestUnlockedLevel = entity.highestUnlockedLevel,
                        soundEnabled = entity.soundEnabled,
                        hapticEnabled = entity.hapticEnabled,
                        lastClaimedDate = entity.lastClaimedDate,
                        unlockedThemes = entity.unlockedThemes.split(",").filter { it.isNotBlank() },
                        activeTheme = entity.activeTheme,
                        nextLifeTime = entity.nextLifeTime
                    )"""

content = content.replace(mapping_old, mapping_new)

save_old = """                    AppStateEntity(
                        coins = state.coins,
                        lives = state.lives,
                        highestUnlockedLevel = state.highestUnlockedLevel,
                        soundEnabled = state.soundEnabled,
                        hapticEnabled = state.hapticEnabled,
                        lastClaimedDate = state.lastClaimedDate,
                        unlockedThemes = state.unlockedThemes.joinToString(","),
                        activeTheme = state.activeTheme
                    )"""

save_new = """                    AppStateEntity(
                        coins = state.coins,
                        lives = state.lives,
                        highestUnlockedLevel = state.highestUnlockedLevel,
                        soundEnabled = state.soundEnabled,
                        hapticEnabled = state.hapticEnabled,
                        lastClaimedDate = state.lastClaimedDate,
                        unlockedThemes = state.unlockedThemes.joinToString(","),
                        activeTheme = state.activeTheme,
                        nextLifeTime = state.nextLifeTime
                    )"""

content = content.replace(save_old, save_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

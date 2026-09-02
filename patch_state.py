import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

state_old = """data class AppState(
    val screen: Screen = Screen.HOME,
    val coins: Int = 0,
    val lives: Int = 5,
    val highestUnlockedLevel: Int = 1,
    val soundEnabled: Boolean = true,
    val hapticEnabled: Boolean = true,
    val lastClaimedDate: String = "",
    val showDailyBonusDialog: Boolean = false,
    val unlockedThemes: List<String> = listOf("CLASSIC"),
    val activeTheme: String = "CLASSIC"
)"""

state_new = """data class AppState(
    val screen: Screen = Screen.HOME,
    val coins: Int = 0,
    val lives: Int = 5,
    val highestUnlockedLevel: Int = 1,
    val soundEnabled: Boolean = true,
    val hapticEnabled: Boolean = true,
    val lastClaimedDate: String = "",
    val showDailyBonusDialog: Boolean = false,
    val unlockedThemes: List<String> = listOf("CLASSIC"),
    val activeTheme: String = "CLASSIC",
    val nextLifeTime: Long = 0L
)"""

content = content.replace(state_old, state_new)

entity_old = """@Entity(tableName = "app_state")
data class AppStateEntity(
    @PrimaryKey val id: Int = 1,
    val coins: Int,
    val lives: Int,
    val highestUnlockedLevel: Int,
    val soundEnabled: Boolean,
    val hapticEnabled: Boolean,
    val lastClaimedDate: String,
    val unlockedThemes: String,
    val activeTheme: String
)"""

entity_new = """@Entity(tableName = "app_state")
data class AppStateEntity(
    @PrimaryKey val id: Int = 1,
    val coins: Int,
    val lives: Int,
    val highestUnlockedLevel: Int,
    val soundEnabled: Boolean,
    val hapticEnabled: Boolean,
    val lastClaimedDate: String,
    val unlockedThemes: String,
    val activeTheme: String,
    val nextLifeTime: Long = 0L
)"""

content = content.replace(entity_old, entity_new)

db_old = """@Database(entities = [AppStateEntity::class], version = 2, exportSchema = false)"""
db_new = """@Database(entities = [AppStateEntity::class], version = 3, exportSchema = false)"""
content = content.replace(db_old, db_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Add loop to init
init_old = """            withContext(Dispatchers.Main) {
                checkDailyBonus()
                startLevel(_appState.value.highestUnlockedLevel, changeScreen = false)
            }"""
init_new = """            withContext(Dispatchers.Main) {
                checkDailyBonus()
                startLevel(_appState.value.highestUnlockedLevel, changeScreen = false)
            }
            
            kotlinx.coroutines.GlobalScope.launch(Dispatchers.Main) {
                while (true) {
                    checkLifeRegen()
                    kotlinx.coroutines.delay(1000)
                }
            }"""
content = content.replace(init_old, init_new)

check_daily_old = """    private fun checkDailyBonus() {"""
check_daily_new = """    private fun checkLifeRegen() {
        val now = System.currentTimeMillis()
        val state = _appState.value
        if (state.lives < 5 && state.nextLifeTime > 0 && now >= state.nextLifeTime) {
            val timePassed = now - state.nextLifeTime
            val livesGained = 1 + (timePassed / (30 * 60 * 1000L)).toInt()
            val finalLives = (state.lives + livesGained).coerceAtMost(5)
            
            val newNextLifeTime = if (finalLives < 5) {
                state.nextLifeTime + livesGained * 30 * 60 * 1000L
            } else {
                0L
            }
            
            _appState.update { it.copy(lives = finalLives, nextLifeTime = newNextLifeTime) }
        } else if (state.lives < 5 && state.nextLifeTime == 0L) {
            // Fallback just in case
            _appState.update { it.copy(nextLifeTime = now + 30 * 60 * 1000L) }
        }
    }
    
    private fun consumeLife() {
        val state = _appState.value
        if (state.lives <= 0) return
        val now = System.currentTimeMillis()
        val newNextLifeTime = if (state.lives == 5 || state.nextLifeTime == 0L) now + 30 * 60 * 1000L else state.nextLifeTime
        _appState.update { it.copy(lives = state.lives - 1, nextLifeTime = newNextLifeTime) }
    }

    private fun checkDailyBonus() {"""
content = content.replace(check_daily_old, check_daily_new)

restart_old = """    fun restartLevel() {
        if (_appState.value.lives <= 0) return
        _appState.update { it.copy(lives = it.lives - 1) }"""
restart_new = """    fun restartLevel() {
        if (_appState.value.lives <= 0) return
        consumeLife()"""
content = content.replace(restart_old, restart_new)

home_old = """        if (!state.isWon && state.moveCount > 0) {
            if (_appState.value.lives > 0) {
                _appState.update { it.copy(lives = it.lives - 1) }
            }
        }"""
home_new = """        if (!state.isWon && state.moveCount > 0) {
            if (_appState.value.lives > 0) {
                consumeLife()
            }
        }"""
content = content.replace(home_old, home_new)


with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

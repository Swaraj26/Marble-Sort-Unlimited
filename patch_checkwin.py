import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

old_check = """    private fun checkWinCondition() {
        val won = _uiState.value.tubes.all { tube ->
            tube.balls.isEmpty() || (tube.balls.size == tube.maxCapacity && tube.balls.all { it.color == tube.balls.first().color })
        }
        if (won && !_uiState.value.isWon) {
            _soundEvents.tryEmit(SoundEvent.WIN)
            _uiState.update { it.copy(isWon = true, selectedTubeIndex = null) }
            _appState.update {
                it.copy(
                    coins = it.coins + 50,
                    highestUnlockedLevel = max(it.highestUnlockedLevel, _uiState.value.level + 1)
                )
            }
        }
    }"""

new_check = """    private fun checkWinCondition() {
        val state = _uiState.value
        val won = state.tubes.all { tube ->
            tube.balls.isEmpty() || (tube.balls.size == tube.maxCapacity && tube.balls.all { it.color == tube.balls.first().color })
        }
        if (won && !state.isWon) {
            _soundEvents.tryEmit(SoundEvent.WIN)
            _uiState.update { it.copy(isWon = true, selectedTubeIndex = null) }
            _appState.update {
                it.copy(
                    coins = it.coins + 50,
                    highestUnlockedLevel = max(it.highestUnlockedLevel, state.level + 1)
                )
            }
        } else if (!won && state.moveCount >= state.maxMoves && !state.isLost) {
            consumeLife()
            _uiState.update { it.copy(isLost = true, selectedTubeIndex = null) }
        }
    }"""

content = content.replace(old_check, new_check)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

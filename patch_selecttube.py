import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

state_old = """    val isWon: Boolean = false,
    val undoStack: List<MoveAction> = emptyList(),
    val level: Int = 1
) {
    val movesLeft: Int get() = kotlin.math.max(0, maxMoves - moveCount)
}"""

state_new = """    val isWon: Boolean = false,
    val isLost: Boolean = false,
    val undoStack: List<MoveAction> = emptyList(),
    val level: Int = 1
) {
    val movesLeft: Int get() = kotlin.math.max(0, maxMoves - moveCount)
}"""
content = content.replace(state_old, state_new)

undo_old = """        _uiState.update { it.copy(tubes = newTubes, moveCount = it.moveCount - 1, undoStack = it.undoStack.dropLast(1), selectedTubeIndex = null) }
    }"""
undo_new = """        _uiState.update { it.copy(tubes = newTubes, moveCount = it.moveCount - 1, undoStack = it.undoStack.dropLast(1), selectedTubeIndex = null, isLost = false) }
    }"""
content = content.replace(undo_old, undo_new)

select_old = """                    val moveCount = state.moveCount + 1
                    val isWon = checkWin(newTubes)
                    
                    if (isWon) {
                        _soundEvents.tryEmit(SoundEvent.WIN)
                    } else {
                        _soundEvents.tryEmit(SoundEvent.MOVE)
                    }
                    
                    _uiState.update { it.copy(tubes = newTubes, moveCount = moveCount, isWon = isWon, selectedTubeIndex = null, undoStack = it.undoStack + MoveAction(selected, index)) }
                } else {"""

select_new = """                    val moveCount = state.moveCount + 1
                    val isWon = checkWin(newTubes)
                    val isLost = !isWon && moveCount >= state.maxMoves
                    
                    if (isLost) {
                        consumeLife()
                    }
                    
                    if (isWon) {
                        _soundEvents.tryEmit(SoundEvent.WIN)
                    } else {
                        _soundEvents.tryEmit(SoundEvent.MOVE)
                    }
                    
                    _uiState.update { it.copy(tubes = newTubes, moveCount = moveCount, isWon = isWon, isLost = isLost, selectedTubeIndex = null, undoStack = it.undoStack + MoveAction(selected, index)) }
                } else {"""
content = content.replace(select_old, select_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

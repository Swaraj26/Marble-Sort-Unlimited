import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

undo_old = """        _uiState.update {
            it.copy(
                tubes = newTubes,
                moveCount = it.moveCount + 1,
                undoStack = it.undoStack.dropLast(1),
                selectedTubeIndex = null
            )
        }"""

undo_new = """        _uiState.update {
            it.copy(
                tubes = newTubes,
                moveCount = kotlin.math.max(0, it.moveCount - 1),
                undoStack = it.undoStack.dropLast(1),
                selectedTubeIndex = null,
                isLost = false
            )
        }"""

content = content.replace(undo_old, undo_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

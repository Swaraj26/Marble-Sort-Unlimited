import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

state_old = """data class GameState(
    val tubes: List<Tube> = emptyList(),
    val selectedTubeIndex: Int? = null,
    val moveCount: Int = 0,
    val isWon: Boolean = false,
    val undoStack: List<MoveAction> = emptyList(),
    val level: Int = 1
)"""

state_new = """data class GameState(
    val tubes: List<Tube> = emptyList(),
    val selectedTubeIndex: Int? = null,
    val moveCount: Int = 0,
    val maxMoves: Int = 0,
    val isWon: Boolean = false,
    val undoStack: List<MoveAction> = emptyList(),
    val level: Int = 1
) {
    val movesLeft: Int get() = kotlin.math.max(0, maxMoves - moveCount)
}"""

content = content.replace(state_old, state_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

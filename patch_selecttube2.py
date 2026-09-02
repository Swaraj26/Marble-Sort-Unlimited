import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

select_old = """    fun selectTube(index: Int) {
        val state = _uiState.value
        if (state.isWon) return"""

select_new = """    fun selectTube(index: Int) {
        val state = _uiState.value
        if (state.isWon || state.isLost) return"""

content = content.replace(select_old, select_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

statbox_old = """            // Stats
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 24.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                StatBox(label = "MOVES", value = state.moveCount.toString().padStart(3, '0'))
                StatBox(label = "BEST", value = "009")
            }"""

statbox_new = """            // Stats
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 24.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                StatBox(label = "MOVES", value = state.moveCount.toString().padStart(3, '0'))
                StatBox(label = "MOVES LEFT", value = state.movesLeft.toString().padStart(3, '0'))
            }"""
content = content.replace(statbox_old, statbox_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

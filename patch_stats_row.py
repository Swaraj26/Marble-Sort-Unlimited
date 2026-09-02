import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

stats_old = """            // Stats
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 24.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                StatBox(label = "MOVES", value = state.moveCount.toString().padStart(3, '0'))
                StatBox(label = "MOVES LEFT", value = state.movesLeft.toString().padStart(3, '0'))
            }

            Spacer(modifier = Modifier.height(16.dp))"""

stats_new = """            // Stats
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                StatBox(label = "MOVES", value = state.moveCount.toString().padStart(3, '0'))
                StatBox(label = "MOVES LEFT", value = state.movesLeft.toString().padStart(3, '0'))
            }

            Spacer(modifier = Modifier.height(8.dp))"""

if stats_old in content:
    content = content.replace(stats_old, stats_new)
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(content)
    print("Patched Stats Row")
else:
    print("Stats Row not found!")

import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

startLevel_old = """        var currentTubes = tubes.toList()
        val numShuffles = (20 + (level * 5)) + if (isHardLevel) 50 else 0
        var lastMove: Pair<Int, Int>? = null

        for (step in 0 until numShuffles) {
            val validMoves = mutableListOf<Pair<Int, Int>>()
            for (s in currentTubes.indices) {
                val sourceTube = currentTubes[s]
                if (sourceTube.balls.isEmpty()) continue

                val canBackward = sourceTube.balls.size == 1 ||
                        sourceTube.balls[sourceTube.balls.size - 2].color == sourceTube.balls.last().color

                if (canBackward) {
                    for (d in currentTubes.indices) {
                        if (s == d) continue
                        if (currentTubes[d].balls.size < 4) {
                            validMoves.add(s to d)
                        }
                    }
                }
            }
            if (validMoves.isNotEmpty()) {
                val filtered = validMoves.filter { it.first != lastMove?.second || it.second != lastMove?.first }
                val move = if (filtered.isNotEmpty()) filtered.random() else validMoves.random()
                lastMove = move

                val newTubes = currentTubes.toMutableList()
                val sBalls = newTubes[move.first].balls.toMutableList()
                val dBBalls = newTubes[move.second].balls.toMutableList()

                val ball = sBalls.removeAt(sBalls.lastIndex)
                dBBalls.add(ball)

                newTubes[move.first] = newTubes[move.first].copy(balls = sBalls)
                newTubes[move.second] = newTubes[move.second].copy(balls = dBBalls)
                currentTubes = newTubes
            }
        }

        _uiState.value = GameState(
            tubes = currentTubes,
            level = level
        )"""

startLevel_new = """        var currentTubes = tubes.toList()
        val numShuffles = (20 + (level * 5)) + if (isHardLevel) 50 else 0
        var lastMove: Pair<Int, Int>? = null

        val history = mutableListOf<List<Tube>>()
        history.add(currentTubes)

        for (step in 0 until numShuffles) {
            val validMoves = mutableListOf<Pair<Int, Int>>()
            for (s in currentTubes.indices) {
                val sourceTube = currentTubes[s]
                if (sourceTube.balls.isEmpty()) continue

                val canBackward = sourceTube.balls.size == 1 ||
                        sourceTube.balls[sourceTube.balls.size - 2].color == sourceTube.balls.last().color

                if (canBackward) {
                    for (d in currentTubes.indices) {
                        if (s == d) continue
                        if (currentTubes[d].balls.size < 4) {
                            validMoves.add(s to d)
                        }
                    }
                }
            }
            if (validMoves.isNotEmpty()) {
                val filtered = validMoves.filter { it.first != lastMove?.second || it.second != lastMove?.first }
                val move = if (filtered.isNotEmpty()) filtered.random() else validMoves.random()
                lastMove = move

                val newTubes = currentTubes.toMutableList()
                val sBalls = newTubes[move.first].balls.toMutableList()
                val dBBalls = newTubes[move.second].balls.toMutableList()

                val ball = sBalls.removeAt(sBalls.lastIndex)
                dBBalls.add(ball)

                newTubes[move.first] = newTubes[move.first].copy(balls = sBalls)
                newTubes[move.second] = newTubes[move.second].copy(balls = dBBalls)
                currentTubes = newTubes
                history.add(currentTubes)
            }
        }
        
        val dp = IntArray(history.size) { Int.MAX_VALUE }
        dp[history.lastIndex] = 0
        for (i in history.lastIndex downTo 0) {
            if (dp[i] == Int.MAX_VALUE) continue
            if (i > 0) {
                dp[i - 1] = kotlin.math.min(dp[i - 1], dp[i] + 1)
            }
            for (j in 0 until i - 1) {
                if (isOneValidMove(history[i], history[j])) {
                    dp[j] = kotlin.math.min(dp[j], dp[i] + 1)
                }
            }
        }
        
        val minMoves = dp[0]
        val multiplier = if (isHardLevel) 1.3 else 1.5
        val maxMovesAllowed = kotlin.math.max(1, kotlin.math.ceil(minMoves * multiplier).toInt())

        _uiState.value = GameState(
            tubes = currentTubes,
            level = level,
            maxMoves = maxMovesAllowed
        )"""

content = content.replace(startLevel_old, startLevel_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

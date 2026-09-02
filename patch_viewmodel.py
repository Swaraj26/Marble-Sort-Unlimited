import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Add isOneValidMove and isValidMove
methods = """    private fun isOneValidMove(stateA: List<Tube>, stateB: List<Tube>): Boolean {
        var diff1 = -1
        var diff2 = -1
        var diffCount = 0
        for (i in stateA.indices) {
            if (stateA[i].balls != stateB[i].balls) {
                diffCount++
                if (diffCount == 1) diff1 = i
                else if (diffCount == 2) diff2 = i
                else return false
            }
        }
        if (diffCount != 2) return false

        if (isValidMove(stateA, diff1, diff2, stateB)) return true
        if (isValidMove(stateA, diff2, diff1, stateB)) return true
        return false
    }

    private fun isValidMove(stateA: List<Tube>, src: Int, dst: Int, stateB: List<Tube>): Boolean {
        val srcBallsA = stateA[src].balls
        val dstBallsA = stateA[dst].balls
        if (srcBallsA.isEmpty()) return false
        if (dstBallsA.size >= 4) return false
        
        val ballToMove = srcBallsA.last()
        if (dstBallsA.isNotEmpty() && dstBallsA.last().color != ballToMove.color) return false
        
        val expectedSrcB = srcBallsA.dropLast(1)
        val expectedDstB = dstBallsA + ballToMove
        
        return stateB[src].balls == expectedSrcB && stateB[dst].balls == expectedDstB
    }

    fun selectTube"""

content = content.replace("    fun selectTube", methods)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

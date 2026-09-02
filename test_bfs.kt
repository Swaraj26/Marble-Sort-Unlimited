import java.util.*

data class State(val t: LongArray) {
    override fun equals(other: Any?) = other is State && t.contentEquals(other.t)
    override fun hashCode() = t.contentHashCode()
}

fun main() {
    println("Test")
}

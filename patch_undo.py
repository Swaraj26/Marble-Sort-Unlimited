import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

undo_old = "val isUndoEnabled = state.undoStack.isNotEmpty() && !state.isWon"
undo_new = "val isUndoEnabled = state.undoStack.isNotEmpty() && !state.isWon && !state.isLost"
content = content.replace(undo_old, undo_new)

tube_old = "if (!state.isWon) Color(0xFF90E4AD)"
tube_new = "if (!state.isWon && !state.isLost) Color(0xFF90E4AD)"
content = content.replace(tube_old, tube_new)

add_tube_en_old = "enabled = !state.isWon"
add_tube_en_new = "enabled = !state.isWon && !state.isLost"
content = content.replace(add_tube_en_old, add_tube_en_new)

tube_icon_old = "tint = if (!state.isWon) Color(0xFF1E293B) else Color(0xFF1E293B).copy(alpha = 0.5f)"
tube_icon_new = "tint = if (!state.isWon && !state.isLost) Color(0xFF1E293B) else Color(0xFF1E293B).copy(alpha = 0.5f)"
content = content.replace(tube_icon_old, tube_icon_new)

tube_txt_old = "color = if (!state.isWon) Color(0xFF1E293B) else Color(0xFF1E293B).copy(alpha = 0.5f)"
tube_txt_new = "color = if (!state.isWon && !state.isLost) Color(0xFF1E293B) else Color(0xFF1E293B).copy(alpha = 0.5f)"
content = content.replace(tube_txt_old, tube_txt_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

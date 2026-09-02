import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

select_old = """                    checkWinCondition()
                } else {
                    if (state.tubes[index].balls.isNotEmpty()) {
                        _soundEvents.tryEmit(SoundEvent.SELECT)
                        _uiState.update { it.copy(selectedTubeIndex = index) }
                    } else {
                        _uiState.update { it.copy(selectedTubeIndex = null) }
                    }
                }
            }
        }
    }"""

select_new = """                    checkWinCondition()
                } else {
                    _soundEvents.tryEmit(SoundEvent.ERROR)
                }
            }
        }
    }"""

content = content.replace(select_old, select_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

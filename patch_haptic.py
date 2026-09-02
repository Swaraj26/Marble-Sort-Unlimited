import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

enum_old = "enum class SoundEvent {\n    SELECT, MOVE, WIN\n}"
enum_new = "enum class SoundEvent {\n    SELECT, MOVE, WIN, ERROR\n}"
content = content.replace(enum_old, enum_new)

effect_old = """    val haptic = LocalHapticFeedback.current
    LaunchedEffect(viewModel) {
        viewModel.soundEvents.collect { event ->
            val appStateVal = viewModel.appState.value
            if (appStateVal.soundEnabled) {
                when(event) {
                    SoundEvent.SELECT -> soundManager.playSelect()
                    SoundEvent.MOVE -> soundManager.playMove()
                    SoundEvent.WIN -> soundManager.playWin()
                }
            }
            if (appStateVal.hapticEnabled) {
                haptic.performHapticFeedback(HapticFeedbackType.LongPress)
            }
        }
    }"""

effect_new = """    val view = androidx.compose.ui.platform.LocalView.current
    LaunchedEffect(viewModel) {
        viewModel.soundEvents.collect { event ->
            val appStateVal = viewModel.appState.value
            if (appStateVal.soundEnabled) {
                when(event) {
                    SoundEvent.SELECT -> soundManager.playSelect()
                    SoundEvent.MOVE -> soundManager.playMove()
                    SoundEvent.WIN -> soundManager.playWin()
                    SoundEvent.ERROR -> {}
                }
            }
            if (appStateVal.hapticEnabled) {
                when(event) {
                    SoundEvent.MOVE, SoundEvent.WIN -> {
                        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.R) {
                            view.performHapticFeedback(android.view.HapticFeedbackConstants.CONFIRM)
                        } else {
                            view.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY)
                        }
                    }
                    SoundEvent.ERROR -> {
                        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.R) {
                            view.performHapticFeedback(android.view.HapticFeedbackConstants.REJECT)
                        } else {
                            view.performHapticFeedback(android.view.HapticFeedbackConstants.LONG_PRESS)
                        }
                    }
                    SoundEvent.SELECT -> {
                        view.performHapticFeedback(android.view.HapticFeedbackConstants.CLOCK_TICK)
                    }
                }
            }
        }
    }"""

content = content.replace(effect_old, effect_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

package com.example

import android.content.Context
import android.media.AudioAttributes
import android.media.SoundPool
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.TextButton
import androidx.compose.material3.Switch
import androidx.compose.material3.SwitchDefaults
import kotlinx.coroutines.delay
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import androidx.room.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.Crossfade
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.Star
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.ShoppingCart
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Settings
import androidx.compose.ui.zIndex
import androidx.compose.ui.draw.shadow
import kotlin.math.max
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.automirrored.filled.Undo
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Rect
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.ui.theme.MyApplicationTheme
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.asSharedFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update

import androidx.compose.ui.viewinterop.AndroidView
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.compositionLocalOf
import android.app.Activity
import com.google.android.gms.ads.AdError
import com.google.android.gms.ads.AdRequest
import com.google.android.gms.ads.AdSize
import com.google.android.gms.ads.AdView
import com.google.android.gms.ads.FullScreenContentCallback
import com.google.android.gms.ads.LoadAdError
import com.google.android.gms.ads.MobileAds
import com.google.android.gms.ads.interstitial.InterstitialAd
import com.google.android.gms.ads.interstitial.InterstitialAdLoadCallback
import com.google.android.gms.ads.rewarded.RewardedAd
import com.google.android.gms.ads.rewarded.RewardedAdLoadCallback

class AdManager(private val context: Context) {
    var rewardedAd: RewardedAd? = null
    var interstitialAd: InterstitialAd? = null

    init {
        loadRewardedAd()
        loadInterstitialAd()
    }

    fun loadRewardedAd() {
        val adRequest = AdRequest.Builder().build()
        RewardedAd.load(context, "ca-app-pub-2587866419282101/3154625375", adRequest, object : RewardedAdLoadCallback() {
            override fun onAdFailedToLoad(adError: LoadAdError) {
                rewardedAd = null
            }
            override fun onAdLoaded(ad: RewardedAd) {
                rewardedAd = ad
            }
        })
    }

    fun loadInterstitialAd() {
        val adRequest = AdRequest.Builder().build()
        InterstitialAd.load(context, "ca-app-pub-2587866419282101/8217098999", adRequest, object : InterstitialAdLoadCallback() {
            override fun onAdFailedToLoad(adError: LoadAdError) {
                interstitialAd = null
            }
            override fun onAdLoaded(ad: InterstitialAd) {
                interstitialAd = ad
            }
        })
    }

    fun showRewardedAd(activity: Activity, onRewarded: () -> Unit) {
        if (rewardedAd != null) {
            rewardedAd?.fullScreenContentCallback = object: FullScreenContentCallback() {
                override fun onAdDismissedFullScreenContent() {
                    rewardedAd = null
                    loadRewardedAd()
                }
                override fun onAdFailedToShowFullScreenContent(e: AdError) {
                    rewardedAd = null
                    onRewarded()
                }
            }
            rewardedAd?.show(activity) { _ ->
                onRewarded()
            }
        } else {
            onRewarded()
            loadRewardedAd()
        }
    }

    fun showInterstitialAd(activity: Activity, adsRemoved: Boolean, onClosed: () -> Unit) {
        if (adsRemoved) {
            onClosed()
            return
        }
        if (interstitialAd != null) {
            interstitialAd?.fullScreenContentCallback = object: FullScreenContentCallback() {
                override fun onAdDismissedFullScreenContent() {
                    interstitialAd = null
                    loadInterstitialAd()
                    onClosed()
                }
                override fun onAdFailedToShowFullScreenContent(e: AdError) {
                    interstitialAd = null
                    onClosed()
                }
            }
            interstitialAd?.show(activity)
        } else {
            onClosed()
            loadInterstitialAd()
        }
    }
}

val LocalAdManager = compositionLocalOf<AdManager> { error("No AdManager provided") }
val LocalBillingManager = compositionLocalOf<BillingManager> { error("No BillingManager provided") }

@Composable
fun AdmobBanner(adsRemoved: Boolean) {
    if (adsRemoved) return
    Box(
        modifier = Modifier.fillMaxWidth().background(Color.Black),
        contentAlignment = Alignment.Center
    ) {
        AndroidView(
            modifier = Modifier.fillMaxWidth(),
            factory = { context ->
                AdView(context).apply {
                    adUnitId = "ca-app-pub-2587866419282101/4852569054"
                    setAdSize(AdSize.BANNER)
                    try {
                        loadAd(AdRequest.Builder().build())
                    } catch (e: Exception) {
                        e.printStackTrace()
                    }
                }
            }
        )
    }
}

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        try {
            MobileAds.initialize(this) {}
        } catch (e: Exception) {
            e.printStackTrace()
        }
        val adManager = try { AdManager(this) } catch (e: Exception) { null }
        val billingManager = try { BillingManager(this) } catch (e: Exception) { null }
        enableEdgeToEdge()
        setContent {
            MyApplicationTheme {
                CompositionLocalProvider(
                    LocalAdManager provides (adManager ?: AdManager(this)), // fallback just for typing, though usually won't crash
                    LocalBillingManager provides (billingManager ?: BillingManager(this))
                ) {
                    Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                        AppNavHost(
                            modifier = Modifier.padding(innerPadding)
                        )
                    }
                }
            }
        }
    }
}

val GameColors = listOf(
    Color(0xFFE6194B), // Red
    Color(0xFF3CB44B), // Green
    Color(0xFFFFE119), // Yellow
    Color(0xFF4363D8), // Blue
    Color(0xFFF58231), // Orange
    Color(0xFF911EB4), // Purple
    Color(0xFF42D4F4), // Cyan
    Color(0xFFF032E6), // Magenta
    Color(0xFFBFEF45), // Lime
    Color(0xFF9A6324), // Brown
    Color(0xFF000000)  // Black
)

data class Ball(val id: String, val color: Color)
data class Tube(val id: Int, val balls: List<Ball> = emptyList(), val maxCapacity: Int = 4)
data class MoveAction(val fromTube: Int, val toTube: Int)

data class GameState(
    val tubes: List<Tube> = emptyList(),
    val selectedTubeIndex: Int? = null,
    val moveCount: Int = 0,
    val maxMoves: Int = 0,
    val isWon: Boolean = false,
    val isLost: Boolean = false,
    val undoStack: List<MoveAction> = emptyList(),
    val level: Int = 1
) {
    val movesLeft: Int get() = kotlin.math.max(0, maxMoves - moveCount)
}

enum class Screen { HOME, GAME, SHOP, SETTINGS }
enum class PowerUpType { NONE, UNDO, ADD_TUBE }

data class AppState(
    val screen: Screen = Screen.HOME,
    val coins: Int = 0,
    val lives: Int = 5,
    val highestUnlockedLevel: Int = 1,
    val soundEnabled: Boolean = true,
    val hapticEnabled: Boolean = true,
    val lastClaimedDate: String = "",
    val showDailyBonusDialog: Boolean = false,
    val unlockedThemes: List<String> = listOf("CLASSIC"),
    val activeTheme: String = "CLASSIC",
    val nextLifeTime: Long = 0L,
    val adsRemoved: Boolean = false
)

enum class SoundEvent {
    SELECT, MOVE, WIN, ERROR
}

class SoundManager(context: Context) {
    private val soundPool: SoundPool
    private var selectSoundId: Int = 0
    private var moveSoundId: Int = 0
    private var winSoundId: Int = 0

    init {
        val audioAttributes = AudioAttributes.Builder()
            .setUsage(AudioAttributes.USAGE_GAME)
            .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
            .build()
        soundPool = SoundPool.Builder()
            .setMaxStreams(3)
            .setAudioAttributes(audioAttributes)
            .build()
            
        try {
            selectSoundId = soundPool.load(context, R.raw.select, 1)
            moveSoundId = soundPool.load(context, R.raw.move, 1)
            winSoundId = soundPool.load(context, R.raw.win, 1)
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    fun playSelect() {
        if (selectSoundId != 0) soundPool.play(selectSoundId, 1f, 1f, 0, 0, 1f)
    }

    fun playMove() {
        if (moveSoundId != 0) soundPool.play(moveSoundId, 1f, 1f, 0, 0, 1f)
    }

    fun playWin() {
        if (winSoundId != 0) soundPool.play(winSoundId, 1f, 1f, 0, 0, 1f)
    }

    fun release() {
        soundPool.release()
    }
}


@Entity(tableName = "app_state")
data class AppStateEntity(
    @PrimaryKey val id: Int = 1,
    val coins: Int,
    val lives: Int,
    val highestUnlockedLevel: Int,
    val soundEnabled: Boolean,
    val hapticEnabled: Boolean,
    val lastClaimedDate: String,
    val unlockedThemes: String,
    val activeTheme: String,
    val nextLifeTime: Long = 0L,
    val adsRemoved: Boolean = false
)

@Dao
interface AppStateDao {
    @Query("SELECT * FROM app_state WHERE id = 1")
    suspend fun getAppStateOnce(): AppStateEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun saveAppState(appState: AppStateEntity)
}

@Database(entities = [AppStateEntity::class], version = 4, exportSchema = false)
abstract class AppDatabase : RoomDatabase() {
    abstract fun appStateDao(): AppStateDao
}

class BallSortViewModel(application: Application) : AndroidViewModel(application) {
    private val _uiState = MutableStateFlow(GameState())
    val uiState: StateFlow<GameState> = _uiState.asStateFlow()

    private val _appState = MutableStateFlow(AppState())
    val appState: StateFlow<AppState> = _appState.asStateFlow()

    private val _soundEvents = MutableSharedFlow<SoundEvent>(extraBufferCapacity = 10)
    val soundEvents = _soundEvents.asSharedFlow()


    private val db = Room.databaseBuilder(
        application,
        AppDatabase::class.java, "ballsort-database"
    ).fallbackToDestructiveMigration().build()
    private val appStateDao = db.appStateDao()
    
    init {
        viewModelScope.launch(Dispatchers.IO) {
            val entity = appStateDao.getAppStateOnce()
            if (entity != null) {
                _appState.update { 
                    it.copy(
                        coins = entity.coins,
                        lives = entity.lives,
                        highestUnlockedLevel = entity.highestUnlockedLevel,
                        soundEnabled = entity.soundEnabled,
                        hapticEnabled = entity.hapticEnabled,
                        lastClaimedDate = entity.lastClaimedDate,
                        unlockedThemes = entity.unlockedThemes.split(",").filter { it.isNotBlank() },
                        activeTheme = entity.activeTheme,
                        nextLifeTime = entity.nextLifeTime,
                        adsRemoved = entity.adsRemoved
                    )
                }
            }
            
            withContext(Dispatchers.Main) {
                checkDailyBonus()
                startLevel(_appState.value.highestUnlockedLevel, changeScreen = false)
            }
            
            kotlinx.coroutines.GlobalScope.launch(Dispatchers.Main) {
                while (true) {
                    checkLifeRegen()
                    kotlinx.coroutines.delay(1000)
                }
            }
            
            _appState.collect { state ->
                appStateDao.saveAppState(
                    AppStateEntity(
                        coins = state.coins,
                        lives = state.lives,
                        highestUnlockedLevel = state.highestUnlockedLevel,
                        soundEnabled = state.soundEnabled,
                        hapticEnabled = state.hapticEnabled,
                        lastClaimedDate = state.lastClaimedDate,
                        unlockedThemes = state.unlockedThemes.joinToString(","),
                        activeTheme = state.activeTheme,
                        nextLifeTime = state.nextLifeTime,
                        adsRemoved = state.adsRemoved
                    )
                )
            }
        }
    }

    private fun checkLifeRegen() {
        val now = System.currentTimeMillis()
        val state = _appState.value
        if (state.lives < 5 && state.nextLifeTime > 0 && now >= state.nextLifeTime) {
            val timePassed = now - state.nextLifeTime
            val livesGained = 1 + (timePassed / (30 * 60 * 1000L)).toInt()
            val finalLives = (state.lives + livesGained).coerceAtMost(5)
            
            val newNextLifeTime = if (finalLives < 5) {
                state.nextLifeTime + livesGained * 30 * 60 * 1000L
            } else {
                0L
            }
            
            _appState.update { it.copy(lives = finalLives, nextLifeTime = newNextLifeTime) }
        } else if (state.lives < 5 && state.nextLifeTime == 0L) {
            // Fallback just in case
            _appState.update { it.copy(nextLifeTime = now + 30 * 60 * 1000L) }
        }
    }
    
    private fun consumeLife() {
        val state = _appState.value
        if (state.lives <= 0) return
        val now = System.currentTimeMillis()
        val newNextLifeTime = if (state.lives == 5 || state.nextLifeTime == 0L) now + 30 * 60 * 1000L else state.nextLifeTime
        _appState.update { it.copy(lives = state.lives - 1, nextLifeTime = newNextLifeTime) }
    }

    private fun checkDailyBonus() {
        val today = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(Date())
        if (_appState.value.lastClaimedDate != today) {
            _appState.update { it.copy(showDailyBonusDialog = true) }
        }
    }

    fun claimDailyBonus() {
        val today = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(Date())
        _appState.update { 
            it.copy(
                coins = it.coins + 50,
                lastClaimedDate = today,
                showDailyBonusDialog = false
            )
        }
    }
    
    fun dismissDailyBonus() {
        // Option to just hide without claiming, but claiming is automatic upon click usually.
        _appState.update { it.copy(showDailyBonusDialog = false) }
    }

    fun startLevel(level: Int, changeScreen: Boolean = true) {
        if (_appState.value.lives <= 0 && changeScreen) return
        if (changeScreen) {
            _appState.update { it.copy(screen = Screen.GAME) }
        }
        
        val isHardLevel = level % 5 == 0
        val baseColors = 2 + (level / 3) + if (isHardLevel) 1 else 0
        val numColors = kotlin.math.max(3, baseColors).coerceAtMost(GameColors.size)
        
        val colorsToUse = GameColors.shuffled().take(numColors)

        val tubes = mutableListOf<Tube>()
        var ballIdCounter = 0
        for (i in 0 until numColors) {
            val balls = List(4) { Ball(id = "ball_${ballIdCounter++}", color = colorsToUse[i]) }
            tubes.add(Tube(id = i, balls = balls))
        }
        tubes.add(Tube(id = numColors, balls = emptyList()))
        tubes.add(Tube(id = numColors + 1, balls = emptyList()))

        var currentTubes = tubes.toList()
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
        )
    }

    private fun isOneValidMove(stateA: List<Tube>, stateB: List<Tube>): Boolean {
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

    fun selectTube(index: Int) {
        val state = _uiState.value
        if (state.isWon || state.isLost) return

        val selected = state.selectedTubeIndex
        if (selected == null) {
            if (state.tubes[index].balls.isNotEmpty()) {
                _soundEvents.tryEmit(SoundEvent.SELECT)
                _uiState.update { it.copy(selectedTubeIndex = index) }
            }
        } else {
            if (selected == index) {
                _uiState.update { it.copy(selectedTubeIndex = null) }
            } else {
                val sourceTube = state.tubes[selected]
                val destTube = state.tubes[index]

                if (canMove(sourceTube, destTube)) {
                    val newTubes = state.tubes.toMutableList()
                    val sBalls = sourceTube.balls.toMutableList()
                    val dBalls = destTube.balls.toMutableList()

                    val ball = sBalls.removeAt(sBalls.lastIndex)
                    dBalls.add(ball)

                    newTubes[selected] = sourceTube.copy(balls = sBalls)
                    newTubes[index] = destTube.copy(balls = dBalls)

                    val moveAction = MoveAction(selected, index)
                    
                    _soundEvents.tryEmit(SoundEvent.MOVE)

                    _uiState.update {
                        it.copy(
                            tubes = newTubes,
                            selectedTubeIndex = null,
                            moveCount = it.moveCount + 1,
                            undoStack = it.undoStack + moveAction
                        )
                    }
                    checkWinCondition()
                } else {
                    _soundEvents.tryEmit(SoundEvent.ERROR)
                }
            }
        }
    }

    private fun canMove(source: Tube, dest: Tube): Boolean {
        if (source.balls.isEmpty()) return false
        if (dest.balls.size >= dest.maxCapacity) return false
        if (dest.balls.isEmpty()) return true
        return source.balls.last().color == dest.balls.last().color
    }

    private fun checkWinCondition() {
        val state = _uiState.value
        val won = state.tubes.all { tube ->
            tube.balls.isEmpty() || (tube.balls.size == tube.maxCapacity && tube.balls.all { it.color == tube.balls.first().color })
        }
        if (won && !state.isWon) {
            _soundEvents.tryEmit(SoundEvent.WIN)
            _uiState.update { it.copy(isWon = true, selectedTubeIndex = null) }
            _appState.update {
                it.copy(
                    coins = it.coins + 50,
                    highestUnlockedLevel = max(it.highestUnlockedLevel, state.level + 1)
                )
            }
        } else if (!won && state.moveCount >= state.maxMoves && !state.isLost) {
            consumeLife()
            _uiState.update { it.copy(isLost = true, selectedTubeIndex = null) }
        }
    }

    fun undo() {
        val state = _uiState.value
        if (state.undoStack.isEmpty() || state.isWon) return

        val lastMove = state.undoStack.last()
        val newTubes = state.tubes.toMutableList()

        val sBalls = newTubes[lastMove.toTube].balls.toMutableList()
        val dBalls = newTubes[lastMove.fromTube].balls.toMutableList()

        val ball = sBalls.removeAt(sBalls.lastIndex)
        dBalls.add(ball)

        newTubes[lastMove.toTube] = newTubes[lastMove.toTube].copy(balls = sBalls)
        newTubes[lastMove.fromTube] = newTubes[lastMove.fromTube].copy(balls = dBalls)
        
        _soundEvents.tryEmit(SoundEvent.MOVE)

        _uiState.update {
            it.copy(
                tubes = newTubes,
                moveCount = kotlin.math.max(0, it.moveCount - 1),
                undoStack = it.undoStack.dropLast(1),
                selectedTubeIndex = null,
                isLost = false
            )
        }
    }

    fun buyTheme(themeId: String, cost: Int) {
        if (_appState.value.coins >= cost && !_appState.value.unlockedThemes.contains(themeId)) {
            _appState.update { 
                it.copy(
                    coins = it.coins - cost,
                    unlockedThemes = it.unlockedThemes + themeId
                )
            }
        }
    }

    fun setTheme(themeId: String) {
        if (_appState.value.unlockedThemes.contains(themeId)) {
            _appState.update { it.copy(activeTheme = themeId) }
        }
    }
    
    fun addCoins(amount: Int) {
        _appState.update { it.copy(coins = it.coins + amount) }
    }
    
    fun removeAds() {
        _appState.update { it.copy(adsRemoved = true) }
    }

    fun spendCoins(amount: Int): Boolean {
        val currentCoins = _appState.value.coins
        if (currentCoins >= amount) {
            _appState.update { it.copy(coins = it.coins - amount) }
            return true
        }
        return false
    }

    fun addTube() {
        val state = _uiState.value
        if (state.isWon) return
        val newTubes = state.tubes.toMutableList()
        newTubes.add(Tube(id = newTubes.size, balls = emptyList()))
        _uiState.update { it.copy(tubes = newTubes) }
    }

    fun restartLevel() {
        if (_appState.value.lives <= 0) return
        consumeLife()
        val currentState = _uiState.value
        if (currentState.undoStack.isEmpty()) {
            _uiState.update { it.copy(isWon = false, selectedTubeIndex = null) }
            return
        }

        val newTubes = currentState.tubes.toMutableList()
        val undoStack = currentState.undoStack.reversed()

        for (move in undoStack) {
            val sBalls = newTubes[move.toTube].balls.toMutableList()
            val dBalls = newTubes[move.fromTube].balls.toMutableList()
            val ball = sBalls.removeAt(sBalls.lastIndex)
            dBalls.add(ball)
            newTubes[move.toTube] = newTubes[move.toTube].copy(balls = sBalls)
            newTubes[move.fromTube] = newTubes[move.fromTube].copy(balls = dBalls)
        }

        _uiState.update {
            it.copy(
                tubes = newTubes,
                moveCount = 0,
                undoStack = emptyList(),
                isWon = false,
                selectedTubeIndex = null
            )
        }
    }

    fun nextLevel() {
        startLevel(_appState.value.highestUnlockedLevel)
    }

    fun goHome() {
        val state = _uiState.value
        if (!state.isWon && state.moveCount > 0) {
            if (_appState.value.lives > 0) {
                consumeLife()
            }
        }
        _appState.update { it.copy(screen = Screen.HOME) }
    }

    fun navigate(screen: Screen) {
        _appState.update { it.copy(screen = screen) }
    }
    
    fun toggleSound() { _appState.update { it.copy(soundEnabled = !it.soundEnabled) } }
    fun toggleHaptics() { _appState.update { it.copy(hapticEnabled = !it.hapticEnabled) } }
}

@Composable
fun RowScope.StatBox(label: String, value: String, valueColor: Color = Color(0xFF1E293B)) {
    Box(
        modifier = Modifier
            .weight(1f)
            .background(Color.White.copy(alpha = 0.5f), RoundedCornerShape(12.dp))
            .border(1.dp, Color.White.copy(alpha = 0.8f), RoundedCornerShape(12.dp))
            .padding(8.dp)
    ) {
        Column {
            Text(label, fontSize = 8.sp, color = Color(0xFF1E293B).copy(alpha = 0.8f), fontWeight = FontWeight.ExtraBold, letterSpacing = 1.sp)
            Text(value, fontSize = 16.sp, color = valueColor, fontWeight = FontWeight.ExtraBold)
        }
    }
}

@Composable
fun MarbleSortScreen(
    modifier: Modifier = Modifier,
    viewModel: BallSortViewModel = viewModel()
) {
    val state by viewModel.uiState.collectAsState()
    val context = LocalContext.current
    val soundManager = remember { SoundManager(context) }
    
    DisposableEffect(Unit) {
        onDispose { soundManager.release() }
    }
    
    val view = androidx.compose.ui.platform.LocalView.current
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
    }
    
    var showPowerUpDialog by remember { mutableStateOf(PowerUpType.NONE) }
    var showGiveUpDialog by remember { mutableStateOf(false) }
    val adManager = LocalAdManager.current
    val activity = androidx.activity.compose.LocalActivity.current ?: LocalContext.current as Activity
    val appState by viewModel.appState.collectAsState()

    if (showPowerUpDialog != PowerUpType.NONE) {
        val isUndo = showPowerUpDialog == PowerUpType.UNDO
        val title = if (isUndo) "Undo Move" else "Add Extra Tube"
        val desc = if (isUndo) "Reverse your last move!" else "Add an empty tube to help you sort!"
        AlertDialog(
            onDismissRequest = { showPowerUpDialog = PowerUpType.NONE },
            containerColor = Color.White,
            titleContentColor = Color(0xFF1E293B),
            textContentColor = Color(0xFF1E293B),
            title = { Text(title, fontWeight = FontWeight.ExtraBold) },
            text = { Text("$desc\n\nCost: 1000 Coins or Watch an Ad", fontWeight = FontWeight.Medium) },
            confirmButton = {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(
                        onClick = {
                            if (viewModel.spendCoins(1000)) {
                                showPowerUpDialog = PowerUpType.NONE
                                if (isUndo) viewModel.undo() else viewModel.addTube()
                            }
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFF59E0B)),
                        enabled = appState.coins >= 1000
                    ) {
                        Text("1000 Coins", color = Color.Black, fontWeight = FontWeight.Bold)
                    }
                    Button(
                        onClick = {
                            showPowerUpDialog = PowerUpType.NONE
                            adManager.showRewardedAd(activity) {
                                if (isUndo) viewModel.undo() else viewModel.addTube()
                            }
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2563EB))
                    ) {
                        Text("Watch Ad", color = Color.White, fontWeight = FontWeight.Bold)
                    }
                }
            },
            dismissButton = {
                TextButton(onClick = { showPowerUpDialog = PowerUpType.NONE }) { Text("Cancel", color = Color(0xFF475569), fontWeight = FontWeight.Bold) }
            }
        )
    }

    if (showGiveUpDialog) {
        AlertDialog(
            onDismissRequest = { showGiveUpDialog = false },
            containerColor = Color.White,
            titleContentColor = Color(0xFFB91C1C), // Red 700
            textContentColor = Color(0xFF1E293B), // Slate 800
            title = { Text("Are you stuck?", fontWeight = FontWeight.ExtraBold) },
            text = { Text("Give up and lose a life to restart, or watch an ad to reverse your last move for free!", fontWeight = FontWeight.Medium) },
            confirmButton = {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(
                        onClick = {
                            showGiveUpDialog = false
                            viewModel.restartLevel()
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFDC2626)) // Red 600
                    ) {
                        Text("Give Up", color = Color.White, fontWeight = FontWeight.Bold)
                    }
                    Button(
                        onClick = {
                            showGiveUpDialog = false
                            adManager.showRewardedAd(activity) {
                                viewModel.undo()
                            }
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2563EB)) // Blue 600
                    ) {
                        Text("Watch Ad (Undo)", color = Color.White, fontWeight = FontWeight.Bold)
                    }
                }
            },
            dismissButton = {
                TextButton(onClick = { showGiveUpDialog = false }) { 
                    Text("Cancel", color = Color(0xFF475569), fontWeight = FontWeight.Bold) 
                }
            }
        )
    }

    Box(
        modifier = modifier
            .fillMaxSize()
            .background(
                brush = Brush.linearGradient(
                    colors = listOf(
                        Color(0xFFFCD5CE), // Soft peach
                        Color(0xFFD8E2DC), // Light grey/green
                        Color(0xFFB5E4CB)  // Soft mint/cyan
                    ),
                    start = Offset(0f, 0f),
                    end = Offset.Infinite
                )
            )
    ) {

        Column(
            modifier = Modifier.fillMaxSize()
        ) {
            // Header
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 16.dp, start = 16.dp, end = 16.dp, bottom = 8.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    IconButton(
                        onClick = { viewModel.goHome() },
                        modifier = Modifier
                            .size(40.dp)
                            .shadow(4.dp, RoundedCornerShape(10.dp), spotColor = Color(0xFF6B8CE0))
                            .background(Color(0xFF82A6F1), RoundedCornerShape(10.dp))
                    ) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Home", tint = Color(0xFF1E293B), modifier = Modifier.size(20.dp))
                    }
                    Text(
                        text = "Level ${state.level}",
                        color = Color(0xFF172554),
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.ExtraBold
                    )
                }
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
                    var timerText by remember { mutableStateOf(if (appState.lives >= 5) "MAX" else "") }
                    
                    LaunchedEffect(appState.lives, appState.nextLifeTime) {
                        if (appState.lives >= 5) {
                            timerText = "MAX"
                        } else {
                            while (true) {
                                val remaining = appState.nextLifeTime - System.currentTimeMillis()
                                if (remaining > 0) {
                                    val mins = (remaining / 60000).toInt()
                                    val secs = ((remaining % 60000) / 1000).toInt()
                                    timerText = String.format(Locale.getDefault(), "%02d:%02d", mins, secs)
                                } else {
                                    timerText = "00:00"
                                }
                                kotlinx.coroutines.delay(1000)
                            }
                        }
                    }
                    StatPill(icon = Icons.Default.Favorite, tint = Color(0xFFEF4444), text = "${appState.lives}", label = timerText)
                    StatPill(icon = Icons.Default.Star, tint = Color(0xFFFBBF24), text = "${appState.coins}", label = "")
                }
            }

            // Stats
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                StatBox(label = "MOVES", value = state.moveCount.toString().padStart(3, '0'))
                StatBox(label = "MOVES LEFT", value = state.movesLeft.toString().padStart(3, '0'))
            }

            Spacer(modifier = Modifier.height(8.dp))

            // Grid
            TubeGrid(
                modifier = Modifier.weight(1f),
                tubes = state.tubes,
                selectedTubeIndex = state.selectedTubeIndex,
                activeTheme = appState.activeTheme,
                onTubeSelect = { viewModel.selectTube(it) }
            )
            
            Spacer(modifier = Modifier.height(16.dp))

            // Footer - Power Ups
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 24.dp, vertical = 16.dp)
                    .padding(bottom = 90.dp), // Padding to keep above banner ad and nav bar
                horizontalArrangement = Arrangement.SpaceEvenly,
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Add Tube Power Up
                IconButton(
                    onClick = { showPowerUpDialog = PowerUpType.ADD_TUBE },
                    modifier = Modifier
                        .size(84.dp)
                        .shadow(6.dp, RoundedCornerShape(24.dp), spotColor = Color(0xFF76DB9E))
                        .background(if (!state.isWon && !state.isLost) Color(0xFF90E4AD) else Color.White.copy(alpha = 0.5f), RoundedCornerShape(24.dp)),
                    enabled = !state.isWon && !state.isLost
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.Center) {
                        Icon(Icons.Default.Add, contentDescription = "Add Tube", tint = if (!state.isWon && !state.isLost) Color(0xFF1E293B) else Color(0xFF1E293B).copy(alpha = 0.5f), modifier = Modifier.size(32.dp))
                        Spacer(modifier = Modifier.height(2.dp))
                        Text("Tube", color = if (!state.isWon && !state.isLost) Color(0xFF1E293B) else Color(0xFF1E293B).copy(alpha = 0.5f), fontSize = 14.sp, fontWeight = FontWeight.ExtraBold)
                    }
                }
                
                // Undo Power Up
                val isUndoEnabled = state.undoStack.isNotEmpty() && !state.isWon && !state.isLost
                IconButton(
                    onClick = { showPowerUpDialog = PowerUpType.UNDO },
                    modifier = Modifier
                        .size(84.dp)
                        .shadow(6.dp, RoundedCornerShape(24.dp), spotColor = Color(0xFF6B8CE0))
                        .background(if (isUndoEnabled) Color(0xFF82A6F1) else Color.White.copy(alpha = 0.5f), RoundedCornerShape(24.dp)),
                    enabled = isUndoEnabled
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.Center) {
                        Icon(Icons.AutoMirrored.Filled.Undo, contentDescription = "Undo", tint = if (isUndoEnabled) Color(0xFF1E293B) else Color(0xFF1E293B).copy(alpha = 0.5f), modifier = Modifier.size(32.dp))
                        Spacer(modifier = Modifier.height(2.dp))
                        Text("Undo", color = if (isUndoEnabled) Color(0xFF1E293B) else Color(0xFF1E293B).copy(alpha = 0.5f), fontSize = 14.sp, fontWeight = FontWeight.ExtraBold)
                    }
                }
                
                // Restart / Give Up
                IconButton(
                    onClick = { showGiveUpDialog = true },
                    modifier = Modifier
                        .size(84.dp)
                        .shadow(6.dp, RoundedCornerShape(24.dp), spotColor = Color(0xFFE59C69))
                        .background(Color(0xFFFCB682), RoundedCornerShape(24.dp))
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.Center) {
                        Icon(Icons.Default.Refresh, contentDescription = "Restart", tint = Color(0xFF1E293B), modifier = Modifier.size(32.dp))
                        Spacer(modifier = Modifier.height(2.dp))
                        Text("Restart", color = Color(0xFF1E293B), fontSize = 14.sp, fontWeight = FontWeight.ExtraBold)
                    }
                }
            }
            
            // Bottom Indicator line
            Box(modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp), contentAlignment = Alignment.Center) {
                Box(modifier = Modifier.width(128.dp).height(4.dp).background(Color.White.copy(alpha = 0.2f), RoundedCornerShape(50)))
            }
        }

        // Win Overlay
        // Game Banner Ad
        Box(
            modifier = Modifier.align(Alignment.BottomCenter).fillMaxWidth()
        ) {
            AdmobBanner(appState.adsRemoved)
        }

        // Win Overlay
        if (state.isWon) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(Color.Black.copy(alpha = 0.7f)),
                contentAlignment = Alignment.Center
            ) {
                Card(
                    shape = RoundedCornerShape(24.dp),
                    colors = CardDefaults.cardColors(containerColor = Color(0xFF1E1E1E))
                ) {
                    Column(
                        modifier = Modifier.padding(32.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Text(
                            text = "Level Complete!",
                            style = MaterialTheme.typography.headlineLarge,
                            color = Color(0xFFFFB300),
                            fontWeight = FontWeight.Bold
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        Text(
                            text = "Moves: ${state.moveCount}",
                            style = MaterialTheme.typography.bodyLarge,
                            color = Color.White
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            Icon(Icons.Default.Star, contentDescription = "Coins", tint = Color(0xFFFBBF24), modifier = Modifier.size(24.dp))
                            Text(
                                text = "+50",
                                style = MaterialTheme.typography.titleLarge,
                                color = Color(0xFFFBBF24),
                                fontWeight = FontWeight.Bold
                            )
                        }
                        Spacer(modifier = Modifier.height(24.dp))
                        Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                            Button(
                                onClick = { viewModel.goHome() },
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF374151))
                            ) {
                                Text("Home", fontSize = 18.sp, modifier = Modifier.padding(8.dp))
                            }
                            val adManager = LocalAdManager.current
                            val activity = androidx.activity.compose.LocalActivity.current ?: LocalContext.current as Activity
                            Button(
                                onClick = {
                                    val levelsCompleted = viewModel.appState.value.highestUnlockedLevel - 1
                                    if (levelsCompleted % 2 == 0) {
                                        adManager.showInterstitialAd(activity, appState.adsRemoved) {
                                            viewModel.nextLevel()
                                        }
                                    } else {
                                        viewModel.nextLevel()
                                    }
                                },
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF43A047))
                            ) {
                                Text("Next", fontSize = 18.sp, modifier = Modifier.padding(8.dp))
                            }
                        }
                    }
                }
            }
        }
        if (state.isLost && !state.isWon) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(Color.Black.copy(alpha = 0.7f)),
                contentAlignment = Alignment.Center
            ) {
                Card(
                    shape = RoundedCornerShape(24.dp),
                    colors = CardDefaults.cardColors(containerColor = Color(0xFF1E1E1E))
                ) {
                    Column(
                        modifier = Modifier.padding(32.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Text(
                            text = "Out of Moves!",
                            style = MaterialTheme.typography.headlineLarge,
                            color = Color(0xFFEF4444),
                            fontWeight = FontWeight.Bold
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        Text(
                            text = "You lost a life.",
                            style = MaterialTheme.typography.bodyLarge,
                            color = Color.White
                        )
                        Spacer(modifier = Modifier.height(24.dp))
                        Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                            Button(
                                onClick = { viewModel.goHome() },
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF374151))
                            ) {
                                Text("Home", fontSize = 18.sp, modifier = Modifier.padding(8.dp))
                            }
                            val adManager = LocalAdManager.current
                            val activity = androidx.activity.compose.LocalActivity.current ?: LocalContext.current as Activity
                            Button(
                                onClick = {
                                    adManager.showRewardedAd(activity) {
                                        viewModel.undo()
                                    }
                                },
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF82A6F1))
                            ) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(Icons.AutoMirrored.Filled.Undo, contentDescription = null, tint = Color.White)
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Text("Undo (Ad)", fontSize = 16.sp, modifier = Modifier.padding(vertical = 8.dp))
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun TubeGrid(
    modifier: Modifier = Modifier,
    tubes: List<Tube>,
    selectedTubeIndex: Int?,
    activeTheme: String,
    onTubeSelect: (Int) -> Unit
) {
    BoxWithConstraints(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp),
        contentAlignment = Alignment.Center
    ) {
        val screenWidth = maxWidth.value
        val screenHeight = maxHeight.value
        
        // Dynamically compute columns based on screen width. 
        val columns = maxOf(4, (screenWidth / 75).toInt()).coerceAtMost(8)
        val chunks = tubes.chunked(columns)
        
        // Calculate required rows
        val rows = chunks.size
        
        // Base dimensions for a tube + vertical spacing
        val baseTubeHeight = 176f + 48f // Tube height + spacing
        
        // We calculate a width-based scale and a height-based scale, and pick the smaller one to fit!
        val widthScale = (screenWidth / 360f)
        val heightScale = if (rows > 0) (screenHeight / (baseTubeHeight * rows)) * 0.95f else 1f
        
        // Final scale factor ensures it fits vertically and horizontally
        val scaleFactor = minOf(widthScale, heightScale).coerceIn(0.4f, 2.0f)
        
        val tubeWidth = (48 * scaleFactor).dp
        val tubeHeight = (176 * scaleFactor).dp
        val ballSize = (36 * scaleFactor).dp
        val ballSpacing = (38 * scaleFactor).dp
        val liftOffset = (48 * scaleFactor).dp
        val bottomPadding = (6 * scaleFactor).dp
        
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy((48 * scaleFactor).dp)
        ) {
            for (chunk in chunks) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceEvenly
                ) {
                    for (tube in chunk) {
                        val index = tubes.indexOf(tube)
                        TubeView(
                            tube = tube,
                            isSelected = selectedTubeIndex == index,
                            activeTheme = activeTheme,
                            tubeWidth = tubeWidth,
                            tubeHeight = tubeHeight,
                            ballSize = ballSize,
                            ballSpacing = ballSpacing,
                            liftOffset = liftOffset,
                            bottomPadding = bottomPadding,
                            onTubeClick = { onTubeSelect(index) }
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun TubeView(
    tube: Tube,
    isSelected: Boolean,
    activeTheme: String,
    tubeWidth: androidx.compose.ui.unit.Dp = 48.dp,
    tubeHeight: androidx.compose.ui.unit.Dp = 176.dp,
    ballSize: androidx.compose.ui.unit.Dp = 36.dp,
    ballSpacing: androidx.compose.ui.unit.Dp = 38.dp,
    liftOffset: androidx.compose.ui.unit.Dp = 48.dp,
    bottomPadding: androidx.compose.ui.unit.Dp = 6.dp,
    onTubeClick: () -> Unit
) {
    val borderColor = if (isSelected) Color.White.copy(alpha = 0.4f) else Color.White.copy(alpha = 0.2f)
    val ringColor = if (isSelected) Color(0xFF6366F1).copy(alpha = 0.3f) else Color.Transparent
    
    val totalHeight = tubeHeight + liftOffset

    Box(
        contentAlignment = Alignment.BottomCenter,
        modifier = Modifier
            .width(tubeWidth)
            .height(totalHeight)
            .clickable(
                interactionSource = remember { MutableInteractionSource() },
                indication = null,
                onClick = onTubeClick
            )
    ) {
        // Tube Container (Glass effect)
        Box(
            modifier = Modifier
                .width(tubeWidth)
                .height(tubeHeight)
                .align(Alignment.BottomCenter)
                .background(
                    brush = Brush.horizontalGradient(
                        colors = listOf(
                            Color.White.copy(alpha = 0.1f),
                            Color.White.copy(alpha = 0.3f),
                            Color.White.copy(alpha = 0.1f)
                        )
                    ),
                    shape = RoundedCornerShape(bottomStart = tubeWidth / 2, bottomEnd = tubeWidth / 2)
                )
                .border(
                    width = (3 * (tubeWidth.value / 48f)).dp,
                    color = Color.White.copy(alpha = 0.5f),
                    shape = RoundedCornerShape(bottomStart = tubeWidth / 2, bottomEnd = tubeWidth / 2)
                )
                .border(
                    width = if (isSelected) (4 * (tubeWidth.value / 48f)).dp else 0.dp,
                    color = ringColor,
                    shape = RoundedCornerShape(bottomStart = tubeWidth / 2, bottomEnd = tubeWidth / 2)
                )
        ) {
            // Inner shadow / rim highlight
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .border(
                        width = (1 * (tubeWidth.value / 48f)).dp,
                        color = Color.Black.copy(alpha = 0.05f),
                        shape = RoundedCornerShape(bottomStart = tubeWidth / 2, bottomEnd = tubeWidth / 2)
                    )
            )
        }

        // Balls
        tube.balls.forEachIndexed { index, ball ->
            val isTop = index == tube.balls.size - 1
            val isLifting = isSelected && isTop
            val targetY = -(index * ballSpacing.value + bottomPadding.value).dp - if (isLifting) liftOffset else 0.dp
            val yOffset by animateDpAsState(
                targetValue = targetY,
                animationSpec = tween(durationMillis = 300),
                label = "ball_lift"
            )

            BallView(
                ball = ball,
                isSelectedLifting = isLifting,
                activeTheme = activeTheme,
                modifier = Modifier
                    .offset(y = yOffset)
                    .size(ballSize)
            )
        }
    }
}

@Composable
fun BallView(ball: Ball, isSelectedLifting: Boolean, activeTheme: String, modifier: Modifier = Modifier) {
    val isLiftingBorder = if (isSelectedLifting) Color.White.copy(alpha = 0.5f) else Color.Transparent
    Canvas(modifier = modifier) {
        val radius = size.width / 2f
        
        if (activeTheme == "NEON") {
            // Neon Theme
            drawCircle(color = Color.Black)
            drawCircle(
                color = ball.color,
                style = Stroke(width = 4.dp.toPx())
            )
            drawCircle(
                color = ball.color.copy(alpha = 0.5f),
                style = Stroke(width = 8.dp.toPx())
            )
        } else if (activeTheme == "PASTEL") {
            // Pastel Theme
            val pastelColor = ball.color.copy(alpha = 0.4f)
            drawCircle(color = pastelColor)
            drawCircle(
                color = Color.White.copy(alpha = 0.5f),
                radius = size.width * 0.2f,
                center = Offset(size.width * 0.3f, size.height * 0.3f)
            )
        } else {
            // CLASSIC / GLOSSY Theme
            
            // Base shadow
            drawCircle(
                color = Color.Black.copy(alpha = 0.15f),
                radius = radius,
                center = Offset(radius, radius + 2.dp.toPx())
            )

            // Base color with radial gradient
            val radial = Brush.radialGradient(
                colors = listOf(ball.color.copy(alpha = 0.5f), ball.color.copy(alpha = 0.95f), ball.color.copy(alpha = 0.7f)),
                center = Offset(radius, radius),
                radius = radius
            )
            drawCircle(brush = radial)
            
            // Rim light bottom
            val bottomRim = Brush.verticalGradient(
                colors = listOf(Color.Transparent, Color.White.copy(alpha = 0.6f)),
                startY = radius,
                endY = size.height
            )
            drawCircle(brush = bottomRim, style = Stroke(width = 1.dp.toPx()))

            // Specular highlight top
            drawCircle(
                color = Color.White.copy(alpha = 0.5f),
                radius = radius * 0.4f,
                center = Offset(radius * 0.6f, radius * 0.4f)
            )
            drawCircle(
                color = Color.White.copy(alpha = 0.8f),
                radius = radius * 0.1f,
                center = Offset(radius * 0.7f, radius * 0.3f)
            )
        }

        if (isSelectedLifting) {
            drawCircle(
                color = isLiftingBorder,
                style = Stroke(width = 2.dp.toPx())
            )
        }
    }
}

@Composable
fun AppNavHost(modifier: Modifier = Modifier, viewModel: BallSortViewModel = viewModel()) {
    val appState by viewModel.appState.collectAsState()
    val billingManager = LocalBillingManager.current
    val restoredPurchases by billingManager.restoredPurchases.collectAsState()
    
    LaunchedEffect(restoredPurchases) {
        if (restoredPurchases.contains("remove_ads") && !appState.adsRemoved) {
            viewModel.removeAds()
        }
    }

    Crossfade(targetState = appState.screen, modifier = modifier, label = "screen_transition") { screen ->
        when (screen) {
            Screen.GAME -> MarbleSortScreen(viewModel = viewModel)
            else -> MainTabScreen(viewModel = viewModel, screen = screen)
        }
    }
}

@Composable
fun StatPill(icon: androidx.compose.ui.graphics.vector.ImageVector, tint: Color, text: String, label: String, isLarge: Boolean = false) {
    Row(
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier
            .shadow(if (isLarge) 4.dp else 2.dp, CircleShape, spotColor = Color.Black.copy(alpha = 0.05f))
            .background(Color.White.copy(alpha = 0.35f), CircleShape)
            .border(1.dp, Color.White.copy(alpha = 0.6f), CircleShape)
            .padding(horizontal = if (isLarge) 16.dp else 8.dp, vertical = if (isLarge) 8.dp else 4.dp)
    ) {
        Icon(icon, contentDescription = null, tint = tint, modifier = Modifier.size(if (isLarge) 24.dp else 16.dp))
        Spacer(Modifier.width(if (isLarge) 8.dp else 6.dp))
        Text(text, color = Color(0xFF1E293B), fontWeight = FontWeight.ExtraBold, fontSize = if (isLarge) 18.sp else 14.sp)
        if (label.isNotEmpty()) {
            Spacer(Modifier.width(4.dp))
            Text(label, color = Color(0xFF64748B), fontSize = if (isLarge) 12.sp else 10.sp, fontWeight = FontWeight.Bold)
        }
    }
}

@Composable
fun LevelNode(level: Int, isCompleted: Boolean, isCurrent: Boolean, isLocked: Boolean, isHardLevel: Boolean = false) {
    val size = if (isCurrent) 90.dp else 70.dp
    val color = if (isCompleted) {
        Color(0xFF82A6F1) // completed - blue
    } else if (isCurrent) {
        Color(0xFF90E4AD) // current - green
    } else {
        Color.White.copy(alpha = 0.35f) // locked - glass
    }
    val contentColor = if (isLocked) Color(0xFF94A3B8) else Color.White

    Box(
        modifier = Modifier.height(140.dp).width(120.dp),
        contentAlignment = Alignment.Center
    ) {
        Box(modifier = Modifier.width(8.dp).fillMaxHeight().background(Color.White.copy(alpha = 0.4f)))

        Box(
            modifier = Modifier
                .size(size)
                .shadow(if (isCurrent) 8.dp else 4.dp, CircleShape, spotColor = if (isCurrent) Color(0xFF76DB9E) else Color.Black.copy(alpha = 0.05f))
                .background(color, CircleShape)
                .border(2.dp, Color.White.copy(alpha = 0.8f), CircleShape),
            contentAlignment = Alignment.Center
        ) {
            Text("$level", color = contentColor, fontSize = 28.sp, fontWeight = FontWeight.ExtraBold)
        }
    }
}

@Composable
fun TabItem(icon: androidx.compose.ui.graphics.vector.ImageVector, label: String, isSelected: Boolean, onClick: () -> Unit) {
    val color = if (isSelected) Color(0xFF1E293B) else Color(0xFF475569)
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier.clickable(onClick = onClick).padding(8.dp)
    ) {
        Icon(icon, contentDescription = label, tint = color, modifier = Modifier.size(28.dp))
        Spacer(Modifier.height(4.dp))
        Text(label, color = color, fontSize = 12.sp, fontWeight = FontWeight.ExtraBold)
    }
}

@Composable
fun MainTabScreen(viewModel: BallSortViewModel, screen: Screen) {
    val appState by viewModel.appState.collectAsState()
    
    if (appState.showDailyBonusDialog) {
        AlertDialog(
            onDismissRequest = { viewModel.dismissDailyBonus() },
            containerColor = Color.White,
            titleContentColor = Color(0xFF1E293B),
            textContentColor = Color(0xFF1E293B),
            title = { Text("Daily Bonus!", fontWeight = FontWeight.ExtraBold) },
            text = { Text("Welcome back! Here are your 50 daily coins.", fontWeight = FontWeight.Medium) },
            confirmButton = {
                Button(
                    onClick = { viewModel.claimDailyBonus() },
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFFBBF24))
                ) {
                    Text("Claim 50 Coins", color = Color.Black, fontWeight = FontWeight.Bold)
                }
            }
        )
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(
                brush = Brush.linearGradient(
                    colors = listOf(
                        Color(0xFFFCD5CE), // Soft peach
                        Color(0xFFD8E2DC), // Light grey/green
                        Color(0xFFB5E4CB)  // Soft mint/cyan
                    ),
                    start = Offset(0f, 0f),
                    end = Offset.Infinite
                )
            )
    ) {

        Column(modifier = Modifier.fillMaxSize()) {
            Row(modifier = Modifier.fillMaxWidth().padding(24.dp).zIndex(1f), horizontalArrangement = Arrangement.SpaceBetween) {
                var timerText by remember { mutableStateOf(if (appState.lives >= 5) "MAX" else "") }
                
                LaunchedEffect(appState.lives, appState.nextLifeTime) {
                    if (appState.lives >= 5) {
                        timerText = "MAX"
                    } else {
                        while (true) {
                            val remaining = appState.nextLifeTime - System.currentTimeMillis()
                            if (remaining > 0) {
                                val mins = (remaining / 60000).toInt()
                                val secs = ((remaining % 60000) / 1000).toInt()
                                timerText = String.format(Locale.getDefault(), "%02d:%02d", mins, secs)
                            } else {
                                timerText = "00:00"
                            }
                            kotlinx.coroutines.delay(1000)
                        }
                    }
                }
            
                StatPill(icon = Icons.Default.Favorite, tint = Color(0xFFEF4444), text = "${appState.lives}", label = timerText, isLarge = true)
                StatPill(icon = Icons.Default.Star, tint = Color(0xFFFBBF24), text = "${appState.coins}", label = "", isLarge = true)
            }

            Box(modifier = Modifier.weight(1f).fillMaxWidth()) {
                when (screen) {
                    Screen.HOME -> {
                        Box(modifier = Modifier.fillMaxSize()) {
                            val targetIndex = kotlin.math.max(0, appState.highestUnlockedLevel - 1)
                            val startIndex = kotlin.math.max(0, targetIndex - 1)
                            val listState = androidx.compose.foundation.lazy.rememberLazyListState(initialFirstVisibleItemIndex = startIndex)
                            
                            androidx.compose.runtime.LaunchedEffect(targetIndex) {
                                listState.animateScrollToItem(targetIndex)
                            }
    
                            LazyColumn(
                                state = listState,
                                userScrollEnabled = false,
                                reverseLayout = true,
                                contentPadding = PaddingValues(top = 160.dp, bottom = 210.dp),
                                horizontalAlignment = Alignment.CenterHorizontally,
                                modifier = Modifier.fillMaxWidth().fillMaxHeight()
                            ) {
                                items(appState.highestUnlockedLevel + 10) { index ->
                                    val level = index + 1
                                    LevelNode(
                                        level = level,
                                        isCompleted = level < appState.highestUnlockedLevel,
                                        isCurrent = level == appState.highestUnlockedLevel,
                                        isLocked = level > appState.highestUnlockedLevel,
                                        isHardLevel = level % 5 == 0
                                    )
                                }
                            }
                            
                            // Play Button positioned inside the content area (above ads and tabs)
                            Box(modifier = Modifier.align(Alignment.BottomCenter).fillMaxWidth().padding(start = 32.dp, end = 32.dp, bottom = 24.dp)) {
                                Button(
                                    onClick = { if (appState.lives > 0) viewModel.startLevel(appState.highestUnlockedLevel) },
                                    colors = ButtonDefaults.buttonColors(
                                        containerColor = if (appState.lives > 0) Color(0xFF90E4AD) else Color.White.copy(alpha = 0.5f),
                                        contentColor = Color(0xFF1E293B),
                                        disabledContainerColor = Color.White.copy(alpha = 0.5f),
                                        disabledContentColor = Color(0xFF1E293B).copy(alpha = 0.5f)
                                    ),
                                    shape = CircleShape,
                                    elevation = ButtonDefaults.buttonElevation(defaultElevation = 6.dp),
                                    modifier = Modifier.fillMaxWidth().height(64.dp)
                                ) {
                                    Text(
                                        if (appState.lives > 0) "PLAY LEVEL ${appState.highestUnlockedLevel}" else "OUT OF LIVES",
                                        fontSize = 20.sp,
                                        fontWeight = FontWeight.ExtraBold,
                                        letterSpacing = 1.sp
                                    )
                                }
                            }
                        }
                    }
                    Screen.SHOP -> {
                        val billingManager = LocalBillingManager.current
                        val activity = androidx.activity.compose.LocalActivity.current ?: LocalContext.current as Activity
                        val productDetails by billingManager.productDetails.collectAsState()
                        
                        LazyColumn(
                            modifier = Modifier.fillMaxSize().padding(horizontal = 24.dp),
                            verticalArrangement = Arrangement.spacedBy(24.dp),
                            contentPadding = PaddingValues(top = 16.dp, bottom = 170.dp)
                        ) {
                            item {
                                Text("Buy Coins", color = Color(0xFF1E293B), fontSize = 28.sp, fontWeight = FontWeight.ExtraBold)
                                Spacer(modifier = Modifier.height(16.dp))
                            }
                            
                            val coinPacks = listOf(
                                Pair(1000, "coin_pack_1000"),
                                Pair(5000, "coin_pack_5000"),
                                Pair(12000, "coin_pack_12000")
                            )
                            
                            items(coinPacks.size) { index ->
                                val pack = coinPacks[index]
                                val amount = pack.first
                                val productDetail = productDetails[pack.second]
                                val defaultPrice = if (amount == 1000) "$0.99" else if (amount == 5000) "$3.99" else "$7.99"
                                val price = productDetail?.oneTimePurchaseOfferDetails?.formattedPrice ?: defaultPrice
                                
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .background(Color.White.copy(alpha = 0.35f), RoundedCornerShape(16.dp))
                                        .border(1.dp, Color.White.copy(alpha = 0.6f), RoundedCornerShape(16.dp))
                                        .padding(16.dp),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                        Icon(Icons.Default.Star, contentDescription = "Coins", tint = Color(0xFFFBBF24))
                                        Text("$amount Coins", color = Color(0xFF1E293B), fontSize = 20.sp, fontWeight = FontWeight.Bold)
                                    }
                                    Button(
                                        onClick = {
                                            billingManager.initiatePurchaseFlow(activity, pack.second) {
                                                viewModel.addCoins(amount)
                                            }
                                        },
                                        shape = CircleShape,
                                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF90E4AD), contentColor = Color(0xFF1E293B))
                                    ) {
                                        Text(price, fontWeight = FontWeight.ExtraBold)
                                    }
                                }
                            }
                            
                            if (!appState.adsRemoved) {
                                item {
                                    Spacer(modifier = Modifier.height(32.dp))
                                    Text("Premium", color = Color(0xFF1E293B), fontSize = 28.sp, fontWeight = FontWeight.ExtraBold)
                                    Spacer(modifier = Modifier.height(16.dp))
                                    
                                    val productDetail = productDetails["remove_ads"]
                                    val price = productDetail?.oneTimePurchaseOfferDetails?.formattedPrice ?: "$9.99"
                                    
                                    Row(
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .background(Color.White.copy(alpha = 0.35f), RoundedCornerShape(16.dp))
                                            .border(1.dp, Color.White.copy(alpha = 0.6f), RoundedCornerShape(16.dp))
                                            .padding(16.dp),
                                        horizontalArrangement = Arrangement.SpaceBetween,
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                            Icon(Icons.Default.Star, contentDescription = "Premium", tint = Color(0xFFFBBF24)) // Ideally a no-ads icon, but Star is fine for now
                                            Text("Remove Ads", color = Color(0xFF1E293B), fontSize = 20.sp, fontWeight = FontWeight.Bold)
                                        }
                                        Button(
                                            onClick = {
                                                billingManager.initiatePurchaseFlow(activity, "remove_ads") {
                                                    viewModel.removeAds()
                                                }
                                            },
                                            shape = CircleShape,
                                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF90E4AD), contentColor = Color(0xFF1E293B))
                                        ) {
                                            Text(price, fontWeight = FontWeight.ExtraBold)
                                        }
                                    }
                                }
                            }

                            item {
                                Spacer(modifier = Modifier.height(32.dp))
                                Text("Themes", color = Color(0xFF1E293B), fontSize = 28.sp, fontWeight = FontWeight.ExtraBold)
                                Spacer(modifier = Modifier.height(16.dp))
                            }
                            
                            val themes = listOf(
                                Triple("CLASSIC", "Classic", 0),
                                Triple("NEON", "Neon Glow", 5000),
                                Triple("PASTEL", "Pastel Dream", 10000),
                                Triple("COSMIC", "Cosmic", 25000),
                                Triple("FANTASY", "Fantasy", 50000)
                            )
                            
                            items(themes.size) { index ->
                                val theme = themes[index]
                                val themeId = theme.first
                                val isUnlocked = appState.unlockedThemes.contains(themeId)
                                val isActive = appState.activeTheme == themeId
                                
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .background(if (isActive) Color.White.copy(alpha = 0.6f) else Color.White.copy(alpha = 0.35f), RoundedCornerShape(16.dp))
                                        .border(
                                            width = if (isActive) 2.dp else 1.dp,
                                            color = if (isActive) Color(0xFF82A6F1) else Color.White.copy(alpha = 0.6f),
                                            shape = RoundedCornerShape(16.dp)
                                        )
                                        .padding(16.dp),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text(theme.second, color = Color(0xFF1E293B), fontSize = 20.sp, fontWeight = FontWeight.Bold)
                                    if (isActive) {
                                        Text("Equipped", color = Color(0xFF82A6F1), fontWeight = FontWeight.ExtraBold)
                                    } else if (isUnlocked) {
                                        Button(
                                            onClick = { viewModel.setTheme(themeId) },
                                            shape = CircleShape,
                                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF82A6F1), contentColor = Color(0xFF1E293B))
                                        ) { Text("Equip", fontWeight = FontWeight.ExtraBold) }
                                    } else {
                                        Button(
                                            onClick = { viewModel.buyTheme(themeId, theme.third) },
                                            enabled = appState.coins >= theme.third,
                                            shape = CircleShape,
                                            colors = ButtonDefaults.buttonColors(
                                                containerColor = Color(0xFFFBBF24),
                                                contentColor = Color(0xFF1E293B),
                                                disabledContainerColor = Color.White.copy(alpha = 0.4f),
                                                disabledContentColor = Color(0xFF1E293B).copy(alpha = 0.5f)
                                            )
                                        ) {
                                            Text("${theme.third} Coins", fontWeight = FontWeight.ExtraBold)
                                        }
                                    }
                                }
                            }
                        }
                    }
                    Screen.SETTINGS -> {
                        Column(
                            modifier = Modifier.fillMaxSize().padding(32.dp),
                            verticalArrangement = Arrangement.spacedBy(24.dp)
                        ) {
                            Text("Settings", color = Color(0xFF1E293B), fontSize = 32.sp, fontWeight = FontWeight.ExtraBold)
                            
                            Row(modifier = Modifier.fillMaxWidth().background(Color.White.copy(alpha = 0.35f), RoundedCornerShape(16.dp)).border(1.dp, Color.White.copy(alpha = 0.6f), RoundedCornerShape(16.dp)).padding(16.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                Text("Sound", color = Color(0xFF1E293B), fontSize = 20.sp, fontWeight = FontWeight.Bold)
                                Switch(
                                    checked = appState.soundEnabled,
                                    onCheckedChange = { viewModel.toggleSound() },
                                    colors = SwitchDefaults.colors(checkedThumbColor = Color(0xFF82A6F1), checkedTrackColor = Color(0xFF82A6F1).copy(alpha=0.5f))
                                )
                            }
                            
                            Row(modifier = Modifier.fillMaxWidth().background(Color.White.copy(alpha = 0.35f), RoundedCornerShape(16.dp)).border(1.dp, Color.White.copy(alpha = 0.6f), RoundedCornerShape(16.dp)).padding(16.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                Text("Haptic Feedback", color = Color(0xFF1E293B), fontSize = 20.sp, fontWeight = FontWeight.Bold)
                                Switch(
                                    checked = appState.hapticEnabled,
                                    onCheckedChange = { viewModel.toggleHaptics() },
                                    colors = SwitchDefaults.colors(checkedThumbColor = Color(0xFF82A6F1), checkedTrackColor = Color(0xFF82A6F1).copy(alpha=0.5f))
                                )
                            }
                        }
                    }
                    else -> {}
                }
            }
            
            // Bottom Tabs Island
            Row(
                modifier = Modifier
                    .padding(horizontal = 32.dp, vertical = 12.dp)
                    .fillMaxWidth()
                    .shadow(16.dp, CircleShape, spotColor = Color.Black.copy(alpha = 0.1f))
                    .background(Color.White.copy(alpha = 0.8f), CircleShape)
                    .border(1.dp, Color.White, CircleShape)
                    .padding(vertical = 8.dp, horizontal = 24.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                TabItem(Icons.Default.ShoppingCart, "Shop", screen == Screen.SHOP) { viewModel.navigate(Screen.SHOP) }
                TabItem(Icons.Default.Home, "Home", screen == Screen.HOME) { viewModel.navigate(Screen.HOME) }
                TabItem(Icons.Default.Settings, "Settings", screen == Screen.SETTINGS) { viewModel.navigate(Screen.SETTINGS) }
            }
            
            // Banner Ad at the very bottom
            Box(modifier = Modifier.fillMaxWidth(), contentAlignment = Alignment.Center) {
                AdmobBanner(appState.adsRemoved)
            }
        }

    }
}

import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# 1. Update MarbleSortScreen
screen_old = """            Spacer(modifier = Modifier.weight(1f))

            // Grid
            TubeGrid(
                tubes = state.tubes,
                selectedTubeIndex = state.selectedTubeIndex,
                activeTheme = appState.activeTheme,
                onTubeSelect = { viewModel.selectTube(it) }
            )
            
            Spacer(modifier = Modifier.weight(1f))

            // Footer - Power Ups
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 24.dp, vertical = 16.dp)
                    .padding(bottom = 56.dp), // Padding to keep above banner ad"""
screen_new = """            Spacer(modifier = Modifier.height(16.dp))

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
                    .padding(bottom = 90.dp), // Padding to keep above banner ad and nav bar"""
content = content.replace(screen_old, screen_new)

# 2. Update TubeGrid signature and BoxWithConstraints modifier
grid_old = """@Composable
fun TubeGrid(
    tubes: List<Tube>,
    selectedTubeIndex: Int?,
    activeTheme: String,
    onTubeSelect: (Int) -> Unit
) {
    BoxWithConstraints(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp),
        contentAlignment = Alignment.Center
    ) {"""
grid_new = """@Composable
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
    ) {"""
content = content.replace(grid_old, grid_new)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

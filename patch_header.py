import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

header_old = """            // Header
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 32.dp, start = 24.dp, end = 24.dp, bottom = 24.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                    IconButton(
                        onClick = { viewModel.goHome() },
                        modifier = Modifier
                            .size(52.dp)
                            .shadow(8.dp, RoundedCornerShape(14.dp), spotColor = Color(0xFF6B8CE0))
                            .background(Color(0xFF82A6F1), RoundedCornerShape(14.dp))
                    ) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Home", tint = Color(0xFF1E293B), modifier = Modifier.size(28.dp))
                    }
                    Column {
                        Text(
                            text = "PUZZLE SOLVER",
                            color = Color(0xFF1E293B),
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 1.sp
                        )
                        Text(
                            text = "Level ${state.level}",
                            color = Color(0xFF172554),
                            style = MaterialTheme.typography.headlineMedium,
                            fontWeight = FontWeight.ExtraBold
                        )
                    }
                }"""

header_new = """            // Header
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 16.dp, start = 16.dp, end = 16.dp, bottom = 12.dp),
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
                    Column {
                        Text(
                            text = "PUZZLE SOLVER",
                            color = Color(0xFF1E293B),
                            fontSize = 10.sp,
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 1.sp
                        )
                        Text(
                            text = "Level ${state.level}",
                            color = Color(0xFF172554),
                            style = MaterialTheme.typography.titleLarge,
                            fontWeight = FontWeight.ExtraBold
                        )
                    }
                }"""

if header_old in content:
    content = content.replace(header_old, header_new)
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(content)
    print("Patched Header")
else:
    print("Header not found!")

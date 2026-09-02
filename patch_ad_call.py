import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

ad_old = """                                    adManager.showRewardedAd(activity, {
                                        viewModel.undo()
                                    }, {
                                        viewModel.undo() // Fallback if ad fails to load
                                    })"""

ad_new = """                                    adManager.showRewardedAd(activity) {
                                        viewModel.undo()
                                    }"""

if ad_old in content:
    content = content.replace(ad_old, ad_new)
else:
    print("Not found")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

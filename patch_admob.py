import re

# Update AndroidManifest.xml
with open('app/src/main/AndroidManifest.xml', 'r') as f:
    manifest_content = f.read()

manifest_old = """        <!-- Sample AdMob app ID -->
        <meta-data
            android:name="com.google.android.gms.ads.APPLICATION_ID"
            android:value="ca-app-pub-3940256099942544~3347511713"/>"""
            
manifest_new = """        <!-- AdMob app ID -->
        <meta-data
            android:name="com.google.android.gms.ads.APPLICATION_ID"
            android:value="ca-app-pub-2587866419282101~8949877533"/>"""

if manifest_old in manifest_content:
    manifest_content = manifest_content.replace(manifest_old, manifest_new)
    with open('app/src/main/AndroidManifest.xml', 'w') as f:
        f.write(manifest_content)
    print("Patched AndroidManifest.xml")
else:
    print("AdMob ID in manifest not found!")

# Update MainActivity.kt
with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    main_content = f.read()

# Replace Rewarded
main_content = main_content.replace(
    'RewardedAd.load(context, "ca-app-pub-3940256099942544/5224354917", adRequest, object : RewardedAdLoadCallback()',
    'RewardedAd.load(context, "ca-app-pub-2587866419282101/3154625375", adRequest, object : RewardedAdLoadCallback()'
)

# Replace Interstitial
main_content = main_content.replace(
    'InterstitialAd.load(context, "ca-app-pub-3940256099942544/1033173712", adRequest, object : InterstitialAdLoadCallback()',
    'InterstitialAd.load(context, "ca-app-pub-2587866419282101/8217098999", adRequest, object : InterstitialAdLoadCallback()'
)

# Replace Banner
main_content = main_content.replace(
    'adUnitId = "ca-app-pub-3940256099942544/6300978111"',
    'adUnitId = "ca-app-pub-2587866419282101/4852569054"'
)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(main_content)
print("Patched MainActivity.kt")


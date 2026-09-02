import re

with open('metadata.json', 'r') as f:
    content = f.read()
content = content.replace('"name": "Marble Sort"', '"name": "Marble Sort Ultimate"')
with open('metadata.json', 'w') as f:
    f.write(content)

with open('app/src/main/res/values/strings.xml', 'r') as f:
    content = f.read()
content = content.replace('>Marble Sort<', '>Marble Sort Ultimate<')
with open('app/src/main/res/values/strings.xml', 'w') as f:
    f.write(content)

with open('settings.gradle.kts', 'r') as f:
    content = f.read()
content = content.replace('rootProject.name = "Marble Sort"', 'rootProject.name = "Marble Sort Ultimate"')
with open('settings.gradle.kts', 'w') as f:
    f.write(content)

print("Names updated successfully!")

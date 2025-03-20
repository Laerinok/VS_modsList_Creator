Mod list generator for Vintage Story in JSON format


This script generates a `modlist.json` file of the mods installed in the 'mods' folder of the Vintage Story game.

It uses the modpath from the VS_ModsUpdater configuration file, so place the executable in the VS_ModsUpdater folder or create a config.ini file as below (with your modspath):
```ini
[ModPath] 
path = C:\Users\UserName\AppData\Roaming\VintagestoryData\Mods
```

Example of generated modlist.json :
```json
{
    "Mods": [
        {
            "Name": "A Culinary Artillery",
            "Version": "1.2.5",
            "ModId": "aculinaryartillery",
            "Side": "both",
            "Description": "An armory of tools for food-based mods and modpack makers",
            "url_mod": "https://mods.vintagestory.at/show/mod/4151",
            "url_download": "https://moddbcdn.vintagestory.at/ACulinaryArtillery+1_d7a64a8bcfe7ff7204c7154277ece52b.zip?dl=ACulinaryArtillery 1.2.5.zip"
        },
        {
            "Name": "Alternative Map Icon Renderer Patch",
            "Version": "1.0.0",
            "ModId": "altmapiconrendererpatch",
            "Side": "client",
            "Description": "Alters player and waypoint icon rendering. [Patched] For 1.20.0-pre.13!",
            "url_mod": "https://mods.vintagestory.at/show/mod/16135",
            "url_download": "https://moddbcdn.vintagestory.at/AltMapIconRendererPa_292fa3bc984411a5e6580e3753d45206.zip?dl=AltMapIconRendererPatch.zip"
        },
        {
            "Name": "Animal cages",
            "Version": "3.2.1",
            "ModId": "animalcages",
            "Side": "both",
            "Description": "Mod that adds cages for animals so you can catch, transport and display them.",
            "url_mod": "https://mods.vintagestory.at/show/mod/1194",
            "url_download": "https://moddbcdn.vintagestory.at/animalcages_v3.2.1_53b286dba4f508f65f1bc0334b4a017a.zip?dl=animalcages_v3.2.1.zip"
        },
        {
            "Name": "Custom Flowerpots",
            "Version": "1.2.1",
            "ModId": "apeflowerpots",
            "Side": "both",
            "Description": "Recycle old anvil molds, boots etc. as flowerpots",
            "url_mod": "https://mods.vintagestory.at/show/mod/19922",
            "url_download": "https://moddbcdn.vintagestory.at/apeflowerpots-1.20.4_b34cb937d2b07ff986b963cde118cc23.zip?dl=apeflowerpots-1.20.4-v1.2.1.zip"
        },
        {
            "Name": "Grapes and wine",
            "Version": "1.2.6",
            "ModId": "apegrapes",
            "Side": "both",
            "Description": "Adds grapes and grape vines/bushes",
            "url_mod": "https://mods.vintagestory.at/show/mod/15276",
            "url_download": "https://moddbcdn.vintagestory.at/apegrapes-v1.20.4-1._71a066f20997d97c32aec320182384ba.zip?dl=apegrapes-v1.20.4-1.2.6.zip"
        }
    ]
}
```
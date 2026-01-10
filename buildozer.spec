[app]
title = Draktharr
package.name = draktharr
package.domain = org.draktharr
source.dir = .
source.include_exts = py
version = 1.0

# CORRIGIDO: Ordem e versões específicas
requirements = python3==3.10.0,hostpython3==3.10.0,kivy==2.3.0,requests,certifi,urllib3,charset-normalizer,idna

orientation = portrait
fullscreen = 0

# Permissões necessárias
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = armeabi-v7a

# Importante para requests funcionar
p4a.bootstrap = sdl2
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1

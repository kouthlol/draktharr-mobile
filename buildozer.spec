[app]
title = Draktharr
package.name = draktharr
package.domain = org.draktharr
source.dir = .
source.include_exts = py,png,jpg,kv,atlas  # Adicione extensões de imagem se tiver
version = 1.0

# Adicionado openssl para o requests funcionar com HTTPS
requirements = python3, kivy==2.3.0, requests, certifi, urllib3, charset-normalizer, idna, openssl

orientation = portrait
fullscreen = 0

android.permissions = INTERNET, ACCESS_NETWORK_STATE

android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
# Adicionado 64 bits para compatibilidade moderna
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1

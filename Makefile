CONSOLE := --disable-console

ifeq ($(filter onefile standalone, $(firstword $(MAKECMDGOALS))),)
    MAKECMDGOALS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
endif

ifeq ($(filter console, $(MAKECMDGOALS)), console)
    CONSOLE := --enable-console
endif

onefile:
	python -m nuitka --onefile $(CONSOLE) --remove-output --output-dir=telegramtrac_onefile --onefile-tempdir-spec="%CACHE_DIR%/%COMPANY%/%PRODUCT%/%VERSION%" --company-name=telegramtrac --product-name=telegramtrac --file-version=0.1 --product-version=0.6 --include-data-files=venv/Lib/site-packages/webview/lib/runtimes/win-x64/native/WebView2Loader.dll=webview/lib/runtimes/win-x64/native/WebView2Loader.dll --include-data-files=app.py=app.py --include-data-files=build-datasets.py=build-datasets.py --include-data-files=channels-to-network.py=channels-to-network.py --include-data-files=connect.py=connect.py --include-data-files=main.py=main.py --include-data-files=sign_in.py=sign_in.py --include-data-files=.streamlit/config.toml=.streamlit/config.toml --include-data-files=telegram_tracker/api/__init__.py=telegram_tracker/api/__init__.py --include-data-files=telegram_tracker/cryptography/__init__.py=telegram_tracker/cryptography/__init__.py --include-data-files=telegram_tracker/utils/__init__.py=telegram_tracker/utils/__init__.py --include-data-files=telegram_tracker/__init__.py=telegram_tracker/__init__.py --windows-icon-from-ico=images/icon.ico --onefile-windows-splash-screen-image=images/splash-screen-0.6.png --msvc=14.3 telegramtrac.py

standalone:
	python -m nuitka --standalone $(CONSOLE) --remove-output --output-dir=telegramtrac_standalone --include-data-files=venv/Lib/site-packages/webview/lib/runtimes/win-x64/native/WebView2Loader.dll=webview/lib/runtimes/win-x64/native/WebView2Loader.dll --include-data-files=app.py=app.py --include-data-files=build-datasets.py=build-datasets.py --include-data-files=channels-to-network.py=channels-to-network.py --include-data-files=connect.py=connect.py --include-data-files=main.py=main.py --include-data-files=sign_in.py=sign_in.py --include-data-files=.streamlit/config.toml=.streamlit/config.toml --include-data-files=telegram_tracker/api/__init__.py=telegram_tracker/api/__init__.py --include-data-files=telegram_tracker/cryptography/__init__.py=telegram_tracker/cryptography/__init__.py --include-data-files=telegram_tracker/utils/__init__.py=telegram_tracker/utils/__init__.py --include-data-files=telegram_tracker/__init__.py=telegram_tracker/__init__.py --windows-icon-from-ico=images/icon.ico --msvc=14.3 telegramtrac.py

test:
	python -m nuitka --enable-console --output-dir=telegramtrac_test --windows-icon-from-ico=images/icon.ico telegramtrac.py

.PHONY: onefile standalone test
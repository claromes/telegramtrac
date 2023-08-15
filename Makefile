# To use the target 'dev', change 'app_path' variable in telegramtrac.py file to 'app_path_dev'

onefile:
	python \
	-m  \
	nuitka \
	--onefile \
	--enable-console \
	--remove-output \
	--output-dir=telegramtrac_onefile \
	--onefile-tempdir-spec='%CACHE_DIR%/Programs/%PRODUCT%/%VERSION%' \
	--product-name=telegramtrac \
	--file-version=0.1 \
	--product-version=0.6 \
	--include-package=annotated_text \
	--include-package=streamlit \
	--include-package=camera_input_live \
	--include-package=streamlit_card \
	--include-package=streamlit_embedcode \
	--include-package=streamlit_extras \
	--include-package=faker \
	--include-package=streamlit_image_coordinates \
	--include-package=streamlit_toggle \
	--include-package=streamlit_vertical_slider \
	--include-package=telethon \
	--include-package=pandas \
	--include-package=openpyxl \
	--include-package=tqdm \
	--include-package=networkx \
	--include-package=matplotlib \
	--include-package=psutil \
	--include-package=Crypto \
	--include-data-dir=venv/Lib/site-packages/streamlit=streamlit \
	--include-data-dir=venv/Lib/site-packages/streamlit_card=streamlit_card \
	--include-data-dir=venv/Lib/site-packages/streamlit_image_coordinates=streamlit_image_coordinates \
	--include-data-dir=venv/Lib/site-packages/streamlit_toggle=streamlit_toggle \
	--include-data-dir=venv/Lib/site-packages/streamlit_vertical_slider=streamlit_vertical_slider \
	--include-data-files=app.py=app.py \
	--include-data-files=build-datasets.py=build-datasets.py \
	--include-data-files=channels-to-network.py=channels-to-network.py \
	--include-data-files=connect.py=connect.py \
	--include-data-files=main.py=main.py \
	--include-data-files=sign_in.py=sign_in.py \
	--include-data-files=telegram_tracker/api/__init__.py=telegram_tracker/api/__init__.py \
	--include-data-files=telegram_tracker/cryptography/__init__.py=telegram_tracker/cryptography/__init__.py \
	--include-data-files=telegram_tracker/utils/__init__.py=telegram_tracker/utils/__init__.py \
	--include-data-files=telegram_tracker/__init__.py=telegram_tracker/__init__.py \
	--windows-icon-from-ico=images/icon.ico \
	--onefile-windows-splash-screen-image=images/splash-screen-telegram-0.6.png \
	--msvc=14.3 \
	telegramtrac.py

standalone:
	python \
	-m \
	nuitka \
	--standalone \
	--enable-console \
	--remove-output \
	--output-dir=telegramtrac_standalone \
	--follow-imports \
	--include-package=annotated_text \
	--include-package=streamlit \
	--include-package=camera_input_live \
	--include-package=streamlit_card \
	--include-package=streamlit_embedcode \
	--include-package=streamlit_extras \
	--include-package=faker \
	--include-package=streamlit_image_coordinates \
	--include-package=streamlit_toggle \
	--include-package=streamlit_vertical_slider \
	--include-package=telethon \
	--include-package=pandas \
	--include-package=openpyxl \
	--include-package=tqdm \
	--include-package=networkx \
	--include-package=matplotlib \
	--include-package=psutil \
	--include-package=Crypto \
	--include-data-dir=venv/Lib/site-packages/streamlit=streamlit \
	--include-data-dir=venv/Lib/site-packages/streamlit_card=streamlit_card \
	--include-data-dir=venv/Lib/site-packages/streamlit_image_coordinates=streamlit_image_coordinates \
	--include-data-dir=venv/Lib/site-packages/streamlit_toggle=streamlit_toggle \
	--include-data-dir=venv/Lib/site-packages/streamlit_vertical_slider=streamlit_vertical_slider \
	--include-data-files=app.py=app.py \
	--include-data-files=build-datasets.py=build-datasets.py \
	--include-data-files=channels-to-network.py=channels-to-network.py \
	--include-data-files=connect.py=connect.py \
	--include-data-files=main.py=main.py \
	--include-data-files=sign_in.py=sign_in.py \
	--include-data-files=telegram_tracker/api/__init__.py=telegram_tracker/api/__init__.py \
	--include-data-files=telegram_tracker/cryptography/__init__.py=telegram_tracker/cryptography/__init__.py \
	--include-data-files=telegram_tracker/utils/__init__.py=telegram_tracker/utils/__init__.py \
	--include-data-files=telegram_tracker/__init__.py=telegram_tracker/__init__.py \
	--windows-icon-from-ico=images/icon.ico \
	telegramtrac.py

dev:
	python \
	-m \
	nuitka \
	--enable-console \
	--output-dir=telegramtrac_dev \
	--windows-icon-from-ico=images/icon.ico \
	telegramtrac.py

.PHONY: onefile standalone dev
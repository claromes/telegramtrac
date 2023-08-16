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
	--include-package=app.py \
	--include-package=build-datasets.py \
	--include-package=channels-to-network.py \
	--include-package=connect.py \
	--include-package=main.py \
	--include-package=sign_in.py \
	--include-package=telegram_tracker \
	--include-data-dir=venv/Lib/site-packages/streamlit=streamlit \
	--include-data-dir=venv/Lib/site-packages/streamlit_card=streamlit_card \
	--include-data-dir=venv/Lib/site-packages/streamlit_image_coordinates=streamlit_image_coordinates \
	--include-data-dir=venv/Lib/site-packages/streamlit_toggle=streamlit_toggle \
	--include-data-dir=venv/Lib/site-packages/streamlit_vertical_slider=streamlit_vertical_slider \
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
	--include-package=app.py \
	--include-package=build-datasets.py \
	--include-package=channels-to-network.py \
	--include-package=connect.py \
	--include-package=main.py \
	--include-package=sign_in.py \
	--include-package=telegram_tracker \
	--include-data-dir=venv/Lib/site-packages/streamlit=streamlit \
	--include-data-dir=venv/Lib/site-packages/streamlit_card=streamlit_card \
	--include-data-dir=venv/Lib/site-packages/streamlit_image_coordinates=streamlit_image_coordinates \
	--include-data-dir=venv/Lib/site-packages/streamlit_toggle=streamlit_toggle \
	--include-data-dir=venv/Lib/site-packages/streamlit_vertical_slider=streamlit_vertical_slider \
	--include-data-dir=config=config \
	--include-data-dir=session=session \
	--include-data-dir=sign_in=sign_in \
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
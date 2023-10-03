session:
	rm -rf output_*/
	rm config/config_* \
	session/session_file_* \
	sign_in/encrypted_code_* \
	sign_in/encrypted_password_*

.PHONY: session
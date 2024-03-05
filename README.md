# Template for dataset ninja repos

## How to use

1. Fill all fields in `settings.py` in the section `Before uploading to instance`.
2. Implement the `convert_and_upload_supervisely_project()` function in `convert.py`.
3. Run `main.py` to upload the dataset to the Supervisely instance.
4. Check the result in the web interface, select an image for preview and check if annotations are having correct colors.
5. Fill all required fields in `settings.py` in the section `After uploading to instance`.
6. If needed fill in optional fields in `settings.py` in the section `After uploading to instance`.
7. Run `main.py` to change the `custom_data` of the project and build the required files in the repository.
8. Fill necessary fields in `options.py` to configure visualizations.
9. Commit and push changes to the repository.

from huggingface_hub import upload_folder

upload_folder(
    repo_id="anisha-14/MentiFy-DistilBERT",
    folder_path="model",
    repo_type="model",
)

print("✅ Model uploaded successfully!")
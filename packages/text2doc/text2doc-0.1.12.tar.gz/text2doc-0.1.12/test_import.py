try:
    import text2doc
    print(f"Successfully imported text2doc version: {text2doc.__version__}")
except ImportError as e:
    print(f"Failed to import text2doc: {e}")

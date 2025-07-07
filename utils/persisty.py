def save_obj(obj, path):
    """Persiste objeto em disco."""
    import pickle
    with open(path, 'wb') as f:
        pickle.dump(obj, f)

def load_obj(path):
    """Carrega objeto persistido."""
    import pickle
    with open(path, 'rb') as f:
        return pickle.load(f)

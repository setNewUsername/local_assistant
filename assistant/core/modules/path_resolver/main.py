if __name__ == '__main__':
    from PathResolver.PathResolver import PathResolver

    path = PathResolver()
    print(path.rootAssistantFolderPath)
    print(path.getLocalDataStoragePath())
    print(path.getDBDataStoragePath())
    print(path.getLogsPath())
    print(path.getConfigsPath())

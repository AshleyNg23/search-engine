from indexer import Index

def main(dir_name):
    dir_indexer = Index()
    dir_indexer.index(dir_name)
    dir_indexer.printReport()


if __name__ == "__main__":
    main("DEV")
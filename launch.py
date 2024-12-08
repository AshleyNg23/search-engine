from indexer import Index
import os


def deletePartialIndexes(directory):
    # Loop through all files in the given directory
    for filename in os.listdir(directory):
        # Check if the file starts with "PartialIndex"
        if filename.startswith("PartialIndex") or filename.startswith("FinalIndex.pkl"):
            # Construct the full file path
            filePath = os.path.join(directory, filename)
            try:
                # Remove the file
                os.remove(filePath)
                print(f"Deleted: {filePath}")
            except Exception as e:
                print(f"Error deleting {filePath}: {e}")


def deleteFinalIndexes(directory):
    # Loop through all files in the given directory
    for filename in os.listdir(directory):
        # Check if the file starts with "PartialIndex"
        if filename.startswith("FinalIndex.pkl"):
            # Construct the full file path
            filePath = os.path.join(directory, filename)
            try:
                # Remove the file
                os.remove(filePath)
                print(f"Deleted: {filePath}")
            except Exception as e:
                print(f"Error deleting {filePath}: {e}")


def main(dir_name):
    deletePartialIndexes(os.getcwd())
    deleteFinalIndexes(os.getcwd())
    print(dir_name)
    dir_indexer = Index()
    dir_indexer.index(dir_name)
    dir_indexer.printReport()
    deletePartialIndexes(os.getcwd())




if __name__ == "__main__":
<<<<<<< HEAD
    main(r"F:\CompSci 121\cs-121-search-engine-5\DEV")
=======
    main("DEV")
>>>>>>> da426cd933e6ac61c2531b0db542d674b7d00fa9


from indexer import Index
import os
import pickle

def deletePartialIndexes(directory):
    # Loop through all files in the given directory
    for filename in os.listdir(directory):
        # Check if the file starts with "PartialIndex"
        if filename.startswith("PartialIndex") or filename.startswith("FinalIndex.pkl") or filename.startswith("IndexesWith"):
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
    print(dir_name)
    dir_indexer = Index()
    dir_indexer.index(dir_name)
    dir_indexer.printReport()


if __name__ == "__main__":
    main(r"C:\Users\Rudy1\Downloads\developer\DEV")
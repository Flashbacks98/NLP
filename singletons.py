from collections import defaultdict

def replace_singletons_with_unk(inputFile, outputFile):
    # Count the occurrences of each word in the input file
    word_counts = {}
    for line in inputFile:
        words = line.strip().split()
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1

    # Reset the file pointer to the beginning
    inputFile.seek(0)
    vocabulary = set()
    
    # Replace singletons with <unk> and write to the output file
    for line in inputFile:
        words = line.strip().split()
        new_words = [word if word_counts[word] > 1 else "<unk>" for word in words]
        vocabulary.update([word for word in words if word_counts[word] > 1])
        outputFile.write("<cs> " + " ".join(new_words) + " </s>\n")

    return vocabulary

# Replace words not observed in the training file with <unk> in the test file
def replace_unseen_with_unk(testFile, outputFile, vocabulary):
    for line in testFile:
        words = line.strip().split()
        new_words = [word if word in vocabulary else "<unk>" for word in words]
        outputFile.write("<cs> " + " ".join(new_words) + " </s>\n")

def bigrams(inputFile):
    # Create bigrams from the input file
    bigram_counts = defaultdict(int)
    inputFile.seek(0)
    
    for line in inputFile:
        words = line.strip().split()
        words = [word for word in words if word != "<cs>"]  # Exclude <cs> but keep </s>
        for i in range(len(words) - 1):
            bigram = (words[i], words[i+1])
            bigram_counts[bigram] += 1
            
    return bigram_counts

def calculate_bigram_oov_percentage(testFile, train_bigrams):
    total_bigrams = 0
    oov_bigrams = 0
    test_bigram_types = set()
    oov_bigram_types = set()

    for line in testFile:
        words = line.strip().split()
        words = [word for word in words if word != "<cs>"]
        for i in range(len(words) - 1):
            bigram = (words[i], words[i+1])
            total_bigrams += 1
            test_bigram_types.add(bigram)
            if bigram not in train_bigrams:
                oov_bigrams += 1
                oov_bigram_types.add(bigram)

    # Calculate the OOV percentages
    token_oov_percentage = (oov_bigrams / total_bigrams) * 100 if total_bigrams > 0 else 0
    type_oov_percentage = (len(oov_bigram_types) / len(test_bigram_types)) * 100 if test_bigram_types else 0

    return token_oov_percentage, type_oov_percentage

if __name__ == "__main__":
    # Open files for reading and writing
    testFile = open("test.txt", "r", errors="ignore")
    trainFile = open("train.txt", "r", errors="ignore")

    processedTestFile = open("processedTest.txt", "w")
    processedTrainFile = open("processedTrain.txt", "w")

    # Replace singletons with <unk> in the training file
    vocabulary = replace_singletons_with_unk(trainFile, processedTrainFile)

    # Replace unseen words with <unk> in the test file
    replace_unseen_with_unk(testFile, processedTestFile, vocabulary)

    # Reopen processed files for bigram calculations
    processedTestFile = open("processedTest.txt", "r")
    processedTrainFile = open("processedTrain.txt", "r")

    # Calculate bigrams from the processed training file
    train_bigrams = bigrams(processedTrainFile)

    # Calculate OOV percentages for bigrams in the test file
    token_oov_percentage, type_oov_percentage = calculate_bigram_oov_percentage(processedTestFile, train_bigrams)

    # Print the results
    print(f"OOV Bigram Token Percentage: {token_oov_percentage:.2f}%")
    print(f"OOV Bigram Type Percentage: {type_oov_percentage:.2f}%")

    # Close all opened files
    processedTrainFile.close()
    processedTestFile.close()
    trainFile.close()
    testFile.close()
    
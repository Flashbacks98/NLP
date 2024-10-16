import math

def count_words(inputFile):
    # Initialize a dictionary to store word counts
    words_dict = {}
    inputFile.seek(0)  # Reset file pointer to the beginning of the file
    for line in inputFile:  # Iterate through each line in the file
        for word in line.split():  # Split line into words
            lowerCaseWord = word.lower()  # Convert word to lowercase
            if (lowerCaseWord not in words_dict):
                # If the word is not in the dictionary, add it with a count of 1
                words_dict.update({lowerCaseWord: 1})
            else:
                # If the word is already in the dictionary, increment its count
                words_dict[lowerCaseWord] += 1
    return words_dict  # Return the dictionary of word counts

def unk_sentences(inputFile, outputFile, words_dict, bannedWords):
    inputFile.seek(0)  # Reset file pointer to the beginning of the file
    for line in inputFile:  # Iterate through each line in the input file
        outputFile.write("<s> ")  # Write start of sentence tag
        for word in line.split():  # Split line into words
            writtenWord = word.lower()  # Convert word to lowercase
            # Check if the word is a singleton or a banned word
            if (writtenWord in words_dict) and (words_dict[writtenWord] == 1):
                writtenWord = "<unk>"  # Replace singleton words with <unk>
            elif writtenWord in bannedWords:
                writtenWord = "<unk>"  # Replace banned words with <unk>
            outputFile.write(writtenWord + " ")  # Write the processed word
        outputFile.write("</s>\n")  # Write end of sentence tag

def compare_to(dict1, dict2):
    # Return a list of elements in dict1 that are not in dict2
    return [element for element in dict1 if element not in dict2]

def unigramModel(words_dict, totalWords):
    # Create a unigram model with probabilities
    unigramModel = {}
    for key in words_dict:
        # Calculate the probability of each word
        probability = round(words_dict[key] / totalWords, 8)
        unigramModel.update({key: probability})  # Update the unigram model
    return unigramModel  # Return the unigram model

def createBigram(inputFile):
    # Initialize a dictionary to store bigram counts
    bigram = {}
    inputFile.seek(0)  # Reset file pointer to the beginning of the file
    for line in inputFile:  # Iterate through each line in the file
        words = line.split()  # Split line into words
        for i in range(0, len(words)):
            # Check if the bigram exists in the dictionary
            if (i < len(words) - 1) and (tuple([words[i], words[i + 1]]) not in bigram): 
                bigram.update({tuple([words[i], words[i + 1]]): 1})  # Add new bigram with count 1
            elif (i < len(words) - 1):
                # Increment the count for existing bigram
                bigram[tuple([words[i], words[i + 1]])] += 1
    return bigram  # Return the bigram dictionary

def bigramModel(bigram_dict, word_dict):
    # Create a bigram model with probabilities
    bigramModel = {}
    for key in bigram_dict:
        # Calculate the probability of each bigram
        probability = round(bigram_dict[key] / word_dict[key[0]], 8)
        bigramModel.update({key: probability})  # Update the bigram model
    return bigramModel  # Return the bigram model

def addOneSmoothingModel(bigram_dict, word_dict, uniqueWords):
    # Create a bigram model with Add-One smoothing
    addOneSmoothingModel = {}
    for key in bigram_dict:
        # Calculate the smoothed probability
        probability = round(((1.0 + bigram_dict[key]) / (uniqueWords + word_dict[key[0]])), 8)
        addOneSmoothingModel.update({key: probability})  # Update the smoothed model
    return addOneSmoothingModel  # Return the Add-One smoothed model

def writeDict(dict, outputFile):
    # Write the contents of a dictionary to a file
    for key in dict:
        outputFile.write("{" + str(key) + "}" + ": " + str(dict[key]) + "\n")  # Write key-value pairs
    outputFile.write("\n")  # Write a newline for separation

def processSentence(sentence, words_dict):
    # Process a sentence to replace unseen words with <unk>
    processedSentence = "<s> "  # Initialize the processed sentence with start tag
    for word in sentence.split():  # Split the sentence into words
        if word.lower() not in words_dict:
            processedSentence += "<unk> "  # Replace unseen word with <unk>
        else:
            processedSentence += (word.lower() + " ")  # Append the known word
    processedSentence += " </s>"  # Append end tag
    return processedSentence  # Return the processed sentence

def calculateUnigramLog(sentence, unigramModel):
    # Calculate the log probability of a unigram sentence
    probability = 0
    for word in sentence.split():
        probability += math.log(unigramModel[word], 2)  # Sum log probabilities of each word
    probability = round(probability, 4)  # Round the result
    return probability  # Return the calculated probability

def calculateBigramLog(sentence, bigramModel, unigramModel):
    # Calculate the log probability of a bigram sentence
    probability = 0
    words = sentence.split()
    probability += math.log(unigramModel[words[0]], 2)  # Add the log probability of the first word
    for i in range(0, len(words) - 1):
        tupleWord = tuple([words[i], words[i + 1]])  # Create a tuple for the bigram
        if tupleWord in bigramModel:
            probability += math.log(bigramModel[tupleWord], 2)  # Add log probability of the bigram
    probability = round(probability, 4)  # Round the result
    return probability  # Return the calculated probability

def calculateAddOneSmoothingLog(sentence, addOneSmoothingModel, unigramModel):
    # Calculate the log probability of a sentence using Add-One smoothing
    probability = 0
    words = sentence.split()
    probability += math.log(unigramModel[words[0]], 2)  # Add log probability of the first word
    for i in range(0, len(words) - 1):
        tupleWord = tuple([words[i], words[i + 1]])  # Create a tuple for the bigram
        if tupleWord in addOneSmoothingModel:
            probability += math.log(addOneSmoothingModel[tupleWord], 2)  # Add log probability of the smoothed bigram
    probability = round(probability, 4)  # Round the result
    return probability  # Return the calculated probability

def calculatePerplexity(logModel, totalWords):
    # Calculate perplexity based on log probability and total words
    result = math.exp((-1.0 / totalWords) * logModel)  # Use the exponential function
    return round(result, 4)  # Round the result

def calculateUnigramLogFile(inputFile, unigramModel):
    inputFile.seek(0)  # Reset file pointer to the beginning of the file
    probability = 0
    for line in inputFile:
        for word in line.split():
            probability += math.log(unigramModel[word], 2)  # Sum log probabilities of each word in the file
    probability = round(probability, 4)  # Round the result
    return probability  # Return the calculated probability

def calculateBigramLogFile(inputFile, bigramModel, unigramModel):
    inputFile.seek(0)  # Reset file pointer to the beginning of the file
    probability = 0
    for line in inputFile:
        words = line.split()
        for i in range(0, len(words) - 1):
            if i == 0:
                probability += math.log(unigramModel[words[0]], 2)  # Add log probability of the first word
            tupleWord = tuple([words[i], words[i + 1]])  # Create a tuple for the bigram
            if tupleWord in bigramModel:
                probability += math.log(bigramModel[tupleWord], 2)  # Add log probability of the bigram
    probability = round(probability, 4)  # Round the result
    return probability  # Return the calculated probability

def calculateAddOneSmoothingLogFile(inputFile, addOneSmoothingModel, unigramModel):
    probability = 0
    # Initialize this to prevent using an undefined variable 'sentence'
    inputFile.seek(0)  # Reset file pointer to the beginning of the file
    for line in inputFile:
        words = line.split()  # Split line into words
        for i in range(0, len(words) - 1):
            if i == 0:
                probability += math.log(unigramModel[words[0]], 2)  # Add log probability of the first word
            tupleWord = tuple([words[i], words[i + 1]])  # Create a tuple for the bigram
            if tupleWord in addOneSmoothingModel:
                probability += math.log(addOneSmoothingModel[tupleWord], 2)  # Add log probability of the smoothed bigram
    probability = round(probability, 4)  # Round the result
    return probability  # Return the calculated probability

if __name__=="__main__":
    # Open the test and training files
    testFile = open("test.txt", "r", errors="ignore")
    trainputFile = open("train.txt", "r", errors="ignore")

    # Open files to write processed data
    processedTestFile = open("processedTest.txt", "w")
    processedTrainputFile = open("processedTrain.txt", "w")

    # Count words in the training file
    words_dict = count_words(trainputFile)
    
    # Identify banned words that are in the test file but not in the training file
    bannedWords = compare_to(count_words(testFile), words_dict)

    # Process test and training files for unknown words
    unk_sentences(testFile, processedTestFile, words_dict, bannedWords)
    unk_sentences(trainputFile, processedTrainputFile, words_dict, [])

    # Close the processed files after writing
    processedTrainputFile.close()
    processedTestFile.close()

    # 1.2: Create language models
    processedTestFile = open("processedTest.txt", "r")
    processedTrainputFile = open("processedTrain.txt", "r")

    # Re-count words in the processed training file
    words_dict = count_words(processedTrainputFile)

    # Calculate the total token count in the training data
    totalTokenCount = sum(words_dict.values())
    
    # Build the unigram model from the word counts
    unigramModel = unigramModel(words_dict, totalTokenCount)

    # Create bigrams from the processed training data
    bigram_dict = createBigram(processedTrainputFile)
    
    # Build the bigram model using counts from bigrams and words_dict
    bigramModel = bigramModel(bigram_dict, words_dict)

    # Calculate unique token counts for Add-One smoothing
    uniqueTokens = len(words_dict)
    
    # Create the Add-One smoothed bigram model
    addOneSmoothingModel = addOneSmoothingModel(bigram_dict, words_dict, uniqueTokens)

    # Open a file to write model probabilities
    outputFile = open("1.2 Probabilities.txt", "w")

    # Write models to the output file
    outputFile.write("< A unigram maximum likelihood model >\n")
    writeDict(unigramModel, outputFile)
    outputFile.write("< A bigram maximum likelihood model >\n")
    writeDict(bigramModel, outputFile)
    outputFile.write("< A bigram model with Add-One smoothing >\n")
    writeDict(addOneSmoothingModel, outputFile)

    # 1.3: Calculate log probabilities for a sample sentence
    sentence = "I look forward to hearing your reply ."
    sentence = processSentence(sentence, words_dict)
    
    # Calculate log probabilities using the different models
    unigramLog = calculateUnigramLog(sentence, unigramModel)
    bigramLog = calculateBigramLog(sentence, bigramModel, unigramModel)
    addOneLog = calculateAddOneSmoothingLog(sentence, addOneSmoothingModel, unigramModel)

    # Calculate the total number of words in the processed sentence
    totalSentenceWords = len(sentence.split())

    # Calculate perplexities for each model
    perplexityUnigram = calculatePerplexity(unigramLog, totalSentenceWords)
    perplexityBigram = calculatePerplexity(bigramLog, totalSentenceWords)
    perplexityAddOne = calculatePerplexity(addOneLog, totalSentenceWords)

    # Calculate log probabilities for the processed test file using each model
    unigramLogFile = calculateUnigramLogFile(processedTestFile, unigramModel)
    bigramLogFile = calculateBigramLogFile(processedTestFile, bigramModel, unigramModel)
    addOneLogFile = calculateAddOneSmoothingLogFile(processedTestFile, addOneSmoothingModel, unigramModel)

    # Calculate perplexities based on the processed test file logs
    perplexityUnigramFile = calculatePerplexity(unigramLogFile, totalTokenCount)
    perplexityBigramFile = calculatePerplexity(bigramLogFile, totalTokenCount)
    perplexityAddOneFile = calculatePerplexity(addOneLogFile, totalTokenCount)

    # Print perplexities to the console
    print(perplexityUnigramFile)
    print(perplexityBigramFile)
    print(perplexityAddOneFile)

    # Close all open files
    outputFile.close()
    processedTrainputFile.close()
    processedTestFile.close()
    trainputFile.close()
    testFile.close()